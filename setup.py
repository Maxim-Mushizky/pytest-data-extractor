# sample ./setup.py file
from setuptools import setup

setup(
    name="pytest_data_extractor",
    version= '0.1.0',
    description = 'A pytest plugin to extract relevant metadata about tests into an external file (currently only json support)',
    author= 'Maxim Mushizky',
    author_email= 'maximmu87@gmail.com',
    license='MIT',
    packages=["src"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["pytest_data_extractor = test_data_extractor.pytest_extractor"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)