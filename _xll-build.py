import xlcall_build

from cffi import FFI

ffi = FFI()

ffi.include(xlcall_build.ffi)

MAX_CALLBACKS = 0x8000

ffi.cdef('')
ffi.set_source('_xll',
   f"""     
   #include <XLCALLDEF.h> 
   """,
   include_dirs=['src'],
   extra_link_args=['/DEF:_xll.def'],
   #extra_compile_args=['/FAc'],
   sources=['src/DllMain.cpp'],
   )
ffi.embedding_api('''   
    extern "Python" int __stdcall xlAutoOpen(void);
    extern "Python" int __stdcall xlAutoClose(void);
    extern "Python" void __stdcall xlAutoFree12(LPXLOPER12);           
    extern "Python" int __stdcall xlAutoAdd(void);
    extern "Python" int __stdcall xlAutoRemove(void);
                
    extern "Python" double __stdcall TheNumberOneInPy();
    extern "Python" LPXLOPER12 __stdcall test_c_string(wchar_t*);
    extern "Python" LPXLOPER12 __stdcall os_environ(LPXLOPER12);
                                
''')

ffi.embedding_init_code('''
import sys
try:
   import xll.addin   
except:
   sys.excepthook(*sys.exc_info())
   raise
''')

if __name__ == '__main__':
    ffi.compile(target='python.xll')

