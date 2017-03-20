
from setuptools import setup, find_packages

from shop import __version__

setup(
    name='django-mp-shop',
    version=__version__,
    description='Django shop apps',
    long_description=open('README.md').read(),
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url='https://github.com/pmaigutyak/mp-shop',
    download_url='https://github.com/pmaigutyak/mp-shop/archive/%s.tar.gz' % __version__,
    packages=find_packages(),
    package_data={'shop': ['*']},
    include_package_data=True,
    license='MIT',
    install_requires=[]
)
