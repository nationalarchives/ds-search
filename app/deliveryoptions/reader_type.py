import logging
import os
from ipaddress import IPv4Address, IPv6Address, ip_address, ip_network
from typing import Dict, List, Optional, Union

from app.deliveryoptions.constants import (
    IP_ONSITE_RANGES,
    IP_STAFFIN_RANGES,
    Reader,
)
from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)


def is_onsite(visitor_ip_address: str) -> bool:
    """
    Check if a visitor's IP address is within the on-site IP ranges.

    Args:
        visitor_ip_address: The visitor's IP address

    Returns:
        bool: True if the visitor is on-site, False otherwise
    """
    return is_ip_in_cidr(visitor_ip_address, IP_ONSITE_RANGES)


def is_subscribed() -> bool:
    """
    Check if the user has a subscription.

    Returns:
        bool: True if the user has a subscription, False otherwise
    """
    # TODO once user management is in place
    return False


def is_staff(visitor_ip_address: str) -> bool:
    """
    Check if a visitor's IP address is within the staff IP ranges.

    Args:
        visitor_ip_address: The visitor's IP address

    Returns:
        bool: True if the visitor is staff, False otherwise
    """
    return is_ip_in_cidr(visitor_ip_address, IP_STAFFIN_RANGES)


def get_dev_reader_type() -> Reader:
    """
    Get the reader type from the environment variable for development/testing.
    Returns:
        Reader: The reader type from the environment variable or UNDEFINED if not set
    """
    # Get raw environment variable
    override_reader_type_str = os.getenv("OVERRIDE_READER_TYPE")

    # If environment variable exists, try to process it
    if override_reader_type_str is not None:
        try:
            # Convert the environment variable to an integer
            reader_value = int(override_reader_type_str)

            # For IntEnum, use the list of values from the enum members
            valid_values = [item.value for item in Reader]

            # Check if it's a valid Reader enum value
            if reader_value in valid_values:
                return Reader(reader_value)
        except Exception as e:
            logger.warning(
                f"Override reader type '{override_reader_type_str}' cannot be determined - returning UNDEFINED ({type(e)}: {e.args})"
            )

    # Default to UNDEFINED if any condition fails
    return Reader.UNDEFINED


def get_reader_type(request: HttpRequest) -> Reader:
    """
    Determine the reader type based on request information.

    Args:
        request: The HTTP request

    Returns:
        Reader: The determined reader type
    """
    reader = Reader.UNDEFINED

    try:
        visitor_ip_address = get_client_ip(request)
    except Exception as e:
        logger.warning(
            f"Cannot determine the users ip address - returning OFFSITE ({type(e)}: {e.args})"
        )
        return Reader.OFFSITE

    # Check if there is an override of reader type - used for testing and demonstrations.
    reader = get_dev_reader_type()

    if reader == Reader.UNDEFINED:
        if is_subscribed():
            reader = Reader.SUBSCRIPTION
        elif is_onsite(visitor_ip_address):
            reader = Reader.ONSITEPUBLIC
        elif is_staff(visitor_ip_address):
            reader = Reader.STAFFIN
        else:
            reader = Reader.OFFSITE

    return reader


def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
    Extract the client IP address from the HTTP request in a secure manner.

    This function properly handles IP address extraction by:
    1. Only trusting X-Forwarded-For headers when they come from trusted proxies
    2. Validating IP addresses for proper format
    3. Handling multiple proxy hops correctly

    The function will use REMOTE_ADDR by default unless the request comes from
    a trusted proxy (defined in settings.TRUSTED_PROXIES), in which case it will
    use the leftmost non-trusted-proxy IP in the X-Forwarded-For chain.

    Args:
        request (HttpRequest): The Django HTTP request object

    Returns:
        Optional[str]: The client's IP address, or None if it couldn't be determined
                      or was invalid

    Example:
        ip = get_client_ip(request)
        if ip:
            # Process valid IP
        else:
            # Handle missing/invalid IP

    Note:
        Configure TRUSTED_PROXIES in Django settings to specify which IP
        addresses are allowed to set X-Forwarded-For headers.
    """
    # Define trusted proxies
    TRUSTED_PROXIES = getattr(settings, "TRUSTED_PROXIES", [])

    # Get the immediate client IP
    remote_addr = request.META.get("REMOTE_ADDR")

    # Check if we have X-Forwarded-For header
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    # If no X-Forwarded-For or remote_addr isn't a trusted proxy, use remote_addr
    if not forwarded_for or remote_addr not in TRUSTED_PROXIES:
        return validate_ip(remote_addr)

    # Process X-Forwarded-For from trusted proxy
    # Format: client, proxy1, proxy2, ...
    forwarded_ips = [ip.strip() for ip in forwarded_for.split(",")]

    # Return the leftmost IP that isn't a trusted proxy
    for ip in forwarded_ips:
        if ip not in TRUSTED_PROXIES:
            return validate_ip(ip)

    # If all IPs in the chain are trusted, use the leftmost one
    return (
        validate_ip(forwarded_ips[0])
        if forwarded_ips
        else validate_ip(remote_addr)
    )


def validate_ip(ip_str: str) -> Optional[str]:
    """
    Validate that the string is a proper IP address.

    Args:
        ip_str (str): String representation of an IP address

    Returns:
        Optional[str]: Valid IP address string or None if invalid
    """
    if not ip_str:
        return None

    try:
        # This will raise ValueError for invalid IPs
        ip = ip_address(ip_str)
        return str(ip)
    except ValueError:
        return None


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
        ip_obj = ip_address(ip)

        # Parse the CIDR range
        for cidr_obj in cidr:
            network = ip_network(cidr_obj["Address"], strict=False)

            if ip_obj in network:
                return True

        # Check if the IP address is in the network
        return False
    except ValueError as e:
        raise ValueError(f"Invalid IP or CIDR: {e}")
