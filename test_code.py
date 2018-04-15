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
        'id': "6",
        'primary': {
            "subnets": [{
                "cidr": "4.4.4.0/24",
                "vm_ips": ["4.4.4.3"],
            }, {
                "cidr": "5.5.5.0/24",
                "vm_ips": ["5.5.5.2"],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "4.4.4.0/24",
                "vm_ips": ["4.4.4.5"],
            }
            , {
            "cidr": "6.6.6.0/24",
            "vm_ips": ["6.6.6.2"],
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
