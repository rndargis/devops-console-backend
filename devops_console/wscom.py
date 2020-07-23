from aiohttp import web, WSMsgType
import logging
import json

async def wscom_generic_handler(request, dispatchers_app_key):
    """Websocket Generic handler

    This generic handler will respond to a specific message type only.
    By security, if the message is malformed, the websocket will be closed.

    This handler is using dispatcher functions set with wscom_setup()
    
    Message expected:
    {
        "uniqueId": "<str>",
        "request": "<deeplink>:<action>:<path>",
        "dataRequest": <json values>
    }

    Response on success:
    {
        "uniqueId": "<str>",
        "dataResponse": <json values>
    }

    Response on error:
    {
        "uniqueId": "<str>",
        "error": "<str>"
    }

    Reserved Messages request are:
    - "ws:ctl:close" : Ask the server to close the websocket
    
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    logging.info("connected")
    
    request.app["websockets"].add(ws)
    dispatchers = request.app.get(dispatchers_app_key, {})
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    _ = data["uniqueId"]
                    request_headers = data.pop("request")
                    body = data.pop("dataRequest")

                    deeplink, action, path = request_headers.split(":")
                except (AttributeError, ValueError, json.decoder.JSONDecodeError):
                    # Malformed request.
                    logging.error(f"malformed request. ws will be closed")
                    
                    # Closing the websocket
                    break
                
                if request_headers == "ws:ctl:close":
                    # Closing the websocket
                    break

                dispatch = dispatchers.get(deeplink)

                if dispatch is None:
                    logging.warn(f"There is no dispatcher to support {request_headers}")
                    data["error"] = f"There is no dispatcher to support {deeplink}"
                else:
                    logging.info(f"dispatching {request_headers}")
                    try:
                        data["dataResponse"] = await dispatch(request, action, path, body)
                    except Exception as e:
                        data["error"] = str(e)

                await ws.send_json(data)

            elif msg.type == WSMsgType.ERROR:
                logging.error("ws connection closed with exception {}".format(ws.exception()))
    finally:
        logging.info("disconnected")
        request.app["websockets"].discard(ws)

    return ws

class DispatcherUnsupportedRequest(Exception):
    def __init__(self, action, path):
        Exception.__init__(self, f"Dispatcher does not support {action}:{path} with provided dataRequest")

class DeepLinkAlreadySet(Exception):
    def __init__(self, deeplink, dispatchers_app_key):
        Exception.__init__(self, f"The deeplink {deeplink} is already registred for {dispatchers_app_key}")

def wscom_setup(app, dispatchers_app_key, deeplink, dispatch):
    """Setup a dispatcher function for a deeplink
    
    Final target is a dict of dispatcher functions for all deeplink that will be received on the websocket.

    app[dispatchers_app_key] = {
            "<deeplink 1>": dispatch_func1,
            "<deeplink 2>": dispatch_func2,
            ...
        }
    """

    if app.get(dispatchers_app_key) is None:
        app[dispatchers_app_key] = {}
    
    if app[dispatchers_app_key].get(deeplink) is not None:
        raise DeepLinkAlreadySet(deeplink, dispatchers_app_key)

    app[dispatchers_app_key][deeplink] = dispatch
