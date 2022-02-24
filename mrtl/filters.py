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


class BaseLineMatchBroadcaster(lw.Broadcaster, lw.Listener):
    subscribe_to = [LineBroadcaster]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = None

    def update_line(self, line_no, line):
        match = self.regex.match(line)
        if match:
            if self.group is None:
                self.broadcast(line_no, line)
            else:
                self.broadcast(line_no, line, match[self.group])

    def eof(self):
        self._broadcast("eof")


class IfdefBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the `ifdef <block_name> or `ifndef <block_name>."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = re.compile("\s*`if(n)*def\s+(\w+)")
        self.group = 2


class EndifBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the `endif // <foo>."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = re.compile("\s*`endif")


class BeginModuleBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the opening line of the definition of a module."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = re.compile("\s*module")


class EndModuleBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the closing line of the definition of a module."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = re.compile("\s*endmodule")


class BeginCaseBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the opening line of a case statement."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = re.compile("\s*((priority|unique)\s+)*case\s*\(.+\)")


class EndCaseBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the closing line of a case statement."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = re.compile("\s*endcase")


class ModuleLineBroadcaster(lw.Broadcaster, lw.Listener):
    """Triggers only on lines in between the first and closing line of a module."""
    subscribe_to = [BeginModuleBroadcaster, EndModuleBroadcaster, LineBroadcaster]

    def __init__(self, *args, **kwargs):
        super(ModuleLineBroadcaster, self).__init__(*args, **kwargs)
        self.active = False
        self.beginmodule_line = -1

    def update_beginmodule(self, line_no, line):
        self.active = True
        self.beginmodule_line = line_no

    def update_endmodule(self, line_no, line):
        self.active = False

    def update_line(self, line_no, line):
        if self.active and line_no != self.beginmodule_line:
            self.broadcast(line_no, line)

    def eof(self):
        self._broadcast("eof")


class CaseLineBroadcaster(lw.Broadcaster, lw.Listener):
    """Triggers only on lines in between the first and closing line of a case statement."""
    subscribe_to = [BeginCaseBroadcaster, EndCaseBroadcaster, ModuleLineBroadcaster]

    def __init__(self, *args, **kwargs):
        super(CaseLineBroadcaster, self).__init__(*args, **kwargs)
        self.active = False
        self.begincase_line = -1

    def update_begincase(self, line_no, line):
        self.active = True
        self.begincase_line = line_no

    def update_endcase(self, line_no, line):
        self.active = False

    def update_moduleline(self, line_no, line):
        if self.active and line_no != self.begincase_line:
            self.broadcast(line_no, line)

    def eof(self):
        self._broadcast("eof")
