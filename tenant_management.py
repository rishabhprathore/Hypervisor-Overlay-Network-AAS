from __future__ import print_function

import ipaddress
import unicodedata

import creation
import functions
import values
import vmManagement as vmm
from connection import Connection


primary_data, secondary_data, tertiary_data = values.get_value()

#conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
#functions.get_connection()
#functions.create_gre_tunnel('1.1.1.1', '2.2.2.2', 'gre_test', primary=True)

#primary_conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
# Example @TODO: Please uncomment them.
# creation.create_tenant(5)

isPrimaryGreCreated=False
isSecondaryGreCreated = False

interface_primary="eth0"
interface_secondary="eth0"
prefix_veth = "Y"

def _check_need_to_create_vxlan_primary(data):
    """
    returns list of cidrs that are common in primary and secondary and tertiary
    """
    ret = []
    flag_s = False
    flag_t = False
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    common_cidrs_ps = set(p_cidrs).intersection(set(s_cidrs))
    ret.append(list(common_cidrs_ps))
    #Between Primary and Tertiary
    common_cidrs_pt = set(p_cidrs).intersection(set(t_cidrs))
    ret.append(list(common_cidrs_pt))

    if len(common_cidrs_ps)>0:
        flag_s = True
    if len(common_cidrs_pt)>0:
        flag_t=True
    return flag_s, flag_t

def _check_need_to_create_vxlan_secondary(data):
    """
    returns list of cidrs that are common in primary and secondary and tertiary
    """
    ret = []
    flag_p = False
    flag_t = False
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    common_cidrs_ps = set(p_cidrs).intersection(set(s_cidrs))
    ret.append(list(common_cidrs_ps))
    #Between Secondary and Tertiary
    common_cidrs_st = set(s_cidrs).intersection(set(t_cidrs))
    ret.append(list(common_cidrs_st))

    if len(common_cidrs_ps) > 0:
        flag_p = True
    if len(common_cidrs_st) > 0:
        flag_t = True
    return flag_p, flag_t


def _check_need_to_create_vxlan_tertiary(data):
    """
    returns list of cidrs that are common in primary and secondary and tertiary
    """
    ret = []
    flag_s = False
    flag_t = False
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    common_cidrs_ts = set(t_cidrs).intersection(set(s_cidrs))
    ret.append(list(common_cidrs_ts))
    #Between Primary and Tertiary
    common_cidrs_pt = set(p_cidrs).intersection(set(t_cidrs))
    ret.append(list(common_cidrs_pt))

    if len(common_cidrs_ts) > 0:
        flag_s = True
    if len(common_cidrs_pt) > 0:
        flag_p = True
    return flag_p, flag_s


def _check_need_to_create_gre_primary(data):
    """
    returns list of cidrs that are different in primary and secondary and tertiary
    """
    ret = []
    flag_s = False
    flag_t = False
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    p_cidrs_copy = list(p_cidrs)
    s_cidrs_copy = list(s_cidrs)

    common_cidrs_ps = set(p_cidrs).intersection(set(s_cidrs))
    for i in list(common_cidrs_ps):
        s_cidrs_copy.remove(i)
    for i in list(common_cidrs_ps):
        p_cidrs_copy.remove(i)
    if len(s_cidrs_copy)!=0 or len(p_cidrs_copy)!=0:
        flag_s = True

    #Between Primary and Tertiary
    p_cidrs_copy = list(p_cidrs)
    t_cidrs_copy = list(t_cidrs)

    common_cidrs_pt = set(p_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_pt):
        t_cidrs_copy.remove(i)
    for i in list(common_cidrs_pt):
        p_cidrs_copy.remove(i)
    if len(p_cidrs_copy) != 0 or len(t_cidrs_copy) != 0:
        flag_t = True

    return flag_s, flag_t, s_cidrs_copy, t_cidrs_copy


def _check_need_to_create_gre_secondary(data):
    """
    returns list of cidrs that are different in  secondary and tertiary
    """
    ret = []
    flag_p = False
    flag_t = False
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    p_cidrs_copy = list(p_cidrs)
    s_cidrs_copy = list(t_cidrs)

    common_cidrs_ps = set(p_cidrs).intersection(set(s_cidrs))
    for i in list(common_cidrs_ps):
        p_cidrs_copy.remove(i)
    for i in list(common_cidrs_ps):
        s_cidrs_copy.remove(i)
    if len(s_cidrs_copy) != 0 or len(p_cidrs_copy) != 0:
        flag_p = True

    #Between Primary and Tertiary
    s_cidrs_copy = list(s_cidrs)
    t_cidrs_copy = list(t_cidrs)

    common_cidrs_st = set(s_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_st):
        t_cidrs_copy.remove(i)
    for i in list(common_cidrs_st):
        s_cidrs_copy.remove(i)
    if len(s_cidrs_copy) != 0 or len(t_cidrs_copy) != 0:
        flag_t = True

    return flag_p, flag_t, p_cidrs_copy, t_cidrs_copy


