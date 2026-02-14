from __future__ import annotations

from .enum import enum, Case
from collections.abc import Generator
from typing import TypeVar, Generic, Callable, Any

class UnwrappingError(Exception): pass

T = TypeVar("T")

@enum
class Option(Generic[T]):
    Some = Case(value=T)
    Nothing = Case()

    def unwrap(self) -> T:
        match self:
            case Option.Some(value): return value
            case _: raise UnwrappingError

    D = TypeVar("D")

    def unwrap_or(self, default_value: D = None) -> T | D:
        match self:
            case Option.Some(value): return value
            case _: return default_value

    R = TypeVar("R")

    def map(self, mapping_function: Callable[[T], R]) -> Option[R]:
        match self:
            case Option.Some(value): return Option.Some(mapping_function(value))
            case _: return self

    def and_then(self, mapping_function: Callable[[T], R]) -> Option[T].Nothing | R:
        match self:
            case Option.Some(value): return mapping_function(value)
            case _: return self

    def or_else(self, f: Callable[[], R]) -> R | Option[T].Some:
        match self:
            case Option.Some(_): return self
            case _: return f()

    def is_some(self):
        match self:
            case Option.Some(_): return True
            case _: return False

    @classmethod
    def next(cls, generator: Generator) -> Option[Any]:
        return next((cls.Some(e) for e in generator), cls.Nothing())