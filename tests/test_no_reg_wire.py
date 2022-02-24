import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.no_reg_wire import NoRegWire

import test

lbc = filters.LineBroadcaster


class NoRegWireTestCase(test.TestCase):

    cut = NoRegWire

    def test_reg_in_autos_block(self):
        """this reg is in an AUTOs block so it's OK"""
        content = StringIO("""
        module foo;
        /*AUTOREGINPUT*/
        // Beginning of automatic reg inputs (for undeclared instantiated-module inputs)
        reg                   eu___acc__eu__done;     // To dut of eu.v
        // End of automatics
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

    def test_reg_outside_of_autos_block(self):
        """illegal usage of reg"""
        content = StringIO("""
        module foo;
        reg eu___acc__eu__done;
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

    def test_wire_in_autos_block(self):
        """this wire is in an AUTOs block so it's OK"""
        content = StringIO("""
        module foo;
        /*AUTOWIRE*/
        // Beginning of automatic wires (for undeclared instantiated-module outputs)
        wire                  eu__core__intr;         // From dut of eu.v
        // End of automatics
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

    def test_reg_outside_of_autos_block(self):
        """illegal usage of wire"""
        content = StringIO("""
        module foo;
        wire eu__core__intr;
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
