Python scaffold with aiohttp server
===================================

Provides skeleton of an aiohttp server service with swagger, prometheus, sub application, sync to asyncio helper, docker, json config...

Quick Start
-----------

Installation
^^^^^^^^^^^^

This package is available for Python 3.7+.

.. code:: bash

    pip3 install --user -e .

With docker:

.. code:: bash

    docker build --build-arg BRANCH_NAME=dev -t scaffold-aiohttp .

Start the service
^^^^^^^^^^^^^^^^^

On a local installation:

.. code:: bash

    BRANCH_NAME=dev python -m svc.run

With docker:

.. code:: bash

    docker run -it --rm -p 5000:5000 scaffold-aiohttp:latest

Test it
^^^^^^^

.. code:: bash

    curl http://localhost:5000/helloworld/
    curl http://localhost:5000/helloworld/test


Create a real project from the scaffold
---------------------------------------

.. code:: bash

    mkdir demo-aiohttp
    cd demo-aiohttp
    git init
    git remote add tpl https://github.com/croixbleueqc/scaffold-aiohttp
    git fetch tpl
    git merge tpl/master

    # Use python setup.py init -h for more details
    python setup.py init --name=demo_aiohttp --desc="This is a demo" -g

    # you are ready to go !
    docker build --build-arg BRANCH_NAME=dev -t demo-aiohttp .
    docker run -it --rm -p 5000:5000 demo-aiohttp:latest

    # alternative (install dependencies before)
    # BRANCH_NAME=dev python -m demo_aiohttp.run

BRANCH_NAME and configurations
------------------------------

BRANCH_NAME is the execution environment which permits to select the right configuration for the application in the config folder.

See config.py for more details.