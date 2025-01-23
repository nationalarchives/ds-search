import os
import unittest
from unittest.mock import Mock, patch

from app.deliveryoptions.reader_type import (
    IP_ONSITE_RANGES,
    IP_STAFFIN_RANGES,
    get_client_ip,
    is_ip_in_cidr,
)
from app.deliveryoptions.utils import (
    Reader,
    get_dev_reader_type,
    is_dev,
    is_onsite,
    is_staff,
)


class TestIPFunctions(unittest.TestCase):
    def test_get_client_ip_from_headers(self):
        request = Mock()
        request.META = {
            "HTTP_X_FORWARDED_FOR": "203.0.113.45, 192.168.1.100",
            "REMOTE_ADDR": "192.168.1.50",
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
    @patch("app.deliveryoptions.utils.get_client_ip")
    def test_is_staff_with_mocked_ip(self, mock_get_client_ip):
        # Mock staff IP within range
        ip_address = mock_get_client_ip.return_value = "10.252.21.17"
        self.assertTrue(is_staff(ip_address))

        # Mock non-staff IP outside range
        ip_address = mock_get_client_ip.return_value = "8.8.8.8"
        self.assertFalse(is_staff(ip_address))

    @patch("app.deliveryoptions.utils.get_client_ip")
    def test_is_onsite_with_mocked_ip(self, mock_get_client_ip):
        # Mock onsite IP within range
        ip_address = mock_get_client_ip.return_value = "167.98.93.94"
        self.assertTrue(is_onsite(ip_address))

        # Mock offsite IP outside range
        ip_address = mock_get_client_ip.return_value = "167.98.93.95"
        self.assertFalse(is_onsite(ip_address))

    @patch("app.deliveryoptions.utils.get_client_ip")
    def test_is_not_onsite_or_staff_with_mocked_ipv6(self, mock_get_client_ip):
        # Mock offsite IPv6 address
        ip_address = mock_get_client_ip.return_value = "2001:db8:4::1"
        self.assertFalse(is_onsite(ip_address))
        self.assertFalse(is_staff(ip_address))


class TestIsDev(unittest.TestCase):
    def test_local_ip_v4(self):
        # Test with IPv4 loopback address
        ip_address = "127.0.0.1"
        result = is_dev(ip_address)
        self.assertTrue(result)  # Should return True for local machine

    def test_local_ip_v6(self):
        # Test with IPv6 loopback address
        ip_address = "::1"
        result = is_dev(ip_address)
        self.assertTrue(result)  # Should return True for local machine

    def test_non_local_ip(self):
        # Test with a non-local IP address
        ip_address = "192.168.1.1"
        result = is_dev(ip_address)
        self.assertFalse(result)  # Should return False for non-local machine


class TestGetDevReaderType(unittest.TestCase):
    @patch.dict(
        os.environ, {"OVERRIDE_READER_TYPE": "0"}
    )  # Mock environment variable to the minimum valid value
    def test_min_valid_reader_type(self):
        result = get_dev_reader_type()
        self.assertEqual(
            result, Reader.STAFFIN
        )  # Should return 0 as it is within the valid range (0-3)

    @patch.dict(
        os.environ, {"OVERRIDE_READER_TYPE": "3"}
    )  # Mock environment variable to the maximum valid value
    def test_max_valid_reader_type(self):
        result = get_dev_reader_type()
        self.assertEqual(
            result, Reader.OFFSITE
        )  # Should return 3 as it is within the valid range (0-3)

    @patch.dict(
        os.environ, {"OVERRIDE_READER_TYPE": "4"}
    )  # Mock environment variable to an invalid value
    def test_invalid_reader_type_high(self):
        result = get_dev_reader_type()
        self.assertEqual(
            result, Reader.UNDEFINED
        )  # Should return -1 as the value is outside the valid range

    @patch.dict(
        os.environ, {"OVERRIDE_READER_TYPE": "-1"}
    )  # Mock environment variable to a negative value
    def test_invalid_reader_type_negative(self):
        result = get_dev_reader_type()
        self.assertEqual(
            result, Reader.UNDEFINED
        )  # Should return -1 as the value is outside the valid range

    @patch.dict(
        os.environ, {"OVERRIDE_READER_TYPE": "not_a_number"}
    )  # Mock environment variable to a non-numeric value
    def test_invalid_reader_type_non_numeric(self):
        result = get_dev_reader_type()
        self.assertEqual(
            result, Reader.UNDEFINED
        )  # Should return -1 as the value is not numeric

    @patch.dict(
        os.environ, {}, clear=True
    )  # Mock environment variable to be unset
    def test_no_override_set(self):
        result = get_dev_reader_type()
        self.assertEqual(
            result, Reader.UNDEFINED
        )  # Should return -1 as the environment variable is not set
