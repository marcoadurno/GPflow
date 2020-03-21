#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: skip-file

import os
import sys
from pathlib import Path

from pkg_resources import parse_version
from setuptools import find_packages, setup
import json
from urllib import request
from distutils.version import StrictVersion
import re

is_py37 = sys.version_info.major == 3 and sys.version_info.minor == 7
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'  # copied from the docs

# Dependencies of GPflow
requirements = [
    'numpy>=1.10.0',
    'scipy>=0.18.0',
    'multipledispatch>=0.4.9',
    'tabulate'
]

if not is_py37:
    requirements.append("dataclasses")

if not on_rtd:
    requirements.append("tensorflow-probability>=0.9")

min_tf_version = '2.1.0'
tf_cpu = 'tensorflow'
tf_gpu = 'tensorflow-gpu'


def latest_version(package_name):
    url = f"https://pypi.python.org/pypi/{package_name}/json"
    data = json.load(request.urlopen(url))
    # filter out rc and b releases and, more in general, any realeses that do not contain exclusively numbers and dots.
    versions = [v for v in data["releases"].keys() if re.match('[0-9\.]+$',v)]  
    versions.sort(key=StrictVersion)
    return versions[-1]  # return latest version


# Only detect TF if not installed or outdated. If not, do not do not list as
# requirement to avoid installing over e.g. tensorflow-gpu
# To avoid this, rely on importing rather than the package name (like pip).

try:
    # If tf not installed, import raises ImportError
    import tensorflow as tf
    if parse_version(tf.__version__) < parse_version(min_tf_version):
        # TF pre-installed, but below the minimum required version
        raise DeprecationWarning("TensorFlow version below minimum requirement")
except (ImportError, DeprecationWarning):
    # Add TensorFlow to dependencies to trigger installation/update
    if not on_rtd:
        # Do not add TF if we are installing GPflow on readthedocs
        requirements.append(tf_cpu)
        gast_requirement = 'gast>=0.2.2,<0.3' if latest_version('tensorflow') < parse_version('2.2') else 'gast>=0.3.3'
        requirements.append(gast_requirement)
        

with open(str(Path(".", "VERSION").absolute())) as version_file:
    version = version_file.read().strip()

packages = find_packages('.', exclude=["tests"])

setup(name='gpflow',
      version=version,
      author="James Hensman, Alex Matthews",
      author_email="james.hensman@gmail.com",
      description="Gaussian process methods in TensorFlow",
      license="Apache License 2.0",
      keywords="machine-learning gaussian-processes kernels tensorflow",
      url="http://github.com/GPflow/GPflow",
      packages=packages,
      include_package_data=True,
      install_requires=requirements,
      extras_require={'Tensorflow with GPU': [tf_gpu]},
      python_requires=">=3.6",
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ])
