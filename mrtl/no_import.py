"""Ban import <pkg>::* inside RTL modules.

"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters


class NoImport(filters.LineListener):
    """Ban import packages.

    This is anything of the format 'import <pkg>::<type_or_wildcard>'.

    While doing an import may reduce the amount of typing you need
    to do in your module and you could argue it improves readability, it makes
    tracing much more difficult.

    Params and types no longer indicate their parent package which is where you would find their definition.

    By explicitly refering to content withing a package, you know implcilitly
    where the definition lives. It also makes it more obvious how tightly
    coupled a module is to a package: you can easily count the number of
    references to the package.

    Types and params should be explicitly scoped:
    <pkg>::<type> <net_name>;
    logic [<pkg>::<param>-1:0] <net_name>;
    """
    subscribe_to = [filters.LineBroadcaster]

    import_re = re.compile("^\s*import.*::")

    ERROR_MSG = "Do not use imports. Explicitly reference items in the package."

    def _update(self, line_no, line):
        if self.import_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_line = _update
