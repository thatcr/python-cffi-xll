# auto-generated file
import _cffi_backend

ffi = _cffi_backend.FFI('xlcall._xlcall',
    _version = 0x2601,
    _types = b'\x00\x00\x03\x0D\x00\x00\x00\x0F\x00\x00\x03\x0D\x00\x00\x07\x01\x00\x00\x0F\x03\x00\x00\x07\x01\x00\x00\x04\x03\x00\x00\x02\x0F\x00\x00\x11\x09\x00\x00\x10\x09\x00\x00\x0D\x03\x00\x00\x0C\x03\x00\x00\x13\x09\x00\x00\x12\x09\x00\x00\x10\x03\x00\x00\x15\x09\x00\x00\x14\x09\x00\x00\x16\x03\x00\x00\x13\x03\x00\x00\x17\x09\x00\x00\x13\x05\x00\x00\x00\x01\x00\x00\x16\x09\x00\x00\x16\x05\x00\x00\x00\x01\x00\x00\x1A\x03\x00\x00\x02\x01\x00\x00\x0E\x01\x00\x00\x1B\x05\x00\x00\x00\x01\x00\x00\x09\x01\x00\x00\x05\x01\x00\x00\x01\x09\x00\x00\x02\x09\x00\x00\x03\x09\x00\x00\x04\x09\x00\x00\x06\x09\x00\x00\x08\x09\x00\x00\x09\x09\x00\x00\x0A\x09\x00\x00\x0B\x09\x00\x00\x0D\x09\x00\x00\x05\x09\x00\x00\x07\x09\x00\x00\x00\x09\x00\x00\x0C\x09\x00\x00\x0E\x09\x00\x00\x0F\x09\x00\x00\x31\x03\x00\x00\x04\x01\x00\x00\x0A\x01\x00\x00\x06\x01\x00\x00\x35\x03\x00\x00\x00\x01\x00\x00\x37\x03\x00\x00\x10\x01',
    _globals = (b'\x00\x00\x02\x23Excel12v',0,b'\x00\x00\x00\x23XLCallVer',0),
    _struct_unions = ((b'\x00\x00\x00\x2C\x00\x00\x00\x03$1',b'\x00\x00\x1B\x11num',b'\x00\x00\x19\x11str',b'\x00\x00\x33\x11bool',b'\x00\x00\x33\x11err',b'\x00\x00\x1F\x11w',b'\x00\x00\x25\x11sref',b'\x00\x00\x26\x11mref',b'\x00\x00\x27\x11array',b'\x00\x00\x28\x11flow',b'\x00\x00\x29\x11bigdata'),(b'\x00\x00\x00\x20\x00\x00\x00\x02$10',b'\x00\x00\x33\x11count',b'\x00\x00\x13\x11ref'),(b'\x00\x00\x00\x21\x00\x00\x00\x02$11',b'\x00\x00\x0B\x11lpmref',b'\x00\x00\x32\x11idSheet'),(b'\x00\x00\x00\x22\x00\x00\x00\x02$12',b'\x00\x00\x04\x11lparray',b'\x00\x00\x03\x11rows',b'\x00\x00\x03\x11columns'),(b'\x00\x00\x00\x23\x00\x00\x00\x02$13',b'\x00\x00\x2A\x11valflow',b'\x00\x00\x03\x11rw',b'\x00\x00\x03\x11col',b'\x00\x00\x31\x11xlflow'),(b'\x00\x00\x00\x2A\x00\x00\x00\x03$14',b'\x00\x00\x03\x11level',b'\x00\x00\x03\x11tbctrl',b'\x00\x00\x32\x11idSheet'),(b'\x00\x00\x00\x24\x00\x00\x00\x02$15',b'\x00\x00\x2B\x11h',b'\x00\x00\x1E\x11cbData'),(b'\x00\x00\x00\x2B\x00\x00\x00\x03$16',b'\x00\x00\x30\x11lpbData',b'\x00\x00\x34\x11hdata'),(b'\x00\x00\x00\x25\x00\x00\x00\x02$2',b'\x00\x00\x33\x11count',b'\x00\x00\x16\x11ref'),(b'\x00\x00\x00\x26\x00\x00\x00\x02$3',b'\x00\x00\x0A\x11lpmref',b'\x00\x00\x32\x11idSheet'),(b'\x00\x00\x00\x27\x00\x00\x00\x02$4',b'\x00\x00\x0E\x11lparray',b'\x00\x00\x33\x11rows',b'\x00\x00\x33\x11columns'),(b'\x00\x00\x00\x28\x00\x00\x00\x02$5',b'\x00\x00\x2D\x11valflow',b'\x00\x00\x33\x11rw',b'\x00\x00\x31\x11col',b'\x00\x00\x31\x11xlflow'),(b'\x00\x00\x00\x2D\x00\x00\x00\x03$6',b'\x00\x00\x1F\x11level',b'\x00\x00\x1F\x11tbctrl',b'\x00\x00\x32\x11idSheet'),(b'\x00\x00\x00\x29\x00\x00\x00\x02$7',b'\x00\x00\x2E\x11h',b'\x00\x00\x1E\x11cbData'),(b'\x00\x00\x00\x2E\x00\x00\x00\x03$8',b'\x00\x00\x30\x11lpbData',b'\x00\x00\x34\x11hdata'),(b'\x00\x00\x00\x2F\x00\x00\x00\x03$9',b'\x00\x00\x1B\x11num',b'\x00\x00\x36\x11str',b'\x00\x00\x03\x11xbool',b'\x00\x00\x03\x11err',b'\x00\x00\x03\x11w',b'\x00\x00\x20\x11sref',b'\x00\x00\x21\x11mref',b'\x00\x00\x22\x11array',b'\x00\x00\x23\x11flow',b'\x00\x00\x24\x11bigdata'),(b'\x00\x00\x00\x09\x00\x00\x00\x02_FP',b'\x00\x00\x33\x11rows',b'\x00\x00\x33\x11columns',b'\x00\x00\x1C\x11array'),(b'\x00\x00\x00\x08\x00\x00\x00\x02_FP12',b'\x00\x00\x03\x11rows',b'\x00\x00\x03\x11columns',b'\x00\x00\x1C\x11array'),(b'\x00\x00\x00\x0D\x00\x00\x00\x02xlmref',b'\x00\x00\x33\x11count',b'\x00\x00\x17\x11reftbl'),(b'\x00\x00\x00\x0C\x00\x00\x00\x02xlmref12',b'\x00\x00\x33\x11count',b'\x00\x00\x14\x11reftbl'),(b'\x00\x00\x00\x10\x00\x00\x00\x02xloper',b'\x00\x00\x2C\x11val',b'\x00\x00\x33\x11xltype'),(b'\x00\x00\x00\x0F\x00\x00\x00\x02xloper12',b'\x00\x00\x2F\x11val',b'\x00\x00\x32\x11xltype'),(b'\x00\x00\x00\x16\x00\x00\x00\x02xlref',b'\x00\x00\x33\x11rwFirst',b'\x00\x00\x33\x11rwLast',b'\x00\x00\x31\x11colFirst',b'\x00\x00\x31\x11colLast'),(b'\x00\x00\x00\x13\x00\x00\x00\x02xlref12',b'\x00\x00\x03\x11rwFirst',b'\x00\x00\x03\x11rwLast',b'\x00\x00\x03\x11colFirst',b'\x00\x00\x03\x11colLast')),
    _typenames = (b'\x00\x00\x00\x03BOOL',b'\x00\x00\x00\x03COL',b'\x00\x00\x00\x09FP',b'\x00\x00\x00\x08FP12',b'\x00\x00\x00\x32IDSHEET',b'\x00\x00\x00\x0ALPXLMREF',b'\x00\x00\x00\x0BLPXLMREF12',b'\x00\x00\x00\x0ELPXLOPER',b'\x00\x00\x00\x04LPXLOPER12',b'\x00\x00\x00\x11LPXLREF',b'\x00\x00\x00\x12LPXLREF12',b'\x00\x00\x00\x03RW',b'\x00\x00\x00\x37XCHAR',b'\x00\x00\x00\x0DXLMREF',b'\x00\x00\x00\x0CXLMREF12',b'\x00\x00\x00\x10XLOPER',b'\x00\x00\x00\x0FXLOPER12',b'\x00\x00\x00\x16XLREF',b'\x00\x00\x00\x13XLREF12'),
)
