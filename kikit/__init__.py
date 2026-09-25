
from . import _version
__version__ = _version.get_versions()['version']

import pcbnew

# Work around KiCad's SWIG iterator bug until its generated bindings are fixed:
# https://gitlab.com/kicad/code/kicad/-/work_items/25423
# https://github.com/yaqwsx/KiKit/issues/938
if not hasattr(pcbnew.SwigPyIterator, "next"):
    pcbnew.SwigPyIterator.next = lambda it: next(it)
