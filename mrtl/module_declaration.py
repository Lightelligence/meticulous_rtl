"""
Check for module declaration
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class ModuleDeclaration(filters.LineListener):
    """ 
    Format module declaration using 'module <module_name>' on its own line, then a newline with 2 spaces and open paren, then newline and signals)

i.e.
module eu
  (
    """
    subscribe_to = [filters.BeginModuleBroadcaster, filters.ModuleLineBroadcaster]

    ERROR_MSG = "Module format invalid... (put 'module <module_name>' on its own line, then a newline with 2 spaces and open paren, then newline and signals)"

    def __init__(self, *args, **kwargs):
        super(ModuleDeclaration, self).__init__(*args, **kwargs)
        self.in_module = False
        self.param = False
        self.skip_one_line = False

    def update_moduleline(self, line_no, line):
        if re.search("\s\s#\(\s*$", line):
            self.param = True
        elif self.param and re.search("^\s*\)", line):
            self.param = False
            self.skip_one_line = True

        if not self.param:
            if self.in_module and not self.skip_one_line:
                self.in_module = False
                if not re.search("^  \($", line):
                    self.error(line_no, line, self.ERROR_MSG)
            self.skip_one_line = False

    def update_beginmodule(self, line_no, line, match):
        self.in_module = True
        if not re.search("module\s\w+\s*(\/\/.*)*$", line):
            self.error(line_no, line, self.ERROR_MSG)
