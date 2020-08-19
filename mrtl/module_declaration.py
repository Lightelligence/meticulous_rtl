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
    FIXME: module declaration
    """
    subscribe_to = [filters.BeginModuleBroadcaster, filters.ModuleLineBroadcaster]

    module_re = re.compile("^\s{2}\((?!.)") #"^\s*module\s\w+\s*\\n\s{2}\((?!(\s*\w+))")

    ERROR_MSG = "Module format invalid... (module <module_name> on one line, following line 2 spaces then open paren"
    def __init__(self, *args, **kwargs):
        super(ModuleDeclaration, self).__init__(*args, **kwargs)
        self.in_module = False

    def update_moduleline(self, line_no, line):
        if self.in_module:
            # todo: check second line
            self.in_module = False
            if not re.search("^  \($"):
                self.error()
            # print("moduleline", line_no, line)
        # if not self.module_re.search(line): # if regex returns None, raise error
        #     self.error(line_no, line, self.ERROR_MSG)

    def update_beginmodule(self, line_no, line, match):
        self.in_module = True
        if not re.search("module <.*>", line):
            error()
        # print("bm", line_no, line)
        # todo: check first line

    