def _check_need_to_create_gre_tertiary(data):
    """
    returns list of cidrs that are different in  secondary and tertiary
    """
    ret = []
    flag_p = False
    flag_s = False
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    p_cidrs_copy = list(p_cidrs)
    t_cidrs_copy = list(t_cidrs)

    common_cidrs_pt = set(p_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_pt):
        p_cidrs_copy.remove(i)
    for i in list(common_cidrs_pt):
        t_cidrs_copy.remove(i)
    if len(t_cidrs_copy) != 0 or len(p_cidrs_copy) != 0:
        flag_p = True

    #Between Secondary and Tertiary
    s_cidrs_copy = list(s_cidrs)
    t_cidrs_copy = list(t_cidrs)

    common_cidrs_st = set(s_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_st):
        t_cidrs_copy.remove(i)
    for i in list(common_cidrs_st):
        s_cidrs_copy.remove(i)
    if len(s_cidrs_copy) != 0 or len(t_cidrs_copy) != 0:
        flag_s = True

    return flag_p, flag_s, p_cidrs_copy, s_cidrs_copy


def _get_gre_subnets_for_primary(data):
    """
    returns list of cidrs that are different in primary and secondary and tertiary
    """
    ret = []
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    common_cidrs_ps = set(p_cidrs).intersection(set(s_cidrs))
    for i in list(common_cidrs_ps):
        s_cidrs.remove(i)

    #Between Primary and Tertiary
    common_cidrs_pt = set(p_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_pt):
        t_cidrs.remove(i)
    
    return s_cidrs, t_cidrs


def _get_gre_subnets_for_secondary(data):
    """
    returns list of cidrs that are different in primary and secondary and tertiary
    """
    ret = []
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    common_cidrs_ps = set(p_cidrs).intersection(set(s_cidrs))
    for i in list(common_cidrs_ps):
        p_cidrs.remove(i)

    #Between Primary and Tertiary
    common_cidrs_st = set(s_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_st):
        t_cidrs.remove(i)

    return p_cidrs, t_cidrs


def _get_gre_subnets_for_tertiary(data):
    """
    returns list of cidrs that are different in primary and secondary and tertiary
    """
    ret = []
    p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
    #Between Primary and Secondary
    common_cidrs_pt = set(p_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_pt):
        p_cidrs.remove(i)

    #Between Primary and Tertiary
    common_cidrs_st = set(s_cidrs).intersection(set(t_cidrs))
    for i in list(common_cidrs_st):
        s_cidrs.remove(i)

    return p_cidrs, s_cidrs





def _give_cidr_ps(data):
    primary = data.get("primary")
    secondary = data.get("secondary")
    tertiary = data.get("tertiary")

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
    
    tertiary_subnet = tertiary.get('subnets')
    t_cidrs = []
    for s in tertiary_subnet:
        sub = s.get('cidr')
        t_cidrs.append(sub)

    return p_cidrs, s_cidrs, t_cidrs

def _is_subnet_in_list(subnet, s_list):
    if s_list is None:
        return False
    if subnet in s_list:
        return True
    return False

