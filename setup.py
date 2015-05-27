from setuptools import setup

setup(
    name=feeds.py,
    version='0.1',
    description='scrape JATS XML to EIF JSON',
    long_description=open('README.md', 'r').read(),
    license=open('gpl.txt', 'r').read(),
    install_requires=open('requirements.txt', 'r').read().splitlines()
)
