from setuptools import setup
from codecs import open
from os import path

setup_dir = path.abspath(path.dirname(__file__))

with open(path.join(setup_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pylaser',
    version='0.0.0.dev0',
    description='Python lib for laser cutting.',
    long_description=long_description,
    url='https://github.com/andersroos/pylaser',
    author='Anders Roos',
    author_email='anders.roos@gmail.com',
    license='Apache-2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='',
    packages=["pylaser"],
    install_requires=[
        'svgwrite',
    ],
    test_suite='test',
)
