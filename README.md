# pytest-data-extractor ![example workflow](https://github.com/Maxim-Mushizky/pytest-data-extractor/actions/workflows/python-app.yml/badge.svg) [![PyPI version](https://badge.fury.io/py/pytest-data-extractor.svg)](https://badge.fury.io/py/pytest-data-extractor)

Pytest plugin intended for extracting test data and metadata and serializing it into a file. 
The plugin currently support json files.

This is a completely open source project so everyone are more than welcome to join and extended it.

## Version 0.1.7
# Use case

pip install the package to your project's virtual environment. Directly from plugin folder:

```bash
pip install -e .
```

or pip install it from Pypi:
```bash
pip install pytest-data-extractor
```

Go to a test file and now simply add upload_manager fixture in order to save a variable (except callable), Like so:

```python
# test_foo.py

def test_bar(upload_manager):
    expected_value = upload_manager(1000)
    assert expected_value == 1000, "assert failed"
```

Activate the plugin with the pytest cli with the command:

```bash
pytest --output_test_data True
```

Now the data passed to upload_manager, as well as the test data that is specified at the TestData container will be
stored in an external file. For a json file output:

```json
[
  {
        "test_input": [
            {
                "test_file_path": "_20220719_21_00_10_806534.csv",
                "file_type": "csv"
            }
        ],
        "expected_result": null,
        "actual_result": null,
        "test_operator": null,
        "test_func": "test_bar",
        "test_status": 1,
        "test_duration": 0.046707000000000054,
        "meta_data": null
    }
]

```
In version 0.1.7 there's no recording of the expected_result, actual_result and test_operator since the test result is a PASS.
Additionally, all objects passed to the upload_manager fixture will be saved as an external file that will be associated by test_file_path param.
<b>There's no garbage collection so be mindful how and where the files are stored.

## Miscellaneous

For order sakes, the plugin will use a test comparison convention of:

    * left- actual result.
    * right- expected result.

## conftest.py hooks and fixtures

In order to change the folder for either cache or output files, use conftest.py with the correct fixtures. example:

```python
# conftest.py
import pytest


@pytest.fixture
def suite_output_dir():
    return "my_files.output"


@pytest.fixture
def suite_cache_dir():
    return "my_files.temp"

@pytest.fixture
def suite_output_file_prefix():
    return "my_special_prefix"

```

## Enumeration
By default there are 3 values for the test values in the data_containers.py file:
```python
class TestStatus(Enum):
    Skip = -1
    Fail = 0
    Pass = 1

```

The default directories will be at the root where the pytest is called.
Supports automatic pipeline