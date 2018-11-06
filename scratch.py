from cffi import FFI

ffi = FFI()

ffi.cdef(r"""
    typedef struct _IMAGE_EXPORT_DIRECTORY {
        DWORD	Characteristics;
        DWORD	TimeDateStamp;
        WORD	MajorVersion;
        WORD	MinorVersion;
        DWORD	Name;
        DWORD	Base;
        DWORD	NumberOfFunctions;
        DWORD	NumberOfNames;
        DWORD	AddressOfFunctions;
        DWORD	AddressOfNames;
        DWORD	AddressOfNameOrdinals;
    } IMAGE_EXPORT_DIRECTORY,*PIMAGE_EXPORT_DIRECTORY;
    
    DWORD                   pRVABase;
    IMAGE_EXPORT_DIRECTORY* pExportDirectory;
    
    void* PointerFromAddress(DWORD Address);    
    DWORD AddressFromPointer(void* Pointer);        
""")

ffi.set_source("scratch", r"""
#include <assert.h>
#include <WINDOWS.h>

extern DWORD pRVABase = 0;
IMAGE_EXPORT_DIRECTORY* pExportDirectory = 0; 

extern CFFI_DLLEXPORT __declspec(naked) _0() { ExitProcess(0x00FF0000 + 0); }
extern CFFI_DLLEXPORT __declspec(naked) _1() { ExitProcess(0x00FF0000 + 1); }
extern CFFI_DLLEXPORT __declspec(naked) _3() { ExitProcess(0x00FF0000 + 2); }
extern CFFI_DLLEXPORT __declspec(naked) _02() { ExitProcess(0x00FF0000 + 02); }

extern void* PointerFromAddress(DWORD Address)
{
    return (void*)(Address + pRVABase);    
}


extern DWORD AddressFromPointer(void* Pointer)
{
    return (DWORD)(Pointer) - pRVABase;    
}

// initialize this from the 
extern void** exports= 0;

BOOL WINAPI DllMain(HINSTANCE hInstDll, DWORD fdwReason, LPVOID lpvReason)
{    
    if (pRVABase) 
        return TRUE;
        
    // figure out the location of the export able, this is easyier than 
    // using pythongf
    pRVABase = (DWORD) hInstDll;
    

    IMAGE_DOS_HEADER* pDosHeader = 
        (IMAGE_DOS_HEADER*) hInstDll;
    assert(pDosHeader->e_magic == 0x4550);    
    
    IMAGE_NT_HEADERS32* pNtHeaders32 = 
        (IMAGE_NT_HEADERS32*) (pDosHeader->e_lfanew + pRVABase);
    assert(pNtHeaders32->Signature == 0x4550);
    
    assert(pNtHeaders32->OptionalHeader.DataDirectory[0].VirtualAddress != 0);
    assert(pNtHeaders32->OptionalHeader.DataDirectory[0].Size != 0);
        
    pExportDirectory = 
        (IMAGE_EXPORT_DIRECTORY*)     
        (pNtHeaders32->OptionalHeader.DataDirectory[0].VirtualAddress + pRVABase);
        
    _cffi_initialize_python();                  
    
    return TRUE;    
}
""")

ffi.embedding_init_code(open("scratch-init.py", "r").read())

ffi.compile(target="scratch.dll", verbose=True)

def test_it():
    ffi = FFI()
    ffi.cdef("""
        int _0(int, int);
    """)

    api = ffi.dlopen('scratch.dll')

    # why no api call here?

    print(api._0(1, 10))

    # assert 3 == api._0(1, 2)

test_it()




