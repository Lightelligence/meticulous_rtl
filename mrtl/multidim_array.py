"""
Ban multidimensional arrays
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class MultiDimArray(filters.LineListener):
    """ 
    FIXME: ADD REASONING
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    multidim_re = re.compile("logic.*\w+((\[.*\:.*\]){2}|(\[.*\:.*\]){3})")

    ERROR_MSG = "Multidimensional array of logic type detected. Use typedef instead."

    def _update(self, line_no, line):
        if self.multidim_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
