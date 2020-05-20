# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

here = os.path.dirname(__file__)
if here == "":
    here = '.'
packages = find_packages(where=here)
package_dir = {k: os.path.join(here, k.replace(".", "/")) for k in packages}

with open(os.path.join(here, "requirements.txt"), "r") as f:
    requirements = f.read().strip(' \n\r\t').split('\n')
if len(requirements) == 0 or requirements == ['']:
    requirements = []

setup(name='brownian',
      version='0.1',
      description="Implémentation de simulations d'un mouvement brownien",
      long_description=""
                       "",
      author='Baptiste Pasquier',
      author_email='baptiste.pasquier@ensae.fr',
      url='https://github.com/baptiste-pasquier/brownian',
      packages=packages,
      package_dir=package_dir,
      requires=requirements)
