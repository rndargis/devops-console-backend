'''
Configuration module to parse json configuration files correctly

Config files are stored in the config folder inside the module.

the BRANCH_NAME determines the configuration to load.

Config will merge (listed as less to more important):
- default.json
- <BRANCH_NAME>.json
- local.json

In addition, Config will replace all {env} string in a json file to the BRANCH_NAME value.

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

import json
import os

from functools import reduce
from copy import deepcopy

class Config(dict):
    '''
    Configuration class
    '''
    def __init__(self):
        super().__init__()

        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        if os.environ.get("BRANCH_NAME") is None:
            os.environ["BRANCH_NAME"] = "undefined"

        config = self.__load_config()
        self.update(config)

        self.__deep_replace(self, env=os.environ["BRANCH_NAME"])

    def use_resource(self, resource):
        return '{dir}/resources/{resource}'.format(dir=self.dir_path, resource=resource)

    def __load_config(self):
        default = self.__load_config_file('default')
        env = self.__load_config_file(os.environ["BRANCH_NAME"])
        local = self.__load_config_file('local')

        # Order is important inside the list
        return reduce(self.__deep_merge, [{}, default, env, local])

    def __load_config_file(self, file_name):
        file_path = '{dir}/config/{name}.json'.format(dir=self.dir_path, name=file_name)
        return self.__load_json(file_path)

    def __load_json(self, json_file):
        '''Load JSON file

        Args:
            json_file (str): filename of a json file

        Returns:
            dict: content of the file
        '''
        try:
            with open(json_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def __deep_merge(self, dict_base, dict_custom):
        result = deepcopy(dict_base)
        for key, value in dict_custom.items():
            if isinstance(value, dict):
                node = result.setdefault(key, {})
                mergedNode = self.__deep_merge(node, value)
                result[key] = mergedNode
            else:
                result[key] = value

        return result

    def __deep_replace(self, dict_base, **kwargs):
        for name, value in dict_base.items():
            if isinstance(value, dict):
                self.__deep_replace(value, **kwargs)
            elif isinstance(value, str):
                dict_base[name] = value.format(**kwargs)
