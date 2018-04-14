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
                "cidr": "10.2.5.0/24",
                "vm_ips": ["10.2.5.3"],
            }, {
                "cidr": "10.2.6.0/24",
                "vm_ips": ["10.2.6.2"],
            }]
    },
        'secondary': {
            "subnets": [{
                "cidr": "10.2.5.0/24",
                "vm_ips": ["10.2.5.5"],
            }]
    }
}}

def main():
    functions.get_connection()
    #tm.primary(user_data_tenant3)
    #tm.secondary(user_data_tenant3)

if __name__ == '__main__':
    main()
