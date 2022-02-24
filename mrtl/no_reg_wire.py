"""
Ensures the else of an if statement has the preceeding end on the same line
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class NoRegWire(filters.LineListener):
    """
    Keywords reg and wire are banned in favor of using custom-types or the logic keyword. use of reg and wire
    is less-portable than use of logic because it requires the designer to consider whether they need a net or a variable.
    Modern EDA tools can correctly infer net vs. variable when they encounter the logic type. 

    This rule does not apply to AUTOREGINPUT and AUTOWIRE blocks which will automatically use wire and reg types.
    """
    subscribe_to = [
        filters.ModuleLineBroadcaster, filters.AutoRegInputBroadcaster, filters.AutoWireBroadcaster,
        filters.EndAutosBroadcaster
    ]

    reg_wire_re = re.compile("\s*(reg|wire)\s+\w+;")
    in_autos = False

    ERROR_MSG = "reg and wire types are banned. use logic or a custom type."

    def update_moduleline(self, line_no, line):
        if not self.in_autos and re.match(self.reg_wire_re, line):
            self.error(line_no, line, self.ERROR_MSG)

    def update_autoreginput(self, line_no, line):
        self.in_autos = True

    def update_autowire(self, line_no, line):
        self.in_autos = True

    def update_endautos(self, line_no, line):
        self.in_autos = False
