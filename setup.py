from setuptools import setup, find_packages

# TODO addin xlcall as a python module
# TODO add the python.xll build to deliver into the prefix?

setup(
    name='python-cffi-excel',
    version='0.0.1',
    packages=find_packages('src'),
    platforms=['Windows'],

    entry_points = {

    }
)

