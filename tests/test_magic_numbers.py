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
        """An OK number"""
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
        """An illegal magic number0"""
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
        """An illegal magic number1"""
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
        """An illegal magic number2"""
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
          for (var_name= 0; var_name < 3; var_name++) begin : label_name
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
