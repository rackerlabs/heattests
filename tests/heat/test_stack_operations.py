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


class TestStackOperations(base.TestBase):

    def setUp(self):
        super(TestStackOperations, self).setUp()

    def test_list_stack(self):
        resp = self.heat_client.list_stacks()
        self.assertEqual(resp.status_code, 200)

    def test_create_stack(self):
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = self.config.template_url
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 201)
        self.stack_list[resp.json()['stack']['id']] = stack_name

    def test_find_stack(self):
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = self.config.template_url
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        stack_id = body['stack']['id']
        self.stack_list[stack_id] = stack_name

        resp = self.heat_client.find_stack(stack_id=stack_id)
        body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(body['stack']['stack_name'], stack_name)
        self.assertEqual(body['stack']['id'], stack_id)
        self.assertEqual(body['stack']['stack_user_project_id'],
                         self.user_project_id)

    def test_show_stack(self):
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = self.config.template_url
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        stack_id = body['stack']['id']
        self.stack_list[stack_id] = stack_name

        resp = self.heat_client.show_stack(stack_name=stack_name,
                                           stack_id=stack_id)
        body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(body['stack']['stack_name'], stack_name)
        self.assertEqual(body['stack']['id'], stack_id)
        self.assertEqual(body['stack']['stack_user_project_id'],
                         self.user_project_id)

    def test_preview_stack(self):
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = self.config.template_url

        resp = self.heat_client.preview_stack(stack_name=stack_name,
                                              template_url=temp_url)
        self.assertEqual(resp.status_code, 200)

    def test_delete_stack(self):
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = self.config.template_url
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        stack_id = body['stack']['id']

        resp = self.heat_client.delete_stack(stack_name=stack_name,
                                             stack_id=stack_id)
        self.assertEqual(resp.status_code, 204)

    def test_update_stack(self):
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = self.config.template_url
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        stack_id = body['stack']['id']

        self.stack_list[stack_id] = stack_name
        resp = self.heat_client.update_stack(stack_name=stack_name,
                                             stack_id=stack_id,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 202)

    def test_abandon_stack(self):
        self.skipTest('Not working - Test needs to be updated')
        # Add the use of the test.yaml and check nova to ensure server exists
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = 'https://raw.githubusercontent.com/BeenzSyed/heat-ci/' \
                   'add_test_template/dev/test.yaml'
        params = {'flavor': '1 GB Performance',
                  'image': '9d29f10e-4fc2-4556-8d25-532d1784329a'}
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url,
                                             parameters=params)
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        stack_id = body['stack']['id']

        resp = self.heat_client.abandon_stack(stack_name=stack_name,
                                              stack_id=stack_id)
        self.assertEqual(resp.status_code, 200)

    def test_adopt_stack(self):
        self.skipTest('Not working - Adopt stack might be taken out of Heat')
        stack_name = self.generate_random_string(prefix='Heat_QE')
        temp_url = 'https://raw.githubusercontent.com/BeenzSyed/heat-ci/' \
                   'add_test_template/dev/test.yaml'
        params = {'flavor': '1 GB Performance',
                  'image': '9d29f10e-4fc2-4556-8d25-532d1784329a'}
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url,
                                             parameters=params)
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        stack_id = body['stack']['id']
        self.stack_list.append(stack_id)
        self.stack_url = resp.headers['location']

        # Wait to ensure that stack has completed
        self.heat_client.wait_for_stack_status(
            location=self.stack_url,
            status='CREATE_COMPLETE',
            abort_on_status='FAILED',
            retry_interval=5,
            retry_timeout=300)

        resp = self.heat_client.abandon_stack(stack_name=stack_name,
                                              stack_id=stack_id)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()

        resp = self.heat_client.adopt_stack(stack_name, adopt_stack_data=body,
                                            template_url=temp_url)
        self.assertEqual(resp.status_code, 201)

    def tearDown(self):
        super(TestStackOperations, self).tearDown()
