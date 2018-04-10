from connection import Connection
import os
print("fucntions imported")

conn = None
prefix = 'sudo ip netns exec '
def get_connection():
    global conn
    global prefix
    if conn:
        return conn
    else:
        conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
    return conn

def create_namespace(name, primary='True'):
    cmd = 'sudo ip netns add {}'.format(name)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def create_vethpair(name1, name2, primary='True'):
    cmd = 'sudo ip link add {} type veth peer name {}'.format(name1, name2)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def set_link_up(interface_name,primary=True):
    cmd1= 'sudo ip link set dev {} up'.format(interface_name)
    if primary == True:
        os.system(cmd1)
        return
    conn.ssh_remote([cmd1])
    return


def set_link_up_in_namespace(name_space, interface, primary=True):
    global prefix
    cmd= prefix + name_space + 'ip link set dev {} up'.format(interface)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def assign_ip_address_namespace(name_space, interface, ip_address, primary=True):
    global prefix
    cmd = prefix + name_space + 'ip addr add '+ ip_address + ' dev {}'.format(interface)
    set_link_up_in_namespace(name_space, interface, primary)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def assign_ip_address(interface, ip_address, primary=True):
    cmd = 'sudo ip addr add {} dev {}'.format(ip_address,interface)
    set_link_up(interface, primary)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def move_veth_to_namespace(vethname, name_space, primary=True):
    cmd = 'sudo ip link set {} netns {}'.format(vethname, name_space)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def move_veth_to_bridge(vethname, bridge_name, primary=True):
    cmd = 'sudo brctl addif {} {}'.format(bridge_name, vethname)
    if primary==True:
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


