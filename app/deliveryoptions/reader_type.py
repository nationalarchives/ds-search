import ipaddress
from typing import List

from django.http import HttpRequest

IP_STAFFIN_RANGES = [
    {"Address": "172.31.8.0/22", "Description": "Front-end Web servers"},
    {
        "Address": "10.96.0.0/13",
        "Description": "UPTOS servers- all NA- servers",
    },
    {
        "Address": "10.104.0.0/13",
        "Description": "Staff Edge User Access",
    },
    {
        "Address": "10.95.48.0/24",
        "Description": "TNA WVD",
    },
    {
        "Address": "172.31.0.0/21",
        "Description": "BIA Excluding web servers and load balanced services",
    },
    {
        "Address": "10.252.16.0/21",
        "Description": "Staff Remote Access",
    },
    {
        "Address": "10.252.21.0/24",
        "Description": "F5 VPN Staff Remote Access",
    },
    {
        "Address": "10.114.1.0/24",
        "Description": "F5 BIG-IP",
    },
]

IP_ONSITE_RANGES = [
    {
        "Address": "10.136.0.0/19",
        "Description": "Public reading rooms device (Thin clients and PCs) VLAN",
    },
    {
        "Address": "167.98.93.94/32",
        "Description": "Public Wi-Fi",
    },
    {
        "Address": "10.120.0.0/13",
        "Description": "Public Edge User Access",
    },
    {
        "Address": "10.112.0.0/13",
        "Description": "Untrusted servers- all WB- servers ( including reading rooms thin client pcs incl staff and public wifi)",
    },
]


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def is_ip_in_cidr(ip: str, cidr: list[dict]) -> bool:
    try:
        # Parse the IP address
        ip_obj = ipaddress.ip_address(ip)

        # Parse the CIDR range
        for cidr_obj in cidr:
            network = ipaddress.ip_network(cidr_obj["Address"], strict=False)

            if ip_obj in network:
                return True

        # Check if the IP address is in the network
        return False
    except ValueError as e:
        raise ValueError(f"Invalid IP or CIDR: {e}")
