# external imports
import argparse


class SmartFormatter(argparse.HelpFormatter):
    """
        argparse formatter to display new lines in help messages
    """
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)
