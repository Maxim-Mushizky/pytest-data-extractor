from .data_containers import TestData, TestStatus
from .output_generators import SuiteDataOutputGenerator
import pytest
import inspect
from typing import (
    List,
    TypeVar,
    Optional
)

TestInput = TypeVar("TestInput")


class ClassProperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class Cache:
    # Cache data
    _activate: bool = False  # activate plugin
    _data: List[TestData] = []

    @ClassProperty
    def data(cls):
        if cls._activate:
            return cls._data
        return [TestData]  # So will not crash


##### User editable fixtures #####
def pytest_addoption(parser):
    parser.addoption('--output_test_data', action='store', default=False, type=bool)


@pytest.fixture(autouse=True)
def activate_plugin(request) -> None:
    Cache._activate = request.config.getoption('--output_test_data')


@pytest.fixture
def suite_output_dir():
    return None


@pytest.fixture
def suite_cache_dir():
    return None


@pytest.fixture
def suite_output_file_prefix():
    return None


@pytest.fixture(autouse=True)
def update_suite_output_dir(suite_output_dir) -> None:
    """
    This fixture changes SuiteDataOutputGenerator output file folder path
    To use it create in a conftest.py a fixture with the name suite_output_dir
    :param output_dir: new output dir
    :return: None
    """
    if suite_output_dir is not None:
        SuiteDataOutputGenerator.OUTPUT_DIR = suite_output_dir


@pytest.fixture(autouse=True)
def update_suite_temp_dir(suite_cache_dir) -> None:
    """
    This fixture changes SuiteDataOutputGenerator cache file folder path.
    To use it create in a conftest.py a fixture with the name suite_cache_dir
    :param suite_cache_dir: Relative of absolute path to the cache directory
    :return: None
    """
    if suite_cache_dir is not None:
        SuiteDataOutputGenerator.CACHE_FILES_DIR = suite_cache_dir


@pytest.fixture(autouse=True)
def update_suite_output_file_prefix(suite_output_file_prefix: Optional[str]) -> None:
    """
    This fixture changes SuiteDataOutputGenerator file prefix.
    To use it create in a conftest.py a fixture with the name suite_output_file_prefix
    :param suite_output_file_prefix: prefix of the output files
    :return: None
    """
    if suite_output_file_prefix is not None:
        SuiteDataOutputGenerator.FILE_PREFIX = suite_output_file_prefix


@pytest.hookimpl(tryfirst=True)
def pytest_assertrepr_compare(op, left, right):
    if len(Cache.data) and Cache.data[-1].test_status is None:
        if Cache.data[-1].actual_result is None:
            Cache.data[-1].actual_result = left
        if Cache.data[-1].expected_result is None:
            Cache.data[-1].expected_result = right
        Cache.data[-1].test_operator = op
        # Storage.data[-1].func_args = func_args
    else:
        test_data = TestData(actual_result=left, expected_result=right, test_operator=op)  # func_args=func_args)
        Cache.data.append(test_data)


##### Main #####
@pytest.hookimpl
def pytest_assertion_pass():
    if Cache.data[-1].expected_result is None and Cache.data[-1].actual_result is None:
        Cache.data[-1].expected_result = True
        Cache.data[-1].actual_result = True
    Cache.data[-1].test_status = TestStatus.Pass.value


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish():
    if Cache._activate is True:  # output only if requested
        SuiteDataOutputGenerator(data=Cache.data).output_to_json()


@pytest.fixture(scope="function")
def upload_manager():
    def manager(var_value: TestInput,
                expected_result: Optional[TestInput] = None,
                actual_result: Optional[TestInput] = None) -> TestInput:
        test_data = TestData(test_input=var_value,
                             expected_result=expected_result,
                             actual_result=actual_result,
                             test_func=inspect.stack()[1][3])
        Cache.data.append(test_data)
        return var_value

    return manager


@pytest.hookimpl
def pytest_report_teststatus(report):
    if report.when == "call" and report.skipped:
        Cache.data[-1].test_status = TestStatus.Skip.value
    elif report.when == "call" and not report.skipped:
        if report.passed:
            Cache.data[-1].test_status = TestStatus.Pass.value
        else:
            Cache.data[-1].test_status = TestStatus.Fail.value

        # manage times
    if report.when == "call":
        Cache.data[-1].test_duration = report.duration


@pytest.hookimpl
def pytest_runtest_protocol(item):
    # global func_args
    if hasattr(item, "function") and hasattr(item, "funcargs"):
        # func_args = item.funcargs
        test_data = TestData(test_func=item.function.__name__)  # func_args=func_args
        if len(Cache.data) > 0:
            if Cache.data[-1].test_func is None:
                Cache.data[-1].test_func = test_data.test_func
                # Storage.data[-1].func_args = test_data.test_input
            else:
                Cache.data.append(test_data)
        else:
            Cache.data.append(test_data)


@pytest.hookimpl(trylast=True)
def pytest_exception_interact(call, report):
    if hasattr(report, 'failed') and report.failed is True:
        if Cache.data[-1].test_operator is None:
            Cache.data[-1].actual_result = False
            Cache.data[-1].expected_result = True
        Cache.data[-1].test_status = TestStatus.Fail.value
