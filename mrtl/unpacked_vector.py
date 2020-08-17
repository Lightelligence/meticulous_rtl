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
    FIXME: reason why no unpacked vectors
    """
    subscribe_to = [filters.LineBroadcaster]

    unpacked_re = re.compile("\s*\w+\s*\[\w+(-\w+|\s*)+\:\w+\]")

    ERROR_MSG = "Unpacked vector detected. Only packed vectors are permitted."

    def _update(self, line_no, line):
        if self.unpacked_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_line = _update
