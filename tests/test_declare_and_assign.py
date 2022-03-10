import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.declare_and_assign import DeclareAndAssign

import test

lbc = filters.LineBroadcaster


class DeclareAndAssignTestCase(test.TestCase):

    cut = DeclareAndAssign

    def test_only_declare(self):
        """simple declaration of a logic-type."""
        content = StringIO("""
        logic bar;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_assign(self):
        """simple assignment."""
        content = StringIO("""
        assign foo = 1'b1;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_declare_and_assign_custom_type(self):
        """simple assignment."""
        content = StringIO("""
        module foo;
        type_rypkg::type_t bar = 1'b1;
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

    def test_only_declare_reg(self):
        """simple declaration of a reg-type."""
        content = StringIO("""
        reg bar;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_declare_and_assign_singleline_logic(self):
        """declare and assign of a logic on 1 line"""
        content = StringIO("""
        module foo;
        logic bar = 1'b1;
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

    def test_declare_and_assign_multiline_logic(self):
        """declare and assign of a logic on multiple lines"""
        content = StringIO("""
        module foo;
        logic bar = 
        1'b1;
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

    def test_declare_and_assign_singleline_reg(self):
        """declare and assign of a reg on 1 line"""
        content = StringIO("""
        module foo;
        reg bar = 1'b1;
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

    def test_declare_and_assign_multiline_reg(self):
        """declare and assign of a reg on multiple lines"""
        content = StringIO("""
        module foo;
        reg bar = 
        1'b1;
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
