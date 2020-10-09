# Copyright 2019 mickybart
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

from .wscom import wscom_setup
from .apis import wscom1
from .apis import health
from .apis import sccs
from .apis import kubernetes

def setup(api):
    api.add_routes(health.routes)

    api.add_routes(wscom1.routes)
    wscom_setup(api, wscom1.DISPATCHERS_APP_KEY, "sccs", sccs.wscom_dispatcher)

    wscom_setup(api, wscom1.DISPATCHERS_APP_KEY, "k8s", kubernetes.wscom_dispatcher)

    return api
