from typing import (
    Optional,
    List
)
from dataclasses import dataclass
import dataclasses
import os
import pandas as pd
import json
import datetime


class SessionOutputGenerator:
    __DEFAULT_TEMP = "extractor_files.temp"
    __DEFAULT_OUTPUT = "extractor_files.output"
    __DEFAULT_FILE_PREFIX = "output_data_"
    __TIME_FORMAT = "%Y%m%d_%H_%M_%S_%f"

    def __init__(
            self,
            output_dir: Optional[str] = None,
            temp_dir: Optional[str] = None,
            data: Optional[dataclass] = None,
    ) -> None:
        if output_dir is None:
            output_dir = self.__DEFAULT_OUTPUT
        if temp_dir is None:
            temp_dir = self.__DEFAULT_TEMP
        self._output_dir = output_dir
        self._temp_dir = temp_dir
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

    def output_json(self, file_prefix: Optional[str] = None,
                    temp_dir_extensions: Optional[str] = None) -> "SessionOutputGenerator":
        if file_prefix is None:
            file_prefix = self.__DEFAULT_FILE_PREFIX
        if temp_dir_extensions is None:
            temp_dir_extensions = 'json'

        storage_as_dict = []
        for d in self.data:
            if d.expected is None and d.actual is None and d.test_input is None:
                continue  # Drop from the finished file all irrelevant calls for the upload_manager fixture
            if isinstance(d.test_input, pd.DataFrame):
                fpath = DirDataSerializer(dirname=self._temp_dir).get_pandas_filename(data=d.test_input,
                                                                                      f_ext=temp_dir_extensions,
                                                                                      time_format=self.__TIME_FORMAT)
                d.test_input = fpath  # pass the full filename path as test input

            storage_as_dict.append(dataclasses.asdict(d))
        self.__mkdir_if_none_exists(self._output_dir)
        _path = self._get_output_full_path_in_dir(self._output_dir, file_prefix)
        with open(_path, "w") as f:
            json.dump(storage_as_dict, f, indent=4)

        return self

    def __mkdir_if_none_exists(self, dirname: str) -> None:
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def _get_output_full_path_in_dir(self, dirname: str, file_prefix: str, f_ext: Optional[str] = None) -> str:
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


class DirDataSerializer:

    def __init__(self, dirname: str, filename: Optional[str] = None) -> None:
        self._dirname = dirname
        if filename is None:
            filename = ''  # reset as an empty string
        self._filename = filename

    def get_pandas_filename(self, data: pd.DataFrame,
                            time_format: str,
                            f_ext: str) -> str:
        """
        Protect method:
            Create and get file using a pandas dataframe object.
        :param data: Pandas DataFrame to be serialized
        :param dirname: Directory to save the serialized data
        :param filename: Default to None
        :param f_ext: Extension of the file, will determine what serialization method to use
        :return:
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f"This method is intended only for pandas dataframe objects. The data given is of type {type(data)}")

        self.__mkdir_if_none_exists(self._dirname)
        now = datetime.datetime.now().strftime(time_format)
        self._filename += "_" + now
        full_filename_path = f"{os.path.join(self._dirname, self._filename)}.{f_ext}"

        # cases for filetypes
        if f_ext == 'json':
            data.to_json(path_or_buf=full_filename_path,
                         orient='records',
                         indent=4)
        elif f_ext == 'csv':
            data.to_csv(path_or_buf=full_filename_path)
        else:
            raise Exception(f"Cannot handle given file extension {f_ext}")

        return full_filename_path

    def __mkdir_if_none_exists(self, dirname: str) -> None:
        if not os.path.exists(dirname):
            os.mkdir(dirname)
