'''Test service module
'''

# Copyright 2019 mickybart

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from multiprocessing import Process

import time
import unittest
import requests

from svc.app import App #pylint: disable=E0401

class ServiceTest(unittest.TestCase):
    '''Test suite for the whole service
    '''
    def setUp(self):
        def run_server():
            ms = App()
            ms.run()

        # Start the server
        self.server = Process(target=run_server)
        self.server.start()

        # Need to wait a little bit to be sure that the server is running
        time.sleep(2)

    def tearDown(self):
        self.server.terminate()
        self.server.join()

    def test_service_started(self):
        '''Test that health endpoint responds correctly
        '''
        response = requests.get("http://localhost:5000/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status' : True})
