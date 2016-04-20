Heat Tests
=========



How to Run the Tests
================

1. Create a new virtualenv and install the dependencies::

    NOTE: At the time of this writing opencafe is not compatible with python 3.
          So you will need to create virtualenv with python 2.

    $ pip install -r requirements.txt
    $ cafe-config init
    $ cafe-config plugins install http

2. Set the following environment variables::

    export CAFE_CONFIG_FILE_PATH={path/to/heattests/etc/tests.conf}
    export CAFE_ROOT_LOG_PATH=~/.heat/logs
    export CAFE_TEST_LOG_PATH=~/.heat/logs

3. If you desire highlighting in the output, set the following environment variables::

    export NOSE_WITH_OPENSTACK=1
    export NOSE_OPENSTACK_COLOR=1
    export NOSE_OPENSTACK_RED=0.05
    export NOSE_OPENSTACK_YELLOW=0.025
    export NOSE_OPENSTACK_SHOW_ELAPSED=1
    export NOSE_OPENSTACK_STDOUT=1

4. Make a directory ~/.heat to store the log files in::

    mkdir ~/.heat

5. Create your config file by running the below script. This will create your config file under heattests/etc::

    $ python scripts/create_config_file.py --tenant_name {tenant name (not id)} --env {environment endpoint} --template_url {template url}

6. Set the following environment variables using a service account::

    $ export RACKER_USERNAME={username of service account}
    $ export RACKER_PASSWORD={password of service account}

7. Once you are ready to run the tests::

    $ nosetests tests
