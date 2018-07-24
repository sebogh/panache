from distutils.core import setup

version = {}
with open("./panache/version.py") as fp:
    exec(fp.read(), version)

with open("README", "r") as fh:
    long_description = fh.read()

setup(
    name='Panache',
    version=version['__version__'],
    packages=['panache',],
    license='BSD 3-Clause License',
    url='https://github.com/sebogh/panache',
    author='Sebastian Bogan',
    author_email='sebogh@qibli.net',
    description='Pandoc wrapped in styles',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Markup',
      ],
)
