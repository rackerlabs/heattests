# coding= utf-8

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

import ddt

from heattests import base


@ddt.ddt
class TestTemplateID(base.TestBase):

    def setUp(self):
        super(TestTemplateID, self).setUp()

    @ddt.data(1, True)
    def test_get_template_id_with_metadata(self, data):
        resp = self.fusion_client.get_templates(with_metadata=data)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        #save_file(file_name=my_method_name(), body_of_file=body)
        #true_body = get_file(file_name=my_method_name())
        #self.assertEqual(body, true_body)
