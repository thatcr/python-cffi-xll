import os
from xlcall import lib
from xll import Excel, xlAutoFree12, to_xloper, from_xloper

# install the deallocator from the xll module
__ffi__.def_extern(name='xlAutoFree12')(xlAutoFree12)

cb = None

@__ffi__.def_extern(error=0)
def xlAutoOpen():
    print('xlAutoOpen')
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
    id = Excel(lib.xlfRegister,
               module_text,
               'os_environ',
               'QQ',
               'OS.ENVIRON',
               'Name',
               1,
               'test_xll',
               )

    id = Excel(lib.xlfRegister,
               module_text,
               'test_c_string',
               'QC%',
               'test_c_string',
               'Name',
               1,
               'test_xll',
               )

    def test_callback(a, b):
        print('test_callback')
        return to_xloper(f'answer is: {a + b}')
    print(dir(__lib__))


    global cb
    cb = __ffi__.callback("LPXLOPER12 __stdcall(int, int)", test_callback)
    __lib__.callbacks[0] = cb

    print(__lib__.callbacks[0])

    id =Excel(lib.xlfRegister,
              module_text,
              '_callback0@0',
              'QJJ',
              'test_callback',
              'a, b',
              1,
              'test_xll'
              )




    return 1

# TODO pick these up from the runpy, spoof if not there.
# ideally xlAutoRemove will de-initialize _Everything_ so we can reload...

@__ffi__.def_extern()
def xlAutoClose():
    print('xlAutoClose')
    return 1

@__ffi__.def_extern()
def xlAutoAdd():
    print('xlAutoAdd')
    return 1

@__ffi__.def_extern()
def xlAutoRemove():
    # note if we are being unloaded (not just excel closed) we get xlAutoRemove first, then xlAutoClose.
    # so unregister in xlAutoRemove, but not xlAutoClose,
    # https://social.msdn.microsoft.com/Forums/office/en-US/9886393d-be6d-4fed-9c17-4fc563c11669/xll-and-xlautoclose?forum=exceldev
    print('xlAutoRemove')
    return 1

@__ffi__.def_extern()
def TheNumberOneInPy():
    print('TheNumberOneInPy')
    return 123.123

@__ffi__.def_extern()
def os_environ(key):
    print(key, type(key))
    key = from_xloper(key)
    print(dir(key))
    print(f'Hello From {key}')
    return to_xloper(os.environ[key])

@__ffi__.def_extern()
def test_c_string(key):
    print(key, type(key))
    key = __ffi__.string(key)
    print(f'Hello From {key}')
    return to_xloper(f'Python Got: {key}')





