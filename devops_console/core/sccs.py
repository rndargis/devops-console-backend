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

import logging
from devops_sccs.core import Core as SccsCore

class Sccs:
    """Sccs Core"""

    def __init__(self, config):
        self.config = config
        self.core = None

    async def init(self, app):
        self.core = await SccsCore.create(self.config)

    def context(self, plugin_id, args):
        return self.core.context(plugin_id, args)

    async def get_repositories(self, plugin_id, session, args):
        try:
            async with self.core.context(plugin_id, session) as ctx:
                return await ctx.get_repositories(args)
        except:
            logging.exception("get repositories")
            raise

    async def watch_repositories(self, plugin_id, session, args):
        async with self.core.context(plugin_id, session) as ctx:
            async for event in await ctx.watch_repositories(args=args):
                yield event

    async def passthrough(self, plugin_id, session, request, args):
        async with self.core.context(plugin_id, session) as ctx:
            return await ctx.passthrough(request, args)

    async def get_continuous_deployment_config(self, plugin_id, session, repository, environments, args):
        async with self.core.context(plugin_id, session) as ctx:
            return await ctx.get_continuous_deployment_config(repository, environments, args=args)

    async def watch_continous_deployment_config(self, plugin_id, session, repository, environments, args):
        async with self.core.context(plugin_id, session) as ctx:
            async for event in await ctx.watch_continuous_deployment_config(repository, environments, args=args):
                yield event

    async def watch_continuous_deployment_versions_available(self, plugin_id, session, repository, args):
        async with self.core.context(plugin_id, session) as ctx:
            async for event in await ctx.watch_continuous_deployment_versions_available(repository, args=args):
                yield event

    async def trigger_continuous_deployment(self, plugin_id, session, repository, environment, version, args):
        try:
            async with self.core.context(plugin_id, session) as ctx:
                return await ctx.trigger_continuous_deployment(repository, environment, version, args)
        except:
            logging.exception("trigger_continuous_deployment")
            raise

    async def get_continuous_deployment_environments_available(self, plugin_id, session, repository, args):
        async with self.core.context(plugin_id, session) as ctx:
            return await ctx.get_continuous_deployment_environments_available(repository, args)

    async def watch_continuous_deployment_environments_available(self, plugin_id, session, repository, args):
        async with self.core.context(plugin_id, session) as ctx:
            async for event in await ctx.watch_continuous_deployment_environments_available(repository, args=args):
                yield event

    async def bridge_repository_to_namespace(self, plugin_id, session, repository, environment, untrustable=True, args=None):
        async with self.core.context(plugin_id, session) as ctx:
            return await ctx.bridge_repository_to_namespace(repository, environment)

    async def get_add_repository_contract(self, plugin_id, session):
        async with self.core.context(plugin_id, session) as ctx:
            return ctx.get_add_repository_contract()

    async def add_repository(self, plugin_id, session, repository, template,  template_params, args):
        async with self.core.context(plugin_id, session) as ctx:
            return await ctx.add_repository(repository, template,  template_params, args)

    async def compliance_report(self, plugin_id, session, args):
        async with self.core.context(plugin_id, session) as ctx:
            return await ctx.compliance_report(args)

    async def cleanup(self,app):
        await self.core.cleanup()