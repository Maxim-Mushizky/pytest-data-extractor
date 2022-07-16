from dataclasses import dataclass, field
from typing import (
    Optional,
    Any,
    List
)
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class TestStatus(Enum):
    Skip = -1
    Fail = 0
    Pass = 1


@dataclass
class MetaData:
    project_name: Optional[str] = field(default_factory=str)


@dataclass
class TestData:
    test_input: Optional[Any] = field(default=None)
    expected_result: Optional[Any] = field(default=None)
    actual_result: Optional[Any] = field(default=None)
    test_operator: Optional[str] = field(default=None)
    test_func: Optional[str] = field(default=None)
    test_status: Optional[int] = field(default=None)
    test_duration: float = field(default_factory=float)
    meta_data: Optional[MetaData] = field(default=None)

# class TestData(BaseModel):
#     # timestamp = Optional[datetime] = Field(default=None)
#     test_input: List[Optional[Any]] = Field(default_factory=list)
#     expected_result: Optional[Any] = Field(default=None)
#     actual_result: Optional[Any] = Field(default=None)
#     test_operator: Optional[str] = Field(default=None)
#     test_func: Optional[str] = Field(default=None)
#     test_status: Optional[int] = Field(default=None)
#     test_duration: float = Field(default_factory=float)
#     meta_data: Optional[MetaData] = Field(default=None)
#
#
# if __name__ == '__main__':
#     print("hello")
