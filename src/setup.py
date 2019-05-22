from setuptools import setup

setup(
    name="socialchoice",
    version="0.0.0",
    packages=["socialchoice", "socialchoice.pairwisecollapse"],
    package_dir={"": "src"},
    url="https://github.com/julian-zucker/socialchoice",
    license="Apache 2.0",
    author="Julian Zucker",
    author_email="julian.zucker@gmail.com",
    description="Social Choice Theory in Python",
)
