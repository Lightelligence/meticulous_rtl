"""
Module name must match filename
"""
# Python Imports
import os
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class ModuleName(filters.LineListener):
    """
    Module names shoulds match the file name to improve navigation.
    If a module name matches its filename, its definition can be found intuitively  
    """
    subscribe_to = [filters.BeginModuleBroadcaster]

    ERROR_MSG = "Module name does not match filename. Rename module name/filename so both match."

    def __init__(self, filename, fstream, *args, **kwargs):
        super(ModuleName, self).__init__(filename, fstream, *args, **kwargs)
        self.file_name = filename

    def update_beginmodule(self, line_no, line, match):
        if not re.search("(?<=(module)\s)\w+", line).group() == re.search("\w+(?=.sv)", self.file_name).group():
            self.error(line_no, line, self.ERROR_MSG)
