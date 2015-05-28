from setuptools import setup
#import feeds as module

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
    # name = module.__name__,
    # version = module.__version__,
    # description = module.__description__,

    name = 'jats-scraper',
    version = 1,
    description ='awesome description',
    long_description = open('README.md', 'r').read(),
    #packages = [module.__name__],
    license = open('gpl.txt', 'r').read(),
    **requirements()
)
