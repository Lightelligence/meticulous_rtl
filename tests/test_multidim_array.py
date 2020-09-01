import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.multidim_array import MultiDimArray

import test

lbc = filters.LineBroadcaster


class MultiDimArrayTestCase(test.TestCase):

    cut = MultiDimArray

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

    def test_logic_multidimarray1(self):
        """An illegal multidimensional array 1"""
        content = StringIO("""
        module foo;
          logic array[2:0][3:0];
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_logic_multidimarray2(self):
        """An illegal multidimensional array 2"""
        content = StringIO("""
        module foo;
          logic array_name[BIT_LENGTH-1:0][BITLENGTH:0];
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_logic_multidimarray3(self):
        """An illegal multidimensional array 3"""
        content = StringIO("""
        module foo;
          logic array_name[BIT_LENGTH-1:0][BITLENGTH:0][0:7];
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_logic_multidimarray4(self):
        """An illegal multidimensional array (w/ spaces) 4"""
        content = StringIO("""
        module foo;
          logic array_name [BIT_LENGTH-1:0] [BITLENGTH:0] [0:7] ;
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_nonlogic_multidimarray(self):
        """An illegal multidimensional array"""
        content = StringIO("""
        module foo;
          bit array[BIT_LENGTH-1:0][BITLENGTH:0];
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

    def test_singledimarray(self):
        """An OK non-multidimensional array declaration"""
        content = StringIO("""
        module foo;
          logic array[BITLENGTH:0];
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

    def test_logic_multidimarray_nameafter(self):
        """An illegal MDA with signal name after"""
        content = StringIO("""
        module foo;
          logic [2:0][3:0]array;
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_logic_multidimarray_nameafter1(self):
        """An illegal MDA with signal name after 1"""
        content = StringIO("""
        module foo;
          logic   [BIT_LENGTH-1:0] [BITLENGTH:0] array_name;
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_logic_multidimarray_nameafter2(self):
        """An illegal MDA with signal name after 2"""
        content = StringIO("""
        module foo;
          logic [BIT_LENGTH-1:0][BITLENGTH:0][0:7]array_name;
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_logic_multidimarray_nameafter3(self):
        """An illegal MDA with signal name after 2"""
        content = StringIO("""
        module foo;
          logic [BIT_LENGTH-1:0] [BITLENGTH:0]  [0:7]           array_name;
        endmodule
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, MultiDimArray.ERROR_MSG)

    def test_logic_nonmultidimarray_nameafter(self):
        """An OK MDA with signal name after 1"""
        content = StringIO("""
        module foo;
          bit [BIT_LENGTH-1:0][BITLENGTH:0] array;
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

    def test_logic_nonmultidimarray_nameafter1(self):
        """An OK MDA with signal name after 2"""
        content = StringIO("""
        module foo;
          logic [BITLENGTH : 0 ] array;
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
