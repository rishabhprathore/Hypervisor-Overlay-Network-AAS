from __future__ import print_function
from connection import Connection
import functions
import creation
import ipaddress
import unicodedata
import vmManagement as vmm
import tenant_management as tm
import values



def main():
    for a in values.get_user_data()['data']['tenants']:
        tm.run(a)


if __name__ == '__main__':
    main()
