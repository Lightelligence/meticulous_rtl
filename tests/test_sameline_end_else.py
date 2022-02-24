import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.sameline_end_else import SameLineEndElse

import test

lbc = filters.LineBroadcaster


class SameLineEndElseTestCase(test.TestCase):

    cut = SameLineEndElse

    def test_sameline_end_else(self):
        """same-line end."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
        if (~reset_n) begin
        q <= 1'b0;
        end else begin
        q <= d;
        end
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_sameline_end_else_if(self):
        """same-line end with else if."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
        if (~reset_n) begin
        q <= 1'b0;
        end else if (foo) begin
        q <= d;
        end
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_singleline_else_assign_nonblocking(self):
        """single-line else with non-blocking assignment."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
        if (~reset_n) q <= 1'b0;
        else q <= d;
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_singleline_else_assign_blocking(self):
        """single-line else with blocking assignment."""
        content = StringIO("""
        module foo;
        always_comb begin
        if (foo) q = 1'b0;
        else q = d;
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_singleline_else_if_assign_blocking(self):
        """single-line else if with blocking assignment."""
        content = StringIO("""
        module foo;
        always_comb begin
        if (foo) q = 1'b0;
        else if (bar) q = d;
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_newline_end_else_if(self):
        """newline else if without end."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
        if (~reset_n) begin
        q <= 1'b0;
        end 
        else if (foo) begin
        q <= d;
        end
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, self.cut.ERROR_MSG)
            
    def test_newline_end_else(self):
        """newline else without end."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
        if (~reset_n) begin
        q <= 1'b0;
        end 
        else begin
        q <= d;
        end
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, self.cut.ERROR_MSG)

    def test_newline_end_else_begin(self):
        """newline else without end."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
        if (~reset_n) begin
        q <= 1'b0;
        end 
        else
        begin
        q <= d;
        end
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, self.cut.ERROR_MSG)

    def test_newline_end_else_comment(self):
        """newline else without end with a comment."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
        if (~reset_n) begin
        q <= 1'b0;
        end 
        else // comment
        begin
        q <= d;
        end
        end
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, self.cut.ERROR_MSG)
