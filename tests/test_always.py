import unittest
from unittest import mock
from io import StringIO

from mrtl import filters
from mrtl.always import Always

import test

lbc = filters.LineBroadcaster


class AlwaysTestCase(test.TestCase):

    cut = Always

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

    def test_always_latch(self):
        """An illegal always_latch"""
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, Always.ERROR_MSG)

    def test_always_ff(self):
        """An OK always_ff block"""
        content = StringIO("""
        module foo;
          always_ff @(signal)
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
            iut.error.assert_not_called()

    def test_always_comb(self):
        """An OK always_comb block"""
        content = StringIO("""
        module foo;
          always_comb (signal):
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
            iut.error.assert_not_called()

    def test_always(self):
        """An illegal always block"""
        content = StringIO("""
        module foo;
          always @(signal)
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
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, Always.ERROR_MSG)


if __name__ == '__main__':
    unittest.main()
