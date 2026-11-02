#!/usr/bin/env python3
"""Independent strict binary grammar validator for LSPV-1 327.
Declared encoding: n:16, m:16, then each clause 3 x (sign:1,id:16).
"""
from collections import Counter
import json
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-x for x in c) for c in N)
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
G=Y+tuple(tuple(-x for x in c) for c in Y)
def encode(clauses):
    n=max(abs(x) for c in clauses for x in c)
    return f'{n:016b}{len(clauses):016b}'+''.join(
        ('1' if x<0 else '0')+f'{abs(x):016b}' for c in clauses for x in c)
def decode(s):
    if len(s)<32 or set(s)-{'0','1'}:return None
    n=int(s[:16],2);m=int(s[16:32],2)
    if n<1 or m<1 or len(s)!=32+51*m:return None
    rows=[];counts=Counter()
    for j in range(m):
        c=[]
        for k in range(3):
            i=32+51*j+17*k
            neg=s[i]=='1';v=int(s[i+1:i+17],2)
            if v<1 or v>n:return None
            c.append(-v if neg else v);counts[v,neg]+=1
        if len({abs(v) for v in c})!=3 or len({v<0 for v in c})!=1:return None
        rows.append(tuple(c))
    if len({tuple(sorted(c)) for c in rows})!=m:return None
    if any(counts[v,False]!=2 or counts[v,True]!=2 for v in range(1,n+1)):return None
    return tuple(rows)
def run():
    assert decode(encode(F))==F and decode(encode(G))==G
    bits=encode(F)
    def replace(a,b,s):return bits[:a]+s+bits[b:]
    bad=['',bits+'0',bits[:-1],bits.replace('0','2',1),
         '0'*16+bits[16:],bits[:16]+'0'*16+bits[32:],
         replace(33,49,'0'*16),replace(33,49,f'{10:016b}'),
         replace(32,33,'1'),replace(50,66,bits[33:49]),
         replace(83,134,bits[32:83]),replace(134,135,'1')]
    for x in bad:assert decode(x) is None
    print(json.dumps({'status':'PASS','source_roundtrips':2,
          'malformed_binary_payload_rejects':len(bad),'P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':run()
