import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.no_import import NoImport
from mrtl.unpacked_vector import UnpackedVector
from mrtl.pragma import Pragma

import test

lbc = filters.LineBroadcaster


class PragmaTestCase(test.TestCase):

    cut = Pragma
    restrictions = [Pragma, NoImport, UnpackedVector]

    def test_no_wildcard(self):
        """No wildcard import here."""
        content = StringIO("""
        module stuff;
          some other content
        endmodule
        """)
        with mock.patch.object(NoImport, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, NoImport)
            iut.error.assert_not_called()

    def test_wilcard_fails(self):
        """There's a wildcard import in here."""
        content = StringIO("""
        module stuff;
          import foobar::*;
        endmodule
        """)
        with mock.patch.object(NoImport, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, NoImport)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, NoImport.ERROR_MSG)

    def test_pragma(self):
        """Wildcard import exists, but its been disabled by pragma"""
        content = StringIO("""
        module stuff;
          // mrtl: disable=NoImport
          import foobar::*;
        endmodule
        """)
        with mock.patch.object(NoImport, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, NoImport)
            iut.error.assert_not_called()

    def test_pragma_reenabled(self):
        """Only the second issue should be caught here."""
        content = StringIO("""
        module stuff;
          // mrtl: disable=NoImport
          import foobar::*;
          // mrtl: enable=NoImport
          import foobar::*;
        endmodule
        """)
        with mock.patch.object(NoImport, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, NoImport)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, NoImport.ERROR_MSG)

    def test_pragma_unknown_class(self):
        """Here's an example of a bad pragma which should throw an error."""
        content = StringIO("""
        // mrtl: disable=ThisClassDoesntExist
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY,
                                         "could not find listener (ThisClassDoesntExist) class used in pragma")

    def test_pragma_multiple(self):
        """Example wher a rule is enabled and disabled multiple times."""
        content = StringIO("""
// Copyright (c) 2020 Lightelligence
//
// Parameterized channel flop module with arrayed outputs
//
// Author: Cameron Glass

module ch_flop_arr
  #(
    parameter [31:0] STAGES = 2,
    parameter type NET_TYPE_T = logic
    )
  (
   input  eclk,
   input  reset_n,

   input  NET_TYPE_T in_net,

   // See comment below on why we're using an unpacked vector
   // mrtl: disable=UnpackedVector
   output NET_TYPE_T out_net [STAGES:0]
   // mrtl: enable=UnpackedVector

   );

  
  // Use an array of size STAGES + 1 to make the generate block cleaner
  // Need to use unpacked array to make sure that ch_flop[N] points to something of type NET_TYPE_T
  // mrtl: disable=UnpackedVector
  // If the type of ch_flop was 'NET_TYPE_T [STAGES:0] ch_flop', then if NET_TYPE_T were an indexed type ch_flop[0] would index into NET_TYPE_T not into a stage
  NET_TYPE_T ch_flop [STAGES:0];
  // mrtl: enable=UnpackedVector

  assign ch_flop[0] = in_net;
  assign out_net = ch_flop;

  generate
    // Because index 0 is always in_net, the generate loop that looks ahead always works
    for (genvar stage_num = 0; stage_num < STAGES; stage_num++) begin : gen_stages
      always_ff @(posedge eclk) begin
        ch_flop[stage_num + 1] <= ch_flop[stage_num];
      end
    end
  endgenerate

endmodule
""")
        with mock.patch.object(UnpackedVector, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(*self.restrictions))
            iut = self.get_listener(lb, UnpackedVector)
            iut.error.assert_not_called()


if __name__ == '__main__':
    unittest.main()
