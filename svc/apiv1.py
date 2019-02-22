from .apis import health
from .apis import helloworld

def setup(api):
    api.add_routes(health.routes)
    api.add_subapp('/helloworld/', helloworld.sub)

    return api