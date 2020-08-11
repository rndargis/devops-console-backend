# Copyright 2020 Croix Bleue du Québec

# This file is part of devops-console-backend.

# devops-console-backend is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# devops-console-backend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with devops-console-backend.  If not, see <https://www.gnu.org/licenses/>.

from aiohttp import web
from ..core import Core
from ..wscom import DispatcherUnsupportedRequest

routes = web.RouteTableDef()

@routes.post('/repositories')
async def repositories(request):
    """
    List repositories
    ---
    summary: List repositories
    tags:
      - Source Code Control Systems
    requestBody:
        description: Configuration for devops_sccs/get_repositories
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                plugin:
                  type: string
                  required: true
                  example: demo
                session:
                  type: object
                  required: true
                  example:
                    user: test
                args:
                  type: object
    responses:
        "200":
            description: success
    """
    core: Core = request.config_dict['core']

    body = await request.json()
    result = await core.sccs.get_repositories(body["plugin"], body["session"], body.get("args"))

    return web.json_response(result)

@routes.post('/{plugin_id}/repositories')
async def repositories_long(request):
    """
    List repositories (alternative)
    ---
    summary: List repositories (explicit path)
    tags:
      - Source Code Control Systems
    parameters:
      - in: path
        name: plugin_id
        required: true
        description: plugin to use
        schema:
          type: string
        example: demo
    requestBody:
        description: Configuration for devops_sccs/get_repositories
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                session:
                  type: object
                  required: true
                  example:
                    user: test
                args:
                  type: object
    responses:
        "200":
            description: success
    """
    core: Core = request.config_dict['core']

    body = await request.json()
    plugin_id = request.match_info["plugin_id"]

    result = await core.sccs.get_repositories(plugin_id, body["session"], body.get("args"))

    return web.json_response(result)

@routes.post('/passthrough')
async def passthrough(request):
    """
    Passthrough interface
    ---
    summary: Passthrough interface
    tags:
      - Source Code Control Systems
    requestBody:
        description: Configuration for devops_sccs/passthrough
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                plugin:
                  type: string
                  required: true
                  example: demo
                session:
                  type: object
                  required: true
                  example:
                    user: test
                request:
                  type: string
                  required: true
                  example: echo
                args:
                  type: object
    responses:
        "200":
            description: success
    """
    core: Core = request.config_dict['core']

    body = await request.json()

    result = await core.sccs.passthrough(body["plugin"], body["session"], body["request"], body.get("args"))

    return web.json_response(result)

@routes.post('/{plugin_id}/passthrough/{request}')
async def passthrough_long(request):
    """
    Passthrough interface (alternative)
    ---
    summary: Passthrough interface (explicit path)
    tags:
      - Source Code Control Systems
    parameters:
      - in: path
        name: plugin_id
        required: true
        description: plugin to use
        schema:
          type: string
        example: demo
      - in: path
        name: request
        required: true
        description: request
        schema:
          type: string
        example: echo
    requestBody:
        description: Configuration for devops_sccs/passthrough
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                session:
                  type: object
                  required: true
                  example:
                    user: test
                args:
                  type: object
    responses:
        "200":
            description: success
    """
    core: Core = request.config_dict['core']

    body = await request.json()
    plugin_id = request.match_info["plugin_id"]
    plugin_request = request.match_info["request"]

    result = await core.sccs.passthrough(plugin_id, body["session"], plugin_request, body.get("args"))

    return web.json_response(result)


sub = web.Application()
sub.add_routes(routes)

# WebSocket (wscom) section

async def wscom_dispatcher(request, action, path, body):
    core: Core = request.config_dict['core']

    if action == "read":
        if path == "/repositories":
            return await core.sccs.get_repositories(body["plugin"], body["session"], body.get("args"))
    elif action == "":
        if path == "/passthrough":
            return await core.sccs.passthrough(body["plugin"], body["session"], body["request"], body.get("args"))

    raise DispatcherUnsupportedRequest(action, path)

