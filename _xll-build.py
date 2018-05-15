import xlcall_build

from cffi import FFI

ffi = FFI()

ffi.include(xlcall_build.ffi)

MAX_CALLBACKS = 0x8000

ffi.cdef(f"""
   extern void* callbacks[{MAX_CALLBACKS}];
   extern unsigned int ncallbacks;   
""")

"""
with naked we see exactly the stack we want, but must do our own returning..

[0] = 0x1A108FE
TOS[1] = 0x1
TOS[2] = 0x2
TOS[3] = 0x3
TOS[4] = 0x0
TOS[5] = 0x4A
TOS[6] = 0x0
TOS[7] = 0x3FDADC
"""
"""
assembly is here
; Function compile flags: /Ogtpy
_TEXT	SEGMENT
_tos$ = -4						; size = 4
_a$ = 8							; size = 4
_b$ = 12						; size = 4
_c$ = 16						; size = 4
_InspectStack@12 PROC
; File e:\src\python-cffi-excel\_xll.c
; Line 1151
	mov	DWORD PTR _tos$[ebp], esp
; Line 1162
	push	DWORD PTR _tos$[ebp]
	push	OFFSET $SG4294967271
	call	_printf
	add	esp, 8
; Line 1163
	xor	esi, esi
$LL4@InspectSta:
; Line 1165
	mov	eax, DWORD PTR _tos$[ebp]
	push	DWORD PTR [eax+esi*4]
	push	esi
	push	OFFSET $SG4294967270
	call	_printf
	inc	esi
	add	esp, 12					; 0000000cH
	cmp	esi, 8
	jb	SHORT $LL4@InspectSta
_InspectStack@12 ENDP"""

# _test_xll should be generated here?

ffi.set_source('_xll',
   r"""   
   #include <XLCALLDEF.h>
     
   __declspec(noinline) void print_arg_data(const unsigned int* args)
   {
      int i;
      for (i = 8; i > -8; --i) { 
         printf("args[%03d] = 0x%08X\n", i, args[i]);
      }            
   }
   
   
                    
   __declspec(dllexport) int __stdcall Test(const int a, const int b, const int c) {
  
         
      __asm {
         mov eax, ebp
         add eax, 8
         
         push eax
         call print_arg_data      
         mov eax, 123      
         
         // restore stack base pointer 
         mov	 esp, ebp
  		 pop	 ebp
         
         // get return location from the stack
         pop ecx
         
         // remove all the arguments - needs to be variable
         add esp, 12
         
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

