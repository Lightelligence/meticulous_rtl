import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.clk import Clk

import test

lbc = filters.LineBroadcaster


class ClkTestCase(test.TestCase):

    cut = Clk

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

    def test_clk(self):
        """An OK clk usage"""
        content = StringIO("""
        module foo;
          .clk            (clk)
          .clk            (eclk)
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

    def test_clk_bad(self):
        """An illegal clk usage"""
        content = StringIO("""
        module foo;
          .eclk (aclk)
          .aclk (eclk)
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, Clk.ERROR_MSG)

    def test_clk_specificity(self):
        """A legal name-change where clock goes from more-specific to less-specific"""
        content = StringIO("""
        module foo;
          .sclk (ccu31_sclk)
          .clk  (eclk)
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
