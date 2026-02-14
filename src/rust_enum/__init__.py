"""Rust-style enumerations."""
from .enum import enum, Case
from .option import Option, UnwrappingError
from .result import Result

__all__ = ["enum", "Case", "Option", "UnwrappingError", "Result"]
