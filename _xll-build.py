import xlcall_build

from cffi import FFI

ffi = FFI()

ffi.include(xlcall_build.ffi)

ffi.cdef("""
   extern void* callbacks[1];   
""")

# how do we register?
# use entry points, and unify.
# have seperate xlls for load/unload.

# _test_xll should be generated here?
ffi.set_source('_xll',
   r"""   
   #include <XLCALLDEF.h>
   CFFI_DLLEXPORT double __stdcall TheNumberOneInC() { return 1.0; }
   
   void* callbacks[1];
   
   __declspec(dllexport,naked) void __stdcall callback0(void) { 
      __asm { jmp callbacks + 0 * 4 }
   };
         
   """,
   include_dirs=['src'],
   extra_link_args=['/DEF:_xll.def'],
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

# should we define our entry points here explicitly
ffi.embedding_init_code('''
import _xll
import runpy
runpy.run_module('test.xll', init_globals = { '__ffi__' : _xll.ffi, '__lib__' : _xll.lib })
''')

EXCEL = r"C:\Program Files (x86)\Microsoft Office\Office15\EXCEL.EXE"

if __name__ == '__main__':
    ffi.compile(target='test_xll.xll')

