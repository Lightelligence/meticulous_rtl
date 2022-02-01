"""
Ensure the initial keyword is not used unless it's inside of an ifdef TBV
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class NoInitial(filters.LineListener):
    """
    The initial keyword should not be used in RTL as it is not recognized by the synthesis tool. This can cause synth vs. sim behavioral mismatches that cannot be
    detected until gate-sim.
    """
    subscribe_to = [filters.IfdefBroadcaster, filters.EndifBroadcaster, filters.LineBroadcaster]

    _in_ifdef = False

    initial_re = re.compile("^\s*initial\s+")

    ERROR_MSG = "Do not use the intial keyword unless it is inside of an `ifdef TBV block"

    def _update_ifdef(self, line_no, line, label):
        if label == "TBV":
            self._in_ifdef = True

    def _update_endif(self, line_no, line):
        self._in_ifdef = False

    def _update_line(self, line_no, line):
        match = self.initial_re.search(line)
        if match and not self._in_ifdef:
            self.error(line_no, line, self.ERROR_MSG)

    update_ifdef = _update_ifdef
    update_endif = _update_endif
    update_line  = _update_line
