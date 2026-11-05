#!/usr/bin/env python3
"""LSPV-2/425 compact independent replay. Standalone; source includes fresh
OR gates; results are mathematical controls only, not FLMV-machine timings.
Full original 2,371-assertion producer and 795,237-check JS verifier are
preserved in the separately delivered reproducibility archive.
"""
import hashlib, json, sys
def gamma(n):
    s=bin(n)[2:]
    return '0'*(len(s)-1)+s
def make(m,s,t):
    M=1<<m; n=m; cs=[]; gate=[]
    for tag,mask in enumerate((s,t)):
        for a in range(M):
            n+=1;u=n;cs.append([u if mask>>a&1 else -u])
            bits=[i+1 if not(a>>i&1) else -i-1 for i in range(m)]
            cur=bits[0]; nodes=[]
            for lit in bits[1:]+[u]:
                n+=1;v=n
                cs.extend([[-cur,v],[-lit,v],[cur,lit,-v]])
                nodes.append((v,cur,lit))
                cur=v
            cs.append([cur]); gate.append((u,bool(mask>>a&1),nodes))
    return n,cs,gate
def encode(m,n,cs):
    w=n.bit_length()
    data='01101100'+gamma(m)+gamma(n)+gamma(len(cs))+gamma(w)
    for clause in cs:
        data+=format(len(clause),'02b')
        for j in range(3):
            v=clause[j] if j<len(clause) else 0
            data+=('1' if v<0 else '0')+format(abs(v),f'0{w}b')
    return data
def test(m,s,t):
    n,cs,gate=make(m,s,t)
    assert n==m+2*(1<<m)*(m+1)
    assert len(cs)==2*(1<<m)*(3*m+2)
    text=encode(m,n,cs)
    cnt=0
    for x in range(1<<m):
        values={i+1:bool(x>>i&1) for i in range(m)}
        for u,on,nodes in gate:
            values[u]=on
            for v,p,q in nodes:
                def ev(l): return values[abs(l)] if l>0 else not values[-l]
                values[v]=ev(p) or ev(q)
        def ev(l): return values[abs(l)] if l>0 else not values[-l]
        sat=all(any(ev(l) for l in clause) for clause in cs)
        expected=bool((s>>x&1) and (t>>x&1))
        assert sat==expected
        cnt+=sat
    # actual selector-sign bits can be read from the canonical encoded stream
    stride=3*m+2; w=n.bit_length()
    header=len('01101100'+gamma(m)+gamma(n)+gamma(len(cs))+gamma(w))
    width=2+3*(w+1)
    def sign(block,a):
        k=(block*(1<<m)+a)*stride
        return text[header+k*width+2]=='0'
    indexed=any(sign(0,a) and sign(1,a) for a in range(1<<m))
    assert indexed==bool(s&t)
    return dict(m=m,N=len(text),V=n,C=len(cs),M=1<<m,models=cnt,
       label='SAT' if indexed else 'UNSAT',
       sha256_ascii_bits=hashlib.sha256(text.encode()).hexdigest())
def run():
    out=[]; checks=0
    for s in range(16):
        for t in range(16):
            p=test(2,s,t);checks+=1
    for m in (3,4,5):
        full=(1<<(1<<m))-1
        for s,t in ((0,0),(1,1),(1,2),(full,full),(full,0)):
            out.append(test(m,s,t));checks+=1
    print(json.dumps({'status':'restricted','pair_checks':checks,'cases':out},indent=2))
if __name__=='__main__':run()
