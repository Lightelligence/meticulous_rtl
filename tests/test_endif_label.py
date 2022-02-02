import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.endif_label import EndifLabel

import test

lbc = filters.LineBroadcaster


class EndifLabelTestCase(test.TestCase):

    cut = EndifLabel

    def test_correct_labeling(self):
        """endif label matches ifdef label."""
        content = StringIO("""
        `ifdef TBV
          initial begin
            a = 1'b0;
          end
        `endif // TBV
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_mismatched_label(self):
        """ifdef label mismatch"""
        content = StringIO("""
        module foo;
        `ifdef TBV
          initial begin
            a = 1'b0;
          end
        `endif // TBC
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

    def test_no_endif_label(self):
        """missing endif label"""
        content = StringIO("""
        module foo;
        `ifdef TBV
          initial begin
            a = 1'b0;
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
