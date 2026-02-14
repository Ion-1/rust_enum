# Rust-style enums for Python

Enumerations that can contain data and be matched.

```python
from rust_enum import enum, Case
from dataclasses import field

@enum
class DivisionResult:
    Undefined = Case()
    Some = Case(number=float) # Equivalent: Some = Case(number=(float, field()))

def divide(a: float, b: float) -> DivisionResult:
    if b == 0: return DivisionResult.Undefined()
    return DivisionResult.Some(a / b)

match divide(3, 3):
    case DivisionResult.Some(n): assert n == 1
    case _: assert False
```

Provide a `tuple[type, dataclasses.Field]` to use dataclass features:
```python
from rust_enum import enum, Case
from dataclasses import field

@enum
class DivisionResult:
    Undefined = Case()
    Some = Case(number=(float, field(doc="The division result")))
```

Both Option and Result are implemented, so you can do it even faster in most cases:

```python
from rust_enum import Option, Result

class DivByZeroError(Exception):
    pass

def divide(a: float, b: float) -> Option[float]:
    if b == 0: return Option.Nothing()
    return Option.Some(a / b)

def divide_res(a: float, b: float) -> Result[float, DivByZeroError]:
    if b == 0: return Result.Err(DivByZeroError())
    return Result.Ok(a / b)

assert divide(6, 2).unwrap() == 3
assert divide(6, 2).unwrap_or(None) == 3
assert divide(6, 0).unwrap_or(None) is None
assert divide(6, 2).map(lambda v: v * 3) == Option.Some(9)
assert divide(6, 0).map(lambda v: v * 3) == Option.Nothing()
assert divide(6, 2).and_then(lambda v: divide(v, 3)) == Option.Some(1)

assert divide_res(6, 2).unwrap() == 3
assert divide_res(6, 2).unwrap_or(None) == 3
assert divide_res(6, 0).unwrap_or(None) is None
assert divide_res(6, 2).map(lambda v: v * 3) == Result.Ok(9)
assert divide_res(6, 0).map(lambda v: v * 3) == Result.Err(DivByZeroError())
assert divide_res(6, 2).and_then(lambda v: divide_res(v, 3)) == Result.Ok(1)
```

## Installation

```bash
pip install rust_enum
```
