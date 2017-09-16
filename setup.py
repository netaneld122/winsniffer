try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='winsniffer',
    version='1.0',
    install_requires=['dpkt', 'hexdump', 'pypcap', 'wxpython'],
    packages=['winsniffer'],
    url='https://bitbucket.org/netaneld122/winsniffer',
    license='GPL License',
    author='Netanel Dziubov',
    description='Simple network sniffer for Windows',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ]
)
