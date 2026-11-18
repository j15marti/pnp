#!/usr/bin/env python3
"""Online no-length-preamble Fibonacci-rule lookup versus SLP expansion."""
import json

def online_symbol(i):
    lengths=[1,2]
    while lengths[-1] <= i:
        lengths.append(lengths[-1]+lengths[-2])
    k=len(lengths)-1
    while k>=2:
        left=lengths[k-1]
        if i<left:
            k-=1
        else:
            i-=left
            k-=2
    return 0 if k==0 or i==0 else 1

def fib_word(n):
    f0='0';f1='01'
    while len(f1)<n:
        f0,f1=f1,f1+f0
    return f1[:n]

for n in range(1,17):
    N=1<<n
    f=fib_word(N)
    for i,bit in enumerate(f):
        assert online_symbol(i)==int(bit),(n,i)
print(json.dumps({'cases':sum(1<<n for n in range(1,17)),'largest_length':65536,'failures':0,'model':'Fibonacci rule schedule online without input length header'},sort_keys=True))
