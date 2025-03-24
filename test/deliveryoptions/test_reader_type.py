import logging
import os
import unittest
from unittest.mock import Mock, patch

from app.deliveryoptions.constants import (
    IP_ONSITE_RANGES,
    IP_STAFFIN_RANGES,
)
from app.deliveryoptions.reader_type import (
    Reader,
    get_client_ip,
    is_ip_in_cidr,
    is_onsite,
    is_staff,
)
from django.test import override_settings


class TestIPFunctions(unittest.TestCase):
    @override_settings(TRUSTED_PROXIES=["192.168.1.50"])
    def test_get_client_ip_from_headers(self):
        request = Mock()
        request.META = {
            "HTTP_X_FORWARDED_FOR": "203.0.113.45, 192.168.1.100",
            "REMOTE_ADDR": "192.168.1.50",  # This is now a trusted proxy
        }
        ip = get_client_ip(request)
        self.assertEqual(ip, "203.0.113.45")  # Extract first IP from header

    def test_get_client_ip_from_remote_addr(self):
        request = Mock()
        request.META = {"REMOTE_ADDR": "10.0.0.100"}
        ip = get_client_ip(request)
        self.assertEqual(ip, "10.0.0.100")

    def test_get_client_ip_no_ip_found(self):
        request = Mock()
        request.META = {}
        ip = get_client_ip(request)
        self.assertEqual(ip, None)

    def test_is_ip_in_cidr_staff_ip(self):
        self.assertTrue(is_ip_in_cidr("172.31.8.27", IP_STAFFIN_RANGES))
        self.assertTrue(is_ip_in_cidr("10.114.1.254", IP_STAFFIN_RANGES))

    def test_is_ip_in_cidr_onsite_ip(self):
        self.assertTrue(is_ip_in_cidr("167.98.93.94", IP_ONSITE_RANGES))
        self.assertTrue(is_ip_in_cidr("10.120.0.0", IP_ONSITE_RANGES))

    def test_is_ip_in_cidr_offsite_ip(self):
        self.assertFalse(is_ip_in_cidr("8.8.8.8", IP_STAFFIN_RANGES))
        self.assertFalse(is_ip_in_cidr("203.0.113.5", IP_ONSITE_RANGES))

    def test_is_ip_in_cidr_edge_cases(self):
        self.assertTrue(is_ip_in_cidr("10.114.1.0", IP_STAFFIN_RANGES))
        self.assertTrue(is_ip_in_cidr("10.252.23.255", IP_STAFFIN_RANGES))
        self.assertFalse(
            is_ip_in_cidr("10.252.24.0", IP_STAFFIN_RANGES)
        )  # Out of range

    def test_is_ip_in_cidr_invalid_ip(self):
        self.assertRaises(
            ValueError, is_ip_in_cidr, "invalid_ip", IP_STAFFIN_RANGES
        )
        self.assertRaises(ValueError, is_ip_in_cidr, "", IP_STAFFIN_RANGES)
        self.assertRaises(
            ValueError, is_ip_in_cidr, "1.2.3.4.5", IP_STAFFIN_RANGES
        )


class TestVisitorTypeDetection(unittest.TestCase):
    @patch("app.deliveryoptions.reader_type.get_client_ip")
    def test_is_staff_with_mocked_ip(self, mock_get_client_ip):
        # Mock staff IP within range
        ip_address = mock_get_client_ip.return_value = "10.252.21.17"
        self.assertTrue(is_staff(ip_address))

        # Mock non-staff IP outside range
        ip_address = mock_get_client_ip.return_value = "8.8.8.8"
        self.assertFalse(is_staff(ip_address))

    @patch("app.deliveryoptions.reader_type.get_client_ip")
    def test_is_onsite_with_mocked_ip(self, mock_get_client_ip):
        # Mock onsite IP within range
        ip_address = mock_get_client_ip.return_value = "167.98.93.94"
        self.assertTrue(is_onsite(ip_address))

        # Mock offsite IP outside range
        ip_address = mock_get_client_ip.return_value = "167.98.93.95"
        self.assertFalse(is_onsite(ip_address))

    @patch("app.deliveryoptions.reader_type.get_client_ip")
    def test_is_not_onsite_or_staff_with_mocked_ipv6(self, mock_get_client_ip):
        # Mock offsite IPv6 address
        ip_address = mock_get_client_ip.return_value = "2001:db8:4::1"
        self.assertFalse(is_onsite(ip_address))
        self.assertFalse(is_staff(ip_address))


class TestGetDevReaderType(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        super().tearDownClass()
