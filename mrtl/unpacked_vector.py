"""
Ban any unpacked vectors
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class UnpackedVector(filters.LineListener):
    """ 
    Unpacked vectors are less efficient in memory, waveform programs sometimes don't render them correctly, and you can't assign to the entire vector at once (such as in reset blocks). Avoid usage.
    """
    subscribe_to = [filters.LineBroadcaster]

    unpacked_re = re.compile("\s*\w+\s*\[\w+(-\w+|\s*)+\:\w+\]")

    ERROR_MSG = "Unpacked vector detected. Only packed vectors are permitted."

    def _update(self, line_no, line):
        if self.unpacked_re.search(line):
            # Hack to avoid comments, doesn't capture block comments
            if not re.search("^\s*//", line):
                # Parameters with specified widths seem to be caught by accident right now
                if not re.search("^\s*parameter", line):
                    self.error(line_no, line, self.ERROR_MSG)

    update_line = _update
