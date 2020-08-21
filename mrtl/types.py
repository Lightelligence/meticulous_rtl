"""
Ban casex and casez, use case...inside only
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class Types(filters.LineListener):
    """ 
    Ban the following types: bit, real, integer (should use int instead), string, byte, shortint, longint, wand, wor, tri, triand, trior, tri0, tri1, supply0, supply1, trireg, shortreal, realtime, class
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    type_re = re.compile(
        "^\s*(bit|real|time|integer|string|byte|shortint|longint|wand|wor|tri|triand|trior|tri0|tri1|supply0|supply1|trireg|shortreal|realtime|class)\\b"
    )

    ERROR_MSG = "Banned type detected."

    def _update(self, line_no, line):
        if self.type_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
