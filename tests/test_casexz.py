import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.casexz import CaseXZ

import test

lbc = filters.LineBroadcaster

class CaseXZTestCase(test.TestCase):

    cut = CaseXZ

    def test_passing(self):
        """Nothing wrong here."""
        content = StringIO("""
        some other content
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_casex(self):
        """An illegal widlcard"""
        content = StringIO("""
        module foo;
          casex (signal):
            FOO : nothing;
          endcase
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, CaseXZ.ERROR_MSG)

    def test_casez(self):
        """An illegal widlcard"""
        content = StringIO("""
        module foo;
          casez (signal):
            FOO : nothing;
          endcase
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, CaseXZ.ERROR_MSG)

    def test_case(self):
        """An illegal widlcard"""
        content = StringIO("""
        module foo;
          case (signal):
            FOO : nothing;
          endcase
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

            
if __name__ == '__main__':
    unittest.main()
