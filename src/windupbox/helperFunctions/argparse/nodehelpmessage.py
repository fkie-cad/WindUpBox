# external imports
from anytree import Node
import argparse

# configure logging
import logging
log = logging.getLogger(__name__)


class NodeHelpMessage(Node):
    """
        can be used to create parser with correct help messages in loop
    """
    parser: argparse.ArgumentParser

    def set_help(self):
        self.parser.set_defaults(func=lambda args: self.parser.print_help())

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.set_help()
