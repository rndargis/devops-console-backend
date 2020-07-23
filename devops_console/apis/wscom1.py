from aiohttp import web
from ..wscom import wscom_generic_handler

routes = web.RouteTableDef()

DISPATCHERS_APP_KEY="wscom1_dispatchers"

@routes.get('/wscom1')
async def wscom1_handler(request):
    """Websocket Com1"""

    ws = await wscom_generic_handler(request, DISPATCHERS_APP_KEY)

    return ws
