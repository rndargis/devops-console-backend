from .core import Core

_core = None

def getCore(config=None):
    """Get a unique core

    Returns:
        Core: a common core instance
    """
    global _core
    if _core is None:
        _core = Core(config)

    return _core