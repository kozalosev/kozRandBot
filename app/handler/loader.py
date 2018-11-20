import inspect
import pkgutil
import importlib
from typing import *

from .abc import InlineHandler
from . import impls

T = TypeVar('T')
TextProcessorTypesPair = Tuple[Type[InlineHandler], Type[InlineHandler]]
TextProcessorsPair = Tuple[InlineHandler, InlineHandler]


def get_implementations_from_module(cls: Type[T], module) -> Iterable[Type[T]]:
    """
    Scan the module and return a list of non-abstract implementations of
    the abstract 'cls' class.
    """
    assert inspect.isabstract(cls)

    def only_non_abstract_subclasses(obj):
        return inspect.isclass(obj) and hasattr(obj, '__message_handler__') and not inspect.isabstract(obj)
    classes = inspect.getmembers(module, only_non_abstract_subclasses)
    return [class_object for name, class_object in classes]


def get_implementations_from_package(cls: Type[T], package) -> Iterable[Type[T]]:
    """Call 'get_implementations_from_module' for all modules in the package."""
    assert hasattr(package, '__path__')

    module_names = (t[1] for t in pkgutil.iter_modules(package.__path__) if not t[2])
    module_full_names = ("{}.{}".format(package.__name__, name) for name in module_names)
    modules = (importlib.import_module(name) for name in module_full_names)
    impls = (get_implementations_from_module(cls, module) for module in modules)
    return (x for module_impls in impls for x in module_impls)


def get_implementations(cls: Type[T], obj) -> Iterable[Type[T]]:
    """Shortcut that determines whether 'obj' is a module or package automatically."""
    if hasattr(obj, '__path__'):
        return get_implementations_from_package(cls, obj)
    else:
        return get_implementations_from_module(cls, obj)


class InlineHandlersLoader:
    """
    Container of inline handlers, that is intended for end users. Depending of
    the constructor parameter, it gathers all concrete implementations of
    the 'InlineHandler' class from either a module or all modules in some
    package. By default, it returns all built-in implementations from the
    'impls' submodule.
    """
    handlers: Iterable[Type[InlineHandler]] = None

    def __init__(self, module_or_package=impls):
        self.handlers = set(get_implementations(InlineHandler, module_or_package))

    def match_handlers(self, query: str) -> Iterable[InlineHandler]:
        """
        Iterate over the list of inline handlers and returns the list of
        instances of all handlers which can process the query.
        """
        return [x() for x in self.handlers if x.can_process(query)]
