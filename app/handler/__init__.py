"""
System for automatic dynamic loading of inline handlers.

It automatically loads all non-abstract implementations of the 'InlineHandler'
class from some module or a whole package. Just use the 'InlineHandlersLoader'
class.

If you want to develop a new handler, see the 'abc' module.
"""

from .loader import InlineHandlersLoader
from .abc import InlineHandler
