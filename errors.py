from collections.abc import Callable
from inspect import currentframe
from pathlib import Path
from typing import Self, TypeVar, ParamSpec, Concatenate


class Err:
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


def through(f: Callable[Concatenate[S, P], T]) -> Callable[Concatenate[S | Err, P], T | Err]:
    def inner(arg: S | Err, *args: P.args, **kwargs: P.kwargs) -> T | Err:
        if isinstance(arg, Err):
            return arg
        return f(arg, *args, **kwargs)

    return inner
