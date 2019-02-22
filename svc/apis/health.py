from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/health')
async def health(request):
    """
    ---
    description: Health check endpoint
    tags:
    - Health check
    produces:
    - application/json
    responses:
        "200":
            description: success
    """
    return web.json_response({'status' : True})
