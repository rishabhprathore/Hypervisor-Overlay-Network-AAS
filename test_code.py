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
        'id': "11",
        'primary': {
            "subnets": [{
                "cidr": "11.13.2.0/24",
                "vm_ips": ["11.13.2.3"],
            }, {
                "cidr": "11.14.2.0/24",
                "vm_ips": ["11.14.2.2"],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "11.13.2.0/24",
                "vm_ips": ["11.13.2.5"],
            }
            , {
            "cidr": "11.15.2.0/24",
            "vm_ips": ["11.15.2.2"],
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
