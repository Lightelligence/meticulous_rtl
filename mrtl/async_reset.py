"""
Our methodology is to primarily use sync reset.
Explicitly requiring a waiver encourages the usage of sync reset.
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class AsyncReset(filters.LineListener):
    """
    Our methodology is to primarily use sync reset.
    Explicitly requiring a waiver encourages the usage of sync reset.
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    async_re = re.compile("^\s*always.*\(.*edge\s+[a-zA-Z0-9_]*re*se*t")
    # async_re = re.compile("^\s*always.*\(.*edge")

    ERROR_MSG = "async reset detected. sync reset preferred if possible."

    def _update(self, line_no, line):
        if self.async_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
