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

SC1_id, SC1_pid = None, None
LC1_id, LC1_pid = None, None
LC2_id, LC2_pid = None, None
SC2_id, SC2_pid = None, None

cli = client.APIClient(base_url='unix://var/run/docker.sock')
docker_con = docker.from_env()

def create_container(c_name):
    host_c = cli.create_host_config(privileged=True)
    c_id_list = docker_con.containers.list(filters={'name':c_name})
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


def underlay():
    #import pdb; pdb.set_trace()

    global SC1_id, SC1_pid
    global LC1_id, LC1_pid
    global LC2_id, LC2_pid
    global SC2_id, SC2_pid
    SC1_id, SC1_pid = create_container('SC1')
    LC1_id, LC1_pid = create_container('LC1')
    LC2_id, LC2_pid = create_container('LC2')
    SC2_id, SC2_pid = create_container('SC2')
    return
    # SC1 and LC1
    create_veth_pair(veth0, veth1)
    move_veth_to_container(SC1_pid, veth0)
    move_veth_to_container(LC1_pid, veth1)
    assign_ip_container(SC1_id, '192.168.1.2/24', veth0)
    assign_ip_container(LC1_id, '192.168.1.1/24', veth1)

    # SC1 and LC2
    create_veth_pair(veth2, veth3)
    move_veth_to_container(SC1_pid, veth2)
    move_veth_to_container(LC2_pid, veth3)
    assign_ip_container(SC1_id, '192.168.2.2/24', veth2)
    assign_ip_container(LC2_id, '192.168.2.1/24', veth3)

    # SC2 and LC2
    create_veth_pair(veth4, veth5)
    move_veth_to_container(SC2_pid, veth4)
    move_veth_to_container(LC2_pid, veth5)
    assign_ip_container(SC2_id, '192.168.4.1/24', veth4)
    assign_ip_container(LC2_id, '192.168.4.2/24', veth5)

    # SC2 and LC1
    create_veth_pair(veth6, veth7)
    move_veth_to_container(SC2_pid, veth6)
    move_veth_to_container(LC1_pid, veth7)
    assign_ip_container(SC2_id, '192.168.3.2/24', veth6)
    assign_ip_container(LC1_id, '192.168.3.1/24', veth7)

    # SC2
    add_route_container(SC2_id, "192.168.2.0/24", "192.168.4.2")
    add_route_container(SC2_id, "192.168.1.0/24", "192.168.3.1")

    # SC1
    add_route_container(SC1_id, "192.168.4.0/24", "192.168.2.1")
    add_route_container(SC1_id, "192.168.3.0/24", "192.168.1.1")

    # LC1
    add_route_container(LC1_id, "192.168.2.0/24", "192.168.1.2")
    add_route_container(LC1_id, "192.168.4.0/24", "192.168.3.2")

    # LC2
    add_route_container(LC2_id, "192.168.3.0/24", "192.168.4.1")
    add_route_container(LC2_id, "192.168.1.0/24", "192.168.2.2")

    create_gre_tunnel(SC1_id, 'GRE1', '50.50.1.1',
                      '192.168.1.2', '192.168.3.2')
    create_gre_tunnel(SC2_id, 'GRE1', '60.60.1.1',
                      '192.168.3.2', '192.168.1.2')
    add_route_container(SC1_id, '60.60.1.1', '192.168.1.1')
    add_route_container(SC2_id, '50.50.1.1', '192.168.3.1')
    prefix = "sudo docker exec -i --privileged "
    cmd = prefix + \
        "{} ip route add {} dev {}".format(SC1_id, '50.50.1.1/32', 'GRE1')
    os.system(cmd)
    cmd = prefix + \
        "{} ip route add {} dev {}".format(SC2_id, '60.60.1.1/32', 'GRE1')
    os.system(cmd)


def connect_two_containers_with_veth(c1_cidr, c2_cidr):
    _c1name = 'C1-' + c1_cidr
    _c2name = 'C2-' + c2_cidr
    c1_id, c1_pid = create_container(_c1name)
    c2_id, c2_pid = create_container(_c2name)
    create_veth_pair(_c1name, _c2name)
    move_veth_to_container(c1_pid, _c1name)
    move_veth_to_container(c2_pid, _c2name)
    assign_ip_container(c1_id, c1_cidr + '/24', _c1name)
    assign_ip_container(c2_id, c2_cidr + '/24', _c2name)


def create_bridge(bridge_name):
    cmd = "sudo brctl addbr {} ".format(bridge_name)
    os.system(cmd)
    cmd = "sudo ip link set dev {} up".format(bridge_name)
    os.system(cmd)


