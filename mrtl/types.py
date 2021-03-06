"""
Ban certain type keywords which can lead to non-portable or non-synthesizable code.
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class Types(filters.LineListener):
    """Synthesizable SV RTL should only use a subset of all SV types available.
    Ban the following types: bit, real, integer (should use int instead), string, byte, shortint, longint, wand, wor, tri, triand, trior, tri0, tri1, supply0, supply1, trireg, shortreal, realtime, class
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    type_re = re.compile(
        "\s*(bit|real|time|integer|string|byte|shortint|longint|wand|wor|tri|triand|trior|tri0|tri1|supply0|supply1|trireg|shortreal|realtime|class)\\b"
    )

    ERROR_MSG = "Banned type detected."

    def _update(self, line_no, line):
        if self.type_re.match(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
