from __future__ import print_function
import sys
import libvirt
import sys
import paramiko

class Connection:

    def init(self, remote_ip, username, pkey_path='/root/.ssh/id_rsa'):
        try:
            self.ssh = paramiko.SSHClient()
            privkey = paramiko.RSAKey.from_private_key_file(pkey_path)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote_ip, username=username, pkey=privkey)
        except as e:
            print("Error while initiating connection to remote hypervisor: ", e)

    def ssh_remote(self, cmd_list):
        for cmd in cmd_list:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
            print(stdout.read())

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