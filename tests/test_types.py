import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.types import Types

import test

lbc = filters.LineBroadcaster


class TypesTestCase(test.TestCase):

    cut = Types

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

    def test_banned_type(self):
        """An illegal type"""
        content = StringIO("""
        module foo;
          integer              i,j,k;
          shortreal            f;
          realtime             now;
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, Types.ERROR_MSG)

    def test_nonbanned_type(self):
        """An OK type"""
        content = StringIO("""
        module foo;
          logic [BIT_LENGTH-1:0] adr;
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
