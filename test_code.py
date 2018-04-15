from __future__ import print_function
from connection import Connection
import functions
import creation
import ipaddress
import unicodedata
import vmManagement as vmm
import tenant_management as tm

user_data_tenant3 = {
    'tenant': {
        'id': "2",
        'primary': {
            "subnets": [{
                "cidr": "10.7.2.0/24",
                "vm_ips": ["10.7.2.3"],
            }, {
                "cidr": "10.8.2.0/24",
                "vm_ips": ["10.8.2.2"],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "10.7.2.0/24",
                "vm_ips": ["10.7.2.5"],
            }
            , {
            "cidr": "10.9.2.0/24",
            "vm_ips": ["10.9.2.2"],
        }
]
    }
}}

def main():
    #conn = functions.get_connection()
    import pdb
    pdb.set_trace()
    
    tm.primary(user_data_tenant3.get("tenant"))
    tm.secondary(user_data_tenant3.get("tenant"))


if __name__ == '__main__':
    main()
