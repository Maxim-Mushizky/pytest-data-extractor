from .data_containers import TestData
import pytest
import dataclasses
import inspect
import json

from typing import List, Callable, TypeVar

TestInput = TypeVar("TestInput")


class Storage:
    data: List[TestData] = []


_PATH = "test_data.json"


@pytest.hookimpl(tryfirst=True)
def pytest_assertrepr_compare(op, left, right):
    if len(Storage.data) and Storage.data[-1].operator is None:
        Storage.data[-1].actual = left
        Storage.data[-1].expected = right
        Storage.data[-1].operator = op
        Storage.data[-1].func_args = func_args
    else:
        test_data = TestData(
            actual=left, expected=right, operator=op, func_args=func_args
        )
        Storage.data.append(test_data)


@pytest.hookimpl
def pytest_assertion_pass():
    Storage.data[-1].test_status = 1


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish():
    storage_as_dict = []

    for data in Storage.data:
        if data.expected is None and data.actual is None and data.test_input is None:
            continue  # Drop from the finished file all irrelevant calls for the upload_manager fixture
        if isinstance(data.func_args, dict):
            for ik, iv in data.func_args.items():
                if isinstance(iv, Callable):
                    data.func_args[ik] = "function"
        storage_as_dict.append(dataclasses.asdict(data))
    with open(_PATH, "w") as f:
        json.dump(storage_as_dict, f, indent=4)


@pytest.fixture(scope="function")
def upload_manager():
    def manager(var_value: TestInput) -> TestInput:
        test_data = TestData(test_input=var_value, test_func=inspect.stack()[1][3])
        Storage.data.append(test_data)
        return var_value

    return manager


@pytest.hookimpl
def pytest_report_teststatus(report):
    if report.when == "call" and report.skipped:
        Storage.data[-1].test_status = -1  # Test was skipped

    if report.when == "setup":
        Storage.data[-1].setup_duration = report.duration
    elif report.when == "call":
        Storage.data[-1].call_duration = report.duration


@pytest.hookimpl
def pytest_runtest_protocol(item):
    global func_args
    if hasattr(item, "function") and hasattr(item, "funcargs"):
        func_args = item.funcargs
        test_data = TestData(test_func=item.function.__name__, func_args=func_args)
    if len(Storage.data) > 0:
        if Storage.data[-1].test_func is None:
            Storage.data[-1].test_func = test_data.test_func
            Storage.data[-1].func_args = test_data.test_input
        else:
            Storage.data.append(test_data)
    else:
        Storage.data.append(test_data)
