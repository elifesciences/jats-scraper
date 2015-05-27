from setuptools import setup
import feeds as module

setup(
    name=module.__name__,
    version=module.__version__,
    description=module.__description__,
    long_description=open('README.md', 'r').read(),
    license=open('gpl.txt', 'r').read(),
    install_requires=open('requirements.txt', 'r').read().splitlines()
)
