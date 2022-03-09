from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum


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