def attach_bridge_to_container(bridge_name, container_list, create=True):
    # create a bridge
    if create:
        create_bridge(bridge_name)
    
    for container in container_list:
        cid, pid = create_container(str(container))
        cname = 'c' + str(container)
        bname = 'b' + str(container)
        create_veth_pair(cname, bname)
        move_veth_to_container(pid, cname)
        assign_ip_container(cid, container + '/24', cname)
        
        os.system("sudo brctl addif {} {}".format(bridge_name, bname))
        os.system("sudo ip link set dev {} up".format(bridge_name))
        os.system("sudo ip link set dev {} up".format(bname))

"""
def gre_tunnel():
    bridge1 = 'B1'
    bridge2 = 'B2'
    container_list1 = ['CS1', 'CS2']
    container_list2 = ['CS3', 'CS4']
    veth0 = 'vethB1'
    veth1 = 'vethlc1'
    veth2 = 'vethB2'
    veth3 = 'vethlc2'
    create_bridge(bridge1)
    os.system("sudo ip link set dev {} up".format(bridge1))
    create_bridge(bridge2)
    os.system("sudo ip link set dev {} up".format(bridge2))

    attach_bridge_to_container(bridge1, container_list1)
    create_veth_pair(veth0, veth1)
    move_veth_to_container(LC1_pid, veth1)
    assign_ip_container(LC1_pid, ip_add, veth1)
    os.system("sudo brctl addif {} {}".format(bridge1, veth0))
    add_route_container(CS1_id, container_list2[0] + '/24', lc1_ip_address)

    attach_bridge_to_container(bridge2, container_list2)
    create_veth_pair(veth2, veth3)
    move_veth_to_container(LC2_pid, veth3)
    assign_ip_container(LC2_pid, ip_add, veth3)
    os.system("sudo brctl addif {} {}".format(bridge2, veth2))
    add_route_container(CS3_id, container_list1[0] + '/24', lc2_ip_address)

    # add route in LC1 for GRE tunnel
    add_route_container(LC1_id, container_list2(ip), '192.168.1.2')

    # add route in SC1
    add_route_container(SC1_id, container_list1(ip), '192.168.1.1')
    os.system('ip route add {} dev {}'.format(container_list2, grename))

    # add route in SC2
    add_route_container(SC2_id, container_list2(ip), '192.168.4.2')
    os.system('ip route add {} dev {}'.format(container_list1, grename))

    # add route in LC2
    add_route_container(LC2_id, container_list1(ip), '192.168.4.1')
"""

def gre_tunnel(c1name, c2name):
    import pdb; pdb.set_trace()
    global SC1_id, SC1_pid
    global LC1_id, LC1_pid
    global LC2_id, LC2_pid
    global SC2_id, SC2_pid

    bridge1 = 'B1_'+c1name
    bridge2 = 'B2_'+c2name
    veth0 = 'vethB1'
    veth1 = 'vethlc1'
    veth2 = 'vethB2'
    veth3 = 'vethlc2'
    ns1 = "ns1-"+bridge1
    ns2 = "ns2-"+bridge2
    bridge_ns_name1 = 'b-ns-'+bridge1
    bridge_ns_name2 = 'b-ns-'+bridge2

    create_namespace_and_bridge(ns1, bridge_ns_name1)
    create_namespace_and_bridge(ns2, bridge_ns_name2)

    create_bridge(bridge1)
    create_bridge(bridge2)
    cid1, pid1 = create_container(c1name)
    cid2, pid2 = create_container(c2name)
    # bridge1
    br_ns_br1 = "b_n_{}".format(bridge1)
    br_br1_ns = "b_{}_n".format(bridge1)
    create_veth_pair(br_ns_br1, br_br1_ns)
    attach_veth_pair_to_bridge_and_namespace_bridge(
        ns1, bridge1, bridge_ns_name1, br_ns_br1, br_br1_ns)

    # bridge2
    br_ns_br2 = "b_n_{}".format(bridge2)
    br_br2_ns = "b_{}_n".format(bridge2)
    create_veth_pair(br_ns_br2, br_br2_ns)
    attach_veth_pair_to_bridge_and_namespace_bridge(
        ns2, bridge2, bridge_ns_name2, br_ns_br2, br_br2_ns)

    # Attach veth to conatiner
    c_br_1 = "c_{}_1".format(bridge1)
    br_c_1 = "{}_c_1".format(bridge1)
