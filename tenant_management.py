from __future__ import print_function
from connection import Connection
import functions
import creation
import ipaddress
import unicodedata
import vmManagement as vmm

#conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
#functions.get_connection()
#functions.create_gre_tunnel('1.1.1.1', '2.2.2.2', 'gre_test', primary=True)

#primary_conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
# Example @TODO: Please uncomment them.
# creation.create_tenant(5)

username='ckogant'
primary_ip_l3='152.46.20.191'
secondary_ip_l3='152.46.19.135'
primary_ip_l2='10.25.11.205'
secondary_ip_l2='10.25.7.94'
isPrimaryGreCreated=False
isSecondaryGreCreated = False

interface_primary="eth0"
interface_secondary="eth0"
prefix_veth = "veth"

def _check_need_to_create_vxlan(data):
    """
    returns list of cidrs that are common in primary and secondary
    """
    p_cidrs, s_cidrs = _give_cidr_ps(data)
    common_cidrs = set(p_cidrs).intersection(set(s_cidrs))
    return list(common_cidrs)


def _give_cidr_ps(data):
    primary = data.get("primary")
    tenant_id = data.get("id")
    secondary = data.get("secondary")
    primary_subnet = primary.get('subnets')
    p_cidrs = []
    for s in primary_subnet:
        sub = s.get('cidr')
        p_cidrs.append(sub)

    secondary_subnet = secondary.get('subnets')
    s_cidrs = []
    for s in secondary_subnet:
        sub = s.get('cidr')
        s_cidrs.append(sub)
    return p_cidrs, s_cidrs


def _check_need_to_create_gre(data):
    p_cidrs, s_cidrs = _give_cidr_ps(data)
    if len(set(p_cidrs).intersection(set(s_cidrs))) == 0:
        return False
    return True


def _get_subnets_for_gre_primary(data):
    p_cidrs, s_cidrs = _give_cidr_ps(data)
    sp = set(p_cidrs)
    cp = set(s_cidrs)
    intersection = list(sp.intersection(cp))
    for i in intersection:
        s_cidrs.remove(i)
    return s_cidrs


def _get_subnets_for_gre_secondary(data):
    global prefix_veth
    p_cidrs, s_cidrs = _give_cidr_ps(data)
    sp = set(p_cidrs)
    cp = set(s_cidrs)
    intersection = list(sp.intersection(cp))
    for i in intersection:
        p_cidrs.remove(i)
    return p_cidrs


