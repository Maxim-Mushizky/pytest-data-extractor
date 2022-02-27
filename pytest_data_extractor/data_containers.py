from dataclasses import dataclass,field
from typing import (
    Optional,
    Any,
    Dict
)

@dataclass
class TestData:
    test_input: Optional[Any] = field(default=None)
    func_args: Optional[Dict] = field(default_factory=dict)
    expected_result: Optional[Any] = field(default=None)
    actual_result: Optional[Any] = field(default=None)
    test_operator: Optional[str] = field(default=None)
    test_func: Optional[str] = field(default=None)
    test_status: int = field(default=0) # 1- Pass , 0- Fail, -1- Skip
    test_duration: float = field(default_factory=float)
    setup_duration: float = field(default_factory=float)
