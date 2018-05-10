import os

from _test_xll import ffi

from xlcall import lib
from xll import Excel, xlAutoFree12, to_xloper, from_xloper

import logging

# install the deallocator from the xll module
ffi.def_extern(name='xlAutoFree12')(xlAutoFree12)

@ffi.def_extern(error=0)
def xlAutoOpen():
    logging.debug('xlAutoOpen')
    module_text = Excel(lib.xlGetName)

    #
    # res = Excel(lib.xlUDF, 'TheNumberOneInC')
    # assert res == 1.0
    #

    id = Excel(lib.xlfRegister,
               module_text,
               'TheNumberOneInPy',
               'B',
               'TheNumberOneInPy',
               '',
               1,
               'test_xll',
               )
    print('REGISTERED', id)

    id = Excel(lib.xlfRegister,
               module_text,
               'os_environ',
               'QQ',
               'OS.ENVIRON',
               'Name',
               1,
               'test_xll',
               )
    print('REGISTERED', id)

    return 1

@ffi.def_extern()
def xlAutoClose():
    logging.debug('xlAutoOpen')
    print('xlAutoClose')
    return 1

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