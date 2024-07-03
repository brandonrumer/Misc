#!/usr/bin/env python3
"""
Summary:
    Connects to eve and powers on the virtual hosts 
    starting with the name ESXi

Description:
    Not optimized for speed. I wrote this during a meeting.
    Working as of 20240702

"""

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


def power_on_node(cookies, node_id):
    url = f"{EVE_NG_URL}/api/labs/{lab_name}.unl/nodes/{node_id}/start"
    response = requests.get(url=url,cookies=cookies,headers=headers)
    response.raise_for_status()
    return response.json()


def wipe_node(cookies, node_id):
    url = f"{EVE_NG_URL}/api/labs/{lab_name}.unl/nodes/{node_id}/wipe"
    response = requests.get(url=url,cookies=cookies,headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    cookies = eve_login()
    nodes = get_nodes(cookies)


    #  Power on (fake) ESXi hosts
    for node_id, node_info in nodes.items():
        node_name = node_info['name']
        if node_name.startswith('ESXi'):
            print(f"Powering on node '{node_name}' with ID '{node_id}'")
            power_on_node(cookies, node_id)

    print('Sleeping for 20 seconds.')
    time.sleep(20)


    #  Power on Cisco 8000Vs
    #  C8000v needs to be wiped if a previous config exists bc it sucks
    for node_id, node_info in nodes.items():
        node_name = node_info['name']
        if node_name.startswith('Cisco'):
            print(f"Wiping node '{node_name}' with ID '{node_id}'")
            wipe_node(cookies, node_id)
            print(f"Powering on node '{node_name}' with ID '{node_id}'")
            power_on_node(cookies, node_id)

    print('Sleeping for 20 seconds.')    
    time.sleep(20)


    #  Power on Firewalls
    for node_id, node_info in nodes.items():
        node_name = node_info['name']
        if 'FW' in node_name:
            print(f"Powering on node '{node_name}' with ID '{node_id}'")
            power_on_node(cookies, node_id)

    print('Sleeping for 20 seconds.')    
    time.sleep(20)


    #  Power on a list of hosts
    for node_id, node_info in nodes.items():
        node_name = node_info['name']
        if node_name in Single_Nodes:
            print(f"Powering on node '{node_name}' with ID '{node_id}'")
            power_on_node(cookies, node_id)


if __name__ == "__main__":
    main()

