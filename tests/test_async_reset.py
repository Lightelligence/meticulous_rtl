import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.async_reset import AsyncReset

import test

lbc = filters.LineBroadcaster


class AsyncResetTestCase(test.TestCase):

    cut = AsyncReset

    def test_passing(self):
        """Nothing wrong here."""
        content = StringIO("""
        module foobar;
          always_ff @(posedge eclk) begin
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

    def test_negedge_abbrv_n(self):
        """An negedged active-low with abbreviated name"""
        content = StringIO("""
        module foobar;
          always_ff @(posedge eclk or negedge rst_n) begin
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, AsyncReset.ERROR_MSG)

    def test_negedge_abbrv(self):
        """An posedge active-high with abbreviated name."""
        content = StringIO("""
        module foobar;
          always_ff @(posedge eclk or posedge rst) begin
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, AsyncReset.ERROR_MSG)

    def test_negedge(self):
        """An negedge active-low with full name."""
        content = StringIO("""
        module foobar;
          always_ff @(posedge eclk or negedge reset_n) begin
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, AsyncReset.ERROR_MSG)

    def test_negedge_long_name(self):
        """An negedge active-low with full name."""
        content = StringIO("""
        module foobar;
          always_ff @(posedge eclk or negedge sys_ctl_reset_n) begin
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, AsyncReset.ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
