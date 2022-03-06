import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest_data_extractor",
    version="0.1.3",
    author="Maxim Mushizky",
    author_email="maximmu87@gmail.com",
    maintainer="Maxim Mushizky",
    license="MIT",
    description="A pytest plugin to extract relevant metadata about tests into an external file (currently only json support)",
    long_description=read("README.md"),
    install_requires=[
        "pytest>=7.0.1",
        "pandas>=1.3.5"
    ],
    classifiers=[
        "Framework :: Pytest",
        "Licence :: MIT",
        "Operating System :: Multi-platform",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "pytest11": [
            "name_of_plugin = pytest_data_extractor.pytest_extractor",
        ],
    },
    packages=["pytest_data_extractor"],
)
