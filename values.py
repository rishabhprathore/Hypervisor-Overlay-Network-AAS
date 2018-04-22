import json

def get_value():
    primary_data = {
        'username': 'rirathor',
        'ip': '152.46.20.80',
        'l2_ip': '10.25.7.241'
    }
    secondary_data = {
        'username': 'rirathor',
        'ip': '152.46.20.80',
        'l2_ip': '10.25.7.241'
    }
    tertiary_data = {
        'username': 'rirathor',
        'ip': '152.46.20.80',
        'l2_ip': '10.25.7.241'
    }
    return primary_data, secondary_data, tertiary_data
def get_user_data():
    user_data = None
    with open("user_data.json", 'r') as f:
        user_data = json.load(f)
    #print(user_data)
    return user_data
    #
    # user_data = {
    #     'data': {
    #         'tenants': [{
    #             'id': "3",
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