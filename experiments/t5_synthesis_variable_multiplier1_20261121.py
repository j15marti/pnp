"""Finite arithmetic/header checks; synthetic headers are not full T5 instances."""
import json, hashlib
from pathlib import Path

def shift(x, e, width, left=False):
    mask=(1<<width)-1
    for j in range(width.bit_length()):
        if (e>>j)&1:
            x=((x<<(1<<j)) if left else (x>>(1<<j))) & mask
    return x

def header(n,m):
    b=bin(m+1)[2:]
    return '1'*n+'0'+'0'*(len(b)-1)+b

def parse(s):
    n=0
    while s[n]=='1': n+=1
    t=s[n+1:]; z=0
    while t[z]=='0': z+=1
    m=int(t[z:2*z+1],2)-1
    return n,m

checks=0
for w in range(1,17):
    for x in range(min(1<<w,256)):
        for e in range(w+1):
            assert shift(x,e,w)==x>>e
            assert shift(x,e,w,True)==(x<<e)&((1<<w)-1)
            checks+=2
rows=[]
for v in range(9):
    for e in range(v*(v-1)//2+1):
        n,m=55+18*v+11*e,65+20*v+13*e
        E=10+3*v+2*e
        N=n+2+2*((m+1).bit_length()-1)+3*m*n.bit_length()
        assert parse(header(n,m))==(n,m)
        assert (3*m-n)%14==0 and (3*m-n)//14==E
        # Admissible arithmetic samples, not asserted graph counts.
        for q in (0,1,7,6848):
            y=10*(q<<E)
            assert y<=5**n
            assert shift(y//10,E,3*N)==q
            assert 10*shift(q,E,3*N,True)==y
        rows.append([v,e,n,m,E,N])
print(json.dumps({'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'shift_checks':checks,'parameter_rows':rows,'header_cases':len(rows),
 'arithmetic_roundtrips':4*len(rows),'status':'PASS',
 'limitations':'Synthetic headers; no new full T5 counts, circuit minimization or tape benchmark.'},separators=(',',':')))
