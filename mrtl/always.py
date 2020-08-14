"""
Ban always_latch & always blocks, allow always_ff & always_comb
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters

class Always(filters.LineListener):
    """ FIXME
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    always_re = re.compile("^\s*always(_latch|\s)")
    
    ERROR_MSG = "Do not use always or always_latch. Unsafe why?" # FIXME better message

    def _update(self, line_no, line):
        if self.always_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
