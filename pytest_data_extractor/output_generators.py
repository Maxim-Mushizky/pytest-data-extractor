from typing import (
    Optional,
    List,
    Any,
    Sequence,
    Dict
)
from dataclasses import dataclass
import os
from pathlib import Path
import pandas as pd
import json

from pytest_data_extractor import utils
import pytest_data_extractor.data_containers as dc
import pytest_data_extractor.data_storers as ds


def get_cached_test_input_data(single_input: Any,
                               cache_files_dir: str,
                               cache_dir_file_extensions: str = 'csv') -> dc.TestInput:
    if isinstance(single_input, (str, Path)):
        if os.path.exists(single_input):
            return dc.TestInput(
                test_file_path=single_input,
                file_type=os.path.splitext(single_input)[1][1:]  # ignore . before file extension
            )
    elif isinstance(single_input, pd.DataFrame):
        return dc.TestInput(
            test_file_path=ds.DataFrameStore(
                data=single_input,
                to=cache_files_dir).generate_file(f_ext=cache_dir_file_extensions, file_name_only=True)
        )
    elif isinstance(single_input, Sequence):
        return dc.TestInput(
            test_file_path=ds.ArrayStore(data=single_input,
                                         to=cache_files_dir).generate_file(f_ext=cache_dir_file_extensions,
                                                                           file_name_only=True)
        )
    return dc.TestInput(
        test_file_path=ds.AnyValueStore(data=single_input,
                                        to=cache_files_dir).generate_file(f_ext='csv',
                                                                          file_name_only=True)
    )


class SuiteDataOutputGenerator:
    CACHE_FILES_DIR = "extractor_files.temp"
    OUTPUT_DIR = "extractor_files.output"
    FILE_PREFIX = "output_data_"
    _TIME_FORMAT = "%Y%m%d_%H_%M_%S_%f"

    def __init__(self, data: Optional[dataclass] = None) -> None:
        self._data = data

    @property
    def data(self) -> dataclass:
        return self._data

    @data.setter
    def data(self, new_data: List) -> None:
        if isinstance(new_data, list):
            self._data = new_data
        else:
            print(f"Wrong data type, dataclass is required but instead was fed {type(new_data)}")

    def output_to_json(self, file_prefix: Optional[str] = None,
                       cache_dir_extension: str = 'json') -> "SuiteDataOutputGenerator":
        """
        Output the test suite data into a json file.
        If object cannot be serialized it will be cached locally and the relative path to it will be stored instead.
        :param file_prefix: Prefix of output json
        :param cache_file_extensions: Extension of the cached files
        :return: the original object
        """
        if file_prefix is None:
            file_prefix = self.FILE_PREFIX

        dump_stage = self._get_dumping_data(cache_dir_extension=cache_dir_extension)
        utils.mkdir_if_none_exists(self.OUTPUT_DIR)
        with open(self.output_path(file_prefix=file_prefix), "w") as f:
            json.dump(dump_stage, f, indent=4)

        return self

    def output_path(self, file_prefix: str) -> str:
        return utils.get_output_full_path_in_dir(self.OUTPUT_DIR, file_prefix)

    def _get_dumping_data(self, cache_dir_extension: str) -> List[Dict]:
        dumping_data = []
        for test_doc in self._data:
            test_doc.test_input = [get_cached_test_input_data(
                single_input=single_input,
                cache_files_dir=self.CACHE_FILES_DIR,
                cache_dir_file_extensions=cache_dir_extension
            ) for single_input in test_doc.test_input]
            if test_doc is not None:
                dumping_data.append(utils.dataclass_to_dict(data=test_doc))
        return dumping_data
