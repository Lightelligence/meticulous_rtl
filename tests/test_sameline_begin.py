import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.same_line_begin import SameLineBegin

import test

lbc = filters.LineBroadcaster


class SameLineBeginTestCase(test.TestCase):

    cut = SameLineBegin

    def test_always_ff_begin(self):
        """always_ff with begin."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin
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

    def test_always_ff_no_begin(self):
        """always_ff without begin."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk)
        begin
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

    def test_always_comb_begin(self):
        """always_comb with begin."""
        content = StringIO("""
        module foo;
        always_comb begin
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

    def test_always_comb_no_begin(self):
        """always_comb without begin."""
        content = StringIO("""
        module foo;
        always_comb
        begin
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

    def test_initial_begin(self):
        """initial with begin."""
        content = StringIO("""
        module foo;
        initial begin
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

    def test_initial_no_begin(self):
        """initial without begin."""
        content = StringIO("""
        module foo;
        initial
        begin
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

    def test_gen_for_begin(self):
        """generate for with begin."""
        content = StringIO("""
        module foo;
        generate for (genvar i = 0; i < 1; i++) begin: gen_example
        endgenerate
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

    def test_gen_for_no_begin(self):
        """generate for without begin."""
        content = StringIO("""
        module foo;
        generate for (genvar i = 0; i < 1; i++)
        begin
        end
        endgenerate
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

    def test_gen_if_begin(self):
        """generate if with begin."""
        content = StringIO("""
        module foo;
        generate if (a == b) begin: gen_thing
        endgenerate
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

    def test_gen_if_no_begin(self):
        """generate if without begin."""
        content = StringIO("""
        module foo;
        generate if (a == b)
        begin
        end
        endgenerate
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

    def test_for_begin(self):
        """for with begin."""
        content = StringIO("""
        module foo;
        always_comb begin
        for (int i = 0; i < 1; i++) begin
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

    def test_for_no_begin(self):
        """for without begin."""
        content = StringIO("""
        module foo;        
        always_comb begin
        for (int i = 0; i < 1; i++)
        begin
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

    def test_if_begin(self):
        """if with begin."""
        content = StringIO("""
        module foo;
        always_comb begin
        if (a == b) begin
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

    def test_if_no_begin(self):
        """if without begin."""
        content = StringIO("""
        module foo;        
        always_comb begin
        if (a == b)
        begin
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

    def test_if_singleline(self):
        """if in a single-line."""
        content = StringIO("""
        module foo;        
        always_comb begin
        if (a == b) c = d;
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

    def test_else_begin(self):
        """else with begin."""
        content = StringIO("""
        module foo;
        always_comb begin
        else (a == b) begin
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

    def test_else_no_begin(self):
        """else without begin."""
        content = StringIO("""
        module foo;        
        always_comb begin
        else
        begin
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

    def test_else_singleline(self):
        """else in a single-line."""
        content = StringIO("""
        module foo;        
        always_comb begin
        else c = d;
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

    def test_elseif_begin(self):
        """else if with begin."""
        content = StringIO("""
        module foo;
        always_comb begin
        else if (a == b) begin
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

    def test_elseif_no_begin(self):
        """else if without begin."""
        content = StringIO("""
        module foo;        
        always_comb begin
        else if (a == b)
        begin
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

    def test_elseif_singleline(self):
        """else if in a single-line."""
        content = StringIO("""
        module foo;        
        always_comb begin
        else if (a == b) c = d;
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

    def test_case_begin(self):
        """case-statement with begin."""
        content = StringIO("""
        module foo;
        always_comb begin
        case (foo)
        test_rypkg::TMP: begin
        a = b;
        end
        endcase
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

    def test_case_no_begin(self):
        """case-statement without begin."""
        content = StringIO("""
        module foo;
        always_comb begin
        case (foo)
        test_rypkg::TMP: 
        begin
        a = b;
        end
        endcase
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

    def test_case_singleline(self):
        """else if in a single-line."""
        content = StringIO("""
        module foo;
        always_comb begin
        case (foo)
        test_rypkg::TMP: a = b;
        endcase
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

    def test_always_ff_begin_comment(self):
        """always_ff with begin."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin // safe comment
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

    def test_always_ff_begin_comment(self):
        """always_ff with begin and a comment."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) begin // safe comment
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

    def test_always_ff_no_begin_comment(self):
        """always_ff with no begin, just a comment."""
        content = StringIO("""
        module foo;
        always_ff @(posedge clk) // unsafe comment
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


if __name__ == '__main__':
    unittest.main()
