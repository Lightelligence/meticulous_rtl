import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.import_wildcard import ImportWildcard

import test

lbc = filters.LineBroadcaster

class ImportWildcardTestCase(test.TestCase):

    cut = ImportWildcard

    def test_no_import(self):
        """No imports here."""
        content = StringIO("""
        some other content
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_import_wildcard(self):
        """An illegal widlcard"""
        content = StringIO("""
        module foo;
          import foobar_pkg::*;
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Do not use wildcard imports. Explicitly reference items in the package.")
            
if __name__ == '__main__':
    unittest.main()
