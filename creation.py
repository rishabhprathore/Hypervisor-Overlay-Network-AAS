from connection import Connection
import functions
data_store={'PGW-T1':{'NST1':{'interfaces':{'veth1':'192.168.1.1',
'veth3':'192.168.3.1'},
},'NST2':{'interfaces':{'veth2':'192.168.2.1',
'veth4':'192.168.4.1'},
}}
}

primary_ip_l3=''
secondary_ip_l3=''
primary_ip_l2=''
secondary_ip_l2=''


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

    functions.move_veth_to_namespace(veth_pgw_t, ns_name, primary=True)
    functions.assign_ip_address_namespace(ns_name, veth_pgw_t, veth_pgw_t_ip, primary=True)
    functions.set_link_up_in_namespace(ns_name, veth_pgw_t, primary=True)

    functions.move_veth_to_namespace(veth_t_pgw, tenant_name, primary=True)
    functions.assign_ip_address_namespace(tenant_name, veth_t_pgw, veth_t_pgw_ip, primary=True)
    functions.set_link_up_in_namespace(tenant_name, veth_t_pgw, primary=True)

    #remote :: Another a namespace for tenant (input: tenant_name)
    functions.create_namespace(tenant_name, primary=False)
    


    









    
