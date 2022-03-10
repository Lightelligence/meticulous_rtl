"""
If you are considering making this checker more advanced, please take a peek at draconian_uvm's multiple_classes checker
"""
# Python Imports
import os
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class MultipleModules(filters.LineListener):
    """Each module should be in its own file.

    There are two main reasons to keep each module in its own file:
      1. Readability
         Files remain a reasonable size.
      2. Navigation
         If a module name matches its filename, its defintion can be found intuitively.
    """
    subscribe_to = [filters.BeginModuleBroadcaster]

    def __init__(self, filename, fstream, *args, **kwargs):
        super(MultipleModules, self).__init__(filename, fstream, *args, **kwargs)
        self.found_a_module_on_line = -1

    def update_beginmodule(self, line_no, line):
        if self.found_a_module_on_line >= 0:
            self.error(line_no, line, f"One module per file please: first module on {self.found_a_module_on_line}")
        else:
            self.found_a_module_on_line = line_no
