import os
from setuptools import setup, find_packages

version = '1.0a2'


setup(name='plone.phonehome',
      version=version,
      description="Provide anonymous package usage statistics to the Plone Foundation",
      long_description=open("README.txt").read() + "\n" + open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",        
          ],
      license = "GPL version 2",
      url = "http://plone.org",
      author = 'Plone Foundation',
      author_email = 'plone-developers@lists.sourceforge.net',
      packages = find_packages(),
      namespace_packages = ['plone',],
      include_package_data = True,
      zip_safe = False,
      install_requires = [
        'setuptools',
        ],
      extras_require=dict(test=
        ['Plone']),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,        
      )
