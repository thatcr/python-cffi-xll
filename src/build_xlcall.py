from cffi import FFI

ffi = FFI()

from pathlib import Path

sdk_dir = (Path(__file__).parent / '..' / '..' / 'Excel2013XLLSDK' ).resolve()

ffi.set_source('xlcall._xlcall', None)

# how do we call Excel12v when it is PASCAL?

# wrap this so that it works without the dlopen? i.e. can we spoof
# the Excel12v call do that it is just missing?



ffi.cdef('''
/*
** XL 12 Basic Datatypes
**/

typedef INT32 BOOL;			/* Boolean */
typedef WCHAR XCHAR;			/* Wide Character */
typedef INT32 RW;			/* XL 12 Row */
typedef INT32 COL;	 	      	/* XL 12 Column */
typedef DWORD_PTR IDSHEET;		/* XL12 Sheet ID */

/*
** XLREF structure
**
** Describes a single rectangular reference.
*/

typedef struct xlref
{
	WORD rwFirst;
	WORD rwLast;
	BYTE colFirst;
	BYTE colLast;
} XLREF, *LPXLREF;


/*
** XLMREF structure
**
** Describes multiple rectangular references.
** This is a variable size structure, default
** size is 1 reference.
*/

typedef struct xlmref
{
	WORD count;
	XLREF reftbl[1];					/* actually reftbl[count] */
} XLMREF, *LPXLMREF;


/*
** XLREF12 structure
**
** Describes a single XL 12 rectangular reference.
*/

typedef struct xlref12
{
	RW rwFirst;
	RW rwLast;
	COL colFirst;
	COL colLast;
} XLREF12, *LPXLREF12;


/*
** XLMREF12 structure
**
** Describes multiple rectangular XL 12 references.
** This is a variable size structure, default
** size is 1 reference.
*/

typedef struct xlmref12
{
	WORD count;
	XLREF12 reftbl[1];					/* actually reftbl[count] */
} XLMREF12, *LPXLMREF12;


/*
** FP structure
**
** Describes FP structure.
*/

typedef struct _FP
{
    unsigned short int rows;
    unsigned short int columns;
    double array[1];        /* Actually, array[rows][columns] */
} FP;

/*
** FP12 structure
**
** Describes FP structure capable of handling the big grid.
*/

typedef struct _FP12
{
    INT32 rows;
    INT32 columns;
    double array[1];        /* Actually, array[rows][columns] */
} FP12;


/*
** XLOPER structure
**
** Excel's fundamental data type: can hold data
** of any type. Use "R" as the argument type in the
** REGISTER function.
**/

typedef struct xloper
{
	union
	{
		double num;					/* xltypeNum */
		LPSTR str;					/* xltypeStr */
		WORD bool;					/* xltypeBool */
		WORD err;					/* xltypeErr */
		short int w;					/* xltypeInt */
		struct
		{
			WORD count;				/* always = 1 */
			XLREF ref;
		} sref;						/* xltypeSRef */
		struct
		{
			XLMREF *lpmref;
			IDSHEET idSheet;
		} mref;						/* xltypeRef */
		struct
		{
			struct xloper *lparray;
			WORD rows;
			WORD columns;
		} array;					/* xltypeMulti */
		struct
		{
			union
			{
				short int level;		/* xlflowRestart */
				short int tbctrl;		/* xlflowPause */
				IDSHEET idSheet;		/* xlflowGoto */
			} valflow;
			WORD rw;				/* xlflowGoto */
			BYTE col;				/* xlflowGoto */
			BYTE xlflow;
		} flow;						/* xltypeFlow */
		struct
		{
			union
			{
				BYTE *lpbData;			/* data passed to XL */
				HANDLE hdata;			/* data returned from XL */
			} h;
			long cbData;
		} bigdata;					/* xltypeBigData */
	} val;
	WORD xltype;
} XLOPER, *LPXLOPER;

/*
** XLOPER12 structure
**
** Excel 12's fundamental data type: can hold data
** of any type. Use "U" as the argument type in the
** REGISTER function.
**/

typedef struct xloper12
{
	union
	{
		double num;				       	/* xltypeNum */
		XCHAR *str;				       	/* xltypeStr */
		BOOL xbool;				       	/* xltypeBool */
		int err;				       	/* xltypeErr */
		int w;
		struct
		{
			WORD count;			       	/* always = 1 */
			XLREF12 ref;
		} sref;						/* xltypeSRef */
		struct
		{
			XLMREF12 *lpmref;
			IDSHEET idSheet;
		} mref;						/* xltypeRef */
		struct
		{
			struct xloper12 *lparray;
			RW rows;
			COL columns;
		} array;					/* xltypeMulti */
		struct
		{
			union
			{
				int level;			/* xlflowRestart */
				int tbctrl;			/* xlflowPause */
				IDSHEET idSheet;		/* xlflowGoto */
			} valflow;
			RW rw;				       	/* xlflowGoto */
			COL col;			       	/* xlflowGoto */
			BYTE xlflow;
		} flow;						/* xltypeFlow */
		struct
		{
			union
			{
				BYTE *lpbData;			/* data passed to XL */
				HANDLE hdata;			/* data returned from XL */
			} h;
			long cbData;
		} bigdata;					/* xltypeBigData */
	} val;
	DWORD xltype;
} XLOPER12, *LPXLOPER12;

int XLCallVer(void);
int __stdcall Excel12v(int xlfn, LPXLOPER12 operRes, int count, LPXLOPER12 opers[]);
''')

# the Excel12 API functions should be loaded from the dll,
# we don't support va_args in cparser?
# neither do we support pascal calling convention.
# pascal is just stdcall with different stack parameter orer? so reverse the list?
# can we install the abi?

if __name__ == '__main__':
    ffi.compile()