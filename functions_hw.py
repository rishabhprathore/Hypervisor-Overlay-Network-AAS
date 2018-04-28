from __future__ import print_function
import os
import ipaddress
import sys
import unicodedata
import ipcalc
import docker
from docker import client

veth0 = 'veth_sc1_lc1'
veth1 = 'veth_lc1_sc1'
veth2 = 'veth_sc1_lc2'
veth3 = 'veth_lc2_sc1'
veth4 = 'veth_sc2_lc2'
veth5 = 'veth_lc2_sc2'
veth6 = 'veth_sc2_lc1'
veth7 = 'veth_lc1_sc2'



def create_container(c_name):
    host_c = cli.create_host_config(privileged=True)
    c_id_list = docker_con.containers.list(filters={'name': c_name})
    if c_id_list:
        cid = c_id_list[0].id
    if not c_id_list:
        c_id = cli.create_container(image='atandon70/ubuntu_project:loadedUBUNTUimage',
                                    command='/bin/sleep 30000000',
                                    host_config=host_c,
                                    name=c_name)
        cid = c_id['Id']
        cli.start(cid)
    c_pid = cli.inspect_container(cid)['State']['Pid']
    return cid, c_pid


def move_veth_to_container(c_pid, dev):
    os.system("ip link set dev {} netns {}".format(dev, c_pid))


def assign_ip_container(cid, ip_cidr, dev):
    prefix = "sudo docker exec -i --privileged "
    cmd1 = prefix + "{0} ip addr add {1} dev {2} ".format(
        cid, ip_cidr, dev)
    cmd2 = prefix + " {} ip link set dev {} up".format(cid, dev)
    cmd_list = [cmd1, cmd2]
    for cmd in cmd_list:
        os.system(cmd)


def add_route_container(cid, cidr, next_hop):
    prefix = "sudo docker exec -i --privileged "
    cmd = prefix + " {} ip route add {} via {}".format(cid, cidr, next_hop)
    os.system(cmd)


def create_namespace_and_bridge(name, bridge_name):
    cmd = 'sudo ip netns add {}'.format(name)
    os.system(cmd)
    cmd = "sudo ip netns exec {} ip link add name {} type bridge ".format(
        name, bridge_name)
    os.system(cmd)
    cmd = "sudo ip netns exec {} ip link set dev {} up ".format(
        name, bridge_name)
    os.system(cmd)


def create_veth_pair(veth0, veth1):
    cmd = " sudo ip link add {0} type veth peer name {1}".format(veth0, veth1)
    os.system(cmd)
    os.system(
        " sudo ifconfig {0} up\nsudo ifconfig {1} up".format(veth0, veth1))


def create_gre_tunnel(c_id, grename, greip, local, remote):
    prefix = " sudo docker exec -i --privileged "
    cmd = prefix + \
        "{} ip tunnel add {} mode gre remote {} local {} ttl 255".format(
            c_id, grename, remote, local)
    os.system(cmd)
    cmd = prefix + "{} ip link set {} up".format(c_id, grename)
    os.system(cmd)
    cmd = prefix + "{} ip addr add {} dev {}".format(c_id, greip, grename)
    os.system(cmd)
    return grename


def move_veth_to_namespace(ns_name, veth):
    cmd = "ip link set dev {} netns {}".format(veth, ns_name)
    os.system(cmd)


def attach_veth_to_bridge_inside_namespace(ns_name, bridge_ns_name, veth):
    prefix = "sudo ip netns exec "
    cmd = prefix + \
        " {} brctl addif {} {}".format(ns_name, bridge_ns_name, veth)
    os.system(cmd)

    prefix = "sudo ip netns exec "
    cmd = prefix + " {} ip link set dev {} up".format(ns_name, bridge_ns_name)
    os.system(cmd)

    prefix = "sudo ip netns exec "
    cmd = prefix + " {} ip link set dev {} up".format(ns_name, veth)
    os.system(cmd)


# def attach_bridgenamespace_to_container(ns_name, bridge_name, c_pid)
#
#     prefix = "sudo ip netns exec "
#     cmd = prefix + " {} "


def attach_veth_pair_to_bridge_and_namespace_bridge(ns_name, bridge_name, bridge_ns_name, br_ns_br1, br_br1_ns):
    cmd = "sudo brctl addif {} {}".format(bridge_name, br_br1_ns)
    os.system(cmd)
    move_veth_to_namespace(ns_name, br_ns_br1)
    attach_veth_to_bridge_inside_namespace(ns_name, bridge_ns_name, br_ns_br1)


def create_bridge_in_namespace(ns_name, bridge_ns_name):
    prefix = "sudo ip netns exec "
    cmd = prefix + " {} brctl addbr {}".format(ns_name, bridge_ns_name)
    os.system(cmd)
