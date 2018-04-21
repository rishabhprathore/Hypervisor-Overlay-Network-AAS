import os

import docker
from docker import client

# TAKE veth0 & veth1 INPUT FROM USER
veth0 = "veth0"
veth1 = "veth1"
cli = client.APIClient(base_url='unix://var/run/docker.sock')
cli = client.APIClient(base_url="tcp://0.0.0.0:2375")
host_c = cli.create_host_config(privileged=True)
c_id = cli.create_container(image='atandon70/test:latest2',
                            command='/bin/sleep 3000000',
                            host_config=host_c)
cli.start(c_id['Id'])
#docker inspect --format '{{.State.Pid}}' c_id['Id']
c_pid = cli.inspect_container(c_id['Id'])['State']['Pid']
os.system("ip link add {0} type veth peer name {1}".format(veth0, veth1))
os.system("ifconfig {0} up\nifconfig {1} up".format(veth0,veth1))
os.system("ip link set veth0 netns {}".format(c_pid))
os.system("docker exec -it --privileged {0} ifconfig {1} up".format(c_id['Id'],veth0))
# MAC parsing of veth inside docker
os.system("docker exec -it %s ifconfig %s | grep HWaddr | awk '{print $5}'" %(c_id['Id'],veth0))







"""curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sleep 1
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sleep 2
sudo apt-get update
sleep 2
sudo apt-get install -y docker-ce
sleep 2
sudo usermod -aG docker ${USER}
sleep 2
echo -e "\n\n\n"
su - ${USER}
echo -e "\n\nDownloading ubuntu image now!*****"
docker pull ubuntu
sleep 3
docker run -it ubuntu
sleep 2
apt-get update
sleep 2
apt-get install -y iproute2
sleep 2
apt-get install -y net-tools
sleep 2
apt-get install -y iputils-ping
sleep 2
exit"""
