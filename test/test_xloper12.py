import pytest
import xll
from xlcall import lib

@pytest.mark.parametrize('value', [
'',
'TheNumberOne',
'B',
'The second number',
'nothing here',
'python-cffi-excel',
])
def test_xltypeStr(value):
    xloper = xll.to_xloper(value)

    assert xloper.xltype == lib.xltypeStr | lib.xlbitDLLFree
    assert ord(xloper.val.str[0]) == len(value)
    assert xll.from_xloper(xloper) == value









