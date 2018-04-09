import connection

conn = connection(remote_ip='152.46.18.27', username='ckogant, pkey_path='/root/.ssh/id_rsa')
conn.ssh_remote(['ls'])
