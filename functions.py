from __future__ import print_function

import os
import signal
from time import sleep

import docker
import tenant_management
from connection import Connection
from connection import ssh_remote
from docker import client


class TimedOutExc(Exception):
      pass

def deadline(timeout, *args):
  def decorate(f):
    def handler(signum, frame):
      pass
 
    def new_f(*args):
      
      signal.signal(signal.SIGALRM, handler)
      signal.alarm(timeout)
      return f(*args)

    new_f.__name__ = f.__name__
    return new_f
  return decorate

print("fucntions imported")

prefix = 'sudo ip netns exec '

"""@deadline(60)
def create_vm(vm_name, memory,bridge_name,iso_path,primary):
    cmd = "sudo virt-install --name {} --memory {} " \
        "--vcpu=1 --cpu host  --disk path=/var/lib/libvirt/images/{}.img,size=8" \
        " --network network={} -c {} -v".format(
            vm_name, memory, vm_name, bridge_name, iso_path)
    print(cmd)
    try:
        if primary == True:
            print('local:')
            os.system(cmd)
            return
        ssh_remote(conn, [cmd])
    except Exception as e:
        print("timeout in create_vm {}".format(e))
        pass
    return"""


def create_namespace(name, conn=None, primary=True):
    cmd = 'sudo ip netns add {}'.format(name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd) 
        return
    ssh_remote(conn, [cmd])
    return

def create_vethpair(name1, name2, conn=None, primary=True):
    cmd = 'sudo ip link add {} type veth peer name {}'.format(name1, name2)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return

def set_link_up(interface_name, conn=None, primary=True):
    cmd= 'sudo ip link set dev {} up'.format(interface_name)
    print(cmd)
    if primary == True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def set_link_up_in_namespace(name_space, interface, conn=None, primary=True):
    global prefix
    cmd= prefix + name_space + ' ip link set dev {} up'.format(interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def assign_ip_address_namespace(name_space, interface, ip_address, conn=None, primary=True):
    global prefix
    cmd = prefix + name_space + ' ip addr add '+ ip_address + ' dev {}'.format(interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def assign_ip_address(interface, ip_address, conn=None, primary=True):
    cmd = 'sudo ip addr add {} dev {}'.format(ip_address,interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def move_veth_to_namespace(vethname, name_space, conn=None, primary=True):
    cmd = 'sudo ip link set {} netns {}'.format(vethname, name_space)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def move_veth_to_bridge(vethname, bridge_name, conn=None, primary=True):
    cmd = 'sudo brctl addif {} {}'.format(bridge_name, vethname)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def create_gre_tunnel(remote_ip, local_ip, gre_tunnel_name, conn=None, primary=True):
    cmd = 'sudo ip tunnel add {} mode gre remote {} local {} ttl 255'.format(
          gre_tunnel_name, remote_ip, local_ip)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def add_default_route_in_namespace(ip_address, interface_name, name_space, conn=None, primary=True):
    ip_address=ip_address.split('/')[0]
    global prefix
    cmd = prefix + '{} ip route add default via {} dev {}'.format(name_space, ip_address, interface_name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def add_route_for_gre(ip_address, gre_tunnel_name, conn=None, primary=True):
    ip_address=ip_address.split('/')[0]
    cmd = 'sudo ip route add {} dev {}'.format(ip_address, gre_tunnel_name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def add_route_for_gre_cidr(cidr, gre_tunnel_name, conn=None, primary=True):
    cmd = 'sudo ip route add {} dev {}'.format(cidr, gre_tunnel_name)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def add_route_in_hypervisor(ip_address, interface, conn=None, primary=True):
    ip_address=ip_address.split('/')[0]
    cmd = 'sudo ip route add default via {} dev {}'.format(ip_address, interface)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def add_route_in_hypervisor_non_default(ip_address, subnet, conn=None, primary=True):
    ip_address=ip_address.split('/')[0]
    cmd = 'sudo ip route add {} via {} '.format(subnet, ip_address)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return


def add_route_in_namespace_non_default(name_space, ip_address, subnet, conn=None, primary=True):
    global prefix
    ip_address = ip_address.split('/')[0]
    cmd = prefix+'{} ip route add {} via {} '.format(name_space, subnet, ip_address)
    print(cmd)
    if primary == True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return

def add_route_in_namespace(name_space,ip_address,conn=None, primary=True):
    global prefix
    ip_address=ip_address.split('/')[0]
    cmd = prefix+ 'sudo ip route add default via {}'.format(ip_address)
    print(cmd)
    if primary==True:
        print('local:')
        os.system(cmd)
        return
    ssh_remote(conn, [cmd])
    return

def create_vxlan_tunnel(remote_ip,vxlan_tunnel_name,id,bridge_name,interface,conn=None, primary=True):
    cmd = 'sudo ip link add {} type vxlan id {} remote {} dstport 4789 dev {}'.format(
          vxlan_tunnel_name, id, remote_ip, interface)
    cmd_1 = 'sudo brctl addif {} {}'.format(bridge_name, vxlan_tunnel_name)
    cmd_2 = 'sudo ip link set {} up'.format(vxlan_tunnel_name)

    cmd_list=[cmd,cmd_1,cmd_2]
    print(cmd_list)
    if primary==True:
        print('local:')
        for cmd in cmd_list:
            os.system(cmd)
        return
    conn.ssh_remote(cmd_list)
    return

def create_container(image_name='atandon70/test:latest2'):
    pass
