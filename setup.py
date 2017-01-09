""" Valentine Linguaflow installer
"""
import os
from os.path import join
from setuptools import setup, find_packages

name = 'valentine.linguaflow'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()

setup(name=name,
      version=version,
      description="Valentine Linguaflow",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='linguaplone linguaflow',
      author='Sasha Vincic',
      author_email='sasha dot vincic at valentinewebsystems dot com',
      url='http://svn.plone.org/svn/collective/valentine.linguaflow/trunk/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['valentine'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.monkeypatcher',
          'Products.LinguaPlone',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
