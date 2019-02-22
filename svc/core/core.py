"""Core module"""

from ..config import Config
from . import helloworld

class Core:
    def __init__(self, config=None):
        self.config = config if config else Config()
        self.helloworld = helloworld.Helloworld()