#    create_veth_pair(c_br_1, br_c_1)
    # c1name is list of containers
    attach_bridge_to_container(bridge1, [c1name], create=False)
#    os.system("sudo brctl addif {} {}".format(bridge1, br_c_1))
#    assign_ip_container(cid, ip_cidr, dev)

    c_br_2 = "c_{}_2".format(bridge2)
    br_c_2 = "{}_c_2".format(bridge2)
#    create_veth_pair(c_br_2, br_c_2)
    attach_bridge_to_container(bridge2, [c2name], create=False)
#    os.system("sudo brctl addif {} {}".format(bridge2, br_c_2))
#   assign_ip_container()

    br_ns_lc1 = 'b_z_{}'.format(bridge1)
    lc1_ns_br = 'z_b_{}'.format(bridge1)
    br_ns_lc2 = 'b_z_{}'.format(bridge2)
    lc2_ns_br = 'z_b_{}'.format(bridge2)
    import pdb; pdb.set_trace()
    # Attach Namespace bridge to LC Containers
    create_veth_pair(br_ns_lc1, lc1_ns_br)
    move_veth_to_namespace(ns1, br_ns_lc1)
    attach_veth_to_bridge_inside_namespace(ns1, bridge_ns_name1, br_ns_lc1)
    move_veth_to_container(pid1, lc1_ns_br)
    lc1_cidr = ipcalc.IP(c1name+'/24').guess_network().host_first()
    assign_ip_container(LC1_id, lc1_cidr, lc1_ns_br)

    create_veth_pair(br_ns_lc2, lc2_ns_br)
    move_veth_to_namespace(ns2, br_ns_lc2)
    attach_veth_to_bridge_inside_namespace(ns2, bridge_ns_name2,br_ns_lc2)
    move_veth_to_container(pid2, lc2_ns_br)
    lc2_cidr = ipcalc.IP(c2name + '/24').guess_network().host_first()
    assign_ip_container(LC2_id, lc2_cidr, lc2_ns_br)

#   Adding routes for VXLAN setup
## c1 -> c2  data_path via VXLAN

    c2_network = ipcalc.IP(c2name + '/24').guess_network()
    add_route_container(cid1, c2_network, lc1_cidr)
    add_route_container(LC1_id, c2_network, '192.168.1.2')
    prefix = " sudo docker exec -i --privileged "
    cmd = prefix + \
        "{} ip addr add {} dev {}".format(SC1_id, c2_network, "GRE1")
    os.system(cmd)
    add_route_container(SC2_id, c2_network, '192.168.4.2')

    # add_route_container(cid, cidr, next_hop):

    # cid1, pid1 = create_container(c1name)
    # cid2, pid2 = create_container(c2name)

    c1_network = ipcalc.IP(c1name + '/24').guess_network()
    add_route_container(cid2, c1_network, lc2_cidr)
    add_route_container(LC2_id, c1_network, '192.168.4.1')
    cmd = prefix + \
        "{} ip addr add {} dev {}".format(SC2_id, c1_network, "GRE1")
    os.system(cmd)
    add_route_container(SC1_id, c1_network, '192.168.1.1')

    # prefix = " sudo docker exec -i --privileged "
    # cmd = prefix + "{} ip addr add {} dev {}".format(SC2_id, c2_network, "GRE1")
    # os.system(cmd)



