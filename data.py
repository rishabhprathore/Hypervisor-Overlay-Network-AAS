from pprint import pprint

data_store={'PGW-T1':{'NS1':{'interfaces':{'veth1':'192.168.1.1',
'veth3':'192.168.3.1'},
},'NS2':{'interfaces':{'veth2':'192.168.2.1',
'veth4':'192.168.4.1'},
}}
}

pprint(data_store)

print(data_store['PGW-T1']['NS1']['veth1'])