def primary(data):
    global isPrimaryGreCreated
    conn=functions.get_connection()
    primary = data.get("primary")
    tenant_id = data.get("id")
    secondary = data.get("secondary")

    # Create Tenant
    #functions.get_connection()
    tenant_name = 'T' + str(tenant_id)
    ns_name = 'PGW-' + tenant_name

    veth_hyp = prefix_veth+'hyp-t' + str(tenant_id) + '-pgw'
    veth_ns = prefix_veth+'pgw-hyp-t' + str(tenant_id)
    veth_hyp_ip = '1.1.' + str(tenant_id) + '.2/24'
    veth_ns_ip = '1.1.' + str(tenant_id) + '.1/24'

    # create a namespace for tenant PGW-T1
    functions.create_namespace(ns_name, primary=True)
    # Create veth pair in hypervisor  (pgw-hypt1)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair(veth_hyp, veth_ns, primary=True)

    functions.move_veth_to_namespace(veth_ns, ns_name, primary=True)
    functions.assign_ip_address_namespace(
        ns_name, veth_ns, veth_ns_ip, primary=True)
    functions.set_link_up_in_namespace(ns_name, veth_ns, primary=True)
    functions.assign_ip_address(veth_hyp, veth_hyp_ip, primary=True)
    functions.set_link_up(veth_hyp, primary=True)

    # Create tenant namespace in primary
    functions.create_namespace(tenant_name, primary=True)
    veth_pgw_t = prefix_veth+'pgw-t' + str(tenant_id)
    veth_t_pgw = prefix_veth+'t' + str(tenant_id) + '-pgw'
    veth_pgw_t_ip = '192.168.' + str(tenant_id) + '.1/24'
    veth_t_pgw_ip = '192.168.' + str(tenant_id) + '.2/24'

    functions.create_vethpair(veth_pgw_t, veth_t_pgw, primary=True)

    functions.move_veth_to_namespace(veth_pgw_t, ns_name, primary=True)
    functions.assign_ip_address_namespace(
        ns_name, veth_pgw_t, veth_pgw_t_ip, primary=True)
    functions.set_link_up_in_namespace(ns_name, veth_pgw_t, primary=True)

    functions.move_veth_to_namespace(veth_t_pgw, tenant_name, primary=True)
    functions.assign_ip_address_namespace(
        tenant_name, veth_t_pgw, veth_t_pgw_ip, primary=True)
    functions.set_link_up_in_namespace(tenant_name, veth_t_pgw, primary=True)

    # add default route via 1.1.1.2 in PGW-T1 namespace
    functions.add_default_route_in_namespace(
        veth_hyp_ip, veth_ns, ns_name, primary=True)
    # add route in tenant namespace as a default route as pgw-t1 in primary
    functions.add_default_route_in_namespace(
        veth_pgw_t_ip, veth_t_pgw, tenant_name, primary=True)

    if _check_need_to_create_gre(data) and not isPrimaryGreCreated:
        gre_tunnel_name = 'GRE-TP'
        gre_tunnel_ip_local = '11.1.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_remote = '12.1.'+str(tenant_id)+'.1/32'

        #to create a GRE tunnel in primary
        functions.create_gre_tunnel(
            secondary_ip_l2, primary_ip_l2, gre_tunnel_name, primary=True)
        functions.set_link_up(gre_tunnel_name, primary=True)
        functions.assign_ip_address(
            gre_tunnel_name, gre_tunnel_ip_local, primary=True)
        # adding default routes
        functions.add_route_for_gre(
            gre_tunnel_ip_local, gre_tunnel_name, primary=True)
        functions.add_route_for_gre(
            gre_tunnel_ip_remote, gre_tunnel_name, primary=True)
        #
    
        # adding routes for other subnets on secondary
        get_subnets_for_gre = _get_subnets_for_gre_primary(data)
        for subnet in get_subnets_for_gre:
            functions.add_route_for_gre_cidr(
                subnet, gre_tunnel_name, primary=True)
        isPrimaryGreCreated = True
        
    ## VXLAN part
    primary_subnets = data.get('primary').get('subnets')
    secondary_subnets = data.get('secondary').get('subnets')

    common_cidrs = _check_need_to_create_vxlan(data)
    i=0
    for subnet in primary_subnets:
        cidr = subnet["cidr"]
        vm_ips = subnet["vm_ips"]
        ip = cidr.split('/')[0]

        bridge_name = tenant_name + '-br' + ip
        veth_br_t = prefix_veth+tenant_name+'br-t' + ip
        veth_t_br = prefix_veth+tenant_name+'t-br' + ip
        ip_u = unicode(ip, 'utf-8')
        veth_t_br_ip = str(ipaddress.ip_address(ip_u) + 1)+'/24'


        #add routes for all the primary subnets in primary hypervisor
        functions.add_route_in_hypervisor_non_default(
            veth_ns_ip, cidr, primary=True)

        functions.add_route_in_namespace_non_default(ns_name, veth_t_pgw_ip, cidr, primary=True)

        vmm.defineNetwork(conn.primary_conn, bridge_name)

        functions.create_vethpair(veth_br_t, veth_t_br, primary=True)
        functions.move_veth_to_bridge(veth_br_t, bridge_name, primary=True)
        functions.set_link_up(veth_br_t, primary=True)

        functions.move_veth_to_namespace(veth_t_br, tenant_name, primary=True)
        functions.assign_ip_address_namespace(
            tenant_name, veth_t_br, veth_t_br_ip, primary=True)
        functions.set_link_up_in_namespace(
            tenant_name, veth_t_br, primary=True)

        num_vms = len(vm_ips)
        for vm_ip in vm_ips:
            vm_name = "vm_" + vm_ip
            functions.create_vm(vm_name, "512", bridge_name,
                                "/root/TinyCore.iso", True)
        # spawn vms and connect to bridge

        if cidr in common_cidrs:
            # create vxlan
            vxlan_tunnel_name = 'vx_' + tenant_name + ip
            vx_id=str(int(str(tenant_id+'00')) + i)
            i+=1
            print("vxlan id: {}".format(vx_id))
            functions.create_vxlan_tunnel(
                secondary_ip_l2, vxlan_tunnel_name,vx_id,bridge_name,interface_primary, primary=True)

