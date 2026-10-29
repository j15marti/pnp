#!/usr/bin/env python3
"""Small dependency-free controls for fixed-tree message table registers.
PUBLIC SHORT EXAMPLE, not the locally archived complete 192+40 SAT audit.
Modeled resources are tables, not physical tape cells. Python 3.9+.
"""
import json
from functools import lru_cache

def shape(name, m):
    assert m >= 1 and m % 2 == 1
    if name == "comb":
        if m == 1: return None
        return (None, shape(name, m-2))
    if name == "balanced":
        if m == 1: return None
        a = 2 * (((m - 1) // 2) // 2) + 1
        b = m - 1 - a
        return (shape(name, a), shape(name, b))
    raise ValueError(name)

def size(node):
    return 1 if node is None else 1 + size(node[0]) + size(node[1])

def registers(node, heavy_first):
    if node is None:
        return 1
    left, right = node
    a, b = left, right
    if heavy_first and size(a) < size(b):
        a, b = b, a
    return max(registers(a, heavy_first), 1 + registers(b, heavy_first), 2)

def run():
    rows = []
    for m in (1, 3, 5, 7, 15, 31, 63, 127, 255):
        for name in ("comb", "balanced"):
            tree = shape(name, m)
            l, h = registers(tree, False), registers(tree, True)
            assert h <= 1 + (m.bit_length() - 1)
            if name == "comb" and m >= 3:
                assert l == (m + 1) // 2 and h == 2
            if name == "balanced":
                assert h <= m.bit_length()
                if (m & (m+1)) == 0:
                    assert h == m.bit_length()
            rows.append(dict(shape=name, modules=m, left_tables=l, heavy_tables=h,
                             table_bits_heavy_w4=h * 16))
    assert registers(shape("comb", 5), False) == 3
    assert registers(shape("comb", 5), True) == 2
    print(json.dumps({"result":"PASS","rows":rows},sort_keys=True,indent=2))
if __name__ == "__main__":
    run()
