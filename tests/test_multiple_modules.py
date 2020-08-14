import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.multiple_modules import MultipleModules

import test

lbc = filters.LineBroadcaster


class MultipleModulesTestCase(test.TestCase):
    cut = MultipleModules

    def test_passing_case(self):
        content = StringIO()
        content.write("module foobar();\n")
        for i in range(10):
            content.write("  boring content\n")
        content.write("endmodule : foobar\n")
        for i in range(10):
            content.write("  more boring content\n")
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_multiple_modules(self):
        content = StringIO()
        content.write("module foobar();\n")
        for i in range(10):
            content.write("  boring content\n")
        content.write("endmodule : foobar\n")
        for i in range(10):
            content.write("  more boring content\n")
        content.write("module barfoo();\n")
        for i in range(10):
            content.write("  boring content\n")
        content.write("endmodule : barfoo\n")
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, 22, mock.ANY, "One module per file please: first module on 0")


if __name__ == "__main__":
    unittest.main()
