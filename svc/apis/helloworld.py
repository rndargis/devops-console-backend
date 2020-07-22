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

from aiohttp import web

# Optional dependency. Read hello function
from ..core import getCore

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    """
    ---
    description: Say Helloworld
    tags:
    - Helloworld
    produces:
    - text/plain
    responses:
        "200":
            description: success
    """
    # core object can be requested in 2 way.
    #
    # aiohttp suggest the use of request.app or request.config_dict
    # however it can be interesting to use the getCore() alternative
    # for IDE completion support.

    #core = request.config_dict['core']
    #await core.helloworld.say_hello()

    # OR

    await getCore().helloworld.say_hello()

    return web.Response(text="Hello, world!")

@routes.get('/{name}')
async def hello_who(request):
    """
    ---
    description: Say Hello Name
    tags:
    - Helloworld
    produces:
    - text/plain
    parameters:
    - in: path
      name: name
      description: Your name
      schema:
        type: string
      required: true
    responses:
        "200":
            description: success
    """
    return web.Response(text="Hello, {} !".format(request.match_info['name']))

sub = web.Application()
sub.add_routes(routes)
