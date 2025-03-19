import ipaddress
from typing import List, Dict, Optional, Union

from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    """
    Extract the client IP address from the HTTP request.
    
    Looks for the X-Forwarded-For header first, falling back to the REMOTE_ADDR
    if not present. When using X-Forwarded-For, only the first IP is considered.
    
    Args:
        request (HttpRequest): The Django HTTP request object
        
    Returns:
        str: The client's IP address
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def is_ip_in_cidr(ip: str, cidr: List[Dict[str, str]]) -> bool:
    """
    Check if an IP address is within any of the specified CIDR ranges.
    
    Args:
        ip (str): The IP address to check
        cidr (List[Dict[str, str]]): A list of dictionaries containing CIDR ranges with "Address" keys
        
    Returns:
        bool: True if the IP is within any of the specified ranges, False otherwise
        
    Raises:
        ValueError: If the IP address or CIDR range is invalid
    """
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