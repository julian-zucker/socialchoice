from setuptools import setup, find_packages

with open("../README.md") as readme_fd:
    readme = readme_fd.read()

setup(
    name="socialchoice",
    version="0.0.7",
    url="https://github.com/julian-zucker/socialchoice",
    license="Apache 2.0",
    packages=find_packages(),
    author="Julian Zucker",
    author_email="julian.zucker@gmail.com",
    description="Social Choice Theory in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=["networkx", "pytest", "scipy"],
)
