#!/usr/bin/env python3

import socket
import requests
import json
import ipaddress
from argparse import ArgumentParser


argparser = ArgumentParser()
argparser.add_argument('domain', type=str)


def get_ip_address(domain):
    try:
        str_ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return None
    return ipaddress.ip_address(str_ip)


def fetch_and_parse_aws_ipprefixes():
    try:
        res = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')
    except ConnectionError:
        return None
    response_txt = res.text
    response_dict = json.loads(response_txt)
    return response_dict['prefixes']


def main():
    args = argparser.parse_args()
    domain = args.domain
    host_ip_address = get_ip_address(domain)
    if not host_ip_address:
        print('Failed to lookup {domain}'.format(domain=domain))
        return False
    aws_ip_range = fetch_and_parse_aws_ipprefixes()
    if not aws_ip_range:
        print('Failed to fetch ipranges.json.')
        return False
    for prefix in aws_ip_range:
        net = ipaddress.ip_network(prefix['ip_prefix'])
        if host_ip_address in net:
            print('IP PREFIX: {ip_prefix} / Service: {service}'.format(
                ip_prefix=prefix['ip_prefix'], service=prefix['service']
            ))


if __name__ == '__main__':
    main()
