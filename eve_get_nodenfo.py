#!/usr/bin/env python3
"""
Summary:
    Connects to eve and and gathers the nodes' info for a lab

Description:
    Not optimized for speed.
"""

import json
import time
import requests
from requests.auth import HTTPBasicAuth


EVE_NG_URL = "[sanitized]"
USERNAME = "admin"
PASSWORD = "[sanitized]"
lab_name = "[sanitized]"
headers = {'Accept': 'application/json'}
Single_Nodes = ['[sanitized]', \
                '[sanitized]']


def eve_login():
    login_url = f"{EVE_NG_URL}/api/auth/login"
    payload = '{"username":"admin","password":"eve","html5":"-1"}'
    login = requests.post(url=login_url, data=payload)
    cookies = login.cookies
    return cookies


def get_nodes(cookies):
    url = f"{EVE_NG_URL}/api/labs/{lab_name}.unl/nodes"
    response = requests.get(url=url,cookies=cookies,headers=headers)
    nodes = response.json()['data']
    return nodes


def main():
    cookies = eve_login()
    nodes = get_nodes(cookies)

    print('________________________________________')
    print('Node ID, Node Name, Node Image, Node URL')
    print('________________________________________')
    for node_id, node_info in nodes.items():
        node_name = node_info['name']
        node_image = node_info['image']
        node_url = node_info['url']
        print(f'{node_id}, {node_name}, {node_image}, {node_url}')


if __name__ == "__main__":
    main()

