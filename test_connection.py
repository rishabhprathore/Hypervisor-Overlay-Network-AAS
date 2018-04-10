from connection import Connection
import functions
#conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
#functions.get_connection()
#functions.create_namespace('testNS2', primary=True)
#functions.create_vethpair('test_veth0','test_veth1',primary=True)
#functions.set_link_up('test_veth0')
#functions.set_link_up('test_veth1')
#functions.move_veth_to_namespace('test_veth0', 'testNS2', primary=True)
#functions.assign_ip_address_namespace('testNS2', 'test_veth0', '99.99.99.1/24', primary=True)
#functions.set_link_up_in_namespace('testNS2', 'test_veth0', primary=True)
#functions.assign_ip_address('test_veth1', '99.99.99.2/24', primary=True)
functions.set_link_up('test_veth1', primary=True)





