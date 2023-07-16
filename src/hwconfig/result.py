"""Module for reporting the results of installer operations."""
from dataclasses import dataclass, field
from enum import Enum


class Result(Enum):
    """Enum representing possible results of an installer operation."""

    OK = 0
    WARNING = 1
    ERROR = 2


@dataclass
class Report:
    """A report of the results of an installer operation."""

    result: Result = field(default=Result.OK)
    msg: str = field(default_factory=str)
    exception: Exception | None = field(default=None)
