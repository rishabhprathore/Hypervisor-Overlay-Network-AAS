from connection import Connection
import os

conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
prefix = 'sudo ip netns exec '

def create_namespace(name, primary='True'):
    cmd = 'sudo ip netns add {}'.format(name)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return
