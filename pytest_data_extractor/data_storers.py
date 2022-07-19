import abc
import datetime
import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import (
    Optional,
    Any,
    Union,
    Iterable
)
from pytest_data_extractor import utils


class ObjectStoreException(Exception):
    def __init__(self, msg: Optional[str] = None, errors: Optional[str] = None) -> None:
        if msg is None:
            msg = "Storing Object general error"
        if errors is None:
            errors = "Object cannot be stored"
        super().__init__(msg)
        self.errors = errors


class ObjectStore(abc.ABC, metaclass=abc.ABCMeta):
    TIME_FORMAT = "%Y%m%d_%H_%M_%S_%f"

    def __init__(self,
                 data: Any,
                 to: str,
                 filename: Union[str, Path, None] = None) -> None:
        self._dirname = to
        self._data = data
        if filename is None:
            filename = ""
        self._filename = filename

    @property
    @abc.abstractmethod
    def data(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def generate_file(self, f_ext: Optional[str], file_name_only: bool) -> str:
        raise NotImplementedError

    def get_full_file_path(self, f_ext: str) -> str:
        if not isinstance(f_ext, str):
            raise TypeError("The file extension must be a string")
        utils.mkdir_if_none_exists(dirname=self._dirname)
        return self._add_timestamp_postfix()._get_full_filename(f_ext=f_ext)

    def _add_timestamp_postfix(self) -> "ObjectStore":
        now = datetime.datetime.now().strftime(self.TIME_FORMAT)
        self._filename += "_" + now
        return self

    def _get_full_filename(self, f_ext: str) -> str:
        return f"{os.path.join(self._dirname, self._filename)}.{f_ext}"


class DataFrameStore(ObjectStore):

    def __new__(cls, data: pd.DataFrame, *args, **kwargs):
        if isinstance(data, pd.DataFrame):
            return super(DataFrameStore, cls).__new__(cls)
        raise TypeError(f"Class handles only pandas dataframes. Given {type(data)} was given instead")

    @property
    def data(self) -> Any:
        return self._data

    def generate_file(self, f_ext: Optional[str] = 'csv', file_name_only: bool = False) -> str:
        full_filename_path = self.get_full_file_path(f_ext=f_ext)
        if f_ext == 'json':
            self.data.to_json(path_or_buf=full_filename_path,
                              orient='records',
                              indent=4)
        elif f_ext == 'csv':
            self.data.to_csv(path_or_buf=full_filename_path)
        else:
            raise ObjectStoreException(
                msg="DataFrame serialization error",
                errors=f"Cannot serialize a pandas dataframe to the given file extension {f_ext}"
            )
        return full_filename_path if not file_name_only else utils.get_only_filename(fpath=full_filename_path)


class ArrayStore(ObjectStore):
    def __new__(cls, data: Iterable, *args, **kwargs):
        if isinstance(data, np.ndarray):
            return super(ArrayStore, cls).__new__(cls)
        elif isinstance(data, Iterable):
            data = np.array(data)
            return super(ArrayStore, cls).__new__(cls)
        raise TypeError(f"Class handles only arrays. Given {type(data)} was given instead")

    @property
    def data(self) -> Any:
        return self._data

    def data_to_csv(self, full_filename_path: str) -> None:
        np.savetxt(
            full_filename_path,
            self._data,
            delimiter=",",
            fmt="%s"
        )

    def generate_file(self, f_ext: Optional[str], file_name_only: bool = False) -> str:
        full_filename_path = self.get_full_file_path(f_ext=f_ext)
        if f_ext == 'csv' or f_ext == 'txt':
            self.data_to_csv(full_filename_path=full_filename_path)
            return full_filename_path if not file_name_only else utils.get_only_filename(fpath=full_filename_path)
        raise ObjectStoreException(
            msg="Array serialization error",
            errors=f"Cannot serialize a numpy array to the given file extension {f_ext}"
        )


class AnyValueStore(ObjectStore):

    @property
    def data(self) -> Any:
        return self._data

    def data_to_csv(self, full_filename_path: str) -> None:
        with open(full_filename_path, 'w') as file:
            file.write(f"{self._data}\n")

    def generate_file(self, f_ext: Optional[str], file_name_only: bool = False) -> str:
        full_filename_path = self.get_full_file_path(f_ext=f_ext)
        self.data_to_csv(full_filename_path=full_filename_path)
        return full_filename_path if not file_name_only else utils.get_only_filename(fpath=full_filename_path)
