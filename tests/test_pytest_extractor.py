import pandas as pd


def test_demo_1(upload_manager):
    my_val = upload_manager(15)
    assert my_val == 15, "assertion is incorrect"


def test_dataframe(upload_manager):
    df_dict = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [1, 1, 1]}
    df = upload_manager(pd.DataFrame(df_dict))
    assert isinstance(df, pd.DataFrame)


def test_boolean(upload_manager):
    my_val = upload_manager(1 == 1)
    assert my_val


def test_full_upload_manager(upload_manager):
    my_val = upload_manager(12,
                            expected=144,
                            actual=12 ** 2)
    assert my_val ** 2 == 144, "assertion failed"
