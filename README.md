# pytest-data-extractor
Pytest plugin intended for extracting metadata about the test 

## Version 0.1.1 (Temporary version, the guide will change) usage

1. pip install the package to the your project's virtual environment. Directly from plugin folder:

```bash
~/pytest-data-extractor$ pip install -e .
```

2. Go to a test file and now simply add upload_manager fixture in order to save a variable (except callables), Like so:

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
        "expected": 1000,
        "actual": 1000,
        "operator": "==",
        "test_func": "test_bar",
        "test_status": 1,
        "call_duration": 0.010749192908406258,
    }
]

```
5. The test comparison itself will be stored with a convention of:
    * left- actual result.
    * right- expected result.

6. The data will be stored in a json file in a path specified by the _PATH variable in pytest_extractor.