def run_primary(data, conn):
    import pdb
    pdb.set_trace()
    primary = data.get("primary")
    tenant_id = data.get("id")
    secondary = data.get("secondary")
    tertiary = data.get("tertiary")

    # Create Tenant
    # functions.get_connection()
    tenant_name = 'T' + str(tenant_id)
    pgw_name = 'PGW-' + tenant_name

    veth_hyp = prefix_veth+'hyp-t' + str(tenant_id) + '-pgw'
    veth_hyp_ip = '99.1.' + str(tenant_id) + '.1/24'
    veth_ns = prefix_veth+'pgw-hyp-t' + str(tenant_id)
    veth_ns_ip = '99.1.' + str(tenant_id) + '.2/24'
    # create a namespace for tenant PGW-T1
    functions.create_namespace(pgw_name, primary=True)
    # Create veth pair in hypervisor  (pgw-hypt1)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair(veth_hyp, veth_ns, primary=True)

    functions.move_veth_to_namespace(veth_ns, pgw_name, primary=True)
    functions.assign_ip_address_namespace(
        pgw_name, veth_ns, veth_ns_ip, primary=True)
    functions.set_link_up_in_namespace(pgw_name, veth_ns, primary=True)
    functions.assign_ip_address(veth_hyp, veth_hyp_ip, primary=True)
    functions.set_link_up(veth_hyp, primary=True)

    # Creating IGW 
    igw_name = 'IGW-' + tenant_name

    veth_hyp_igw = prefix_veth+'hyp-t' + str(tenant_id) + '-igw'
    veth_hyp_igw_ip = '55.1.' + str(tenant_id) + '.1/24'
    veth_igw_hyp = prefix_veth+'igw-hyp-t' + str(tenant_id)
    veth_igw_hyp_ip = '55.1.' + str(tenant_id) + '.2/24'
    # create a namespace for tenant PGW-T1
    functions.create_namespace(igw_name, primary=True)
    # Create veth pair in hypervisor  (pgw-hypt1)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair(veth_hyp_igw, veth_igw_hyp, primary=True)

    functions.move_veth_to_namespace(veth_igw_hyp, igw_name, primary=True)
    functions.assign_ip_address_namespace(
        igw_name, veth_igw_hyp, veth_igw_hyp_ip, primary=True)
    functions.set_link_up_in_namespace(igw_name, veth_igw_hyp, primary=True)
    functions.assign_ip_address(veth_hyp_igw, veth_hyp_igw_ip, primary=True)
    functions.set_link_up(veth_hyp_igw, primary=True)

    # create veth pair between IGW and PGW

    veth_pgw = prefix_veth+'pgw-t' + str(tenant_id) + '-igw'
    veth_pgw_ip = '56.1.' + str(tenant_id) + '.1/24'
    veth_igw = prefix_veth+'igw-pgw-t' + str(tenant_id)
    veth_igw_ip = '56.1.' + str(tenant_id) + '.2/24'
    
    # Create veth pair in hypervisor  (pgw-hypt1)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair(veth_pgw, veth_igw, primary=True)

    functions.move_veth_to_namespace(veth_igw, igw_name, primary=True)
    functions.assign_ip_address_namespace(
        igw_name, veth_igw, veth_igw_ip, primary=True)
    functions.set_link_up_in_namespace(igw_name, veth_igw, primary=True)

    functions.move_veth_to_namespace(veth_pgw, pgw_name, primary=True)
    functions.assign_ip_address_namespace(
        pgw_name, veth_pgw, veth_pgw_ip, primary=True)
    functions.set_link_up_in_namespace(pgw_name, veth_pgw, primary=True)

    # check if vxlan is reqd
    flag_s, flag_t = _check_need_to_create_vxlan_primary(data)
    vx_bridge_name = 'vx-igw-'+tenant_name
    if flag_s or flag_t:
        # create bridge inside IGW
        
        functions.create_bridge_namespace(igw_name, vx_bridge_name, primary=True)
        vx_device_name = 'vx-igw-'+tenant_name+'-dev'
        vxlan_id = tenant_id
        functions.create_vxlan_tunnel(igw_name,
            vx_device_name, vxlan_id, vx_bridge_name, veth_igw_hyp, primary=True)
        if flag_s:
            remote_ip = '55.2.{}.2'.format(tenant_id)
            functions.add_fdb_entry_in_vxlan_namespace(
                igw_name, remote_ip, vx_device_name)

        if flag_t:
            remote_ip = '55.3.{}.2'.format(tenant_id)
            functions.add_fdb_entry_in_vxlan_namespace(
                igw_name, remote_ip, vx_device_name)
    
    # creating GRE 
    flag_s, flag_t, s_cidrs, t_cidrs = _check_need_to_create_gre_primary(data)

    if flag_s:
        local_ip = veth_igw_hyp_ip.split('/')[0]
        remote_ip = '55.2.{}.2'.format(tenant_id)
        gre_tunnel_name = 'gre-igw-'+tenant_name+'-'+remote_ip.replace('.','')
        functions.create_gre_tunnel_namespace(igw_name, remote_ip, local_ip, gre_tunnel_name)
        gre_tunnel_ip_p_s = '33.1.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_s = '33.2.'+str(tenant_id)+'.1/32'

        #to create a GRE tunnel in primary
        functions.set_link_up_in_namespace(igw_name, gre_tunnel_name, primary=True)
        functions.assign_ip_address_namespace(
            igw_name, gre_tunnel_name, gre_tunnel_ip_p_s, primary=True)
        # adding default routes
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_p_s, gre_tunnel_name, primary=True)
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_s, gre_tunnel_name, primary=True)
        for subnet in s_cidrs:
            functions.add_route_for_gre_cidr_namespace(igw_name, subnet, gre_tunnel_name)
    
    if flag_t:
        local_ip = veth_igw_hyp_ip.split('/')[0]
        remote_ip = '55.3.{}.2'.format(tenant_id)
        gre_tunnel_name = 'gre-igw-'+tenant_name+'-'+remote_ip
        functions.create_gre_tunnel_namespace(
            igw_name, remote_ip, local_ip, gre_tunnel_name)
        gre_tunnel_ip_p_t = '34.1.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_t = '34.2.'+str(tenant_id)+'.1/32'

        #to create a GRE tunnel in primary
        functions.set_link_up_in_namespace(
            igw_name, gre_tunnel_name, primary=True)
        functions.assign_ip_address_namespace(
            igw_name, gre_tunnel_name, gre_tunnel_ip_p_t, primary=True)
        # adding default routes
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_p_t, gre_tunnel_name, primary=True)
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_t, gre_tunnel_name, primary=True)

        for subnet in t_cidrs:
            functions.add_route_for_gre_cidr_namespace(
                igw_name, subnet, gre_tunnel_name)
        
    #create bridge for each subnet in Primary
    primary_subnets = data.get('primary').get('subnets')
    secondary_subnets = data.get('secondary').get('subnets')
    tertiary_subnets = data.get('tertiary').get('subnets')

    i = 0
    for i, subnet in enumerate(primary_subnets):
        cidr = subnet["cidr"]
        vm_ips = subnet["vm_ips"]
        ip = cidr.split('/')[0]

        subnet_bridge_name = tenant_name + '-br' + ip.replace('.', '')
        veth_br_t = prefix_veth+tenant_name+'-br-' + ip.replace('.', '')
        veth_t_br = prefix_veth+tenant_name+'-t-' + ip.replace('.', '')
        ip_u = ip
        veth_t_br_ip = str(ipaddress.ip_address(ip_u) + 1)+'/24'

        vmm.defineNetwork(subnet_bridge_name, conn.primary_conn, primary=True)
        p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
        total_cdr = []
        total_cdr = s_cidrs + t_cidrs

        if _is_subnet_in_list(cidr, total_cdr):
            functions.create_vethpair(veth_br_t, veth_t_br, primary=True)
            functions.move_veth_to_bridge(veth_br_t, subnet_bridge_name, primary=True)
            functions.set_link_up(veth_br_t, primary=True)

            functions.move_veth_to_namespace(veth_t_br, igw_name, primary=True)
            functions.move_veth_to_bridge_namespace(igw_name, veth_t_br, vx_bridge_name, primary=True)
        
        #create a veth pair for conatiners default
        veth_br_igw_default = prefix_veth+tenant_name+'-br-' + ip.replace('.', '')
        veth_igw_br_default = prefix_veth+tenant_name+'-igw-' + ip.replace('.', '')
        ip_u = ip
        veth_igw_br_default_ip = str(ipaddress.ip_address(ip_u) + 1)+'/24'
        functions.create_vethpair(
            veth_br_igw_default, veth_igw_br_default, primary=True)
        functions.move_veth_to_bridge(
            veth_br_igw_default, subnet_bridge_name, primary=True)
        functions.set_link_up(veth_br_igw_default, primary=True)

        functions.assign_ip_address_namespace(
            igw_name, veth_igw_br_default, veth_igw_br_default_ip, primary=True)
        functions.set_link_up_in_namespace(
            igw_name, veth_igw_br_default, primary=True)
        
        num_vms = len(vm_ips)
        data['primary']['subnets'][i]['vm_data']=dict()
        for vm_ip in vm_ips:
            vm_name = "vm-"+tenant_name+'-'+vm_ip
            veth_c_br = prefix_veth+'-cbr-'+tenant_name+vm_ip.replace('.','')
            veth_br_c = prefix_veth+'-brc-'+tenant_name+vm_ip.replace('.', '')
            functions.create_vethpair(
                veth_c_br, veth_br_c, primary=True)
            functions.move_veth_to_bridge(
                veth_br_c, subnet_bridge_name, primary=True)
            functions.set_link_up(veth_br_c, primary=True)

            cidr = vm_ip+'/24'
            c_id = functions.create_docker_container(
                vm_name, veth_c_br, cidr, veth_igw_br_default_ip, conn.primary_docker, primary=True)
            c_mac = functions.get_mac_dockerContainer(
                c_id, primary=True)
            data['primary']['subnets'][i]['vm_data'][vm_ip]=c_mac

    # add route for all other IGWs endpoint in primary
    primary_data, secondary_data, tertiary_data = values.get_value()

    remote_ip_s_igw = '55.2.{}.2/24'.format(tenant_id)
    remote_ip_s_l2 = secondary_data.get('l2_ip')
    remote_ip_t_igw = '55.3.{}.2/24'.format(tenant_id)
    remote_ip_t_l2 = tertiary_data.get('l2_ip')

    functions.add_route_in_hypervisor_non_default(
        remote_ip_s_l2, remote_ip_s_igw, primary=True)

    functions.add_route_in_hypervisor_non_default(
        remote_ip_t_l2, remote_ip_t_igw, primary=True)
    
    functions.add_route_in_namespace_non_default(
        igw_name, veth_hyp_igw_ip, remote_ip_s_igw, primary=True)

    functions.add_route_in_namespace_non_default(
        igw_name, veth_hyp_igw_ip, remote_ip_t_igw, primary=True)

    
    #adding routes for GRE subnets in IGW namespace
    s_cidrs, t_cidrs  = _get_gre_subnets_for_primary(data)
    '''
    for s in s_cidrs.extend(t_cidrs):
        functions.add_route_for_gre_cidr_namespace(igw_name, s, gre_tunnel_name)
    '''

