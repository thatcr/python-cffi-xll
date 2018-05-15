import inspect

from typing import List, Tuple, NewType
from xlcall import ffi
from .convert import to_xloper

Xloper = NewType('Xloper', object)
Oper = NewType('Oper', Xloper)
Xloper12 = NewType('Xloper12', object)
Oper12 = NewType('Oper12', Xloper12)

# what about NamedTuple?

# also need a converter where the type is more specific, but the xll bit generic.

TYPE_MAP = {
    bool : ('A', 'short'),
    float : ('B', 'double'),
    # Ascii[str] : ('C', 'char*') # how do we use this instead of a string? Ascii[str]
    # Bytes[str] : ('F', 'char*') # counted string can extend beyond the \0?
    int : ( 'J', 'int'),
    # List[Tuple[float]] : ('K', 'FP*') # this, or 2D numpy?
    Oper : ('P', 'LPXLOPER'),
    Xloper : ('R', 'LPXLOPER'),
    str : ('C%', 'wchar_t*'),
    # Bytes[str] : ('C%', 'wchat_t*'), # counted string, how>
    # List[Tuple[float]] : ('K%', 'FP12*') # more 2D numpy?
    Oper12 : ('Q', 'LPXLOPER12'),
    Xloper12 : ('U', 'LPXLOPER12'),
}

def udf(func=None, name=None):

    import xlcall
    print(xlcall.__file__)
    if hasattr(func, '__xll_udf_callback__'):
        raise RuntimeError('udf is already registered')

    sig = inspect.signature(func)
    # construct the callback - add more type conversion soon
    callback_type = 'LPXLOPER12 __stdcall({})'.format(
        ','.join(TYPE_MAP[p.annotation][1] for p in sig.parameters)
    )
    def _xll_callback(*args, **kwargs):
        return to_xloper(func(*args, **kwargs))
    func.__xll_callback__ = ffi.callback(callback_type, _xll_callback)

    # arguments to xlfRegister, without the first two which specify the callback
    # or can we do that in the xlcall fully?
    func.__xll_register__ = [
        xlcall.__file__,

        'Q'+''.join(TYPE_MAP[p.annotation][0] for p in sig.parameters),
        name or func.__qualname__,
        ','.join(p.name for p in sig.parameters),
        1,
        func.__module__
    ]

    return func