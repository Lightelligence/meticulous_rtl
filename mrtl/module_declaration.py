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
    subscribe_to = [filters.ModuleLineBroadcaster]

    module_re = re.compile("^\s{2}\((?!.)") #"^\s*module\s\w+\s*\\n\s{2}\((?!(\s*\w+))")

    ERROR_MSG = "Module format invalid... (module <module_name> on one line, following line 2 spaces then open paren"

    def _update(self, line_no, line):
        print(">>>" + line)
        print(self.module_re.search(line))
        if not self.module_re.search(line): # if regex returns None, raise error
            self.error(line_no, line, self.ERROR_MSG)


    update_moduleline = _update
