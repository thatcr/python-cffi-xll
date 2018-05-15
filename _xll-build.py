import xlcall_build

from cffi import FFI

ffi = FFI()

ffi.include(xlcall_build.ffi)

MAX_CALLBACKS = 0x8000

ffi.cdef(f"""
   extern void* callbacks[{MAX_CALLBACKS}];
   extern unsigned int ncallbacks;   
""")

# _test_xll should be generated here?

ffi.set_source('_xll',
   r"""   
   #include <XLCALLDEF.h>
       
   int _dump_args(const char* type_text, const void* args)
   {      
      const unsigned char* arg;
      const char* t;
      int i;
            
      for (arg=(const unsigned char*) args, i = 0, t = type_text + 1; (*t) != 0; ++t, ++i)
      {
         switch(*t) {
            case 'J':               
               printf("arg[% 2d] = %d : int\n", i, *((int*) arg));
               arg += sizeof(int);
               break;                              
            default:
               printf("unknown type code '%c'\n", *t); 
               return 0;
         };         
      }    
      
      return i;       
   }   
   
   static const char* type_text = "JJJJ";
   static const size_t type_size = 12;
   static const void* callback = _dump_args;
                               
   __declspec(dllexport) void __stdcall Test(void) {          
      __asm {
         mov eax, ebp
         add eax, 8
                           
         push eax
         push type_text
         call callback      
         mov eax, 123      
         
         // restore stack base pointer 
         mov	 esp, ebp
  		 pop	 ebp
         
         // get return location from the stack
         pop ecx
         
         // remove all the arguments - needs to be variable
         add esp, type_size
         
         // jmp to the  location, no need to RET
         jmp ecx         
      }
   }
   
   
   """+
   f"""     
   void* callbacks[{MAX_CALLBACKS}];
   unsigned int ncallbacks = 0;
   """,
   include_dirs=['src'],
   extra_link_args=['/DEF:_xll.def'],
   extra_compile_args=['/FAc'],
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


EXCEL = r"C:\Program Files (x86)\Microsoft Office\Office15\EXCEL.EXE"

if __name__ == '__main__':
    ffi.compile(target='python.xll')

