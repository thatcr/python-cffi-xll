from cffi import FFI

MAX_CALLBACKS = 0x8000

ffi = FFI()
ffi.cdef(open('src/XLCALLAPI.H').read() + f'''
extern int Excel12(int xlfn, LPXLOPER12 operRes, int count, ... );

extern const void*    _callback_codes[{MAX_CALLBACKS}];
extern const char*    _callback_types[{MAX_CALLBACKS}];
extern const size_t   _callback_sizes[{MAX_CALLBACKS}];
extern const void*    _callback_funcs[{MAX_CALLBACKS}];
  
extern size_t _callback_count;
''')

ffi.set_source('xlcall',
r"""
#include <XLCALLDEF.h>

#define cxloper12Max 255
#define EXCEL12ENTRYPT "MdCallBack12"

typedef int (PASCAL *EXCEL12PROC) (int xlfn, int coper, LPXLOPER12 *rgpxloper12, LPXLOPER12 xloper12Res);
HMODULE hmodule;
EXCEL12PROC pexcel12;

__forceinline void FetchExcel12EntryPt(void)
{
	if (pexcel12 == NULL)
	{
		hmodule = GetModuleHandle(NULL);
		if (hmodule != NULL)
		{
			pexcel12 = (EXCEL12PROC) GetProcAddress(hmodule, EXCEL12ENTRYPT);
		}
	}
}

void pascal SetExcel12EntryPt(EXCEL12PROC pexcel12New)
{
	FetchExcel12EntryPt();
	if (pexcel12 == NULL)
	{
		pexcel12 = pexcel12New;
	}
}

int __cdecl Excel12(int xlfn, LPXLOPER12 operRes, int count, ...)
{
	LPXLOPER12 rgxloper12[cxloper12Max];
	va_list ap;
	int ioper;
	int mdRet;
		
	FetchExcel12EntryPt();
	if (pexcel12 == NULL)
	{
	    printf("No Entry point!\n");
		mdRet = xlretFailed;
	}
	else
	{
		mdRet = xlretInvCount;
		if ((count >= 0)  && (count <= cxloper12Max))
		{
			va_start(ap, count);
			for (ioper = 0; ioper < count ; ioper++)
			{
				rgxloper12[ioper] = va_arg(ap, LPXLOPER12);
			}
			va_end(ap);			
			mdRet = (pexcel12)(xlfn, count, &rgxloper12[0], operRes);
		}
	}
	return(mdRet);
}""" +
f"""     
const void*    _callback_codes[{MAX_CALLBACKS}];
const char*    _callback_types[{MAX_CALLBACKS}];
const size_t   _callback_sizes[{MAX_CALLBACKS}];
const void*    _callback_funcs[{MAX_CALLBACKS}];

size_t _callback_count;

#pragma warning( disable : 4731 )
       
"""+
''.join(rf"""                                        
__declspec(dllexport) void __stdcall _f{i:04X}(void) {{          
  __asm {{         
     // push the offset to the first pointer on the stack
     mov eax, ebp
     add eax, 8                           
     push eax
     
     // add the type, code and func from the callbacks
     push _callback_types[{i}]
     push _callback_codes[{i}]
     
     // invoke the callback
     call _callback_funcs[{i}]      
                    
     // restore stack pointers stored in the pre-amble by msvc 
     mov	 esp, ebp
     pop	 ebp
     
     // get original return location from the stack
     pop ecx
     
     // remove all the arguments, according to the size calculated
     add esp, _callback_sizes[{i}]
     
     // jmp to the  location, no need to RET
     jmp ecx         
  }}
}}      
""" for i in range(0, MAX_CALLBACKS)),
    include_dirs=['src']
)

# for some reason we need this to trigger windows.h...
ffi.embedding_api('')

if __name__ == '__main__':
    ffi.compile(target='xlcall.pyd')

