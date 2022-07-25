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
        self.disable() # disable the base-class. all children need to enable in their constructor
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
        self.enable()
        self.regex = re.compile("\s*`if(n)*def\s+(\w+)")
        self.group = 2


class EndifBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the `endif // <foo>."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*`endif")


class BeginModuleBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the opening line of the definition of a module."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*module")


class EndModuleBroadcaster(BaseLineMatchBroadcaster):
    """Trigger on the closing line of the definition of a module."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*endmodule\s*(:\s*\w+)?")
        self.group = 1


class ModuleLineBroadcaster(lw.Broadcaster, lw.Listener):
    """Triggers only on lines in between the first and closing line of a module."""
    subscribe_to = [BeginModuleBroadcaster, EndModuleBroadcaster, LineBroadcaster]
    beginmodule_line = -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False

    def update_beginmodule(self, line_no, line):
        self.active = True
        self.beginmodule_line = line_no

    def update_endmodule(self, line_no, line, match):
        self.active = False

    def update_line(self, line_no, line):
        if self.active and line_no != self.beginmodule_line:
            self.broadcast(line_no, line)

    def eof(self):
        self._broadcast("eof")


class BaseModuleLineMatchBroadcaster(lw.Broadcaster, lw.Listener):
    subscribe_to = [ModuleLineBroadcaster]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable() # disable the base-class. all children need to enable in their constructor
        self.group = None

    def update_moduleline(self, line_no, line):
        match = self.regex.match(line)
        if match:
            if self.group is None:
                self.broadcast(line_no, line)
            else:
                self.broadcast(line_no, line, match[self.group])

    def eof(self):
        self._broadcast("eof")


class BeginCaseBroadcaster(BaseModuleLineMatchBroadcaster):
    """Trigger on the opening line of a case statement."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*((priority|unique)\s+)*case\s*\(.+\)")


class EndCaseBroadcaster(BaseModuleLineMatchBroadcaster):
    """Trigger on the closing line of a case statement."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*endcase")


class AutoRegInputBroadcaster(BaseModuleLineMatchBroadcaster):
    """Trigger on the start of an AUTOREGINPUT block."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*/\*\s*AUTOREGINPUT\s*\*/")


class AutoWireBroadcaster(BaseModuleLineMatchBroadcaster):
    """Trigger on the start of an AUTOWIRE block."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*/\*\s*AUTOWIRE\s*\*/")


class EndAutosBroadcaster(BaseModuleLineMatchBroadcaster):
    """Trigger on the end of an AUTOs block."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable()
        self.regex = re.compile("\s*\/\/ End of automatics")


class CaseLineBroadcaster(lw.Broadcaster, lw.Listener):
    """Triggers only on lines in between the first and closing line of a case statement."""
    subscribe_to = [BeginCaseBroadcaster, EndCaseBroadcaster, ModuleLineBroadcaster]
    begincase_line = -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

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
