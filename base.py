# Copyright (c) 2016 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import string

from heattests.utils import client
from heattests.utils import config

from cafe.drivers.unittest import fixtures


class TestBase(fixtures.BaseTestFixture):

    """Child class of fixtures.BaseTestFixture for testing Heat.

    Inherit from this and write your test methods. If the child class defines
    a prepare(self) method, this method will be called before executing each
    test method.
    """

    @classmethod
    def setUpClass(cls):

        super(TestBase, cls).setUpClass()

        import requests.packages.urllib3
        requests.packages.urllib3.disable_warnings()

        cls.auth_config = config.AuthConfig()

        cls.auth_client = client.AuthClient()
        auth_token, cls.user_project_id = \
            cls.auth_client.authenticate_user(
                cls.auth_config.base_url,
                cls.auth_config.user_name,
                cls.auth_config.api_key,
                cls.auth_config.password)

        cls.config = config.HeatConfig()

        cls.url = cls.config.base_url + cls.user_project_id
        cls.fusion_client = client.FusionClient(cls.url, auth_token,
                                        cls.user_project_id,
                                        serialize_format='json',
                                        deserialize_format='json')

        cls.heat_client = client.HeatClient(cls.url, auth_token,
                                        cls.user_project_id,
                                        serialize_format='json',
                                        deserialize_format='json')

    def generate_random_string(self, prefix='Heat-Tests', length=12):
        """Generates a random string of given prefix & length"""
        random_string = ''.join(random.choice(
            string.ascii_lowercase + string.digits)
            for _ in range(length))
        random_string = prefix + random_string
        return random_string

    @classmethod
    def tearDownClass(cls):
        """Deletes the added resources."""
        super(TestBase, cls).tearDownClass()
