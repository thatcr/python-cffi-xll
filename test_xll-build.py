import xlcall_build

from cffi import FFI

ffi = FFI()

ffi.include(xlcall_build.ffi)

ffi.set_source('_test_xll',
   r"""   
   #include <XLCALLDEF.h>
   CFFI_DLLEXPORT double __stdcall TheNumberOneInC() { return 1.0; }
   """,
   include_dirs=['src'],
   extra_link_args=['/DEF:test_xll.def'],
   sources=['src/DllMain.cpp'],
   )

ffi.embedding_api('''
    extern "Python" int __stdcall xlAutoOpen(void);
    extern "Python" int __stdcall xlAutoClose(void);
    extern "Python" int __stdcall xlAutoFree12(LPXLOPER12);           
        
    extern "Python" double __stdcall TheNumberOneInPy();
    extern "Python" LPXLOPER12 __stdcall os_environ(LPXLOPER12);
''')

# should we define our entry points here explicitly
ffi.embedding_init_code('''
# TODO work out the name of this excel, and route to runpy? 
import test_xll
''')

EXCEL = r"C:\Program Files (x86)\Microsoft Office\Office15\EXCEL.EXE"

if __name__ == '__main__':
    ffi.compile(target='test_xll.xll')

