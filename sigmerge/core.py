
import inspect
from functools import wraps
from itertools import chain

__all__ = ["merge_signatures"]

def merge_signatures(*target_funcs):
    """
    Decorator: merge parameters of multiple target functions with the decorated function.

    Example
    -------
    >>> def a1(i, j=0): ...
    >>> def a2(x, y=0): ...
    >>> @merge_signatures(a1, a2)
    ... def b(l, *args, **kwargs): ...
    >>> print(b.__signature__)
    (l, i, x, j=0, y=0)

    Notes
    -----
    - Keeps wrapper's own parameters except *args/**kwargs.
    - Deduplicates parameter names (first wins).
    - Automatically reorders non-default parameters before defaults.
    """

    def decorator(wrapper_func):
        wrapper_sig = inspect.signature(wrapper_func)

        # Extract wrapper's explicit params (not *args/**kwargs)
        wrapper_params = [
            p for p in wrapper_sig.parameters.values()
            if p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
        ]

        # Collect all parameters from target functions
        target_params = list(
            chain.from_iterable(inspect.signature(f).parameters.values() for f in target_funcs)
        )

        # Remove duplicates (first occurrence wins)
        seen = set()
        merged_params = []
        for p in wrapper_params + target_params:
            if p.name not in seen:
                merged_params.append(p)
                seen.add(p.name)

        # Fix ordering (non-defaults before defaults)
        no_default = [p for p in merged_params if p.default is inspect.Parameter.empty]
        with_default = [p for p in merged_params if p.default is not inspect.Parameter.empty]
        ordered_params = no_default + with_default

        new_sig = inspect.Signature(parameters=ordered_params)
        wrapper_func.__signature__ = new_sig
        return wraps(wrapper_func)(wrapper_func)

    return decorator
