from __future__ import print_function
import sys
import libvirt
import sys
import paramiko

class Connection:
    def __init__(self, remote_ip, username, pkey_path='/root/.ssh/id_rsa'):
        try:
            self.ssh = paramiko.SSHClient()
            privkey = paramiko.RSAKey.from_private_key_file(pkey_path)
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(remote_ip, username=username, pkey=privkey)
        except e:
            print("Error while initiating connection to remote hypervisor: ", e)

    def ssh_remote(self, cmd_list):
        res =[]
        for cmd in cmd_list:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
            #print(type(ssh_stdout.read())
            if ssh_stdout is None:
                print("test1")
                if ssh_stderr is not None:
                    res.append('error:',ssh_stderr.read())
                    print(res[-1])
                    continue
            res.append(ssh_stdout.read())
            print(res[-1])
        return res

"""
conn = libvirt.open('qemu+ssh://ckogant@152.46.18.27/system')


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
privkey = paramiko.RSAKey.from_private_key_file ('/root/.ssh/id_rsa')
ssh.connect('152.46.18.27', username='ckogant', pkey=privkey)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls /tmp')
print(stdout.read())

ns_name='NS1'
cmd = "sudo ip add netns {}; ".format(ns_name)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
print(stdout.read())
"""