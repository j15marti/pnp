# Counting bound: smallest g with (10*C(n+g-1,2))^g * ... >= 2^(2^n); upper-bounds #circuits of g gates (ordered, each gate: pair among earlier nodes, 10 ops)
from math import comb, log2
for n in range(2,11):
    g=1
    while True:
        bits=sum(log2(10*comb(n+i,2)) for i in range(g))  # gate i (0-based) picks pair among n+i nodes
        if bits>=2**n: break
        g+=1
    print(n, g-0, 2*(g), "wires >=", 2*g)
