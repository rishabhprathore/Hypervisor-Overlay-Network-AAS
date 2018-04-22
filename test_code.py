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
    primary_data, secondary_data, tertiary_data = values.get_value()
    conn = Connection(secondary_data, tertiary_data)
    for a in values.get_user_data()['data']['tenants']:
        tm.run(conn, a)


if __name__ == '__main__':
    main()
