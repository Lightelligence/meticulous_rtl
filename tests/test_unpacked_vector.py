import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.unpacked_vector import UnpackedVector

import test

lbc = filters.LineBroadcaster


class UnpackedVectorTestCase(test.TestCase):

    cut = UnpackedVector

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

    def test_unpacked(self):
        """An illegal unpacked vector"""
        content = StringIO("""
        module foo (input logic [20] signal_name[31:0]);
          casex (signal)
            FOO : nothing;
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, UnpackedVector.ERROR_MSG)

    def test_unpacked1(self):
        """An illegal unpacked vector"""
        content = StringIO("""
        module foo (input logic [20] signal_name[BIT_LENGTH-1:0]);
          casex (signal)
            FOO : nothing;
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, UnpackedVector.ERROR_MSG)

    def test_packed(self):
        """OK packed vector."""
        content = StringIO("""
        module foo (input logic signal_name [20][31:0]);
          case (signal)
            FOO : nothing;
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

if __name__ == '__main__':
    unittest.main()
