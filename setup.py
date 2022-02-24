# sample ./setup.py file
# from setuptools import setup, find_packages
# from pkg_resources import parse_requirements
# import pathlib
# import codecs
# import os 


# with pathlib.Path("requirements.txt").open() as req_txt:
#     install_req = [str(req) for req in parse_requirements(req_txt)]

# def read(fname):
#     file_path = os.path.join(os.path.dirname(__file__), fname)
#     return codecs.open(file_path, encoding='utf-8').read()


# setup(
#     name="pytest_data_extractor",
#     version= '0.1.0',
#     description = 'A pytest plugin to extract relevant metadata about tests into an external file (currently only json support)',
#     author= 'Maxim Mushizky',
#     author_email= 'maximmu87@gmail.com',
#     license='MIT',
#     package_dir='src',
#     packages=['data_extractor'],
#     # the following makes a plugin available to pytest
#     entry_points={"pytest11": ["pytest_data_extractor = data_extractor.pytest_extractor"]},
#     long_description=read('README.md'),
#     python_requires='>=3.7',
#     install_requires=install_req,
#     # custom PyPI classifier for pytest plugins
#     classifiers=["Framework :: Pytest"]
# )
import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest_data_extractor',
    version='0.1.0',
    author='Maxim Mushizky',
    author_email='maximmu87@gmail.com',
    maintainer='Maxim Mushizky',
    maintainer_email='marszaripov@gmail.com',
    license='MIT',
    description = 'A pytest plugin to extract relevant metadata about tests into an external file (currently only json support)',
    long_description=read('README.md'),
    packages=['src.data_extractor'],
    install_requires=['pytest>=7.0.1'],
    classifiers=[
        'Framework :: Pytest'
    ],
    # entry_points={
    #     'pytest11': [
    #         'data-extractor = src.data_extractors.pytest_extractor',
    #     ],
    # },
)

