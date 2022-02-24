"""
Bans the use of an endmodule label
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class EndmoduleLabel(filters.LineListener):
    """
    endmodule labels are banned. Having one makes a future change to the module name more difficult. They may be helpful in cases
    where multiple-modules are defined in the same file, but doing so would go against our methodology. only 1 module may be defined
    per-file.
    """
    subscribe_to = [filters.EndModuleBroadcaster]

    ERROR_MSG = "endmodule label must be removed"

    def update_endmodule(self, line_no, line, match):
        if match is not None:
            self.error(line_no, line, self.ERROR_MSG)
