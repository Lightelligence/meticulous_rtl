"""
Ensures the else of an if statement has the preceeding end on the same line
"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class SameLineEndElse(filters.LineListener):
    """
    For any if/else statement, the else clause must be on the same line as the end from the precceding if. This is done to reduce 
    unnecessary usage of newlines and to enforce a consistent-coding style. This coding style also helps keep indentation sane for our
    text-editors. This is not enforced for single-line if/else statements.

    DO NOT DO THIS:
    always_ff @(posedge clk)
      if(~reset_n) begin
        q <= 1'b0;
      end
      else begin
        q <= d;
      end
    end

    DO THIS INSTEAD:
    always_ff @(posedge clk)
      if(~reset_n) begin
        q <= 1'b0;
      end else begin
        q <= d;
      end
    end

    Since the above examples use a single-line if/else statement, this would be another acceptable way to write that code:
    always_ff @(posedge clk)
      if(~reset_n) q <= 1'b0;
      else q <= d;
    end
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    else_re = re.compile("else")
    singleline_re = re.compile("\s*else\s+(if\s+)?\w+\s*<?=\s*\w+;")

    ERROR_MSG = "else keyword must be on the same line as the preceeding end keyword"

    def update_moduleline(self, line_no, line):
        if re.search(self.else_re, line):
            if not line.lstrip().startswith("end") and not re.match(self.singleline_re, line):
                self.error(line_no, line, self.ERROR_MSG)
