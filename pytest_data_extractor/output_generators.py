from typing import (
    Optional,
    List,
    Callable
)
from dataclasses import dataclass
import dataclasses
import os
import pandas as pd
import json


class SessionOutputGenerator:
    __DEFAULT_TEMP = "extractor_files.temp"
    __DEFAULT_OUTPUT = "extractor_files.output"
    __DEFAULT_FILE_PREFIX = "output_data_"
    __TIME_FORMAT = "%Y%m%d_%H_%M_%S"

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
        self.output_dir = output_dir
        self.temp_dir = temp_dir
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

    def output_json(self, file_prefix: Optional[str] = None) -> "SessionOutputGenerator":
        if file_prefix is None:
            file_prefix = self.__DEFAULT_FILE_PREFIX

        storage_as_dict = []

        for d in self.data:
            if d.expected is None and d.actual is None and d.test_input is None:
                continue  # Drop from the finished file all irrelevant calls for the upload_manager fixture
            # if isinstance(d.func_args, dict):
            #     for ik, iv in d.func_args.items():
            #         if isinstance(iv, Callable):
            #             d.func_args[ik] = "function"
            if isinstance(d.test_input, pd.DataFrame):
                d.test_input = d.test_input.to_dict(orient="dict")

            storage_as_dict.append(dataclasses.asdict(d))
        self.__mkdir_if_none_exists(self.output_dir)
        _path = self._get_full_path_in_dir(self.output_dir, file_prefix) 
        with open(_path, "w") as f:
            json.dump(storage_as_dict, f, indent=4)

        return self

    def __mkdir_if_none_exists(self, dir_path) -> None:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    def _get_full_path_in_dir(self, dir: str, file_prefix: str, f_ext: Optional[str] = None) -> str:
        max_index = 0
        if f_ext is None:
            f_ext = 'json'
        for f in os.listdir(dir):
            if f.endswith(f_ext) and f.startswith(file_prefix):
                output_file_index = f.replace(file_prefix, "").replace(f".{f_ext}", "")
                try:
                    output_file_index = int(output_file_index)
                    if output_file_index > max_index:
                        max_index = output_file_index
                except ValueError:
                    pass
        filename = f"{file_prefix}{max_index + 1}.{f_ext}"
        return os.path.join(dir, filename)
