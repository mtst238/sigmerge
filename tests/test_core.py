from sigmerge import merge_signatures

def a1(i, j=0): ...
def a2(x, y=0): ...

@merge_signatures(a1, a2)
def b(l, *args, **kwargs): ...

def test_signature_merge():
    sig_str = str(b.__signature__)
    assert "(l, i, x, j=0, y=0)" in sig_str
