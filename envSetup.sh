#!/bin/bash
echo -e "\n## NOTE ## ---> ** Before running the script, switch to root user! If you are not root, "CTRL + C" now!!! **"
sleep 3
echo -e "\n\n******Starting with environment setup******\n"
apt-get -y install qemu-kvm
sleep 2
apt-get -y install libvirt-bin
sleep 2
apt-get -y install virt-manager
sleep 2
apt-get -y install virt-viewer
sleep 2
apt-get -y install libguestfs-tools
sleep 2
apt-get install python-libvirt
sleep 2
apt-get install libvirt-doc
sleep 2
apt install -y python-pip
sleep 2
pip install --upgrade pip
sleep 2
apt-get install python-paramiko -y
sleep 2
#sudo python -m easy_install --upgrade pyOpenSSL
apt-get install python-jinja2 -y
sleep 2
apt-get install python-yaml -y
sleep 2
wget http://distro.ibiblio.org/tinycorelinux/9.x/x86/release/TinyCore-current.iso -O /root/TinyCore.iso

sudo sed -i -e 's/#user/user/g' /etc/libvirt/qemu.conf
sudo sed -i -e 's/#group/group/g' /etc/libvirt/qemu.conf
sudo service libvirtd restart
echo -e "\n\n******Environment setup completed! ****\n"
