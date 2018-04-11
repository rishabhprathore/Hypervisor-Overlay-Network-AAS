#!/bin/bash

#arg1: vm name
#arg2: user name
#arg3: bridge name
#arg4: abs path to iso image

pip uninstall -y pyOpenSSL
vm_name=$1
user_name=$2
virt-install --name $vm_name --memory 1024 --vcpu=1 --cpu host --disk path=/var/lib/libvirt/images/$vm_name.img,size=8 --network network=$3 -c $4 -v
