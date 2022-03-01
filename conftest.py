import pytest

@pytest.fixture(scope = 'session')
def session_output_dir():
    return "extractor_files_maxim.output"