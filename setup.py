from setuptools import setup


def groupby(f, l):
    x, y = [], []
    for v in l:
        (x if f(v) else y).append(v)
    return x, y


def requirements():
    requisites = open('requirements.txt', 'r').read().splitlines()
    pypi, non_pypi = groupby(lambda r: not r.startswith('-e '), requisites)
    non_pypi = map(lambda v: v[len('-e '):], non_pypi)
    return {
        'install_requires': pypi,
        'dependency_links': non_pypi,
    }


setup(
    name__='jats-scraper',
    version='2015.05.28',
    description='JATS XML in a format suitable for ingestion by the eLife website',
    long_description=open('README.md', 'r').read(),
    license=open('gpl.txt', 'r').read(),
    **requirements()
)