def run_secondary(data, conn):
    primary = data.get("primary")
    tenant_id = data.get("id")
    secondary = data.get("secondary")
    tertiary = data.get("tertiary")

    # Create Tenant
    # functions.get_connection()
    tenant_name = 'T' + str(tenant_id)
    # Creating IGW
    igw_name = 'IGW-' + tenant_name

    veth_hyp_igw = prefix_veth+'hyp-t' + str(tenant_id) + '-igw'
    veth_hyp_igw_ip = '55.2.' + str(tenant_id) + '.1/24'
    veth_igw_hyp = prefix_veth+'igw-hyp-t' + str(tenant_id)
    veth_igw_hyp_ip = '55.2.' + str(tenant_id) + '.2/24'
    # create a namespace for tenant PGW-T1
    functions.create_namespace(igw_name, conn.seconday_ssh, primary=False)
    # Create veth pair in hypervisor  (pgw-hypt1)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair(
        veth_hyp_igw, veth_igw_hyp, conn.seconday_ssh, primary=False)

    functions.move_veth_to_namespace(
        veth_igw_hyp, igw_name, conn.seconday_ssh, primary=False)
    functions.assign_ip_address_namespace(
        igw_name, veth_igw_hyp, veth_igw_hyp_ip, conn.seconday_ssh, primary=False)
    functions.set_link_up_in_namespace(
        igw_name, veth_igw_hyp, conn.seconday_ssh, primary=False)
    functions.assign_ip_address(
        veth_hyp_igw, veth_hyp_igw_ip, conn.seconday_ssh, primary=False)
    functions.set_link_up(veth_hyp_igw, conn.seconday_ssh, primary=False)

    # check if vxlan is reqd
    flag_p, flag_t = _check_need_to_create_vxlan_secondary(data)
    vx_bridge_name = 'vx-igw-'+tenant_name
    if flag_p or flag_t:
        # create bridge inside IGW
        
        functions.create_bridge_namespace(
            igw_name, vx_bridge_name, conn.seconday_ssh, primary=False)
        vx_device_name = 'vx-igw-'+tenant_name+'-dev'
        vxlan_id = tenant_id
        functions.create_vxlan_tunnel(igw_name,
                                      vx_device_name, vxlan_id, vx_bridge_name, 
                                      veth_igw_hyp, conn.seconday_ssh, primary=False)
        if flag_p:
            remote_ip = '55.1.{}.2'.format(tenant_id)
            functions.add_fdb_entry_in_vxlan_namespace(
                igw_name, remote_ip, vx_device_name, conn.seconday_ssh, primary=False)

        if flag_t:
            remote_ip = '55.3.{}.2'.format(tenant_id)
            functions.add_fdb_entry_in_vxlan_namespace(
                igw_name, remote_ip, vx_device_name, conn.seconday_ssh, primary=False)

    # creating GRE
    flag_p, flag_t, p_cidrs, t_cidrs = _check_need_to_create_gre_secondary(
        data)

    if flag_p:
        local_ip = veth_igw_hyp_ip.split('/')[0]
        remote_ip = '55.1.{}.2'.format(tenant_id)
        gre_tunnel_name = 'gre-igw-'+tenant_name+'-'+remote_ip
        functions.create_gre_tunnel_namespace(
            igw_name, remote_ip, local_ip, gre_tunnel_name)
        gre_tunnel_ip_s_p = '33.2.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_p = '33.1.'+str(tenant_id)+'.1/32'

        #to create a GRE tunnel in primary
        functions.set_link_up_in_namespace(
            igw_name, gre_tunnel_name, conn.seconday_ssh, primary=False)
        functions.assign_ip_address_namespace(
            igw_name, gre_tunnel_name, gre_tunnel_ip_s_p, conn.seconday_ssh, primary=False)
        # adding default routes
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_s_p, gre_tunnel_name, conn.seconday_ssh, primary=False)
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_p, gre_tunnel_name, conn.seconday_ssh, primary=False)
        for subnet in p_cidrs:
            functions.add_route_for_gre_cidr_namespace(
                igw_name, subnet, gre_tunnel_name, conn.seconday_ssh, primary=False)

    if flag_t:
        local_ip = veth_igw_hyp_ip.split('/')[0]
        remote_ip = '55.3.{}.2'.format(tenant_id)
        gre_tunnel_name = 'gre-igw-'+tenant_name+'-'+remote_ip
        functions.create_gre_tunnel_namespace(
            igw_name, remote_ip, local_ip, gre_tunnel_name)
        gre_tunnel_ip_s_t = '35.1.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_t = '35.2.'+str(tenant_id)+'.1/32'

        #to create a GRE tunnel in secondary
        functions.set_link_up_in_namespace(
            igw_name, gre_tunnel_name, conn.seconday_ssh, primary=False)
        functions.assign_ip_address_namespace(
            igw_name, gre_tunnel_name, gre_tunnel_ip_s_t, conn.seconday_ssh, primary=False)
        # adding default routes
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_s_t, gre_tunnel_name, conn.seconday_ssh, primary=False)
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_t, gre_tunnel_name, conn.seconday_ssh, primary=False)

        for subnet in t_cidrs:
            functions.add_route_for_gre_cidr_namespace(
                igw_name, subnet, gre_tunnel_name, conn.seconday_ssh, primary=False)

    #create bridge for each subnet in Primary
    primary_subnets = data.get('primary').get('subnets')
    secondary_subnets = data.get('secondary').get('subnets')
    tertiary_subnets = data.get('tertiary').get('subnets')

    i = 0
    for i, subnet in enumerate(secondary_subnets):
        cidr = subnet["cidr"]
        vm_ips = subnet["vm_ips"]
        ip = cidr.split('/')[0]

        subnet_bridge_name = tenant_name + '-br' + ip.replace('.','')
        veth_br_t = prefix_veth+tenant_name+'-br-' + ip.replace('.', '')
        veth_t_br = prefix_veth+tenant_name+'-t-' + ip.replace('.', '')
        ip_u = ip
        veth_t_br_ip = str(ipaddress.ip_address(ip_u) + 1)+'/24'

        vmm.defineNetwork(subnet_bridge_name, conn.secondary_con,
                          conn.seconday_ssh, primary=False)
        p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)

        total_cdr = []
        total_cdr = p_cidrs + t_cidrs

        if _is_subnet_in_list(cidr, total_cdr):

            functions.create_vethpair(
                veth_br_t, veth_t_br, conn.seconday_ssh, primary=False)
            functions.move_veth_to_bridge(
                veth_br_t, subnet_bridge_name, conn.seconday_ssh, primary=False)
            functions.set_link_up(veth_br_t, conn.seconday_ssh, primary=False)

            functions.move_veth_to_namespace(
                veth_t_br, igw_name, conn.seconday_ssh, primary=False)
            functions.move_veth_to_bridge_namespace(
                igw_name, veth_t_br, vx_bridge_name, conn.seconday_ssh, primary=False)

        #create a veth pair for conatiners default
        veth_br_igw_default = prefix_veth + \
            tenant_name+'-br-' + ip.replace('.', '')
        veth_igw_br_default = prefix_veth + \
            tenant_name+'-igw-' + ip.replace('.', '')
        ip_u = ip
        veth_igw_br_default_ip = str(ipaddress.ip_address(ip_u) + 1)+'/24'
        functions.create_vethpair(
            veth_br_igw_default, veth_igw_br_default, conn.seconday_ssh, primary=False)
        functions.move_veth_to_bridge(
            veth_br_igw_default, subnet_bridge_name, conn.seconday_ssh, primary=False)
        functions.set_link_up(veth_br_igw_default,
                              conn.seconday_ssh, primary=False)

        functions.assign_ip_address_namespace(
            igw_name, veth_igw_br_default, veth_igw_br_default_ip, conn.seconday_ssh, primary=False)
        functions.set_link_up_in_namespace(
            igw_name, veth_igw_br_default, conn.seconday_ssh, primary=False)

        num_vms = len(vm_ips)
        data['secondary']['subnets'][i]['vm_data'] = dict()
        for vm_ip in vm_ips:
            vm_name = "vm-"+tenant_name+'-'+vm_ip
            veth_c_br = prefix_veth+'-cbr-'+tenant_name+vm_ip.replace('.', '')
            veth_br_c = prefix_veth+'-brc-'+tenant_name+vm_ip.replace('.', '')

            functions.create_vethpair(
                veth_c_br, veth_br_c, conn.seconday_ssh, primary=False)
            functions.move_veth_to_bridge(
                veth_br_c, subnet_bridge_name, conn.seconday_ssh, primary=False)
            functions.set_link_up(veth_br_c, conn.seconday_ssh, primary=False)

            cidr = vm_ip+'/24'
            c_id = functions.create_docker_container(
                vm_name, veth_c_br, cidr, veth_igw_br_default_ip, conn.secondary_docker, primary=False)
            c_mac = functions.get_mac_dockerContainer(
                c_id, conn.seconday_ssh, primary=False)
            data['secondary']['subnets'][i]['vm_data'][vm_ip] = c_mac

    # add route for all other IGWs endpoint in primary
    primary_data, secondary_data, tertiary_data = values.get_value()

    remote_ip_p_igw = '55.1.{}.2/24'.format(tenant_id)
    remote_ip_p_l2 = primary_data.get('l2_ip')
    remote_ip_t_igw = '55.3.{}.2/24'.format(tenant_id)
    remote_ip_t_l2 = tertiary_data.get('l2_ip')

    functions.add_route_in_hypervisor_non_default(
        remote_ip_p_l2, remote_ip_p_igw, conn.seconday_ssh, primary=False)

    functions.add_route_in_hypervisor_non_default(
        remote_ip_t_l2, remote_ip_t_igw, conn.seconday_ssh, primary=False)

    functions.add_route_in_namespace_non_default(
        igw_name, veth_hyp_igw_ip, remote_ip_p_igw, conn.seconday_ssh, primary=False)

    functions.add_route_in_namespace_non_default(
        igw_name, veth_hyp_igw_ip, remote_ip_t_igw, conn.seconday_ssh, primary=False)

    #adding routes for GRE subnets in IGW namespace
    p_cidrs, t_cidrs = _get_gre_subnets_for_secondary(data)

    for s in p_cidrs.extend(t_cidrs):
        functions.add_route_for_gre_cidr_namespace(
            igw_name, s, gre_tunnel_name, conn.seconday_ssh, primary=False)


