DevOps Console Backend
======================

Provides DevOps Console Backend. This is an alpha version without APIs stability.

The main purpose is to provide a service (splitted in multiple services in the future) that will be able to communicate with all "DevOps" systems.
It will be the entrypoint for a DevOps Console UI but not restrictive to this only concern.

Quick Start
-----------

Installation
^^^^^^^^^^^^

This package is available for Python 3.7+.

.. code:: bash

    pip3 install --user -e .

With docker:

.. code:: bash

    docker build -t devops-console-backend .

Start the service
^^^^^^^^^^^^^^^^^

On a local installation:

.. code:: bash

    BRANCH_NAME=dev python -m devops_console.run

With docker:

.. code:: bash

    docker run -it --rm -e BRANCH_NAME=dev -p 5000:5000 devops-console-backend:latest

Swagger
-------

.. code:: bash

    curl http://localhost:5000/api/doc/swagger.json

You can use the Swagger UI at this location: http://localhost:5000/api/doc/

WebSocket
---------

More documentation are available under apis/wscom1.py and wscom.py
