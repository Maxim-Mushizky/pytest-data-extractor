def test_data_extractor_functionality(upload_manager):
    my_list = upload_manager([1,2,3])
    assert isinstance(my_list,list)
