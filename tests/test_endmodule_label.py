import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.endmodule_label import EndmoduleLabel

import test

lbc = filters.LineBroadcaster


class EndmoduleLabelTestCase(test.TestCase):

    cut = EndmoduleLabel

    def test_endmodule(self):
        """ endmodule with no label """
        content = StringIO("""
        module foo;
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

    def test_endmodule_label(self):
        """ endmodule with label """
        content = StringIO("""
        module foo;
        endmodule : foo
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