def secondary(data):
    global prefix_veth
    global isSecondaryGreCreated
    conn = functions.get_connection()
    tenant_id = data["id"]
    tenant_name='T'+str(tenant_id)

    functions.create_namespace(tenant_name, primary=False)
    veth_tenant = prefix_veth+'t'+str(tenant_id)+'-hyp'
    veth_hyp_t = prefix_veth+'hyp-t'+str(tenant_id)
    veth_hyp_t_ip='192.168.'+str(tenant_id)+'.1/24'
    veth_tenant_ip='192.168.'+str(tenant_id)+'.2/24'

    functions.create_vethpair(veth_tenant, veth_hyp_t, primary=False)

    functions.move_veth_to_namespace(veth_tenant, tenant_name, primary=False)
    functions.assign_ip_address_namespace(tenant_name, veth_tenant, veth_tenant_ip, primary=False)
    functions.set_link_up_in_namespace(tenant_name, veth_tenant, primary=False)

    functions.assign_ip_address(veth_hyp_t, veth_hyp_t_ip, primary=False)
    functions.set_link_up(veth_hyp_t, primary=False)


    #route in remote
    functions.add_default_route_in_namespace(veth_hyp_t_ip, veth_tenant, tenant_name, primary=False)

    common_cidrs = _check_need_to_create_vxlan(data)


    if _check_need_to_create_gre(data) and not isSecondaryGreCreated:
        gre_tunnel_name='GRE-TS'
        gre_tunnel_ip_remote='11.1.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_local='12.1.'+str(tenant_id)+'.1/32'


        #to create a GRE tunnel in primary
        functions.create_gre_tunnel(
            primary_ip_l2, secondary_ip_l2, gre_tunnel_name, primary=False)

        functions.set_link_up(gre_tunnel_name, primary=False)
        functions.assign_ip_address(
            gre_tunnel_name, gre_tunnel_ip_local, primary=False)
        # adding default routes
        functions.add_route_for_gre(
            gre_tunnel_ip_local, gre_tunnel_name, primary=False)
        functions.add_route_for_gre(gre_tunnel_ip_remote, gre_tunnel_name, primary=False)

        # adding routes for other subnets on secondary
        get_subnets_for_gre = _get_subnets_for_gre_secondary(data)
        for subnet in get_subnets_for_gre:
            functions.add_route_for_gre_cidr(subnet, gre_tunnel_name, primary=False)
        isSecondaryGreCreated = True

    primary_subnets = data.get('primary').get('subnets')
    secondary_subnets = data.get('secondary').get('subnets')
    i=0
    for subnet in secondary_subnets:
        cidr = subnet["cidr"]
        vm_ips = subnet["vm_ips"]
        ip=cidr.split('/')[0]

        bridge_name=tenant_name+'-br'+ip
        veth_br_t = prefix_veth+'br-t'+ip
        veth_t_br = prefix_veth+'t-br'+ip
        ip_u = unicode(ip, 'utf-8')
        veth_t_br_ip = str(ipaddress.ip_address(ip_u)+1)+'/24'

        vmm.defineNetwork(conn.secondary_con, bridge_name, primary=False)

        functions.create_vethpair(veth_br_t, veth_t_br, primary=False)
        functions.move_veth_to_bridge(veth_br_t, bridge_name, primary=False)
        functions.set_link_up(veth_br_t, primary=False)

        functions.move_veth_to_namespace(veth_t_br, tenant_name, primary=False)
        functions.assign_ip_address_namespace(
            tenant_name, veth_t_br, veth_t_br_ip, primary=False)
        functions.set_link_up_in_namespace(tenant_name, veth_t_br, primary=False)


        num_vms = len(vm_ips)
        
        #spawn vms and connect to bridge
        for vm_ip in vm_ips:
            vm_name = 'vm_'+str(vm_ip)
            functions.create_vm(vm_name, "512", bridge_name,
                                "/root/TinyCore.iso", False)
        
        #add routes for all the primary subnets in primary hypervisor
        functions.add_route_in_hypervisor_non_default(
            veth_tenant_ip, cidr, primary=False)

        if cidr in common_cidrs:
            # create vxlan 
            vxlan_tunnel_name = 'vx_'+tenant_name+ip
            #functions.create_vxlan_tunnel(
            #    secondary_ip_l2, vxlan_tunnel_name, bridge_name, primary=True)
            vx_id=str(int(str(tenant_id+'00')) + i)
            i += 1
            print("vxlan id: {}".format(vx_id))
            functions.create_vxlan_tunnel(
                primary_ip_l2, vxlan_tunnel_name, vx_id, bridge_name, interface_secondary, primary=False)



"""
functions.create_namespace('testNS3', primary=True)
functions.create_vethpair('test_veth2','test_veth3',primary=True)
functions.set_link_up('test_veth2')
functions.set_link_up('test_veth3')
functions.move_veth_to_namespace('test_veth3', 'testNS3', primary=True)
functions.assign_ip_address_namespace('testNS3', 'test_veth3', '99.99.98.1/24', primary=True)
functions.set_link_up_in_namespace('testNS3', 'test_veth3', primary=True)
functions.assign_ip_address('test_veth2', '99.99.98.2/24', primary=True)
functions.set_link_up('test_veth2', primary=True)
"""