##########################################################################
def main():
    underlay()

    while(True):
        cin = raw_input("What you want to do today? \n"
                        "Enter what type of Networking you want ) \n"
                        "Enter 1 for veth pair between containers \n"
                        "Enter 2 for bridge network \n"
                        "Enter 3 for VXLAN Tunnel \n"
                        "Enter 4 for GRE Tunnel \n"
                        "Enter 5 to exit\n")
        if cin:
            print("User choose  %s " % cin)
            if str(cin) == '1':
                print("Now we will ask you both containers IP Address \n")
                cmd = "In this method we will ask you what are containers IPs you want, we will create" \
                    " the containers with same name as IP and connect them to each other\n"
                print(cmd)
                c1name = raw_input("Enter the container 1 IP (Eg: 12.0.0.2) : \n")
                c1name = unicode(c1name, "utf-8")
                try:
                    ip = ipaddress.ip_address(c1name)
                    print('%s is a correct IP%s address.' % (ip, ip.version))
                except:
                    print('address is invalid: %s' % c1name)
                    print('Usage :  12.0.0.2')
                    c1name = None

                c2name = raw_input("Enter the container 2 IP (Eg: 12.0.0.3) : \n")
                c2name = unicode(c2name, "utf-8")
                try:
                    ip = ipaddress.ip_address(c2name)
                    print('%s is a correct IP%s address.' % (ip, ip.version))
                except:
                    print('address is invalid: %s' % c2name)
                    print('Usage :  12.0.0.2')
                    c2name = None
                if c1name and c2name:
                    # call the connecting container IPaddress
                    connect_two_containers_with_veth(c1name, c2name)
                    print(" Done creating resources and connected them")
                else:
                    print("invalid input")

            if str(cin) == '2':
                print("Now we will ask two things, Bridge_name and Containers IP \n")
                cmd = "In this method we will ask you the Bridge name and the Containers IPs (comma seperated)" \
                    " values as to what all containers you want to connect to the bridge\n"
                print(cmd)
                bridge_name = raw_input("Enter the Bridge name")

                c2name = raw_input(
                    "Enter the containers IPs (Eg: 12.0.0.3, 12.0.0.4) : \n")
                import pdb; pdb.set_trace()
                containers = c2name.split(',')
                container_list = []

                for con in containers:
                    try:
                        con = con.strip()
                        c = unicode(con, "utf-8")
                        ip = ipaddress.ip_address(c)
                        container_list.append(c)
                        print('%s is a correct IP%s address.' % (ip, ip.version))
                    except:
                        print('address is invalid: %s' % c2name)
                        print('Usage :  12.0.0.2')
                        container_list = []
                if container_list:
                    # call the bridge network function.
                    attach_bridge_to_container(bridge_name, container_list)

                    print(" Done creating resouces and connected them")
                else:
                    print("invalid input")
            if str(cin) == '3':
                print("Demo VXLAN\n")
                cmd = "In this method we will ask you what are containers IPs you want, we will create" \
                    " the containers with same name as IP and connect them to each other\n"
                cmd = cmd + "Then we create VXLAN tunnel between them using our Underlay" \
                            "(which is already automated as well)"
                print(cmd)
                c1name = raw_input("Enter the container 1 IP (Eg: 12.0.0.2) : \n")
                c1name = unicode(c1name, "utf-8")
                try:
                    ip = ipaddress.ip_address(c1name)
                    print('%s is a correct IP%s address.' % (ip, ip.version))
                except:
                    print('address is invalid: %s' % c1name)
                    print('Usage :  12.0.0.2')
                    c1name = None

                c2name = raw_input("Enter the container 2 IP (Eg: 12.0.0.3) : \n")
                c2name = unicode(c2name, "utf-8")
                try:
                    ip = ipaddress.ip_address(c2name)
                    print('%s is a correct IP%s address.' % (ip, ip.version))
                except:
                    print('address is invalid: %s' % c2name)
                    print('Usage :  12.0.0.2')
                    c2name = None
                if c1name and c2name:
                    # call the vxlan method
                    #vxlan_tunnel(c1name, c2name)
                    print(" Done creating resouces and connected them")
                else:
                    print("invalid input")
                # call the connecting for VXLAN
                
            if str(cin) == '4':
                print("Demo GRE Tunnel\n")
                cmd = "In this method we will ask you what are containers IPs you want, we will create" \
                    " the containers with same name as IP and connect them to each other\n"
                cmd = cmd + "Then we create GRE tunnel between them using our Underlay" \
                            "(which is already automated as well)"
                print(cmd)
                c1name = raw_input("Enter the container 1 IP (Eg: 12.0.0.2) : \n")
                c1name = unicode(c1name, "utf-8")
                try:
                    ip = ipaddress.ip_address(c1name)
                    print('%s is a correct IP%s address.' % (ip, ip.version))
                except:
                    print('address is invalid: %s' % c1name)
                    print('Usage :  12.0.0.2')
                    c1name = None

                c2name = raw_input("Enter the container 2 IP (Eg: 12.0.0.3) : \n")
                c2name = unicode(c2name, "utf-8")
                try:
                    ip = ipaddress.ip_address(c2name)
                    print('%s is a correct IP%s address.' % (ip, ip.version))
                except:
                    print('address is invalid: %s' % c2name)
                    print('Usage :  12.0.0.2')
                    c2name = None
                if c1name and c2name:
                    # call the connecting for GRE Tunnel
                    gre_tunnel(c1name, c2name)
                    print(" Done creating resouces and connected them")
                else:
                    print("invalid input")
            if str(cin) == '5':
                print("Exiting !!!!\n")
                sys.exit(0)


if __name__ == '__main__':
    import pdb; pdb.set_trace()
    main()
