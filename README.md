
# sigmerge 🧠

A lightweight Python decorator that **merges multiple function signatures** dynamically.
Perfect for wrapper functions that call other functions internally and need **intelligent IDE completion**.

## Installation
```bash
pip install sigmerge
```


## Usage
```python
from sigmerge import merge_signatures

def a1(i, j=0): ...
def a2(x, y=0): ...

@merge_signatures(a1, a2)
def b(l, *args, **kwargs):
    return a1(*args, **kwargs) + a2(*args, **kwargs) + l

print(b.__signature__)
# (l, i, x, j=0, y=0)
```
✅ Works beautifully in VS Code and Pyright for autocompletion.




