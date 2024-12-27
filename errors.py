from collections.abc import Callable
from inspect import currentframe
from pathlib import Path
from typing import Self, TypeVar, ParamSpec, Concatenate


class Err:
    """Err is an error type that does not need to be raised."""

    def __init__(self, msg: str, cause: Exception | Self | None = None):
        self.message = msg
        self.cause = cause

        caller = (current := currentframe()) and current.f_back
        if caller is None:
            return

        self.filename = Path(caller.f_code.co_filename)
        self.lineno = caller.f_lineno

    def __str__(self) -> str:
        if self.filename:
            s = f"{self.filename.name}:{self.lineno}: {self.message}"
        else:
            s = f"{self.message}: {self.cause}"

        if self.cause:
            return f"{s}: {self.cause}"
        return s


S = TypeVar("S")
T = TypeVar("T")
P = ParamSpec("P")


def guarded(f: Callable[Concatenate[S, P], T]) ->\
    Callable[Concatenate[S | Err, P], T | Err]:
    """
    The guarded decorator wraps a function.
    If the first argument of the wrapped function is an object of type Err,
    it returns that object.
    If the argument is an object of type other than Err,
    the original function is executed.
    """

    def inner(arg: S | Err, *args: P.args, **kwargs: P.kwargs) -> T | Err:
        if isinstance(arg, Err):
            return arg
        return f(arg, *args, **kwargs)

    return inner
