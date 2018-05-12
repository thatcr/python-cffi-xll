
from cffi import FFI

ffi = FFI()

ffi.cdef(open('src/XLCALLAPI.H').read() + '''
extern int Excel12(int xlfn, LPXLOPER12 operRes, int count, ... );
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
}

""",
include_dirs=['src']
)

# for some reason we need this to trigger windows.h...
ffi.embedding_api('')

if __name__ == '__main__':
    ffi.compile(target='xlcall.pyd')
