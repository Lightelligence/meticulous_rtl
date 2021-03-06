# /usr/env/python

import importlib
import pkgutil
import jinja2
from mrtl import filters
import sys

MD_TEMPLATE = jinja2.Template("""# mrtl rule documentation

{%- for rule in rules %}
## {{ rule.__name__ }}
{{ rule.__doc__ }}
{%- endfor -%}
""")

for (_, name, _) in pkgutil.iter_modules(['mrtl']):
    this_mod = importlib.import_module('.' + name, 'mrtl')

uniques = {}
for cls in filters.LineListener.__subclasses__():
    # I'm not sure why there are duplciates. I think it has something to do with how bazel makes the python env work
    # Regardless, need to only admit one class with each name
    # Specifically ignore the Pragma class because it's part of the infrastructure, not a rule
    if cls.__name__ not in uniques and cls.__name__ != "Pragma":
        uniques[cls.__name__] = cls
        if cls.__doc__.isspace():
            sys.exit("Rule {} has an empty docstring. All rules must be properly documented".format(cls.__name__))

# Need to explicitly sort the classes instead of telling jinja to iterate over sorted(uniques.values) because
# the values don't implement comparison operators.
# I'm not sure why the ordering of uniques is volatile. It might be because iter_modules or doesn't guarantee order
sorted_uniques = []
for unique in sorted(uniques.keys()):
    sorted_uniques.append(uniques[unique])
print(MD_TEMPLATE.render(rules=sorted_uniques))
