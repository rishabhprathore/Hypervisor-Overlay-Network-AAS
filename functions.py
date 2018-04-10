from connection import Connection
import os
print("fucntions imported")

conn = None
prefix = None
def get_connection():
    global conn
    global prefix
    if conn:
        return conn
    else:
        conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
    prefix = 'sudo ip netns exec '
    return conn

def create_namespace(name, primary='True'):
    cmd = 'sudo ip netns add {}'.format(name)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return
