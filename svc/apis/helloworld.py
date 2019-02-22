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
