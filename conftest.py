import pytest

@pytest.fixture
def suite_output_dir():
    return "custom_output"


@pytest.fixture
def suite_cache_dir():
    return "custom_cache"


@pytest.fixture
def suite_output_file_prefix():
    return "random_check_prefix_output"