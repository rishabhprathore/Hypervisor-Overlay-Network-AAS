#!/bin/bash

echo -e "\n*****Begining Script for VM Creation*****"
echo -e "\n\nDo you want to continue with the VM Creation? Press any key!\n"
read answer
read -p "Enter Name for VM: " name_vm
echo "Enter the number of CPU required"
read cpu_vm
echo "Enter the storage required in GB (6-12 GB):"
read storage_vm
echo "Enter the RAM in MB (256-2048 MB):"
read ram_vm
echo "Enter the path for ISO image"
read vm_image
while ! [ -e $vm_image ]; do
    echo "Path for Image is not valid. Please re-entry valid path!" 
    read -p "Enter location/directory with the filename of ISO image file" vm_image
done
read -p "Enter number of interfaces you want on the VM: " inf_count
while ! [[ $inf_count =~ ([1-9]|10) ]]; do
    echo 'Invalid interfaces value. Please retry' 
    read -p "Enter number of interfaces you want on the VM: " inf_count
done
read -p "Please enter Network name for attaching VM: " nw_name
echo -e "\nVerifying if QEMU & libvirt are installed.."
sudo apt-get -y install qemu-kvm >&2
sudo apt-get -y install libvirt-bin >&2
sudo apt-get -y install virt-manager >&2
sudo apt-get -y install virt-viewer >&2
echo -e "\nEnvironment setup ready! Creating your VM now!***"
sudo virt-install -n ${name_vm} -r ${ram_vm} --vcpu=${cpu_vm} --cpu host --disk path=/var/lib/libvirt/images/${name_vm}.img,size=${storage_vm} --network network=default -c ${vm_image} -v | tee out.log