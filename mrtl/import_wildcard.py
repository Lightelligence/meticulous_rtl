"""Ban import <pkg>::* inside RTL modules.

"""
# Python Imports
import re
# Lintwork Imports
# Meticulous RTL imports
from mrtl import filters

class ImportWildcard(filters.LineListener):
    """Ban import packages by wildcard.

    This is anything of the format 'import <pkg>::*'.

    While doing an import by wildcard may reduce the amount of typing you need
    to do in your module and you could argue it improves readability, it makes
    tracing much more difficult.

    Params and types no longer indicate their parent package which is where you would find their definition.

    By explicitly refering to content withing a package, you know implcilitly
    where the definition lives. It also makes it more obvious how tightly
    coupled a module is to a package: you can easily count the number of
    references to the package.
    """
    subscribe_to = [filters.ModuleLineBroadcaster]

    wildcard_re = re.compile("^\s*import\s*.*::\*;")
    
    ERROR_MSG = "Do not use wildcard imports. Explicitly reference items in the package."

    def _update(self, line_no, line):
        if self.wildcard_re.search(line):
            self.error(line_no, line, self.ERROR_MSG)

    update_moduleline = _update
