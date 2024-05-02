from collections.abc import Callable
from typing import ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def singleton(cls: type[T]) -> Callable[..., T]:
    """
    Returns a function that can be used as a decorator to make ``cls`` a singleton.

    The decorator takes the same arguments as ``cls`` and returns an instance of ``cls``.
    Subsequent calls to the decorator will return the same instance.

    Args:
        cls: The class to make a singleton.

    Returns:
        A function that can be used as a decorator to make ``cls`` a singleton.
    """
    instances: dict[type[T], T] = {}

    def get_instance(*args: P.args, **kwargs: P.kwargs) -> T:
        """
        Returns an instance of ``cls``.

        If an instance of ``cls`` has not been created, a new one will be created using
        ``cls(*args, **kwargs)``. Subsequent calls will return the same instance.

        Args:
            *args: The positional arguments to pass to ``cls``.
            **kwargs: The keyword arguments to pass to ``cls``.

        Returns:
            An instance of ``cls``.
        """
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
