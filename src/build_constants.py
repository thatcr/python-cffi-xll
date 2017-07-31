import re
from collections import defaultdict
from inflection import underscore
from keyword import iskeyword

from pkg_resources import resource_filename

XLCALL_H = '../ExcelXLLSDK/INCLUDE/XLCALL.H'

re_define = re.compile(r'^\s*#define (xlHpc|xlMode|[a-z]+)([A-Z][_A-Za-z0-9]+)\s*([^/]+)')


def _extract_defines(code):
    scope = {}
    for line in code.readlines():
        match = re_define.match(line)
        if match:
            prefix, name, value = match.groups()
            scope[prefix+name] = eval(value, scope, scope)
            yield prefix, name, scope[prefix+name]

def identifier(id):
    id = underscore(id)
    if iskeyword(id):
        id = id + '_'
    return id

if __name__ == '__main__':
    defines = defaultdict(list)

    for prefix, key, value in _extract_defines(open(XLCALL_H)):
        defines[prefix].append((key, value))

    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('xlcall'))

    env.filters['identifier'] = identifier
    template = env.get_template('constants.py')

    with open(resource_filename('xlcall', 'constants.py'), 'w+') as f:
        f.write(template.render(defines=defines))



