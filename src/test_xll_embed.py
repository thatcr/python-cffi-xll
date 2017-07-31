from test_xll import ffi as test_xll
from _xlcall import ffi, lib


# TODO - move types, and the

print(__file__)


# we should look for the module we want to expose, and def_extern all of them here?
# then the xlAutoOpen implementation needs to loop over all the def_externs..

@test_xll.def_extern(error=0)
def xlAutoOpen():
    import os
    for key, value in os.environ.items():
        print('{key:<32s} {value}'.format(key=key, value=value))
    import sys
    print(sys.path)
    print(sys.prefix)
    print(sys.executable)
    # this function is exported form XLCALL32, not much use now.
    #print('XlCallVer: {:d}'.format(lib.XLCallVer()))

    import pprint
    pprint.pprint(ffi.list_types())

    from xlcall.constants import xl



    res = ffi.new('LPXLOPER12')
    print(type(xl.get_name))
    print('OK: ', lib.Test(123, res, 0))
    ret = lib.Excel12v(int(xl.get_name.value), res, 0, ffi.new('LPXLOPER12[]', []))
    if ret:
        raise RuntimeError(str(ret))

    '''
    how to wrap XLOPER12? bascially just need a python class that will cast down when passed in
    if we write and XLOPER12 class, can we just pass that in, and have it convert nicely.
    shoudl work fine. need xlcall and _xlcall modules.
    '''


    print(res)
    print(res.xltype)
    print(ord(res.val.str[0]))
    print(str(res.val.str[1:ord(res.val.str[0])]))
    print(ffi.unpack(res.val.str + 1, ord(res.val.str[0])))
    for c in res.val.str[0:ord(res.val.str[0])]:
        print(c)

    # TODO isntanatly shutdown if we're running as a console scripted excel? can we run tests ewtc from here?
    # or do we need another call after registration, how.

    return 1


@test_xll.def_extern(error=0)
def xlAutoClose():
    print('xlAutoClose')
    return 1