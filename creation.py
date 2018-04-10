from connection import Connection
import functions
data_store={'PGW-T1':{'NST1':{'interfaces':{'veth1':'192.168.1.1',
'veth3':'192.168.3.1'},
},'NST2':{'interfaces':{'veth2':'192.168.2.1',
'veth4':'192.168.4.1'},
}}
}

primary_ip_l3='152.46.18.168'
secondary_ip_l3='152.46.18.27'
primary_ip_l2='10.25.7.229'
secondary_ip_l2='10.25.12.13'


def create_tenant(tenant_id=''):
    tenant_name='T'+str(tenant_id)
    #create namespace PGW-TNAME
    ns_name='PGW-'+tenant_name
    veth_hyp = 'pgw-hyp-t'+str(tenant_id)
    veth_ns='hypt'+str(tenant_id)+'-pgw'
    veth_hyp_ip='1.1.'+str(tenant_id)+'.1'
    veth_ns_ip='1.1.'+str(tenant_id)+'.2'
    functions.create_namespace(ns_name, primary=True)
    #Create veth pair in hypervisor  (pgw-hypt11)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair(veth_hyp,veth_ns,primary=True)

    functions.set_link_up(veth_hyp,primary=True)
    functions.move_veth_to_namespace(veth_ns, ns_name, primary=True)
    functions.assign_ip_address_namespace(ns_name, veth_ns, veth_ns_ip, primary=True)
    functions.set_link_up_in_namespace(ns_name, veth_ns, primary=True)
    functions.assign_ip_address(veth_hyp, veth_hyp_ip, primary=True)
    functions.set_link_up(veth_hyp, primary=True)

    #local ::Another a namespace for tenant (input: tenant_name)
    functions.create_namespace(tenant_name, primary=True)
    veth_pgw_t='pgw_t'+str(tenant_id)
    veth_t_pgw='t'+str(tenant_id)+'_pgw'
    veth_pgw_t_ip='192.168.'+str(tenant_id)+'.1'
    veth_t_pgw_ip='192.168.'+str(tenant_id)+'.2'
    functions.create_vethpair(veth_pgw_t,veth_t_pgw,primary=True)

    functions.move_veth_to_namespace(veth_pgw_t, tenant_name, primary=True)
    functions.assign_ip_address_namespace(tenant_name, veth_pgw_t, veth_pgw_t_ip, primary=True)
    functions.set_link_up_in_namespace(tenant_name, veth_pgw_t, primary=True)

    functions.move_veth_to_namespace(veth_t_pgw, tenant_name, primary=True)
    functions.assign_ip_address_namespace(tenant_name, veth_t_pgw, veth_t_pgw_ip, primary=True)
    functions.set_link_up_in_namespace(tenant_name, veth_t_pgw, primary=True)

    #remote :: Another a namespace for tenant (input: tenant_name)
    functions.create_namespace(tenant_name, primary=False)

    veth_tenant='t'+str(tenant_id)+'-hyp'
    veth_t1_hyp='hyp-t'+str(tenant_id)
    veth_t1_hyp_ip='192.168.'+str(tenant_id)+'.1'
    veth_tenant_ip='192.168.'+str(tenant_id)+'.2'

    functions.create_vethpair(veth_tenant, veth_t1_hyp, primary=False)
    functions.move_veth_to_namespace(veth_t1_hyp, tenant_name, primary=False)
    functions.assign_ip_address_namespace(tenant_name, veth_t1_hyp, veth_t1_hyp_ip, primary=False)

    functions.set_link_up_in_namespace(tenant_name, veth_t1_hyp, primary=False)
    functions.assign_ip_address(veth_tenant, veth_tenant_ip, primary=False)
    functions.set_link_up(veth_tenant, primary=False)

    #add default route via 1.1.1.2 in PGW-T1 namespace

    functions.add_default_route_in_namespace(veth_hyp_ip, veth_ns, ns_name, primary=True)

    #add route in tenant namespace as a default route as pgw-t1 in primary

    functions.add_default_route_in_namespace(veth_pgw_t_ip, veth_t_pgw, tenant_name, primary=True)

    #route in remote

    functions.add_default_route_in_namespace(veth_t1_hyp_ip, veth_tenant, tenant_name, primary=False)

    # to create a gre tunnel

    gre_tunnel_name='GRE-T'+str(tenant_id)
    gre_tunnel_ip_local='11.1.'+str(tenant_id)+'.1/32'
    gre_tunnel_ip_remote='12.1'+str(tenant_id)+'.1/32'


    #to create a GRE tunnel in primary
    functions.create_gre_tunnel(secondary_ip_l2+'/20', primary_ip_l2+'/20', gre_tunnel_name, primary=True)
    functions.set_link_up(gre_tunnel_name, primary=True)
    functions.assign_ip_address(gre_tunnel_name, gre_tunnel_ip_local, primary=True)

    functions.add_route_for_gre(gre_tunnel_ip_local, gre_tunnel_name, primary=True)
    functions.add_route_for_gre(gre_tunnel_ip_remote, gre_tunnel_name, primary=True)

    # to create a GRE tunnel in secondary
    functions.create_gre_tunnel(primary_ip_l2+'/20', secondary_ip_l2+'/20', gre_tunnel_name, primary=False)
    functions.set_link_up(gre_tunnel_name, primary=False)
    functions.assign_ip_address(gre_tunnel_name, gre_tunnel_ip_remote, primary=False)

    functions.add_route_for_gre(gre_tunnel_ip_local, gre_tunnel_name, primary=False)
    functions.add_route_for_gre(gre_tunnel_ip_remote, gre_tunnel_name, primary=False)


    









    
