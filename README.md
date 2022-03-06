# pytest-data-extractor

Pytest plugin intended for extracting metadata about the test

## Version 0.1.3

pip install the package to the your project's virtual environment. Directly from plugin folder:

```bash
~/pytest-data-extractor$ pip install -e .
```

Go to a test file and now simply add upload_manager fixture in order to save a variable (except callable), Like so:

```python
# test_foo.py

def test_bar(upload_manager):
    to_compare = upload_manager(1000)
    assert to_compare == to_compare, "assert failed"
```

Run the test suite as per usual. The data passed to upload_manager, 
as well as the test data that is specified at the TestData container will be stored in an external file.
For a json file output:

```json
[
  {
    "test_input": 1000,
    "expected": 1000,
    "actual": 1000,
    "operator": "==",
    "test_func": "test_bar",
    "test_status": 1,
    "call_duration": 0.010749192908406258
  }
]

```
## Miscellaneous 
For order sakes, the plugin will use a test comparison convention of:
    * left- actual result.
    * right- expected result.

## conftest.py hooks and fixtures

In order to change the folder for either temporary or output files use conftest.py with the correct fixtures. example:

```python
# conftest.py
import pytest


@pytest.fixture
def session_output_dir():
    return "my_files.output"


@pytest.fixture
def session_temp_dir():
    return "my_files.temp"

```

The default directories will be at the root where the pytest is called.