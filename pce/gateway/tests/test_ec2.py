#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from pce.gateway.ec2 import EC2Gateway

REGION = "us-west-2"


class TestEC2Gateway(TestCase):
    def setUp(self):
        self.aws_ec2 = MagicMock()
        with patch("boto3.client") as mock_client:
            mock_client.return_value = self.aws_ec2
            self.ec2 = EC2Gateway(REGION)

    def test_describe_availability_zones(self):
        client_return_response = {
            "AvailabilityZones": [
                {
                    "State": "available",
                    "ZoneName": "foo_1_zone",
                },
                {
                    "State": "available",
                    "ZoneName": "foo_2_zone",
                },
                {
                    "State": "information",
                    "ZoneName": "foo_3_zone",
                },
                {
                    "State": "available",
                    "ZoneName": "foo_4_zone",
                },
            ]
        }

        self.aws_ec2.describe_availability_zones = MagicMock(
            return_value=client_return_response
        )

        expected_availability_zones = [
            "foo_1_zone",
            "foo_2_zone",
            "foo_3_zone",
            "foo_4_zone",
        ]

        availability_zones = self.ec2.describe_availability_zones()
        self.assertEqual(expected_availability_zones, availability_zones)

        self.aws_ec2.describe_availability_zones.assert_called()
