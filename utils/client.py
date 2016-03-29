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

import json
import pyrax
import time

from cafe.engine.http import client


class AuthClient(client.HTTPClient):

    """Client Objects for Auth call."""

    def __init__(self):
        super(AuthClient, self).__init__()

        self.default_headers['Content-Type'] = 'application/json'
        self.default_headers['Accept'] = 'application/json'

    def authenticate_user(self, auth_url, user_name, api_key=None,
        password=None):
        """Get Auth Token & Project ID using api_key
        """
        if api_key:
            request_body = {
                "auth": {
                    "RAX-KSKEY:apiKeyCredentials": {
                        "username": user_name,
                        "apiKey": api_key
                    },
                },
            }
        elif password:
            request_body = {
                "auth": {
                    "passwordCredentials": {
                        "username": user_name,
                        "password": password
                    },
                },
            }
        else:
            print "Please provide a password or apikey"

        request_body = json.dumps(request_body)
        url = auth_url + '/tokens'

        response = self.request('POST', url, data=request_body)
        token = response.json()['access']['token']['id']
        project_id = response.json()['access']['token']['tenant']['id']
        return token, project_id

class OrchestrationClient(client.AutoMarshallingHTTPClient):

    """Client objects for all the Orchestration api calls."""

    def __init__(self, url, auth_token, project_id, serialize_format="json",
                 deserialize_format="json"):
        super(HeatClient, self).__init__(serialize_format,
                                          deserialize_format)
        self.url = url
        self.auth_token = auth_token
        self.project_id = project_id
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['X-Project-Id'] = project_id
        self.default_headers['Content-Type'] = 'application/json'

        self.serialize = serialize_format
        self.deserialize_format = deserialize_format

    def create_service(self, service_name=None,
                       domain_list=None, origin_list=None,
                       caching_list=None, restrictions_list=None,
                       requestslib_kwargs=None,
                       flavor_id=None,
                       log_delivery=None):
        """Creates Service
        :return: Response Object containing response code 200 and body with
                details of service
        PUT
        services/{service_name}
        """
        url = '{0}/services'.format(self.url)

        if not log_delivery:
            log_delivery = {"enabled": False}

        if log_delivery:
            request_object = requests.CreateService(
                service_name=service_name,
                domain_list=domain_list,
                origin_list=origin_list,
                caching_list=caching_list,
                restrictions_list=restrictions_list,
                flavor_id=flavor_id,
                log_delivery=log_delivery)
        else:
            request_object = requests.CreateService(
                service_name=service_name,
                domain_list=domain_list,
                origin_list=origin_list,
                caching_list=caching_list,
                restrictions_list=restrictions_list,
                flavor_id=flavor_id)

        return self.request('POST', url, request_entity=request_object,
                            requestslib_kwargs=requestslib_kwargs)

class FusionClient(client.AutoMarshallingHTTPClient):

    """Client objects for all the Fusion api calls."""

    def __init__(self, url, auth_token, project_id, serialize_format="json",
                 deserialize_format="json"):
        super(FusionClient, self).__init__(serialize_format,
                                          deserialize_format)
        self.url = url
        self.auth_token = auth_token
        self.project_id = project_id
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['X-Project-Id'] = project_id
        self.default_headers['Content-Type'] = 'application/json'

        self.serialize = serialize_format
        self.deserialize_format = deserialize_format

    def get_templates(self, templates_type=None, with_metadata=None):
        """Returns the template_catalog from fusion."""
        url = '{0}/templates'.format(self.url)
        params = {}
        if templates_type:
            params['templates_type'] = templates_type
        if with_metadata:
            params['with_metadata'] = str(with_metadata).lower()
        return self.request('GET', url, params=params)
