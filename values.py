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
    #print(user_data)
    return user_data

def convert_data():
    user_input = None
    with open("user_input.json", 'r') as f:
        user_input = json.load(f)
    pprint(user_input)
    type(user_input)
    return user_input
    
    




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
