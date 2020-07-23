from devops_sccs.core import Core as SccsCore

class Sccs:
    """Sccs Core"""

    def __init__(self, config):
        self.core = SccsCore(config)
    
    def context(self, plugin_id, args):
        return self.core.context(plugin_id, args)

    async def get_repositories(self, plugin_id, session, args):
        async with self.core.context(plugin_id, session) as ctx:
            results = await ctx.get_repositories(args)

            # TODO: define a standard Repository structure in devop_sccs project
            data_response = []
            for result in results:
                data_response.append({
                    "name": result
                })

            return data_response

    async def passthrough(self, plugin_id, session, request, args):
        async with self.core.context(plugin_id, session) as ctx:
            return await ctx.passthrough(request, args)
