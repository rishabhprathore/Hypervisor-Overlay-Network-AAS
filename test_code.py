from __future__ import print_function
from connection import Connection
import functions
import creation
import ipaddress
import unicodedata
import vmManagement as vmm
import tenant_management as tm
user_data_tenant2 = {
    'tenant': {
        'id': "2",
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

user_data_tenant3 = {
    'tenant': {
        'id': "3",
        'primary': {
            "subnets": [{
                "cidr": "1.2.2.0/24",
                "vm_ips": ["1.2.2.3"],
            }, {
                "cidr": "1.5.5.0/24",
                "vm_ips": ["1.5.5.2"],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "1.2.2.0/24",
                "vm_ips": ["1.2.2.5"],
            }
            , {
            "cidr": "1.6.6.0/24",
            "vm_ips": ["1.6.6.2"],
        }
]
    }
}}

user_data_tenant4 = {
    'tenant': {
        'id': "4",
        'primary': {
            "subnets": [{
                "cidr": "4.4.4.0/24",
                "vm_ips": ["4.4.4.3"],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "4.4.4.0/24",
                "vm_ips": ["4.4.4.5"],
            }

]
    }
}}


def main():
    #conn = functions.get_connection()
    #tm.primary(user_data_tenant2.get("tenant"))
    #tm.secondary(user_data_tenant2.get("tenant"))

    #tm.primary(user_data_tenant3.get("tenant"))
    #tm.secondary(user_data_tenant3.get("tenant"))

    tm.primary(user_data_tenant4.get("tenant"))
    tm.secondary(user_data_tenant4.get("tenant"))

if __name__ == '__main__':
    main()
