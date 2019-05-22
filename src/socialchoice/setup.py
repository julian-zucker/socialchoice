from distutils.core import setup

from setuptools import find_packages

setup(name="socialchoice", packages=find_packages(), install_requires=["networkx", "pygraphviz"])
