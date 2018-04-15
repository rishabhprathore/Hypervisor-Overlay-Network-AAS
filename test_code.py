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
        'id': "3",
        'primary': {
            "subnets": [{
                "cidr": "10.10.2.0/24",
                "vm_ips": ["10.10.2.3"],
            }, {
                "cidr": "10.11.2.0/24",
                "vm_ips": ["10.11.2.2"],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "10.10.2.0/24",
                "vm_ips": ["10.10.2.5"],
            }
            , {
            "cidr": "10.12.2.0/24",
            "vm_ips": ["10.12.2.2"],
        }
]
    }
}}

def main():
    #conn = functions.get_connection()
    tm.primary(user_data_tenant3.get("tenant"))
    tm.secondary(user_data_tenant3.get("tenant"))


if __name__ == '__main__':
    main()
