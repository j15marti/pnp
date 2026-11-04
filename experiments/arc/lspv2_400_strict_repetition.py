#!/usr/bin/env python3
"""LSPV-2/400: canonical signed-CNF code and strict triple-code counterexample.
Deterministic standard-library producer, no network and no random seed.
Run: python experiments/arc/lspv2_400_strict_repetition.py > result.json
"""
import itertools, json
MAGIC="110101"

def gamma(k):
    assert type(k)==int and k>=1
    b=bin(k)[2:]
    return "0"*(len(b)-1)+b

def encode(n, clauses):
    assert type(n)==int and n>=1
    bits=MAGIC+gamma(n)+gamma(len(clauses)+1)
    w=n.bit_length()
    sign_positions=[]
    for c in clauses:
        bits+=gamma(len(c)+1)
        for lit in c:
            assert type(lit)==int and lit!=0 and abs(lit)<=n
            sign_positions.append(len(bits))
            bits+=("1" if lit>0 else "0")+format(abs(lit),f"0{w}b")
    return bits,sign_positions

def parse(bits):
    if type(bits)!=str or not bits.startswith(MAGIC) or any(b not in "01" for b in bits):
        raise ValueError("bad binary source magic or bits")
    pos=len(MAGIC)
    def readgamma():
        nonlocal pos
        z=0
        while pos<len(bits) and bits[pos]=="0":
            z+=1;pos+=1
        if pos+z>=len(bits): raise ValueError("truncated gamma")
        x=int(bits[pos:pos+z+1],2);pos+=z+1
        return x
    n=readgamma()
    if n<1: raise ValueError("no variables")
    m=readgamma()-1
    if m<0: raise ValueError("bad clause count")
    w=n.bit_length()
    out=[]
    for _ in range(m):
        clen=readgamma()-1
        if clen<0: raise ValueError("bad clause length")
        c=[]
        for __ in range(clen):
            if pos+w>=len(bits): raise ValueError("truncated literal")
            sign=bits[pos];pos+=1
            v=int(bits[pos:pos+w],2);pos+=w
            if v<1 or v>n: raise ValueError("variable out of bound")
            c.append(v if sign=="1" else -v)
        out.append(c)
    if pos!=len(bits): raise ValueError("trailing bits")
    return n,out

def sat(n,F):
    for a in range(1<<n):
        if all(any(bool(a&(1<<(abs(l)-1)))==(l>0) for l in c) for c in F):
            return True
    return False

def rep(bits,r=3):
    return "".join(b*r for b in bits)

def strict_unpack(y,r=3):
    if type(y)!=str or len(y)%r or any(z not in "01" for z in y):
        raise ValueError("invalid repetition code")
    chunks=[y[i:i+r] for i in range(0,len(y),r)]
    if any(len(set(t))!=1 for t in chunks):
        raise ValueError("inconsistent repetition triple")
    return parse("".join(t[0] for t in chunks))

def graph_tseitin(n, edges, odd_first=True):
    adj=[[] for _ in range(n)]
    for j,(a,b) in enumerate(edges,1):
        adj[a].append(j);adj[b].append(j)
    assert all(len(a)==3 for a in adj)
    F=[]
    for v,es in enumerate(adj):
        charge=int(bool(odd_first) and v==0)
        for a in itertools.product((0,1),repeat=3):
            if sum(a)%2!=charge:
                F.append([(-e if t else e) for e,t in zip(es,a)])
    return F

def run():
    universe=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]]
    checks=0
    counts={"sources":0,"SAT":0,"UNSAT":0,"triple_single_bit_malformed":0,
            "Tseitin_source_pivots":0,"Tseitin_triple_blocks":0}
    witnesses=[]
    for mask in range(256):
        F=[universe[i] for i in range(8) if (mask>>i)&1]
        x,positions=encode(2,F)
        assert parse(x)==(2,F);checks+=1
        y=rep(x)
        assert strict_unpack(y)==(2,F);checks+=1
        is_sat=sat(2,F)
        counts["SAT" if is_sat else "UNSAT"]+=1
        for i in range(len(y)):
            mut=y[:i]+("1" if y[i]=="0" else "0")+y[i+1:]
            try:
                strict_unpack(mut)
                raise AssertionError("bad one-bit neighbor accepted")
            except ValueError: pass
            checks+=1;counts["triple_single_bit_malformed"]+=1
        counts["sources"]+=1
        if mask in (0,15,31,255):
            witnesses.append({"mask":mask,"label":"SAT" if is_sat else "UNSAT",
                              "N":len(x),"encoded_N":len(y)})
    graphs=[("K4",4,[(i,j) for i in range(4) for j in range(i+1,4)]),
            ("K33",6,[(i,j) for i in range(3) for j in range(3,6)])]
    sizes=[]
    for name,n,edges in graphs:
        for odd in (True,False):
            F=graph_tseitin(n,edges,odd)
            x,sgn=encode(len(edges),F)
            assert sat(len(edges),F)==(not odd);checks+=1
            y=rep(x)
            assert strict_unpack(y)==(len(edges),F);checks+=1
            if odd:
                for i in sgn:
                    z=x[:i]+("1" if x[i]=="0" else "0")+x[i+1:]
                    zn,zf=parse(z)
                    assert sat(zn,zf);checks+=1
                    zz=rep(z)
                    assert sum(a!=b for a,b in zip(y,zz))==3
                    assert strict_unpack(zz)==(zn,zf)
                    checks+=2
                    counts["Tseitin_source_pivots"]+=1
                    counts["Tseitin_triple_blocks"]+=1
            sizes.append({"graph":name,"charge":"odd" if odd else "even","N":len(x),
                          "N3":len(y),"clauses":len(F),
                          "sign_pivots":len(sgn) if odd else None})
    x,_=encode(2,[[1],[-1]])
    y=rep(x);rejected=0
    for malformed in [y+"0",y[:-1],
        y[:3]+("0" if y[3]=="1" else "1")+y[4:],"111","xxx",""]:
        try: strict_unpack(malformed)
        except ValueError: rejected+=1
    assert rejected==6;checks+=6
    print(json.dumps({"schema":"LSPV2-400-strict-encoding-v1",
          "code":"triple repetition; binary magic+gamma n,m and lengths+fixed-width signed literal fields",
          "status":"COMPUTATIONAL; symbolic theorem separate","checks":checks,
          "counts":counts,"small_controls":witnesses,"graph_controls":sizes,
          "malformed_rejected":rejected,"random_seed":None},sort_keys=True,indent=2))

if __name__=="__main__":
    run()
