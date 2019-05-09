# -*- coding: utf-8 -*-
"""Setup file for the gsheetsender project.
"""


import codecs
import os.path
import re
import sys
from setuptools import setup, find_packages

# avoid a from gsheetsender import __version__ as version (that compiles gsheetsender.__init__ and is not compatible with bdist_deb)
version = None
for line in codecs.open(os.path.join('gsheetsender', '__init__.py'), 'r', encoding='utf-8'):
    matcher = re.match(r"""^__version__\s*=\s*['"](.*)['"]\s*$""", line)
    version = version or matcher and matcher.group(1)

# get README content from README.md file
with codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()


setup(
    name='gsheetsender',
    version=version,
    description='No description yet.',
    long_description=long_description,
    author='gabor.bereczki',
    author_email='gabor.bereczki@icell.hu',
    license='GPL-2',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='gsheetsender.tests',
    install_requires=['google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib',
                      'oauth2client', 'jinja2'],
    setup_requires=[],
    classifiers=['Development Status :: 3 - Alpha', 'Operating System :: MacOS :: MacOS X', 'Operating System :: Microsoft :: Windows', 'Operating System :: POSIX :: BSD', 'Operating System :: POSIX :: Linux', 'Operating System :: Unix', 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)', 'Programming Language :: Python :: 3 :: Only'],
)
