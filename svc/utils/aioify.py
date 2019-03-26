import asyncio
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor

_coreaioify = None

def getCoreAioify(config=None):
    """Get a unique core aioify

    Returns:
        CoreAioify: a common core instance
    """
    global _coreaioify
    if _coreaioify is None:
        _coreaioify = CoreAioify(config)

    return _coreaioify

def aioify(pool=None):
    def aioify_decorator(func):
        @wraps(func)
        async def run(*args, loop=None, pool=pool, **kwargs):
            if loop is None:
                loop = asyncio.get_event_loop()
            executor = None if pool is None else getCoreAioify().get_executor(pool)

            pfunc = partial(func, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)
        return run
    return aioify_decorator

class CoreAioify(object):
    def __init__(self, config=None):
        self.executor_pools = {}

    def create_thread_pool(self, pool_name, max_workers=None, thread_name_prefix='', initializer=None, initargs=()):
        if (self.executor_pools.get(pool_name, False)):
            raise Exception(f"Pool {pool_name} already exist !")

        self.executor_pools[pool_name] = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=thread_name_prefix,
            initializer=initializer,
            initargs=initargs
        )

    def get_executor(self, pool_name):
        return self.executor_pools[pool_name]