def run_tertiary(data, conn):
    primary = data.get("primary")
    tenant_id = data.get("id")
    secondary = data.get("secondary")
    tertiary = data.get("tertiary")

    # Create Tenant
    # functions.get_connection()
    tenant_name = 'T' + str(tenant_id)
    # Creating IGW
    igw_name = 'IGW-' + tenant_name

    veth_hyp_igw = prefix_veth+'hyp-t' + str(tenant_id) + '-igw'
    veth_hyp_igw_ip = '55.3.' + str(tenant_id) + '.1/24'
    veth_igw_hyp = prefix_veth+'igw-hyp-t' + str(tenant_id)
    veth_igw_hyp_ip = '55.3.' + str(tenant_id) + '.2/24'
    # create a namespace for tenant PGW-T1
    functions.create_namespace(igw_name, conn.tertiary_ssh, primary=False)
    # Create veth pair in hypervisor  (pgw-hypt1)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair(
        veth_hyp_igw, veth_igw_hyp, conn.tertiary_ssh, primary=False)

    functions.move_veth_to_namespace(
        veth_igw_hyp, igw_name, conn.tertiary_ssh, primary=False)
    functions.assign_ip_address_namespace(
        igw_name, veth_igw_hyp, veth_igw_hyp_ip, conn.tertiary_ssh, primary=False)
    functions.set_link_up_in_namespace(
        igw_name, veth_igw_hyp, conn.tertiary_ssh, primary=False)
    functions.assign_ip_address(
        veth_hyp_igw, veth_hyp_igw_ip, conn.tertiary_ssh, primary=False)
    functions.set_link_up(veth_hyp_igw, conn.tertiary_ssh, primary=False)

    # check if vxlan is reqd
    flag_p, flag_s = _check_need_to_create_vxlan_tertiary(data)
    vx_bridge_name = 'vx-igw-'+tenant_name
    if flag_p or flag_s:
        # create bridge inside IGW
        
        functions.create_bridge_namespace(
            igw_name, vx_bridge_name, conn.tertiary_ssh, primary=False)
        vx_device_name = 'vx-igw-'+tenant_name+'-dev'
        vxlan_id = tenant_id
        functions.create_vxlan_tunnel(igw_name,
                                      vx_device_name, vxlan_id, vx_bridge_name, 
                                      veth_igw_hyp, conn.tertiary_ssh, primary=False)
        if flag_p:
            remote_ip = '55.1.{}.2'.format(tenant_id)
            functions.add_fdb_entry_in_vxlan_namespace(
                igw_name, remote_ip, vx_device_name, conn.tertiary_ssh, primary=False)

        if flag_s:
            remote_ip = '55.2.{}.2'.format(tenant_id)
            functions.add_fdb_entry_in_vxlan_namespace(
                igw_name, remote_ip, vx_device_name, conn.tertiary_ssh, primary=False)

    # creating GRE
    flag_p, flag_s, p_cidrs, s_cidrs = _check_need_to_create_gre_tertiary(
        data)

    if flag_p:
        local_ip = veth_igw_hyp_ip.split('/')[0]
        remote_ip = '55.1.{}.2'.format(tenant_id)
        gre_tunnel_name = 'gre-igw-'+tenant_name+'-'+remote_ip
        functions.create_gre_tunnel_namespace(
            igw_name, remote_ip, local_ip, gre_tunnel_name)
        gre_tunnel_ip_t_p = '34.3.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_p = '34.1.'+str(tenant_id)+'.1/32'

        #to create a GRE tunnel in primary
        functions.set_link_up_in_namespace(
            igw_name, gre_tunnel_name, conn.tertiary_ssh, primary=False)
        functions.assign_ip_address_namespace(
            igw_name, gre_tunnel_name, gre_tunnel_ip_t_p, conn.tertiary_ssh, primary=False)
        # adding default routes
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_t_p, gre_tunnel_name, conn.tertiary_ssh, primary=False)
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_p, gre_tunnel_name, conn.tertiary_ssh, primary=False)
        for subnet in p_cidrs:
            functions.add_route_for_gre_cidr_namespace(
                igw_name, subnet, gre_tunnel_name, conn.tertiary_ssh, primary=False)

    if flag_s:
        local_ip = veth_igw_hyp_ip.split('/')[0]
        remote_ip = '55.2.{}.2'.format(tenant_id)
        gre_tunnel_name = 'gre-igw-'+tenant_name+'-'+remote_ip
        functions.create_gre_tunnel_namespace(
            igw_name, remote_ip, local_ip, gre_tunnel_name)
        gre_tunnel_ip_s_t = '35.2.'+str(tenant_id)+'.1/32'
        gre_tunnel_ip_t = '35.3.'+str(tenant_id)+'.1/32'

        #to create a GRE tunnel in secondary
        functions.set_link_up_in_namespace(
            igw_name, gre_tunnel_name, conn.tertiary_ssh, primary=False)
        functions.assign_ip_address_namespace(
            igw_name, gre_tunnel_name, gre_tunnel_ip_s_t, conn.tertiary_ssh, primary=False)
        # adding default routes
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_s_t, gre_tunnel_name, conn.tertiary_ssh, primary=False)
        functions.add_route_for_gre_cidr_namespace(
            igw_name, gre_tunnel_ip_t, gre_tunnel_name, conn.tertiary_ssh, primary=False)

        for subnet in s_cidrs:
            functions.add_route_for_gre_cidr_namespace(
                igw_name, subnet, gre_tunnel_name, conn.tertiary_ssh, primary=False)

    #create bridge for each subnet in Primary
    primary_subnets = data.get('primary').get('subnets')
    secondary_subnets = data.get('secondary').get('subnets')
    tertiary_subnets = data.get('tertiary').get('subnets')

    i = 0
    for i, subnet in enumerate(tertiary_subnets):
        cidr = subnet["cidr"]
        vm_ips = subnet["vm_ips"]
        ip = cidr.split('/')[0]

        subnet_bridge_name = tenant_name + '-br' + ip.replace('.','')
        veth_br_t = prefix_veth+tenant_name+'-br-' + ip.replace('.', '')
        veth_t_br = prefix_veth+tenant_name+'-t-' + ip.replace('.', '')
        ip_u = ip
        veth_t_br_ip = str(ipaddress.ip_address(ip_u) + 1)+'/24'

        vmm.defineNetwork(subnet_bridge_name, conn.tertiary_con,
                          conn.seconday_ssh, primary=False)
        p_cidrs, s_cidrs, t_cidrs = _give_cidr_ps(data)
        total_cdr = []
        total_cdr = p_cidrs + s_cidrs

        if _is_subnet_in_list(cidr, total_cdr):
            functions.create_vethpair(
                veth_br_t, veth_t_br, conn.tertiary_ssh, primary=False)
            functions.move_veth_to_bridge(
                veth_br_t, subnet_bridge_name, conn.tertiary_ssh, primary=False)
            functions.set_link_up(veth_br_t, conn.tertiary_ssh, primary=False)

            functions.move_veth_to_namespace(
                veth_t_br, igw_name, conn.tertiary_ssh, primary=False)
            functions.move_veth_to_bridge_namespace(
                igw_name, veth_t_br, vx_bridge_name, conn.tertiary_ssh, primary=False)

        #create a veth pair for conatiners default
        veth_br_igw_default = prefix_veth + \
            tenant_name+'-br-' + ip.replace('.', '')
        veth_igw_br_default = prefix_veth + \
            tenant_name+'-igw-' + ip.replace('.', '')
        ip_u = ip
        veth_igw_br_default_ip = str(ipaddress.ip_address(ip_u) + 1)+'/24'
        functions.create_vethpair(
            veth_br_igw_default, veth_igw_br_default, conn.tertiary_ssh, primary=False)
        functions.move_veth_to_bridge(
            veth_br_igw_default, subnet_bridge_name, conn.tertiary_ssh, primary=False)
        functions.set_link_up(veth_br_igw_default,
                              conn.tertiary_ssh, primary=False)

        functions.assign_ip_address_namespace(
            igw_name, veth_igw_br_default, veth_igw_br_default_ip, conn.tertiary_ssh, primary=False)
        functions.set_link_up_in_namespace(
            igw_name, veth_igw_br_default, conn.tertiary_ssh, primary=False)

        num_vms = len(vm_ips)
        data['tertiary']['subnets'][i]['vm_data'] = dict()
        for vm_ip in vm_ips:
            vm_name = "vm-"+tenant_name+'-'+vm_ip
            veth_c_br = prefix_veth+'-cbr-'+tenant_name+vm_ip.replace('.', '')
            veth_br_c = prefix_veth+'-brc-'+tenant_name+vm_ip.replace('.', '')

            functions.create_vethpair(
                veth_c_br, veth_br_c, conn.tertiary_ssh, primary=False)
            functions.move_veth_to_bridge(
                veth_br_c,subnet_bridge_name, conn.tertiary_ssh, primary=False)
            functions.set_link_up(veth_br_c, conn.tertiary_ssh, primary=False)

            cidr = vm_ip+'/24'
            c_id = functions.create_docker_container(
                vm_name, veth_c_br, cidr, veth_igw_br_default_ip, conn.tertiary_docker, primary=False)
            c_mac = functions.get_mac_dockerContainer(
                c_id, conn.tertiary_ssh, primary=False)
            data['tertiary']['subnets'][i]['vm_data'][vm_ip] = c_mac

    # add route for all other IGWs endpoint in primary
    primary_data, secondary_data, tertiary_data = values.get_value()

    remote_ip_p_igw = '55.1.{}.2/24'.format(tenant_id)
    remote_ip_p_l2 = primary_data.get('l2_ip')
    remote_ip_s_igw = '55.2.{}.2/24'.format(tenant_id)
    remote_ip_s_l2 = secondary_data.get('l2_ip')

    functions.add_route_in_hypervisor_non_default(
        remote_ip_p_l2, remote_ip_p_igw, conn.tertiary_ssh, primary=False)

    functions.add_route_in_hypervisor_non_default(
        remote_ip_t_l2, remote_ip_t_igw, conn.tertiary_ssh, primary=False)

    functions.add_route_in_namespace_non_default(
        igw_name, veth_hyp_igw_ip, remote_ip_p_igw, conn.tertiary_ssh, primary=False)

    functions.add_route_in_namespace_non_default(
        igw_name, veth_hyp_igw_ip, remote_ip_t_igw, conn.tertiary_ssh, primary=False)

    #adding routes for GRE subnets in IGW namespace
    p_cidrs, s_cidrs = _get_gre_subnets_for_tertiary(data)

    for s in p_cidrs.extend(s_cidrs):
        functions.add_route_for_gre_cidr_namespace(
            igw_name, s, gre_tunnel_name, conn.tertiary_ssh, primary=False)

