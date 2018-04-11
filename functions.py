from __future__ import print_function
from connection import Connection
import os

from time import sleep
import alarm

print("fucntions imported")

conn = None
prefix = 'sudo ip netns exec '
def get_connection():
    global conn
    global prefix
    if conn:
        return conn
    else:
        conn = Connection(remote_ip='152.46.18.192', username='rrathor', pkey_path='/root/.ssh/id_rsa')
    return conn
"""
def create_vm(vm_name, memory,bridge_name,iso_path, primary=True):
    cmd="virt-install --name {} --memory {}"\ 
        "--vcpu=1 --cpu host "\
        "--disk path=/var/lib/libvirt/images/{}.img,size=8"\ 
        "--network network={} -c {} -v".format(vm_name,memory,vm_name+".img",bridge_name, iso_path)
    print(cmd)
    if primary==True:
        print('local:')
        try:
            with alarm.Timeout(id='a', seconds=300):
                os.system(cmd) 
        except alarm.TimeoutError as e:
            continue
        return
    conn.ssh_remote([cmd])
    return
"""

def create_namespace(name, primary='True'):
    cmd = 'sudo ip netns add {}'.format(name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd) 
        return
    conn.ssh_remote([cmd])
    return

def create_vethpair(name1, name2, primary='True'):
    cmd = 'sudo ip link add {} type veth peer name {}'.format(name1, name2)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def set_link_up(interface_name,primary=True):
    cmd= 'sudo ip link set dev {} up'.format(interface_name)
    print(cmd)
    if primary == True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def set_link_up_in_namespace(name_space, interface, primary=True):
    global prefix
    cmd= prefix + name_space + ' ip link set dev {} up'.format(interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def assign_ip_address_namespace(name_space, interface, ip_address, primary=True):
    global prefix
    cmd = prefix + name_space + ' ip addr add '+ ip_address + ' dev {}'.format(interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def assign_ip_address(interface, ip_address, primary=True):
    cmd = 'sudo ip addr add {} dev {}'.format(ip_address,interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def move_veth_to_namespace(vethname, name_space, primary=True):
    cmd = 'sudo ip link set {} netns {}'.format(vethname, name_space)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def move_veth_to_bridge(vethname, bridge_name, primary=True):
    cmd = 'sudo brctl addif {} {}'.format(bridge_name, vethname)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def create_gre_tunnel(remote_ip, local_ip, gre_tunnel_name, primary=True):
    cmd= 'sudo ip tunnel add {} mode gre remote {} local {} ttl 255'.format(gre_tunnel_name, remote_ip, local_ip)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def add_default_route_in_namespace(ip_address, interface_name, name_space, primary=True):
    ip_address=ip_address.split('/')[0]
    global prefix
    cmd = prefix + '{} ip route add default via {} dev {}'.format(name_space, ip_address, interface_name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return


def add_route_for_gre(ip_address, gre_tunnel_name,primary=True):
    ip_address=ip_address.split('/')[0]
    cmd = 'sudo ip route add {} dev {}'.format(ip_address, gre_tunnel_name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def add_route_for_gre_cidr(cidr, gre_tunnel_name,primary=True):
    cmd = 'sudo ip route add {} dev {}'.format(cidr, gre_tunnel_name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def add_route_in_hypervisor(ip_address, interface, primary=True):
    ip_address=ip_address.split('/')[0]
    cmd = 'sudo ip route add default via {} dev {}'.format(ip_address, interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def add_route_in_hypervisor_non_default(ip_address,subnet, primary=True):
    ip_address=ip_address.split('/')[0]
    cmd = 'sudo ip route add {} via {} '.format(subnet, ip_address)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def add_route_in_namespace(name_space,ip_address, primary=True):
    global prefix
    ip_address=ip_address.split('/')[0]
    cmd = prefix+ 'sudo ip route add default via {}'.format(ip_address)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    conn.ssh_remote([cmd])
    return

def create_vxlan_tunnel(remote_ip, local_ip, vxlan_tunnel_name,bridge_name, primary=True):
    cmd= 'sudo ip link add {} type vxlan id {} remote {} dstport 4789 dev {}'.format(vxlan_tunnel_name, id, remote_ip, interface)
    cmd_1= 'brctl addif {} {}'.format(bridge_name,vxlan_tunnel_name)
    cmd_2= 'ip link set {} up'.format(vxlan_tunnel_name)

    cmd_list=[cmd,cmd_1,cmd_2]
    print(cmd)
    if primary==True:
        print('local:')
        for cmd in cmd_list:
            os.system(cmd)
        return
    conn.ssh_remote(cmd_list)
    return
