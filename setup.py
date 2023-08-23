from setuptools import find_packages, setup

setup(
    name="classifai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["autochat==0.1.3"],
    author="Benjamin Derville",
    author_email="benderville@gmail.com",
    description="A small ChatGPT wrapper to label data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benderv/classifai",
)
