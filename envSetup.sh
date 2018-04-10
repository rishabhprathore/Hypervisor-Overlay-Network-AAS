#!/bin/bash
echo -e "\n## NOTE ## ---> ** Before running the script, switch to root user! If you are not root, "CTRL + C" now!!! **"
sleep 3
echo -e "\n\n******Starting with environment setup******\n"
apt-get -y install qemu-kvm
apt-get -y install libvirt-bin
apt-get -y install virt-manager
apt-get -y install virt-viewer
apt-get -y install libguestfs-tools
apt-get install python-libvirt
apt-get install libvirt-doc
apt install -y python-pip
pip install --upgrade pip
pip install Jinja2
pip install pyyaml
pip install paramiko
cd /var/lib/libvirt/boot
wget http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
echo -e "\n\n******Environment setup completed! ****\n"
