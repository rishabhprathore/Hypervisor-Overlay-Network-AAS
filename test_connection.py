from connection import Connection

conn = Connection(remote_ip='152.46.18.27', username='ckogant', pkey_path='/root/.ssh/id_rsa')
print(conn.ssh_remote(['ls', 'pwd']))


