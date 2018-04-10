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
    tenant_name='T'+tenant_id
    #create namespace PGW-TNAME
    ns_name='PGW-'+tenant_name
    veth_hyp = 'pgw-hyp-'+tenant_id
    functions.create_namespace(ns_name, primary=True)
    #Create veth pair in hypervisor  (pgw-hypt11)(1.1.1.1)(<1.1.tenant-id.1>)
    functions.create_vethpair('test_veth','test_veth3',primary=True)

    
