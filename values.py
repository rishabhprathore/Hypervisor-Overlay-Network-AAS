import json
from pprint import pprint
        
        

def get_value():
    primary_data = {
        'username': 'ckogant',
        'ip': '152.46.19.135',
        'l2_ip': '10.25.7.94'
    }
    secondary_data = {
        'username': 'atandon',
        'ip': '152.46.19.47',
        'l2_ip': '10.25.8.44'
    }
    tertiary_data = {
        'username': 'atandon',
        'ip': '152.46.20.220',
        'l2_ip': '10.25.11.176'
    }
    return primary_data, secondary_data, tertiary_data

def get_user_data():
    user_data = None
    with open("user_data.json", 'r') as f:
        user_data = json.load(f)
    pprint(user_data)
    return user_data

def convert_data():
    user_input = None
    with open("user_input.json", 'r') as f:
        user_input = json.load(f)
    pprint(user_input)
    user_input = {u'data': {u'tenants': [{u'id': u'12',
                                          u'subnets': [{u'cidr': u'30.1.1.0/24',
                                                        u'vm_ips': [u'30.1.1.3',
                                                                    u'30.1.1.4',
                                                                    u'30.1.1.5']},
                                                       {u'cidr': u'20.1.1.0/24',
                                                        u'vm_ips': [u'20.1.1.3']},
                                                       {u'cidr': u'10.1.1.0/24',
                                                        u'vm_ips': [u'10.1.1.4']},
                                                       {u'cidr': u'40.1.1.0/24',
                                                        u'vm_ips': [u'40.1.1.5']}]},
                                         {u'id': u'11',
                                          u'subnets': [{u'cidr': u'30.1.1.0/24',
                                                        u'vm_ips': [u'30.1.1.3',
                                                                    u'30.1.1.4',
                                                                    u'30.1.1.5']},
                                                       {u'cidr': u'20.1.1.0/24',
                                                        u'vm_ips': [u'20.1.1.3']},
                                                       {u'cidr': u'10.1.1.0/24',
                                                        u'vm_ips': [u'10.1.1.4']},
                                                       {u'cidr': u'40.1.1.0/24',
                                                        u'vm_ips': [u'40.1.1.5']}]}]}}
    list_tenants = user_input["data"]["tenants"]
    tenant_blank = {u'id': u'',
                    u'primary': {u'subnets': []},
                    u'secondary': {u'subnets': []},
                    u'tertiary': {u'subnets': []}
                    }
    user_data = {u'data': {u'tenants': [] 
                            }
                }
    

    for tenant in list_tenants: 
        list_subnets = tenant['subnets']
        print("tenant_id: {}".format(tenant['id']))
        copy_tenant_data = dict(tenant_blank)
        copy_tenant_data['id'] = tenant['id']
        pprint(list_subnets)
        subnets = {}
        for item in list_subnets:
            subnets[item['cidr']] = item['vm_ips']
        print(subnets)
        max_len = 0
        max_len_subnet = None
        max_subnet = {}
        for subnet in subnets:
            len_ = len(subnets[subnet])
            if len_>max_len:
                max_len = len_
                max_len_subnet = subnet
        max_subnet[max_len_subnet] = subnets[max_len_subnet]
        import pdb; pdb.set_trace()
        print(max_subnet)
        del subnets[max_len_subnet]
        pprint(subnets)
        flag1 = flag2 = flag3 = 0
        max_data_p = dict()
        max_data_p[max_len_subnet] = max_subnet[max_len_subnet][0::3]
        max_data_s = dict()
        max_data_s[max_len_subnet] = max_subnet[max_len_subnet][1::3]
        max_data_t = dict()
        max_data_t[max_len_subnet] = max_subnet[max_len_subnet][2::3]
        print(max_data_p)
        print(max_data_s)
        print(max_data_t)
        for i, subnet in enumerate(subnets):
            cidr = subnet
            vm_ips = subnets[subnet]
            data = dict()
            data[cidr] = vm_ips            
            if i%3 == 0:
                copy_tenant_data['primary']['subnets'].append(data)
                if flag1 == 0:
                    copy_tenant_data['primary']['subnets'].append(max_data_p)
                    flag1 = 1 
                    
            elif i % 3 == 1:
                copy_tenant_data['secondary']['subnets'].append(data)
                if flag2 == 0:
                    copy_tenant_data['secondary']['subnets'].append(max_data_s)
                    flag2 = 1
            else:
                copy_tenant_data['tertiary']['subnets'].append(data)
                if flag3 == 0:
                    copy_tenant_data['tertiary']['subnets'].append(max_data_t)
                    flag3 = 1
        import pdb
        pdb.set_trace()
        user_data['data']['tenants'].append(copy_tenant_data)
        pprint(copy_tenant_data)
    
    import pdb
    pdb.set_trace()
    print(user_data)


            
        

        
             

        

    
    




    #
    # user_data = {
    #     'data': {
    #         'tenants': [{
    #             'id': "3",
    #             'primary': {
    #                 "subnets": [{
    #                     "cidr": "1.2.2.0/24",
    #                     "vm_ips": ["1.2.2.3", "1.2.2.4"],
    #                     "vm_data":{'1.2.2.3':'aa',
    #                                '1.2.2.4':'bb'},
    #                 }, {
    #                     "cidr": "1.5.5.0/24",
    #                     "vm_ips": ["1.5.5.2"],
    #                 }]
    #             },
    #             'secondary': {
    #                 "subnets": [{
    #                     "cidr": "1.2.2.0/24",
    #                     "vm_ips": ["1.2.2.5"],
    #                 }, {
    #                     "cidr": "1.6.6.0/24",
    #                     "vm_ips": ["1.6.6.2"],
    #                 }
    #
    #                 ]
    #             },
    #             'tertiary': {
    #                 "subnets": [{
    #                     "cidr": "1.2.2.0/24",
    #                     "vm_ips": ["1.2.2.5"],
    #                 }, {
    #                     "cidr": "1.6.6.0/24",
    #                     "vm_ips": ["1.6.6.2"],
    #                 }
    #
    #                 ]
    #             }
    #
    #         },
    #             {
    #             'id': "4",
    #             'primary': {
    #                 "subnets": [{
    #                     "cidr": "1.2.2.0/24",
    #                     "vm_ips": ["1.2.2.3"],
    #                 }, {
    #                     "cidr": "1.5.5.0/24",
    #                     "vm_ips": ["1.5.5.2"],
    #                 }]
    #             },
    #             'secondary': {
    #                 "subnets": [{
    #                     "cidr": "1.2.2.0/24",
    #                     "vm_ips": ["1.2.2.5"],
    #                 }, {
    #                     "cidr": "1.6.6.0/24",
    #                     "vm_ips": ["1.6.6.2"],
    #                 }
    #
    #                 ]
    #             },
    #             'tertiary': {
    #                 "subnets": [{
    #                     "cidr": "1.2.2.0/24",
    #                     "vm_ips": ["1.2.2.5"],
    #                 }, {
    #                     "cidr": "1.6.6.0/24",
    #                     "vm_ips": ["1.6.6.2"],
    #                 }
    #
    #                 ]
    #             }
    #         }]}}
