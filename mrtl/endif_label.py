"""
Ensure there's an `endif label that matches the `ifdef
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class EndifLabel(filters.LineListener):
    """ 
    An `endif label must be provied for any `ifdef block. This improves code readability and makes it easier for MRTL to disable or enable other checks based on 
    whether it is inside of an `ifdef block.
    """
    subscribe_to = [filters.IfdefBroadcaster, filters.EndifBroadcaster]

    endif_label_re = re.compile("^\s*`endif\s*\/\/\s*(\w+)")

    ERROR_MSG = "an `ifdef <block_name> block must be closed with identification in an in-line comment: `endif // <block_name>"

    def _update_ifdef(self, line_no, line, label):
        self._ifdef_label = label

    def _update_endif(self, line_no, line):
        match = self.endif_label_re.search(line)
        if not match or match.group(1) != self._ifdef_label:
            self.error(line_no, line, self.ERROR_MSG)

    update_ifdef = _update_ifdef
    update_endif = _update_endif
