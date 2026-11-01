#!/usr/bin/env python3
"""LSPV-4 FULL-PAYLOAD310 source-bit adversary, standard library only.
Run from a clone: python experiments/arc/lspv4_310/yes_payload310_compact.py
Full source, separate U198 UNSAT replay and no-import verifiers are in the
reproducibility archive accompanying the role-owned research report.
"""
import ast, collections, itertools, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9=P+[tuple(-x for x in c) for c in Q]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
def good(F,n):
    if n<3 or n%3 or len(F)!=4*n//3:return False
    a=collections.Counter();b=collections.Counter();seen=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if any(x==0 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k)
        (a if c[0]>0 else b).update(map(abs,c))
    return all(a[x]==b[x]==2 for x in range(1,n+1))
def gamma(x):
    z=format(x,"b");return "0"*(len(z)-1)+z
def enc(F,n):
    w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)
def is_valid_bits(s):
    try:
        p=0;v=[]
        for _ in range(2):
            z=0
            while s[p]=='0':z+=1;p+=1
            v.append(int(s[p:p+z+1],2));p+=z+1
        n,m=v
        if n<3 or n%3 or m!=4*n//3:return False
        w=n.bit_length();r=1+3*w
        if len(s)-p!=m*r:return False
        F=[]
        for j in range(m):
            part=s[p+j*r:p+(j+1)*r];t=1 if part[0]=='1' else -1
            F.append(tuple(t*int(part[1+k*w:1+(k+1)*w],2) for k in range(3)))
        return good(F,n)
    except (IndexError,ValueError):return False
def flips(F,n,limit=None):
    s=enc(F,n);h=len(gamma(n))+len(gamma(len(F)))
    assert good(F,n) and is_valid_bits(s)
    end=len(s) if limit is None else min(len(s),h+limit)
    for j in range(h,end):
        mutant=s[:j]+('0' if s[j]=='1' else '1')+s[j+1:]
        assert not is_valid_bits(mutant),(n,j)
    return dict(input_bits=len(s),header_bits=h,payload_bits=len(s)-h,mutations_tested=end-h)
def models(F,n,pins=None):
    p=pins or {};free=[x for x in range(1,n+1) if x not in p];total=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=p.copy();a.update(zip(free,bits))
        total+=all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
    return total
def cyclic(t):
    f=[]
    for k in range(t):
        for j,c in enumerate(F9):
            x=[abs(z)+9*k for z in c]
            if j==0:x[1]=5+9*((k+1)%t)
            sg=1 if c[0]>0 else -1
            f.append(tuple(sg*v for v in x))
    return f
def main():
    assert models(F9,9)==70 and models(Y6,6)==20
    assert models(F9,9,{1:1,2:0,3:1,4:0,8:0})==1
    assert models(F9,9,{1:1,2:1,3:0,4:0,8:0})==0
    src=(ROOT/'experiments/arc/lspv2_296/U198.txt').read_text()
    U=ast.literal_eval(src[src.index('[['):]);V=[c[:] for c in U]
    V[2][2],V[44][2]=V[44][2],V[2][2]
    assert good(U,198) and good(V,198)
    file=(ROOT/'experiments/arc/lspv1_286/verify_three_core286.py').read_text()
    w=re.search(r"S='([01]+)'",file).group(1)
    assert len(w)==198 and all(any(w[abs(x)-1]==str(int(x>0)) for x in c) for c in V)
    a,b=enc(U,198),enc(V,198)
    assert [i for i in range(len(a)) if a[i]!=b[i]]==[106,1156]
    out={'Y6':flips(Y6,6),'F9':flips(F9,9),'U198':flips(U,198),'V198':flips(V,198)}
    for t in (2,4,8,16,128):
        out['G'+str(t)]=flips(cyclic(t),9*t,256 if t==128 else None)
    print(json.dumps({'status':'PASS','F9_models':70,'Y6_models':20,'F9_pin_models':[1,0],
      'U198':'grammar valid; independent UNSAT proof in full verifier',
      'V198':'complete 198-bit SAT witness verified','UV_bit_difference':[106,1156],
      'cases':out,'P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':main()
