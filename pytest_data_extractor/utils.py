import os
from typing import (
    Iterable,
    Optional,
    Dict,
    List
)
from dataclasses import dataclass
import dataclasses


def mkdir_if_none_exists(dirname: str) -> None:
    """
    Generate a directory if one doesn't exist in the given path.
    :param dirname: Full or relative path to the requested directory
    :return:
    """
    if not os.path.exists(dirname):
        os.mkdir(dirname)


def get_output_full_path_in_dir(dirname: str, file_prefix: str, f_ext: Optional[str] = 'json') -> str:
    """
    Generate indexed output files in the desired directory
    :param dirname: Relative or full path to desired directory
    :param file_prefix: Prefix of the used files
    :param f_ext: File extension of the generated files
    :return: The relative path to the new generated file
    """
    max_index = 0
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


def is_array_homogenous(arr: Iterable) -> bool:
    return all(isinstance(sub, type(arr[0])) for sub in arr[1:])


def dataclass_to_dict(data: dataclass, pop_items: Optional[List[str]] = None) -> Dict:
    data_dict = dataclasses.asdict(data)
    if pop_items:

        for item in pop_items:
            data_dict.pop(item)
    return data_dict


def get_only_filename(fpath: str) -> str:
    return os.path.split(fpath)[-1]


class ClassProperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
