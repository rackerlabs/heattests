"""
Copyright 2016 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from heattests import base


class TestStackEvents(base.TestBase):

    def setUp(self):
        super(TestStackEvents, self).setUp()

        stack_name = self.generate_random_string(prefix='Sabeen')
        temp_url = 'https://raw.githubusercontent.com/rackerlabs/heat-ci/' \
                   'master/dev/smoke.yaml'
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 201)
        self.stack_list[resp.json()['stack']['id']] = stack_name

    def tearDown(self):
        super(TestStackEvents, self).tearDown()

    def test_find_stack_events(self):
        resp = self.heat_client.find_stack(stack_id=self.stack_list.keys()[0])
        stack_name = resp.json()['stack']['stack_name']

        resp = self.heat_client.find_stack_events(stack_name=stack_name)
        self.assertEqual(resp.status_code, 200)

    def test_list_stack_events(self):
        resp = self.heat_client.find_stack(stack_id=self.stack_list.keys()[0])
        stack_name = resp.json()['stack']['stack_name']

        resp = self.heat_client.list_stack_events(
                stack_name=stack_name,
                stack_id=self.stack_list.keys()[0])
        self.assertEqual(resp.status_code, 200)

    def test_list_resource_events(self):
        resp = self.heat_client.find_stack(stack_id=self.stack_list.keys()[0])
        stack_name = resp.json()['stack']['stack_name']

        resp = self.heat_client.list_resources(
                stack_name=stack_name,
                stack_id=self.stack_list.keys()[0])
        self.assertEqual(resp.status_code, 200)

        resp = self.heat_client.list_resource_events(
                stack_name=stack_name,
                stack_id=self.stack_list.keys()[0],
                resource_name=resp.json()['resources'][0]['resource_name'])

    def test_show_event_details(self):
        resp = self.heat_client.find_stack(stack_id=self.stack_list.keys()[0])
        stack_name = resp.json()['stack']['stack_name']

        resp_res = self.heat_client.list_resources(
                stack_name=stack_name,
                stack_id=self.stack_list.keys()[0])
        self.assertEqual(resp.status_code, 200)

        resp_event = self.heat_client.list_stack_events(
                stack_name=stack_name,
                stack_id=self.stack_list.keys()[0])
        self.assertEqual(resp.status_code, 200)

        resp = self.heat_client.show_event_details(
                stack_name=stack_name,
                stack_id=self.stack_list.keys()[0],
                res_name=resp_res.json()['resources'][0]['resource_name'],
                event_id=resp_event.json()['events'][0]['id'])
