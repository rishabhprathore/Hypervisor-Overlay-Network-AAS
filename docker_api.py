import docker

from docker import client
cli = client.APIClient(base_url='unix://var/run/docker.sock')
cli = client.APIClient(base_url="tcp://0.0.0.0:2375")
host_c = cli.create_host_config(privileged=True)
c_id = cli.create_container(image='atandon70/test:latest2',
                            command='/bin/sleep 3000000',
                            host_config=host_c)
cli.start(c_id['Id'])
#docker inspect --format '{{.State.Pid}}' c_id['Id']
cli.inspect_container(c_id['Id'])['Pid']





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
