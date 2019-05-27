from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

setup(
    name="socialchoice",
    version="0.0.4",
    packages=["socialchoice", "socialchoice.pairwisecollapse"],
    package_dir={"": "socialchoice"},
    url="https://github.com/julian-zucker/socialchoice",
    license="Apache 2.0",
    author="Julian Zucker",
    author_email="julian.zucker@gmail.com",
    description="Social Choice Theory in Python",
    long_description=readme,
    install_requires=["networkx", "pygraphviz", "pytest", "scipy"],
)
