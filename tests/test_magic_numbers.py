import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.magic_numbers import MagicNumbers

import test

lbc = filters.LineBroadcaster


class MagicNumbersTestCase(test.TestCase):

    cut = MagicNumbers

    def test_passing(self):
        """Nothing wrong here."""
        content = StringIO("""
        some other content
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_nonmagic(self):
        """An OK number (array)"""
        content = StringIO("""
        module foo;
          logic [BIT_LENGTH-1:0];
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

    def test_magic0(self):
        """An illegal magic number (array)"""
        content = StringIO("""
        module foo;
          logic [7:0];
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MagicNumbers.ERROR_MSG)

    def test_magic1(self):
        """An illegal magic number (array) 1"""
        content = StringIO("""
        module foo;
          logic [BIT_LENGTH-9:0];
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MagicNumbers.ERROR_MSG)

    def test_magic2(self):
        """An illegal magic number (array) 2"""
        content = StringIO("""
        module foo;
          logic [NUM_DPM_ENG - 1: 5];
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MagicNumbers.ERROR_MSG)

    def test_magic_resetvals(self):
        """An illegal magic number (reset value)"""
        content = StringIO("""
        module foo;
          always @(*)
            begin
            if(reset == 1'b1)
              reg <= 0; //reset condition
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MagicNumbers.ERROR_MSG)

    def test_nonmagic_resetvals(self):
        """An OK number (reset value)"""
        content = StringIO("""
        module foo;
          always @(*)
            begin
            if(reset == 1'b1)
              reg <= foo; //reset condition
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

    def test_forloop_nonmagic(self):
        """An OK for loop"""
        content = StringIO("""
        module foo;
          for (var_name= 0; var_name < parameter_or_localparam; var_name++) begin : label_name
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

    def test_forloop_magic(self):
        """An illegal magic number in a for loop"""
        content = StringIO("""
        module foo;
          for (var_name= 0; var_name <= 3; var_name++) begin : label_name
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MagicNumbers.ERROR_MSG)

    def test_case_magic(self):
        """An illegal magic number in a case block"""
        content = StringIO("""
        module foo;
          always @(*)
			  begin
				case ({r_VAL_1, r_VAL_2, r_VAL_3})
				  3'b000  : r_RESULT <= 0;
				  3'xABF  : r_RESULT <= 1;
				  'b010  : r_RESULT <= 2;
				  default : r_RESULT <= 9; 
				endcase
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MagicNumbers.ERROR_MSG)

    def test_case_nonmagic(self):
        """An OK number in a case block"""
        content = StringIO("""
        module foo;
          always @(*)
			  begin
				case ({r_VAL_1, r_VAL_2, r_VAL_3})
				  case_item1  : r_RESULT <= 0;
				  case_item2  : r_RESULT <= 1;
				  case_item3: r_RESULT <= 2;
				  default : r_RESULT <= 9; 
				endcase
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

    def test_case_magic_after_case(self):
        """An OK number in a case block"""
        content = StringIO("""
        module foo;
          always @(*)
			  begin
				case ({r_VAL_1, r_VAL_2, r_VAL_3})
				  case_item1  : r_RESULT <= 0;
				  case_item2  : r_RESULT <= 1;
				  case_item3: r_RESULT <= 2;
				  default : r_RESULT <= 9; 
				endcase
              if(reset == 1'b1)
                reg <= 0; //reset condition
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MagicNumbers.ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
