import cffi
import scratch
from scratch import lib, ffi
import pprint

pprint.pprint(dir(scratch))
print(lib.pRVABase)
print(lib.pExportDirectory.Base)



# can we look lib and construct from entry points?

def kernel32():
    ffi = cffi.FFI()
    ffi.cdef("""
        BOOL __stdcall VirtualProtect(
            LPVOID lpAddress, 
            SIZE_T dwSize, 
            DWORD flNewProtect,
            PDWORD lpflOldProtect
            );
            
        #define PAGE_EXECUTE_READ 32
        #define PAGE_EXECUTE 16
        #define PAGE_WRITECOPY 8
        #define PAGE_NOCACHE 512 
        #define PAGE_READONLY 2 
        #define PAGE_READWRITE 4 
        #define PAGE_EXECUTE_READWRITE 64
        #define PAGE_WRITECOMBINE 1024 
        #define PAGE_GUARD 256 
        #define PAGE_NOACCESS 1 
        #define PAGE_EXECUTE_WRITECOPY 128 
    """)

    return ffi.dlopen('kernel32.dll')

# how do we now buoild the call backs?


class ExportDirectory:
    def __init__(self, base, directory):
        self.base = base
        self.directory = directory

        print (self.base + directory.AddressOfNames)

        self.AddressOfNames = ffi.cast(
            f"DWORD[{directory.NumberOfNames}]",
            lib.PointerFromAddress(directory.AddressOfNames)
        )
        self.AddressOfNameOrdinals = ffi.cast(
            f"WORD[{directory.NumberOfNames}]",
            lib.PointerFromAddress(directory.AddressOfNameOrdinals)
        )
        self.AddressOfFunctions = ffi.cast(
            f"DWORD[{directory.NumberOfFunctions}]",
            lib.PointerFromAddress(directory.AddressOfFunctions),
        )

        k32 = kernel32()

        # remove the vtable protection on the export table, so we can
        # manipulate it.
        flOldProtect = ffi.new("DWORD*")
        k32.VirtualProtect(
            self.AddressOfFunctions,
            ffi.sizeof(self.AddressOfFunctions),
            k32.PAGE_READWRITE,
            flOldProtect
        )

    def __iter__(self):
        for i in range(self.directory.NumberOfFunctions):
            yield ffi.string(ffi.cast("char*",
                lib.PointerFromAddress(self.AddressOfNames[i])
            )).decode('utf-8')

    def __setitem__(self, name, function):
        name = name.encode('utf-8')
        for i in range(self.directory.NumberOfFunctions):
            if name != ffi.string(ffi.cast("char*",
                            lib.PointerFromAddress(self.AddressOfNames[i]))):
                continue

            index = self.AddressOfNameOrdinals[i] # - self.directory.Base
            self.AddressOfFunctions[index] = lib.AddressFromPointer(function)
            return

        raise KeyError(f'could not find export {name}')


exports = ExportDirectory(lib.pRVABase, lib.pExportDirectory)


for k in exports:
    print(f"Export {k}")

@ffi.callback("int (*)(int, int)")
def add(a, b):
    return a + b

exports['_0'] = add

print('did it')