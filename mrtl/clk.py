"""
Ensure we don't hook up conflicting clocks
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class Clk(filters.LineListener):
    """Changing clock names through hierarchy is dangerous because it is difficult
    to catch RTL clock wiring bugs in simulation. It is acceptable to change names if you
    are going from more-specific to less specific like in the following examples:
    .clk (eclk)
    or
    .sclk(ccu31_sclk)
    however, it is illegal to completely change clock names on the boundary like:
    .eclk(sclk)
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    clk_re = re.compile("\.(\w+clk)\s*\(\s*(\w+)\s*\)")

    ERROR_MSG = "clk issue detected. Do not change clock names on a hierarchical boundary."

    def _update(self, line_no, line):
        clk_search = self.clk_re.search(line)
        if clk_search:
            port_name = clk_search.group(1)
            net_name  = clk_search.group(2)
            if not net_name.endswith(port_name):
                self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
