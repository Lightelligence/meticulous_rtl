"""

"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters

class CaseXZ(filters.LineListener):
    """ 
    SystemVerilog introduced the case...inside statement to replace casex and casez.
    casex treats X's as don't cares if they are in the case expression or the case item. 
    Pre-synthesis simulations will not propagate X's, but the X's will propagate in gate-sim (if one is run at all).
    casez is has similar behavior as casex, but the X's are Z's. This type of simulation/synthesis mis-match is
    dangerous, and is what case...inside is intended to fix. Always use case...inside instead of casex or casez.
    Also beware that using case...inside with a default case can still lead to X-prop issues. the safest coding
    scheme, when it comes to case statements in general, is to write an assertion that checks whether the case expression 
    has an X in it. A more detailed analysis of this can be found here: https://lcdm-eng.com/papers/snug12_Paper_final.pdf
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    wildcard_re = re.compile("^\s*case[xz]")
    
    ERROR_MSG = "casex or casez detected. Use case...inside"

    def _update(self, line_no, line):
        if self.wildcard_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