def get_macs(hypervisor, data):
    
    if hypervisor == 'primary':
        subnets = data.get('primary').get('subnets')
    elif hypervisor == 'secondary':
        subnets = data.get('secondary').get('subnets')
    else:
        subnets = data.get('tertiary').get('subnets')

    res = []
    for i in range(len(subnets)):
        for vm_ip in data[hypervisor]['subnets'][i]['vm_data'].iteritems():
            res.append(data[hypervisor]['subnets'][i]['vm_data'][vm_ip])
    print("List of MACS on {} hypervisor: {}".format(hypervisor, res))
    return res
        

def add_fdb_tenant(data, conn):

    tenant_id = data.get("id")
    tenant_name = 'T' + str(tenant_id)
    igw_name = 'IGW-' + tenant_name
    vx_device_name = 'vx-igw-'+tenant_name+'-dev'

    remote_ip_p = '55.1.{}.2'.format(tenant_id)
    remote_ip_s = '55.2.{}.2'.format(tenant_id)
    remote_ip_t = '55.3.{}.2'.format(tenant_id)

    # for primary:
    list_macs_s = get_macs('secondary', data)
    for mac in list_macs_s:
        functions.add_fdb_entry_in_vxlan_namespace(
            igw_name, remote_ip_s, vx_device_name, mac, primary=True)
    list_macs_t = get_macs('tertiary', data)
    for mac in list_macs_t:
        functions.add_fdb_entry_in_vxlan_namespace(
            igw_name, remote_ip_t, vx_device_name, mac, primary=True)
    
    # for secondary:
    list_macs_p = get_macs('primary', data)
    for mac in list_macs_p:
        functions.add_fdb_entry_in_vxlan_namespace(
            igw_name, remote_ip_p, vx_device_name, mac, conn.secondary_ssh, primary=False)
    list_macs_t = get_macs('tertiary', data)
    for mac in list_macs_t:
        functions.add_fdb_entry_in_vxlan_namespace(
            igw_name, remote_ip_t, vx_device_name, mac, conn.secondary_ssh, primary=False)

    # for tertiary:s
    list_macs_p = get_macs('primary', data)
    for mac in list_macs_p:
        functions.add_fdb_entry_in_vxlan_namespace(
            igw_name, remote_ip_p, vx_device_name, mac, conn.tertiary_ssh, primary=False)
    list_macs_s = get_macs('secondary', data)
    for mac in list_macs_s:
        functions.add_fdb_entry_in_vxlan_namespace(
            igw_name, remote_ip_s, vx_device_name, mac, conn.tertiary_ssh, primary=False)


        
    
def run(data, conn):
    run_primary(data,conn)
    run_secondary(data, conn)
    run_tertiary(data, conn)
    add_fdb_tenant(data, conn)


