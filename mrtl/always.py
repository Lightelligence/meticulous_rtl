"""
Ban always_latch & always blocks, allow always_ff & always_comb
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class Always(filters.LineListener):
    """
    SystemVerilog adds three new types of procedural always blocks that more clearly express intent. 
    These are: always_comb, always_latch, and always_ff. Simulation, lint, and synthesis can issue warnings 
    if the code modeled within these new procedural blocks does not match the designated type. This is a safer
    and more explicit coding style as opposed to a simple always block like one would see in traditional Verilog.

    We only allow always_comb and always_ff here, because use of latches is generally not preffered, unless in unique circumstances. If such a circumstance arises, use always_latch, and waive this check.
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    always_re = re.compile("\s*always(\\b|_latch)")

    ERROR_MSG = "always or always_latch detected. Only always_comb or always_ff are permitted."

    def _update(self, line_no, line):
        if self.always_re.match(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
