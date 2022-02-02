"""Top level filters to categorizes rules to file types.

"""

import os
import re

from lw import linebase as lb
from lw import base as lw


class LineBroadcaster(lb.LineBroadcaster):
    pass


class LineListener(lb.LineListener):
    pass


class IfdefBroadcaster(lw.Broadcaster, lw.Listener):
    """Trigger on the `ifdef <block_name> or `ifndef <block_name>."""
    subscribe_to = [LineBroadcaster]

    ifdef_re = re.compile("\s*`if(n)*def\s+(\w+)")

    def update_line(self, line_no, line):
        match = self.ifdef_re.match(line)
        if match:
            ifdef_label = match[2]
            self.broadcast(line_no, line, ifdef_label)

    def eof(self):
        self._broadcast("eof")


class EndifBroadcaster(lw.Broadcaster, lw.Listener):
    """Trigger on the `endif // <foo>."""
    subscribe_to = [LineBroadcaster]

    endif_re = re.compile("\s*`endif")

    def update_line(self, line_no, line):
        match = self.endif_re.match(line)
        if match:
            self.broadcast(line_no, line)

    def eof(self):
        self._broadcast("eof")


class BeginModuleBroadcaster(lw.Broadcaster, lw.Listener):
    """Trigger on the opening line of the definition of a module."""
    subscribe_to = [LineBroadcaster]

    # FIXME add more matching info to get type and name?
    begin_module_re = re.compile("\s*module")

    def update_line(self, line_no, line):
        match = self.begin_module_re.match(line)
        if match:
            self.broadcast(line_no, line, match)

    def eof(self):
        self._broadcast("eof")


class EndModuleBroadcaster(lw.Broadcaster, lw.Listener):
    """Trigger on the closing line of the definition of a module."""
    subscribe_to = [LineBroadcaster]

    end_module_re = re.compile("\s*endmodule")

    def update_line(self, line_no, line):
        match = self.end_module_re.match(line)
        if match:
            self.broadcast(line_no, line, match)

    def eof(self):
        self._broadcast("eof")


class ModuleLineBroadcaster(lw.Broadcaster, lw.Listener):
    """Triggers only on lines in between the first and closing line of a module."""
    subscribe_to = [BeginModuleBroadcaster, EndModuleBroadcaster, LineBroadcaster]

    def __init__(self, *args, **kwargs):
        super(ModuleLineBroadcaster, self).__init__(*args, **kwargs)
        self.active = False
        self.beginmodule_line = -1

    def update_beginmodule(self, line_no, line, match):
        self.active = True
        self.beginmodule_line = line_no

    def update_endmodule(self, line_no, line, match):
        self.active = False

    def update_line(self, line_no, line):
        if self.active and line_no != self.beginmodule_line:
            self.broadcast(line_no, line)

    def eof(self):
        self._broadcast("eof")
