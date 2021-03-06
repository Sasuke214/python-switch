# Here is a first pass implementation at adding switch
import uuid
from typing import Callable, Any, List


class switch:
    __no_result = uuid.uuid4()

    def __init__(self, value):
        self.value = value
        self.cases = {}
        self.__result = switch.__no_result

    def default(self, func: Callable[[], Any]):
        self.case('__default__', func)

    def case(self, key, func: Callable[[], Any]):
        if isinstance(key, range):
            for n in key:
                self.case(n, func)
            return

        if isinstance(key, list):
            for i in key:
                self.case(i, func)
            return

        if key in self.cases:
            raise ValueError("Duplicate case: {}".format(key))
        if not func:
            raise ValueError("Action for case cannot be None.")
        if not callable(func):
            raise ValueError("Func must be callable.")

        self.cases[key] = func

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise exc_val

        func = self.cases.get(self.value)
        if not func:
            func = self.cases.get('__default__')

        if not func:
            raise Exception("Value does not match any case and there "
                            "is no default case: value {}".format(self.value))

        # noinspection PyCallingNonCallable
        self.__result = func()

    @property
    def result(self):
        if self.__result == switch.__no_result:
            raise Exception("No result has been computed (did you access switch.result inside the with block?)")

        return self.__result


def closed_range(start: int, stop: int, step=1) -> range:
    if start >= stop:
        raise ValueError("Start must be less than stop.")

    return range(start, stop+step, step)
