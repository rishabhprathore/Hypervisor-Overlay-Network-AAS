import commands
import os
from connection import Connection
import tenant_management
import functions


conn = None
def get_connection():
    global conn
    global prefix
    if conn:
        return conn
    else:
        conn = Connection(remote_ip=tenant_management.secondary_ip_l3,
                          username=tenant_management.username,
                          pkey_path='/root/.ssh/id_rsa')
    return conn


def delete_namespace(primary=True):
    if primary == True:
        print('local:')
        os.system("sudo ip -all netns delete")
        return
    conn.ssh_remote(["sudo ip -all netns delete"])
    return


def delete_veth(primary=True):
    if primary == True:
        print('local:')
        status, output = commands.getstatusoutput("ifconfig | grep veth | awk '{ print $1}'")
        existing = [x for x in output.split("\n")]
        for i in existing:
            cmd = "sudo ip addr delete {}".format(i)
            os.system(cmd)
        return
    else:
        ret = conn.ssh_remote(["ifconfig | grep veth | awk '{ print $1}'"])
        existing = [x for x in ret.split("\n")]
        for i in existing:
            cmd = "sudo ip addr delete {}".format(i)
            conn.ssh_remote([cmd])
        return


def delete_bridge(primary=True):
    if primary == True:
        status, output = commands.getstatusoutput("brctl show | cut -f1")
        existing = [x for x in output.split("\n")]
        for i in existing[1:]:
            cmd = "sudo brctl delbr {}".format(i)
            os.system(cmd)
        return
    else:
        ret = conn.ssh_remote(["brctl show | cut -f1"])
        existing = [x for x in ret.split("\n")]
        for i in existing[1:]:
            cmd = "sudo ip addr delete {}".format(i)
            conn.ssh_remote([cmd])
        return


def delete_network(primary=True):
    if primary == True:
        status, output = commands.getstatusoutput("ls -l /etc/libvirt/qemu/networks/ | awk '{print $9}'")
        existing = [x for x in output.split("\n")]
        for i in existing[3:]:
            cmd1 = "virsh net-destroy {}".format(i[:-4])
            cmd2 = "virsh net-undefine {}".format(i[:-4])
            os.system(cmd1)
            os.system(cmd2)
        return
    else:
        ret = conn.ssh_remote(["ls -l /etc/libvirt/qemu/networks/ | awk '{print $9}'"])
        existing = [x for x in ret.split("\n")]
        for i in existing[3:]:
            cmd1 = "virsh net-destroy {}".format(i[:-4])
            cmd2 = "virsh net-undefine {}".format(i[:-4])
            conn.ssh_remote([cmd1])
            conn.ssh_remote([cmd2])
        return


def delete_routes(primary=True):
    if primary == True:
        status, output = commands.getstatusoutput("ip route | grep 10.2.* | awk '{print $1}")
        existing = [x for x in output.split("\n")]
        for i in existing:
            cmd = "ip route delete {}".format(i)
            os.system(cmd)
        return
    else:
        ret = conn.ssh_remote(["ip route | grep 10.2.* | awk '{print $1}"])
        existing = [x for x in ret.split("\n")]
        for i in existing:
            cmd = "ip route delete {}".format(i)
            conn.ssh_remote([cmd])
        return


def delete_vm(primary=True):
    if primary == True:
        status, output = commands.getstatusoutput("ls -l /etc/libvirt/qemu/ | awk '{print $9}'")
        existing = [x for x in output.split("\n")]
        for i in existing[1:]:
            if i != 'networks':
                cmd1 = "virsh destroy {}".format(i[:-4])
                cmd2 = "virsh undefine {}".format(i[:-4])
                os.system(cmd1)
                os.system(cmd2)
        return
    else:
        ret = conn.ssh_remote(["ls -l /etc/libvirt/qemu/ | awk '{print $9}'"])
        existing = [x for x in ret.split("\n")]
        for i in existing[1:]:
            if i != 'networks':
                cmd1 = "virsh net-destroy {}".format(i[:-4])
                cmd2 = "virsh net-undefine {}".format(i[:-4])
                conn.ssh_remote([cmd1])
                conn.ssh_remote([cmd2])
        return