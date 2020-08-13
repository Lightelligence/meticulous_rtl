import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.import_wildcard import ImportWildcard
from mrtl.pragma import Pragma

import test

lbc = filters.LineBroadcaster

class PragmaTestCase(test.TestCase):

    cut = Pragma
    restrictions = [Pragma, ImportWildcard]

    def test_no_wildcard(self):
        """No wildcard import here."""
        content = StringIO("""
        module stuff;
          some other content
        endmodule
        """)
        with mock.patch.object(ImportWildcard, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, ImportWildcard)
            iut.error.assert_not_called()

    def test_wilcard_fails(self):
        """There's a wildcard import in here."""
        content = StringIO("""
        module stuff;
          import foobar::*;
        endmodule
        """)
        with mock.patch.object(ImportWildcard, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, ImportWildcard)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, ImportWildcard.ERROR_MSG)

    def test_pragma(self):
        """Wildcard import exists, but its been disabled by pragma"""
        content = StringIO("""
        module stuff;
          // mrtl: disable=ImportWildcard
          import foobar::*;
        endmodule
        """)
        with mock.patch.object(ImportWildcard, "error", autospec=True):
           lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(*self.restrictions))
           iut = self.get_listener(lb, ImportWildcard)
           iut.error.assert_not_called()

    def test_pragma_reenabled(self):
        """Only the second issue should be caught here."""
        content = StringIO("""
        module stuff;
          // mrtl: disable=ImportWildcard
          import foobar::*;
          // mrtl: enable=ImportWildcard
          import foobar::*;
        endmodule
        """)
        with mock.patch.object(ImportWildcard, "error", autospec=True):
           lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(*self.restrictions))
           iut = self.get_listener(lb, ImportWildcard)
           iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, ImportWildcard.ERROR_MSG)

    def test_pragma_unknown_class(self):
        """Here's an example of a bad pragma which should throw an error."""
        content = StringIO("""
        // mrtl: disable=ThisClassDoesntExist
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
           lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(*self.restrictions))
           iut = self.get_listener(lb, self.cut)
           iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "could not find listener (ThisClassDoesntExist) class used in pragma")
           
if __name__ == '__main__':
    unittest.main()
