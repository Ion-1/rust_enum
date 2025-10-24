"""Rust-style enumerations."""
from dataclasses import make_dataclass, Field
from option import Option, UnwrappingError
from result import Result

__all__ = ["enum", "Case", "Option", "UnwrappingError", "Result"]


def _expand(case_tuple):
    if (isinstance((field_tuple := case_tuple[1]), tuple) 
            and len(field_tuple) == 2
            and isinstance((field := field_tuple[1]), Field)):
        return case_tuple[0], field_tuple[0], field
    return case_tuple


def enum(cls):
    """Create enumeration from class."""
    for field_name in dir(cls):
        if not isinstance((value := getattr(cls, field_name)), Case): continue
        setattr(cls, field_name, make_dataclass(field_name, [_expand(tup) for tup in value.dict.items()], bases=(cls,)))
    return cls


class Case:
    """Class-placeholder for generation of enumeration members."""
    def __init__(self, **attributes):
        self.dict = attributes

    # to disable warnings
    def __call__(self, *args, **kwargs):
        pass
