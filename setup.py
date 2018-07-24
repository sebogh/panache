from distutils.core import setup

version = {}
with open("./panache/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='Panache',
    version=version['__version__'],
    packages=['panache',],
    license='BSD 3-Clause License',
)