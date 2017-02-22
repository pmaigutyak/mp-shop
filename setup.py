
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='django-mp-shop',
    version='1.0',
    description='Django shop apps',
    long_description=open('README.md').read(),
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url='https://github.com/pmaigutyak/mp-shop',
    download_url='https://github.com/pmaigutyak/mp-shop/archive/1.0.tar.gz',
    packages=['shop'],
    license='MIT',
    install_requires=[]
)
