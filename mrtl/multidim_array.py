"""
Ban multidimensional arrays
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class MultiDimArray(filters.LineListener):
    """ 
    Multi-dimmensional arrays are considered complex data types. They should be defined as typedefs in
    YIS for the purpose of type-safety and documentation.
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    multidim_re = re.compile("(logic\s*\w+(\s*\[.*\:.*\]){2}|logic\s*(\s*\[.*\:.*\]){2}\s*\w+)")

    ERROR_MSG = "Multidimensional array of logic type detected. Use YIS to create a typedef instead."

    def _update(self, line_no, line):
        if self.multidim_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
