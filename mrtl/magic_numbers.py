"""
Ban magic numbers
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class MagicNumbers(filters.LineListener):
    """ 
    In our systemverilog methodology, try to put as many types and parameters either into systemverilog typedefs (or typedef unions or typdef structs) or into localparams. Use typdefs as much as possible since the type name conveys intent (e.g. edl_cmd_t), but in some cases localparams or parameters (e.g. logic [chip_rypkg::NUM_DPM_ENG - 1:0])to define a logic width is okay.
	A declaration like "logic [5:0]" is bad because it doesn't relate to any other defined type. 
    Also, "logic [chip_rypkg::NUM_DPM_ENG - 3:0]" is bad because we don't know where the 3 comes from. 
	It's safe enough to waive "-1" because it's a common pattern, but everything else it should be banned.
		i.e. [VAR_NAME -1:0]
	For loop formatting should follow: "for (var_name= 0; var_name < parameter_or_localparam; var_name++) begin : label_name"
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    magic_re = re.compile(
        "(\[\s*\d+\s*:\s*\d+\]|\[\w+\s*[-+*\/]\s*(?!1\:\s*0).*|^\s*\w+\s*<=\s*\d+|for\s*\(.*;\s*\w+\s*(<|>|<=|>=)\s*\d+;\s*.*\))"
    )
    #                       magic num in bracket|magic num using var but not -1:0|rst val|for loop

    ERROR_MSG = "Magic number detected. Use typdefs or localparams so the type name conveys intent."

    def __init__(self, *args, **kwargs):
        super(MagicNumbers, self).__init__(*args, **kwargs)
        self.is_case = False
        # FIXME: enable after Azure #1811 is resolved 
        self.disable()

    def _update(self, line_no, line):
        if self.magic_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

        if re.search("^\s*case\s+\(.*\)", line):
            self.is_case = True

        if re.search("^\s*endcase", line):
            self.is_case = False

        if self.is_case:
            if re.search("^\s*\d?'[dhxbo][0-9A-Fxz]+\s*\:", line):
                self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
