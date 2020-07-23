# Copyright 2019 mickybart

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .wscom import wscom_setup
from .apis import wscom1
from .apis import health
from .apis import sccs

def setup(api):
    api.add_routes(health.routes)
    api.add_subapp("/sccs/", sccs.sub)

    api.add_routes(wscom1.routes)
    wscom_setup(api, wscom1.DISPATCHERS_APP_KEY, "sccs", sccs.wscom_dispatcher)

    return api
