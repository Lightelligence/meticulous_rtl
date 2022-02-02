"""
Ban in-line declaration and assignment for types that would infer an initial block
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class DeclareAndAssign(filters.LineListener):
    """Declaring a net of type logic or reg and assigning to it in the same line causes the tool to infer an initial block 
    which is not a synthesizable construct. Only the wire type can be safely used for an single-line declaration and assignment.

    DO NOT DO THIS:
    logic foo = 1'b1;

    because it translates to:
    logic foo;
    initial begin
      foo = 1'b1;
    end

    DO THIS INSTEAD:
    logic foo;
    assign foo = 1'b1;
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    declare_and_assign_re = re.compile("\s*(logic|reg)\s+\w+\s*=")

    ERROR_MSG = "In-line declaration and assignment of a logic or reg is invalid. This is only allowed on wires."

    def _update(self, line_no, line):
        if self.declare_and_assign_re.match(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
