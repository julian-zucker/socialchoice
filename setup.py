from setuptools import setup, find_packages

setup(
    name="socialchoice",
    version="0.0.3",
    packages=["socialchoice", "socialchoice.pairwisecollapse"],
    package_dir={"": "socialchoice"},
    url="https://github.com/julian-zucker/socialchoice",
    license="Apache 2.0",
    author="Julian Zucker",
    author_email="julian.zucker@gmail.com",
    description="Social Choice Theory in Python",
    install_requires=["networkx", "pygraphviz", "pytest", "scipy"],
)
