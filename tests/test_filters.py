import unittest
from unittest import mock
from io import StringIO

from mrtl import filters

import test


class ModuleTestCase(test.TestCase):

    def test_simple(self):
        content = StringIO("""
        module foobar
          stuff 
          other stuff
        endmodule : foobar
        """)
        cut = filters.BeginModuleBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/foobar.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]

    def test_endmodule(self):
        content = StringIO("""
        endmodule : foobar
        """)
        cut = filters.EndModuleBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/stuff/foobar.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()

    def test_moduleline(self):
        content = StringIO("""
        module foobar
          stuff 
          other stuff
        endmodule : foobar
        """)
        cut = filters.ModuleLineBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/stuff/foobar.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_has_calls([mock.call(mock.ANY, 2, mock.ANY), mock.call(mock.ANY, 3, mock.ANY)])


class IfdefTestCase(test.TestCase):

    def test_ifdef(self):
        content = StringIO("""
        `ifdef TBV
        """)
        cut = filters.IfdefBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/foobar.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]

    def test_ifndef(self):
        content = StringIO("""
        `ifndef TBV
        """)
        cut = filters.IfdefBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/foobar.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]

    def test_endif(self):
        content = StringIO("""
        `endif // TBV
        """)
        cut = filters.EndifBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/foobar.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][2]


if __name__ == '__main__':
    unittest.main()
