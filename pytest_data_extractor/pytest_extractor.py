from .data_containers import TestData
from .output_generators import SessionOutputGenerator
import pytest
import inspect
from typing import (
    List,
    TypeVar,
    Optional
)

TestInput = TypeVar("TestInput")


class Storage:
    data: List[TestData] = []


@pytest.fixture
def session_output_dir():
    return None


@pytest.fixture
def session_temp_dir():
    return None


@pytest.fixture(scope='function', autouse=True)
def update_session_output_dir(session_output_dir: Optional[str]) -> None:
    """
    This fixture changes SessionOutputGenerator output file folder path
    To use it create in a conftest.py a fixture with the name session_output_dir
    :param output_dir: new output dir
    :return: None
    """
    if session_output_dir is not None:
        SessionOutputGenerator.DEFAULT_OUTPUT = session_output_dir


@pytest.fixture(scope='function', autouse=True)
def update_session_temp_dir(session_temp_dir: Optional[str]) -> None:
    """
    This fixture changes SessionOutputGenerator temp file folder path.
    To use it create in a conftest.py a fixture with the name session_temp_dir
    :param output_dir: new output dir
    :return: None
    """
    if session_temp_dir is not None:
        SessionOutputGenerator.DEFAULT_TEMP = session_temp_dir


@pytest.hookimpl(tryfirst=True)
def pytest_assertrepr_compare(op, left, right):
    if len(Storage.data) and Storage.data[-1].test_operator is None:
        if Storage.data[-1].actual_result is None:
            Storage.data[-1].actual_result = left
        if Storage.data[-1].expected_result is None:
            Storage.data[-1].expected_result = right
        Storage.data[-1].test_operator = op
        # Storage.data[-1].func_args = func_args
    else:
        test_data = TestData(actual_result=left, expected_result=right, test_operator=op)  # func_args=func_args)
        Storage.data.append(test_data)


@pytest.hookimpl
def pytest_assertion_pass():
    Storage.data[-1].test_status = 1


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish():
    session_obj = SessionOutputGenerator(data=Storage.data)
    session_obj.output_json()


@pytest.fixture(scope="function")
def upload_manager():
    def manager(var_value: TestInput,
                expected_result: Optional[TestInput] = None,
                actual_result: Optional[TestInput] = None) -> TestInput:
        test_data = TestData(test_input=var_value,
                             expected_result=expected_result,
                             actual_result=actual_result,
                             test_func=inspect.stack()[1][3])
        Storage.data.append(test_data)
        return var_value

    return manager


@pytest.hookimpl
def pytest_report_teststatus(report):
    if report.when == "call" and report.skipped:
        Storage.data[-1].test_status = -1  # Test was skipped

    # manage times
    if report.when == "call":
        Storage.data[-1].test_duration = report.duration


@pytest.hookimpl
def pytest_runtest_protocol(item):
    # global func_args
    if hasattr(item, "function") and hasattr(item, "funcargs"):
        # func_args = item.funcargs
        test_data = TestData(test_func=item.function.__name__)  # func_args=func_args
    if len(Storage.data) > 0:
        if Storage.data[-1].test_func is None:
            Storage.data[-1].test_func = test_data.test_func
            # Storage.data[-1].func_args = test_data.test_input
        else:
            Storage.data.append(test_data)
    else:
        Storage.data.append(test_data)
