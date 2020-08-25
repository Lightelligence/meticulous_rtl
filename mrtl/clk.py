"""
Ensure we don't hook up aclk to eclk
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class Clk(filters.LineListener):
    """ 
    FIXEME: add motivation
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    clk_re = re.compile("\wclk\s*.*clk")

    ERROR_MSG = "clk issue detected. Do not hook up aclk to eclk (vice versa)."

    def _update(self, line_no, line):
        if self.clk_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
