from prometheus_async import aio

def setup(api):
    api.router.add_get('/metrics', aio.web.server_stats)