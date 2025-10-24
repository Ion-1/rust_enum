from __future__ import annotations

from . import enum, Case, UnwrappingError, Option
from collections.abc import Generator
from typing import TypeVar, Generic, Callable, Any

T = TypeVar("T")
E = TypeVar("E")

@enum
class Result(Generic[T, E]):
    Ok = Case(value=T)
    Err = Case(value=E)

    def is_ok(self) -> bool:
        match self:
            case Result.Ok(_): return True
            case Result.Err(_): return False

    def is_err(self) -> bool:
        match self:
            case Result.Ok(_): return False
            case Result.Err(_): return True

    def unwrap(self) -> T:
        match self:
            case Result.Ok(value): return value
            case _: raise UnwrappingError

    def unwrap_or(self, default_value: T) -> T:
        match self:
            case Result.Ok(value): return value
            case _: return default_value

    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(err): return f(err)

    def expect(self, message: str) -> T:
        match self:
            case Result.Ok(value): return value
            case _: raise UnwrappingError(message)

    def unwrap_err(self) -> E:
        match self:
            case Result.Err(value): return value
            case _: raise UnwrappingError

    def expect_err(self, message: str) -> E:
        match self:
            case Result.Err(value): return value
            case _: raise UnwrappingError(message)

    def ok(self) -> Option[T]:
        match self:
            case Result.Ok(value): return Option.Some(value)
        return Option.Nothing()

    def err(self) -> Option[E]:
        match self:
            case Result.Err(value): return Option.Some(value)
        return Option.Nothing()

    def transpose(self: Result[Option[T], E]) -> Option[Result[T, E]]:
        match self:
            case Result.Ok(value):
                match value:
                    case Option.Some(inner):
                        return Option.Some(Result.Ok(inner))
                    case Option.Nothing():
                        return Option.Nothing()
            case Result.Err(err):
                return Option.Some(Result.Err(err))

    U = TypeVar("U")

    def map(self, f: Callable[[T], U]) -> Result[U, E]:
        match self:
            case Result.Ok(value): return Result.Ok(f(value))
            case Result.Err(err): return Result.Err(err)

    def map_err(self, f: Callable[[E], U]) -> Result[T, U]:
        match self:
            case Result.Ok(value): return Result.Ok(value)
            case Result.Err(err): return Result.Err(f(err))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        match self:
            case Result.Ok(value): return f(value)
            case Result.Err(_): return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        match self:
            case Result.Ok(value): return f(value)
            case Result.Err(err): return default(err)

    def and_(self, res: Result[U, E]) -> Result[U, E]:
        match self:
            case Result.Ok(_): return res
        return self

    def and_then(self, f: Callable[[T], Result[U, E]]) -> Result[U, E]:
        match self:
            case Result.Ok(value): return f(value)
        return self

    F = TypeVar("F")

    def or_(self, res: Result[T, F]) -> Result[T, F]:
        match self:
            case Result.Err(_): return res
        return self

    def or_else(self, f: Callable[[E], Result[T, F]]) -> Result[T, F]:
        match self:
            case Result.Err(err): return f(err)
        return self
