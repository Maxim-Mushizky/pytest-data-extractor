from .data_containers import TestData, TestStatus
from .output_generators import SuiteDataOutputGenerator
import pytest
import inspect
from typing import (
    List,
    TypeVar,
    Optional,
    Iterable
)

from pytest_data_extractor import utils

TestInput = TypeVar("TestInput")


class Cache:
    # Cache data
    activate: bool = False  # activate plugin
    _data: List[TestData] = []

    @utils.ClassProperty
    def data(cls):
        if cls.activate:
            return cls._data
        return [TestData]  # So will not crash


# User editable fixtures
def pytest_addoption(parser):
    parser.addoption('--output_test_data', action='store', default=False, type=bool)


@pytest.fixture(autouse=True)
def activate_plugin(request) -> None:
    Cache.activate = request.config.getoption('--output_test_data')


@pytest.fixture
def suite_output_dir() -> None:
    return None


@pytest.fixture
def suite_cache_dir() -> None:
    return None


@pytest.fixture
def suite_output_file_prefix() -> None:
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
def pytest_assertrepr_compare(config, op, left, right) -> None:
    test_func = ""
    if hasattr(config, '_teamcityReporting'):
        test_func = list(config._teamcityReporting.test_start_reported_mark)[0].split(".")[-1]
    if len(Cache.data) and Cache.data[-1].test_status is None or Cache.data[-1].test_func == test_func:
        if Cache.data[-1].actual_result is None:
            Cache.data[-1].actual_result = left
        if Cache.data[-1].expected_result is None:
            Cache.data[-1].expected_result = right
        Cache.data[-1].test_operator = op
    if (len(Cache.data) == 0) or len(Cache.data) > 0 and Cache.data[-1].test_func not in test_func:
        test_data = TestData(
            actual_result=left,
            expected_result=right,
            test_operator=op,
            test_func=test_func
        )
        Cache.data.append(test_data)


@pytest.hookimpl(trylast=True)
def pytest_assertion_pass():
    Cache.data[-1].expected_result = None
    Cache.data[-1].actual_result = None
    Cache.data[-1].test_operator = None
    Cache.data[-1].test_status = TestStatus.Pass.value


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish():
    if Cache.activate is True:  # output only if requested
        SuiteDataOutputGenerator(data=Cache.data).output_to_json()


@pytest.fixture(scope="function")
def upload_manager():
    def manager(test_input: TestInput,
                expected_result: Optional[TestInput] = None,
                actual_result: Optional[TestInput] = None) -> TestInput:
        test_func = inspect.stack()[1][3]
        if len(Cache.data) == 0 or (len(Cache.data) > 0 or Cache.data[-1].test_func != test_func):
            test_data = TestData(test_input=test_input if isinstance(test_input, Iterable) else [test_input],
                                 expected_result=expected_result,
                                 actual_result=actual_result,
                                 test_func=test_func)
            Cache.data.append(test_data)
        elif len(Cache.data) > 0 and Cache.data[-1].test_func == test_func:
            Cache.data[-1].test_inputs.append(test_input)
        return test_input

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

    if report.when == "call":
        current_test_func = report.nodeid.split("::")[-1]
        if len(Cache.data) > 0 and Cache.data[-1].test_func != current_test_func:
            Cache.data[-1].test_func = current_test_func
        Cache.data[-1].test_duration = report.duration
        if Cache.data[-1].test_func is None:
            Cache.data[-1].test_func = report.head_line


@pytest.hookimpl(trylast=True)
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
    current_test_func = report.nodeid.split("::")[-1]
    if hasattr(report, 'failed') and report.failed is True:
        if len(Cache.data) > 0 and Cache.data[-1].test_func == current_test_func:
            if Cache.data[-1].test_operator is None:
                Cache.data[-1].actual_result = False
                Cache.data[-1].expected_result = True
            elif len(Cache.data) > 0 and Cache.data[-1].test_func != current_test_func:
                test_data = TestData(
                    test_input=[],
                    expected_result=True,
                    actual_result=True,
                    test_func=current_test_func
                )
                Cache.data.append(test_data)
    Cache.data[-1].test_status = TestStatus.Fail.value
