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
apt-get install python-paramiko -y
#sudo python -m easy_install --upgrade pyOpenSSL
apt-get install python-jinja2 -y
apt-get install python-yaml -y
wget http://distro.ibiblio.org/tinycorelinux/9.x/x86/release/TinyCore-current.iso -O /root/TinyCore.iso

sed -i -e 's/#user/user/g' /etc/libvirt/qemu.conf
sed -i -e 's/#group/group/g' /etc/libvirt/qemu.conf
service libvirtd restart
echo -e "\n\n******Environment setup completed! ****\n"
