from cffi import FFI
from pathlib import Path

sdk_dir = (Path(__file__).parent / '..' / '..' / 'Excel2013XLLSDK' ).resolve()


ffi = FFI()

# note need cffi 1.5.1 in order to support __stdcall
ffi.embedding_api('''
    extern int __stdcall xlAutoOpen(void);
    extern int __stdcall xlAutoClose(void);
'''
)

# office 2016 seems to break AttachConsole/AllocConsole. Nasty
# works in office 2013.
# but how do we pick up the right virtualenv?
# if we are in develop mode it's a problem: need to find the base of the tree for PYTHONPATH?
# need to find the location of python.dll, and insall the right virtualenv PATH around it
# not sure that the embedded install does that? or are we just picking upt he wrong one.

# VIRTUAL_ENV can specify where, if not we use the

ffi.set_source('test_xll',
'''
#include <WINDOWS.H>
#include <XLCALL.H>

#include <stdio.h>

#include <fcntl.h>

#include <io.h>


#pragma comment(linker, "/export:xlAutoOpen=_xlAutoOpen@0")
#pragma comment(linker, "/export:xlAutoClose=_xlAutoClose@0")

// if a buffer wasn't initialized because the inherited handle
// was a console, yet the application was not then reopen it
// and make sure it is unbuffered.
static void _reopen_console(const char* name, FILE* fp, const char* mode)
{
    if (_fileno(fp) == -2)
    {
        freopen(name, mode, fp);
        setvbuf(fp, NULL, _IONBF, 0);
    }
}

static void _console()
{
    DWORD dwError;
    char szError[4096];

    // standard handles that are not redirected to console will already
    // have been initialized correctly - mscrt obeys pipe/file redirections
    // even if we are not in a console process.

    sprintf(szError, "%d %d %d\\n",
        (int) GetStdHandle(STD_INPUT_HANDLE),
        (int) GetStdHandle(STD_OUTPUT_HANDLE),
        (int) GetStdHandle(STD_ERROR_HANDLE));
    OutputDebugString(szError);


    // however console handles are not inherited, so first we attach a console
    if (GetConsoleWindow() == NULL)
        AttachConsole(ATTACH_PARENT_PROCESS);

    sprintf(szError, "%d %d %d\\n",
        (int) GetStdHandle(STD_INPUT_HANDLE),
        (int) GetStdHandle(STD_OUTPUT_HANDLE),
        (int) GetStdHandle(STD_ERROR_HANDLE));
    OutputDebugString(szError);

    // for some reason this doesn't now work. is it windows 10 or excel 2016
    // or 32 bit on 64. something changed post windows 7 that stops AllocConsole?

    // if we have no console, and no redirection, then allocate a new console
    if (GetConsoleWindow() == NULL)
    {
        if (!AllocConsole())
        {
            sprintf(szError, "%d %d %d\\n",
            (int) GetStdHandle(STD_INPUT_HANDLE),
            (int) GetStdHandle(STD_OUTPUT_HANDLE),
            (int) GetStdHandle(STD_ERROR_HANDLE));
        OutputDebugString(szError);

            dwError = GetLastError();
            sprintf(szError, "GetLastError: %d\\n", dwError);
            OutputDebugString(szError);
            return;
        }
    }

    // -2 means we had no console window at startup, so fixup the streams
    // that aren't propertly initialized
    _reopen_console("CONIN$", stdin, "rb");
    _reopen_console("CONOUT$", stdout, "ab");
    _reopen_console("CONOUT$", stderr, "ab");

    // some packacges (pytest) assume that file descriptors 0, 1, 2
    // are always stdin/out/err, so dup them back so it works
    if (_fileno(stdin) != 0)
        _dup2(_fileno(stdin), 0);
    if (_fileno(stdout) != 1)
        _dup2(_fileno(stdout), 1);
    if (_fileno(stderr) != 2)
        _dup2(_fileno(stderr), 2);

    printf("Hello From The Other Side.\\n");
}

BOOL WINAPI DllMain(HINSTANCE hInstDLL, DWORD fdwReason, LPVOID lpvReason)
{
    DisableThreadLibraryCalls(hInstDLL);
    if (fdwReason == DLL_PROCESS_ATTACH) {
        _console();
    }
    return TRUE;
}


''', include_dirs=[str(sdk_dir / 'INCLUDE')],
     library_dirs=[str(sdk_dir / 'LIB')],
     libraries = ['XLCALL32'],
     extra_compile_args = [ '/Zi'],
     extra_link_args = ['/DEBUG']
)

ffi.embedding_init_code('''
    from test_xll import ffi

    from xlcall._xlcall import ffi as xlcall
    xlcall = xlcall.dlopen('XLCALL32')

    # we should look for the module we want to expose, and def_extern all of them here?
    # then the xlAutoOpen implementation needs to loop over all the def_externs..

    @ffi.def_extern(error=0)
    def xlAutoOpen():
        import os
        for key, value in os.environ.items():
            print('{key:<32s} {value}'.format(key=key, value=value))
        import sys
        print(sys.path)
        print(sys.prefix)
        print(sys.executable)
        print('XlCallVer: {:d}'.format(xlcall.XLCallVer()))
        return 1

    @ffi.def_extern(error=0)
    def xlAutoClose():
        return 1
''')


if __name__ == '__main__':
    ffi.compile(target='test_xll.xll')