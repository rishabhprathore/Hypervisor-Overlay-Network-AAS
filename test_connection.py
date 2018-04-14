from connection import Connection
import functions
import creation
import ipaddress
import unicodedata

#conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
#functions.get_connection()
#functions.create_gre_tunnel('1.1.1.1', '2.2.2.2', 'gre_test', primary=True)

#primary_conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
# Example @TODO: Please uncomment them.
# creation.create_tenant(5)
user_data_tenant1 = {
    'tenant': {
        'id': "1",
        'primary': {
            "subnets": [{
                "cidr": "",
                "vm_ips": [""],
            }, {
                "cidr": "",
                "vm_ips": [""],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "",
                "vm_ips": [""],
            }, {
                "cidr": "",
                "vm_ips": [""],
            }]
    }
}}


def secondary(data):
    functions.get_connection()
    tenant_id = data["tenant"]["id"]
    tenant_name='T'+str(tenant_id)

    functions.create_namespace(tenant_name, primary=False)
    veth_tenant='t'+str(tenant_id)+'-hyp'
    veth_hyp_t='hyp-t'+str(tenant_id)
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

    secondary_subnets = data["tenant"]["secondary"]["subnets"]
    for subnet in secondary_subnets:
        cidr = subnet["cidr"]
        vm_ips = subnet["vm_ips"]
        ip=cidr.split('/')[0]

        bridge_name=tenant_name+'-br'+ip
        veth_br_t = 'br-t'+ip
        veth_t_br = 't-br'+ip
        ip_u = unicode(ip, 'utf-8')
        veth_t_br_ip = str(ipaddress.ip_address(ip_u)+1)


        functions.create_vethpair(veth_br_t, veth_t_br, primary=False)
        functions.move_veth_to_bridge(veth_br_t, bridge_name, primary=False)
        functions.set_link_up(veth_br_t, primary=False)

        functions.move_veth_to_namespace(veth_t_br, tenant_name, primary=False)
        functions.assign_ip_address_namespace(
            tenant_name, veth_t_br, veth_t_br_ip, primary=False)
        functions.set_link_up_in_namespace(tenant_name, veth_t_br, primary=False)


        num_vms = len(vm_ips)
        #spawn vms and connect to bridge
        




    

print('')

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





