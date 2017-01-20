import os

from setuptools import setup, find_packages


def readme():
    with open('README.rst') as fptr:
        return fptr.read()


PACKAGE_NAME = 'pygigasetelements'
HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = '0.1.0'

PACKAGES = find_packages(exclude=[])

REQUIRES = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license="GPL-3.0",
    url='https://github.com/seppi91/pygigasetelements',
    download_url='https://github.com/seppi91/pygigasetelements/tarball/' + VERSION,
    author='Sebastian Mittnacht',
    author_email='seppi91@gmx.de',
    description='Siemens Gigaset Elements interface',
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=REQUIRES,
    keywords=['home', 'automation', 'siemens', 'gigaset', 'elements', 'smarthome'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Home Automation'
    ],
)
