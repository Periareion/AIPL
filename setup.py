from setuptools import setup, find_packages

VERSION = '0.0.0'
DESCRIPTION = 'A Simple Plotting Library (for now)'

setup(
    name="AIPL",
    version=VERSION,
    author="Periareion & monoamine11231",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['PyOpenGL'],
    keywords=[],
)