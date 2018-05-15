import sys
import os
import xlcall

from xlcall import lib
from _xll import ffi

from . import convert

from .convert import to_xloper, from_xloper
from .api import Excel

@ffi.callback("int(void*,const char*,void*)")
def _invoke_dummy(code, type_text, args):
    code = xlcall.ffi.from_handle(code)
    type_text = ffi.string(type_text)

    print('Hello World!')
    print(code)

    total = 0

    arg = args
    for char in type_text[1:]:
        print(char)
        if char == ord(b'J'):
            total += ffi.cast("int*", arg)[0]
            arg += ffi.sizeof('int')
        else:
            raise RuntimeError(f'Unknown character code {char}')

    return total

type_text = 'JJJJ'
type_text_enc = xlcall.ffi.new("char[]", type_text.encode('ascii'))
handle = xlcall.ffi.new_handle(sys)

@ffi.def_extern(error=0)
def xlAutoOpen():
    print('xlAutoOpen')

    i = lib._callback_count

    lib._callback_codes[i] = handle
    lib._callback_types[i] = type_text_enc
    lib._callback_sizes[i] = 12
    lib._callback_funcs[i] = _invoke_dummy

    id = Excel(lib.xlfRegister,
               xlcall.__file__,
               f'__f{i:04X}@0',
               type_text,
               'InvokeTest',
               '',
               1,
               __name__,
               )
    lib._callback_count = lib._callback_count + 1


    module_text = Excel(lib.xlGetName)

    id = Excel(lib.xlfRegister,
               module_text,
               'TheNumberOneInPy',
               'B',
               'TheNumberOneInPy',
               '',
               1,
               __name__,
               )
    id = Excel(lib.xlfRegister,
               module_text,
               'os_environ',
               'QQ',
               'OS.ENVIRON',
               'Name',
               1,
               __name__,
               )

    id = Excel(lib.xlfRegister,
               module_text,
               'test_c_string',
               'QC%',
               'test_c_string',
               'Name',
               1,
               __name__,
               )
    return 1

@ffi.def_extern(error=0)
def xlAutoClose():
    return 1

@ffi.def_extern(error=0)
def xlAutoAdd():
    return 1

@ffi.def_extern(error=0)
def xlAutoRemove():
    return 1

@ffi.def_extern()
def xlAutoFree12(xloper):
    convert.xlAutoFree12(xloper)

@ffi.def_extern()
def TheNumberOneInPy():
    print('TheNumberOneInPy')
    return 123.123

@ffi.def_extern()
def os_environ(key):
    print(key, type(key))
    key = from_xloper(key)
    print(dir(key))
    print(f'Hello From {key}')
    return to_xloper(os.environ[key])

@ffi.def_extern()
def test_c_string(key):
    print(key, type(key))
    key = ffi.string(key)
    print(f'Hello From {key}')
    return to_xloper(f'Python Got: {key}')
