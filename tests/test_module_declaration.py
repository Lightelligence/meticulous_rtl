import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.module_declaration import ModuleDeclaration

import test

lbc = filters.LineBroadcaster


class ModuleDeclarationTestCase(test.TestCase):

    cut = ModuleDeclaration

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

    def test_module(self):
        """OK module declaration 1."""
        content = StringIO("""
		module eu
  (
""")
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_nonmodule(self):
        """An illegal module declaration."""
        content = StringIO("""
        module foo;
          always_latch
			begin
				FOO : nothing;
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, ModuleDeclaration.ERROR_MSG)

    def test_nonmodule1(self):
        """An illegal module declaration 1"""
        content = StringIO("""
		module foo(
		)
		endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, ModuleDeclaration.ERROR_MSG)

    def test_nonmodule_more_spaces(self):
        """An illegal module declaration 2"""
        content = StringIO("""
        module foo
  (hello
          )
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, ModuleDeclaration.ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
