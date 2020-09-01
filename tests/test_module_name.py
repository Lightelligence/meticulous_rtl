import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.module_name import ModuleName

import test

lbc = filters.LineBroadcaster


class ModuleNameTestCase(test.TestCase):
    cut = ModuleName

    def test_name_match(self):
        """An OK module name/filename match 1"""
        content = StringIO("""
        module foobar;
          for (var_name= 0; var_name < parameter_or_localparam; var_name++) begin : label_name
        endmodule
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/foobar/foobar.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_name_match2(self):
        """An OK module name/filename match 2"""
        content = StringIO()
        content.write("module foobar();\n")
        for i in range(10):
            content.write("  boring content\n")
        content.write("endmodule : foobar\n")
        for i in range(10):
            content.write("  more boring content\n")
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/foobar.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_name_mismatch(self):
        """An illegal module name/filename mismatch 1"""
        content = StringIO()
        content.write("module foobar();\n")
        for i in range(10):
            content.write("  boring content\n")
        content.write("endmodule : foobar\n")
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, ModuleName.ERROR_MSG)

    def test_name_mismatch2(self):
        """An illegal module name/filename mismatch 2"""
        content = StringIO("""
        module foo;
          for (var_name= 0; var_name < parameter_or_localparam; var_name++) begin : label_name
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, ModuleName.ERROR_MSG)


if __name__ == "__main__":
    unittest.main()
