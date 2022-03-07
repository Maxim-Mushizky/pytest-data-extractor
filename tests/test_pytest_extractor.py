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
    my_val = upload_manager(var_value=12,
                            expected_result=144,
                            actual_result=12 ** 2)
    assert my_val ** 2 == 144, "assertion failed"


def test_try_and_skip():
    pytest.skip("Skipping check")


def test_try_and_raise_exception(upload_manager):
    dummy_var = upload_manager([1])
    raise Exception("Raising check exception")


def test_boolean_true(upload_manager):
    my_bool = upload_manager(True)
    assert my_bool

def test_boolean_false(upload_manager):
    my_bool = upload_manager(False)
    assert my_bool
