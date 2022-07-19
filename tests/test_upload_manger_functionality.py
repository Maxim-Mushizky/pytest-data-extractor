import pandas as pd
import numpy as np
import pytest


def test_demo_1(upload_manager):
    my_val = upload_manager(15)
    assert my_val == 15, "assertion is incorrect"


def test_dataframe1(upload_manager):
    # create simple dataframe using a dictionary
    df_dict = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [1, 1, 1]}
    df = upload_manager(pd.DataFrame(df_dict))
    assert isinstance(df, pd.DataFrame)


def test_dataframe2(upload_manager):
    # create a large dataframe
    df = upload_manager(pd.DataFrame(np.random.randint(0, 100, size=(10000, 4)), columns=list('ABCD')))
    assert isinstance(df, pd.DataFrame)


def test_boolean(upload_manager):
    my_val = upload_manager(1 == 1)
    assert my_val


def test_full_upload_manager(upload_manager):
    my_val = upload_manager(test_input=12,
                            expected_result=144,
                            actual_result=12 ** 2)
    assert my_val ** 2 == 144, "assertion failed"


def test_try_and_skip(upload_manager):
    foo = upload_manager("foo")
    pytest.skip("Skipping check")


def test_try_and_raise_exception(upload_manager):
    dummy_var = upload_manager([1])
    with pytest.raises(Exception):
        raise Exception("Raising check exception")


def test_boolean_true(upload_manager):
    my_bool = upload_manager(True)
    assert my_bool


def test_boolean_false(upload_manager):
    my_bool = upload_manager(False)
    assert not my_bool


@pytest.mark.parametrize('x', list(range(10)))
def test_with_parametrize(x, upload_manager):
    tested_val = upload_manager(x)
    assert isinstance(tested_val, int)
    assert tested_val >= 0

# Commented out for passing the pipeline automatic tests
# def test_intentional_failure(upload_manager):
#     my_num: float = upload_manager(1e6)
#     assert 1e6 == 1e6
#     assert 1e6 == 1e6+1e1
#

