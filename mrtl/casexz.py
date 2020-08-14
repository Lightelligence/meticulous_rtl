"""

"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters

class CaseXZ(filters.LineListener):
    """ FIXME
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    wildcard_re = re.compile("^\s*case[xz]")
    
    ERROR_MSG = "Do not use casex. Unsafe why?" # FIXME better message

    def _update(self, line_no, line):
        if self.wildcard_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
