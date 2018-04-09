echo -e "\n\n******Starting with environment setup******\n"
apt-get -y install qemu-kvm
apt-get -y install libvirt-bin
apt-get -y install virt-manager
apt-get -y install virt-viewer
apt-get install python-libvirt
apt-get install libvirt-doc
apt install -y python-pip
pip install --upgrade pip
pip install Jinja2
pip install paramiko
echo -e "\n\n******Environment setup completed!\n"
