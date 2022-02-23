

def test_demo_1(upload_manager):
    my_val = upload_manager(15)
    assert my_val == 15, "assertion is incorrect"