# pytest-data-extractor
Pytest plugin intended for extracting metadata about the test 

## Version 0.1.0 (Temporary version, the guide will change) usage


1. Go to conftest.py file (no matter what level) and import the entirety of the pytest_extractor file in the following way:

```python
from src.test_data_extractor.pytest_extractor import *
```
Alternativly, the data_extractor folder can be placed anywhere in an external project, so the import will change accoridngly.
The important thing is both files need to be present in the same folder, so if you place the files in the folder called infra, the import will be:

```python
from infra.test_data_extractor.pytest_extractor import *
```

2. In the data_containers file you can add additional containers for the test data.
3. Go to a test file and now simply add upload_manager fixture in order to save a variable (except callables), Like so:

```python
# test_foo.py

def test_bar(upload_manager):
    to_compare = upload_manager(1000)
    assert to_compare == to_compare, "assert failed"
```

4. The data will be now stored for the test_name 'test_bar' with the following parameters:
```json
[
    {
        "test_input": 1000,
        "func_args": {
            "upload_manager": "function"
        },
        "expected": 1000,
        "actual": 1000,
        "operator": "==",
        "test_func": "test_bar",
        "test_status": 1,
        "call_duration": 0.010749192908406258,
        "setup_duration": 0.0
    }
]

```
5. The test comparison itself will be stored with a convention of:
    * left- actual result.
    * right- expected result.

6. The data will be stored in a json file in a path specified by the _PATH variable in pytest_extractor.