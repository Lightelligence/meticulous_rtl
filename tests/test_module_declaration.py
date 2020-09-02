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
        """OK module declaration format."""
        content = StringIO("""
module eu
  (
    input signal_name
  );
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

    def test_module1(self):
        """OK module declaration format with parameter."""
        content = StringIO("""
module ch_flop
  #(  
	parameter [31:0] STAGES = 2,
    parameter type NET_TYPE_T = logic
    )
  (
   input  eclk,
   input  reset_n,

   input  NET_TYPE_T in_net,
   output NET_TYPE_T out_net
  
   );

  NET_TYPE_T ch_flop [STAGES:0];
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/rtl/blocka/blocka.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_module_lint_waiver(self):
        """OK module declaration with a lint waiver."""
        content = StringIO("""
module iid // lint: disable=ATLGLC
  (
    input signal_name
  );
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


    def test_nonmodule(self):
        """An illegal module declaration format."""
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
        """An illegal module declaration format 1."""
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

    def test_nonmodule2(self):
        """An illegal module declaration format 2"""
        content = StringIO("""
        module foo
                     (
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
        """An illegal module declaration format 3"""
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

    def test_nonmodule_bad_parameter(self):
        """An illegal module declaration format with parameter."""
        content = StringIO("""
module flop_array_2p
  #(parameter ADDR_WIDTH = 8, DATA_WIDTH = 8, DEPTH = 256) 
  (
   input clk,
  input [ADDR_WIDTH-1:0] waddr, 
  input [ADDR_WIDTH-1:0] raddr, 
  input we,
  input re,
  input [DATA_WIDTH-1:0] wdata,
  output logic [DATA_WIDTH-1:0] rdata 
  );
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
