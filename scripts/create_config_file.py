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
import argparse
import os
import pwsafe
import requests

requests.packages.urllib3.disable_warnings()

sso_username = os.environ.get('RACKER_USERNAME')
sso_password = os.environ.get('RACKER_PASSWORD')


def get_regression_credentials_from_pwsafe(tenant_name):
    cli = pwsafe.PWSafeClient(sso_username, sso_password)
    heat_test_accounts = cli.projects["1256"]
    for creds in heat_test_accounts.credentials:
        if creds.username.split(" ")[0] == tenant_name:
            return "{0}".format(creds.password)


def create_heattests_config_file(env, tenant_name, password, template_url):
    with open("etc/tests.conf", "w") as f:
        f.write('[auth]\n')
        f.write('user_name={username}\n'.format(username=tenant_name))
        f.write('password={password}\n'.format(password=password))
        f.write('base_url=https://identity.api.rackspacecloud.com/v2.0\n\n')
        f.write('[heat]\n')
        f.write('base_url={env}\n'.format(env=env))
        f.write('template_url={template_url}\n'.format(
            template_url=template_url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--env")
    parser.add_argument("--tenant_name")
    parser.add_argument("--template_url")

    args = parser.parse_args()

    password = get_regression_credentials_from_pwsafe(
        tenant_name=args.tenant_name)

    if os.path.exists("etc/tests.conf"):
        os.remove("etc/tests.conf")

    create_heattests_config_file(env=args.env,
                                 tenant_name=args.tenant_name,
                                 password=password,
                                 template_url=args.template_url)
