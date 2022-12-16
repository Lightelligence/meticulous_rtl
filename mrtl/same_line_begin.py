"""
Ensures the begin for a block-statement is on the same line as the block-type keyword
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class SameLineBegin(filters.LineListener):
    """ 
    For any block that requires a begin/end, the begin must be on the same line as the block type. This is done to reduce unnecessary
    usaged of newlines and to enforce a consistent coding-style. This style is enforced for: always_* blocks, for loops, initial blocks,
    and conditions of case or if statements that are multi-line.

    DO NOT DO THIS:
    always_ff @(posedge clk)
      begin
        q <= d;
      end
    end

    DO THIS INSTEAD:
    always_ff @(posedge clk) begin
      q <= d;
    end

    CASE AND IF STATEMENTS:
    a single line condition with assignment does not require a begin/end at all, but a multi-line condition does.

    THIS IS OKAY BECAUSE IT USES SIGNLE-LINE CONDITIONS:
    always_comb begin
    case (foo)
      pkg_name::ENUM_TYPE0: out = in0;
      pkg_name::ENUM_TYPE1: out = in1;
      default: out = 'x;
    endcase

    THIS IS OKAY BECAUSE IT USES MULTI-LINE CONDITIONS WITH BEGIN ON THE FIRST LINE:
    always_comb begin
      case (foo)
        pkg_name::ENUM_TYPE0: begin
          out = in0;
        end
        pkg_name::ENUM_TYPE1: begin
          out = in1;
        end
        default: begin
          out = 'x;
        end
      endcase
    end

    THIS IS INVALID:
    always_comb begin
      case (foo)
        pkg_name::ENUM_TYPE0: 
          begin
            out = in0;
          end
        pkg_name::ENUM_TYPE1: 
          begin
            out = in1;
          end
        default: 
          begin
            out = 'x;
          end
      endcase
    end
    """
    subscribe_to = [filters.ModuleLineBroadcaster, filters.CaseLineBroadcaster]

    missing_begin_re = re.compile(
        "\s*(always_ff\s*@\(\w+\s+\w+\)\s*|always_comb\s+|initial\s+|((generate\s+)?(for|if)|else\s+if)\s*\(.+\)\s*|else\s*)(\/\/.*)*$"
    )
    case_begin_re = re.compile("\s*((\w+::\w+)|\w+):\s*(\/\/.*)*$")

    ERROR_MSG = "always blocks, initial blocks, case and if statements must have the begin keyword on the same line"

    def update_moduleline(self, line_no, line):
        if re.match(self.missing_begin_re, line):
            self.error(line_no, line, self.ERROR_MSG)

    def update_caseline(self, line_no, line):
        if re.match(self.case_begin_re, line):
            self.error(line_no, line, self.ERROR_MSG)
