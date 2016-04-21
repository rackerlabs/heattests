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


def assertable_status_codes(defaults=None):
    """
    Decorator for client methods that return (resp, body). This decorator adds
    the optional kwarg "status_codes" to the signature and will assert that the
    status code in the response matches what was expected. The decorator
    accepts the optional kwarg "defaults", which status_codes will default to
    if it is not included. If neither defaults nor status_codes is specified,
    all status codes are accepted.

    Example usage:

    @assertable_status_codes(defaults=[200])
    def some_client_method(self):
        ...

    client.some_client_method() # will assert status is 200
    client.some_client_method(status_codes=[404]) # will assert status is 404


    @assertable_status_codes()
    def another_client_method(self):
        ...

    # will not assert anything about the status
    client.another_client_method()

    # will assert status is 404
    client.another_client_method(status_codes=[404])
    """
    def decorator(f):
        def wrapper(self, *args, **kwargs):
            status_codes = kwargs.pop('status_codes', defaults)
            resp, body = f(self, *args, **kwargs)

            if status_codes is not None:
                status = int(resp['status'])
                msg = ("Expected status to be one of (%s) but it was actually "
                       "%d. Body: %s" % (', '.join(map(str, status_codes)),
                                         status, body))
                assert (status in status_codes), msg

            return resp, body

        return wrapper

    return decorator
