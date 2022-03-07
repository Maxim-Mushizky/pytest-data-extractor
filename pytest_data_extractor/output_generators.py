from typing import (
    Optional,
    List,
    TypeVar
)
from dataclasses import dataclass
import dataclasses
import os
import pandas as pd
import json
import datetime

TestInput = TypeVar("TestInput")


def _mkdir_if_none_exists(dirname: str) -> None:
    """
    Generate a directory if one doesn't exist in the given path.
    :param dirname: Full or relative path to the requested directory
    :return:
    """
    if not os.path.exists(dirname):
        os.mkdir(dirname)


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
                       cache_file_extensions: str = 'json') -> "SuiteDataOutputGenerator":
        """
        Output the test suite data into a json file.
        If object cannot be serialized it will be cached locally and the relative path to it will be stored instead.
        :param file_prefix: Prefix of output json
        :param cache_file_extensions: Extension of the cached files
        :return: the original object
        """
        if file_prefix is None:
            file_prefix = self.FILE_PREFIX

        storage_as_dict = []
        for test_data in self.data:
            test_data = self._get_test_data_as_serializable(test_data=test_data,
                                                            cache_file_extensions=cache_file_extensions)
            if test_data is not None:
                storage_as_dict.append(dataclasses.asdict(test_data))
        _mkdir_if_none_exists(self.OUTPUT_DIR)
        _path = self._get_indexed_output_paths(self.OUTPUT_DIR, file_prefix)
        with open(_path, "w") as f:
            json.dump(storage_as_dict, f, indent=4)

        return self

    def _get_test_data_as_serializable(self, test_data: TestInput,
                                       cache_file_extensions: str) -> Optional[TestInput]:
        """
        Make sure that all the test data can be stored in a text based format (json, csv and etc).
        If the data of specific large types it will store it as cache and will store as input the path to it.
        Will also return nothing is the data doesn't add anything to final output file (empty tests).
        :param test_data: dataclass containing all fields given in data containers
        :param cache_file_extensions: File extension of the cache data
        :return: serializable dataclass or None
        """
        if test_data.expected_result is None and test_data.actual_result is None and test_data.test_input is None:
            return None
        if isinstance(test_data.test_input, pd.DataFrame):
            fpath = ObjectSerializer(to=self.CACHE_FILES_DIR).get_pandas_filename(data=test_data.test_input,
                                                                                  f_ext=cache_file_extensions,
                                                                                  time_format=self._TIME_FORMAT)
            test_data.test_input = fpath  # pass the full filename path as test input

        return test_data

    def _get_indexed_output_paths(self, dirname: str, file_prefix: str, f_ext: Optional[str] = None) -> str:
        """
        Generate indexed output files in the desired directory
        :param dirname: Relative or full path to desired directory
        :param file_prefix: Prefix of the used files
        :param f_ext: File extension of the generated files
        :return: The relative path to the new generated file
        """
        max_index = 0
        if f_ext is None:
            f_ext = 'json'
        for f in os.listdir(dirname):
            if f.endswith(f_ext) and f.startswith(file_prefix):
                output_file_index = f.replace(file_prefix, "").replace(f".{f_ext}", "")
                try:
                    output_file_index = int(output_file_index)
                    if output_file_index > max_index:
                        max_index = output_file_index
                except ValueError:
                    pass
        filename = f"{file_prefix}{max_index + 1}.{f_ext}"
        return os.path.join(dirname, filename)


class ObjectSerializer:

    def __init__(self, to: str, filename: Optional[str] = None) -> None:
        self._dirname = to
        if filename is None:
            filename = ''  # reset as an empty string
        self._filename = filename

    def get_pandas_filename(self, data: pd.DataFrame,
                            time_format: str,
                            f_ext: str) -> str:
        """
        Generate and get cache file using a pandas dataframe object.
        :param data: Pandas DataFrame to be serialized
        :param dirname: Directory to save the serialized data
        :param filename: Default to None
        :param f_ext: Extension of the file, will determine what serialization method to use
        :return:
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f"This method is intended only for pandas dataframe objects. The data given is of type {type(data)}")

        generated_file_path = self._get_generated_cache_file_path(time_format=time_format,
                                                                  f_ext=f_ext)

        # cases for filetypes
        if f_ext == 'json':
            data.to_json(path_or_buf=generated_file_path,
                         orient='records',
                         indent=4)
        elif f_ext == 'csv':
            data.to_csv(path_or_buf=generated_file_path)
        else:
            raise Exception(f"Cannot handle given file extension {f_ext}")

        return generated_file_path

    def _get_generated_cache_file_path(self, time_format: str, f_ext: str) -> str:
        _mkdir_if_none_exists(self._dirname)
        now = datetime.datetime.now().strftime(time_format)
        self._filename += "_" + now
        return f"{os.path.join(self._dirname, self._filename)}.{f_ext}"
