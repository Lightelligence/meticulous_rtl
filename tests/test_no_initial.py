import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.no_initial import NoInitial

import test

lbc = filters.LineBroadcaster


class NoInitialTestCase(test.TestCase):

    cut = NoInitial

    def test_no_initial(self):
        """No intial here."""
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

    def test_initial(self):
        """An illegal intital block"""
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, self.cut.ERROR_MSG)

    def test_initial_in_tbv_block(self):
        """A leagal intital block because its inside an `ifdef TBV"""
        content = StringIO("""
        module foo;
        `ifdef TBV
          initial begin
          end
        `endif
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

    def test_initial_in_non_tbv_block(self):
        """A leagal intital block because its inside an `ifdef TBV"""
        content = StringIO("""
        module foo;
        `ifdef SYNTH
          initial begin
          end
        `endif
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
