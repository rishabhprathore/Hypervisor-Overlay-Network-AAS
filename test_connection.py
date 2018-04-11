from connection import Connection
import functions
import creation
#conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
#functions.get_connection()
#functions.create_gre_tunnel('1.1.1.1', '2.2.2.2', 'gre_test', primary=True)

#primary_conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
creation.create_tenant(3)
print ''

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





