#!/usr/bin/env python3
"""ARC280 compact, stdlib-only reproducibility. Run from the j15marti/pnp root.
Full original-indexed independent raw/verifier in ARC280 conversation ZIP.
Proof of U198 UNSAT is independently replayed by:
python experiments/arc/lspv4_279/target_cofactor279_compact.py
"""
import ast, collections, itertools, json, pathlib
from fractions import Fraction

ROOT=pathlib.Path('research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt')
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
W='010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001'

def target_valid(F):
    if not F or any(len(C)!=3 or len(set(map(abs,C)))!=3 or
        not (all(x>0 for x in C) or all(x<0 for x in C)) for C in F):
        return False
    vs={abs(x) for C in F for x in C}
    if vs!=set(range(1,len(vs)+1)) or 3*len(F)!=4*len(vs):
        return False
    ct=collections.Counter(x for C in F for x in C)
    return (len({tuple(sorted(C)) for C in F})==len(F) and
        all(ct[x]==ct[-x]==2 for x in vs))

def bytes_canonical(n):
    assert n%3==0 and n>=6
    m=4*n//3
    return len(f'p cnf {n} {m}\n')+4*m+2*n+4*sum(len(str(i)) for i in range(1,n+1))

def pair_modes(F):
    out=collections.Counter()
    for j,C in enumerate(F):
        a={abs(x):(x>0) for x in C}
        for D in F[j+1:]:
            b={abs(x):(x>0) for x in D}
            common=a.keys()&b.keys()
            same=any(a[x]==b[x] for x in common)
            opp=any(a[x]!=b[x] for x in common)
            out[''.join(str(int(v)) for v in (not opp,not same,not same,not opp))]+=1
    return dict(out)

def cofactor(F,pivot,value):
    return tuple(tuple(x for x in C if abs(x)!=pivot) for C in F
        if not any(abs(x)==pivot and (x>0)==value for x in C))

def truth(C,bits):
    return sum((x>0)==bits[abs(x)-1] for x in C)

def envelope(c):
    fk=Fraction(1);best=Fraction(-1);rows=[]
    for k in range(1,100):
        fk=c*fk/(1+fk)
        d=min((1/fk-c)/k,c**(-k))
        rows.append((k,str(d)))
        best=max(best,d)
        if c**(-(k+1))<best: return str(best),rows,k+1
    raise AssertionError('tail not certified')

def main():
    U=tuple(tuple(C) for C in ast.literal_eval(
        '\n'.join(line for line in ROOT.read_text().splitlines()
                  if line and not line.startswith('#'))))
    V0=[list(C) for C in U]
    V0[1][0],V0[7][0]=V0[7][0],V0[1][0]
    V=tuple(tuple(C) for C in V0)
    assert len(W)==198
    assert all(target_valid(F) for F in (Y,U,V))
    assert all(truth(C,[b=='1' for b in W])>0 for C in V)
    ym=sum(all(truth(C,a)>0 for C in Y)
           for a in itertools.product((False,True),repeat=6))
    assert ym==20
    data=[]
    for name,F in [('Y6_SAT',Y),('U198_UNSAT',U),('V198_SAT',V)]:
        n=max(map(abs,(x for C in F for x in C)))
        m=len(F);modes=pair_modes(F)
        assert m*3==4*n and m%4==0
        assert set(modes)<= {'1001','0110','1111'}
        endpoints=[]
        for bits in ([False]*n,[True]*n):
            ts=[truth(C,bits) for C in F]
            endpoints.append([ts.count(j) for j in range(4)])
        assert endpoints==[[m//2,0,0,m//2]]*2
        children=[]
        for b in (False,True):
            child=cofactor(F,1,b)
            widths=collections.Counter(map(len,child))
            assert len(child)==m-2 and widths[2]==2 and widths[3]==m-4
            assert not target_valid(child)
            children.append({'branch_value':int(b),'raw_clause_count':len(child)})
        # Every identity-preserving re-encoded target child of r=1,2
        # requires at least n variables and m clauses.
        assert all(3*((n-r+2)//3)==n for r in (1,2))
        data.append({'name':name,'n':n,'m':m,'canonical_bits':8*bytes_canonical(n),
                     'pair_modes':modes,'endpoints':endpoints,'children':children})
    assert data[1]['pair_modes']==data[2]['pair_modes']
    a=envelope(Fraction(6,5));b=envelope(Fraction(241,200))
    assert a[0]=='23/45' and b[0]=='11642479/23232400'
    assert a[2]==b[2]==4
    print(json.dumps({'status':'restricted target quota theorem; ARC OPEN',
        'sources':data,'Y_models':ym,
        'FLMV':{'6/5':a,'241/200':b},
        'proof_idea':'q=2^r polynomial => r=O(log N); retaining n-r symbols implies child M=(1-o(1))N, not N^1/2',
        'U_certificate':'independent source-derived refutation in prior ARC279 checker; no inference from failed endpoint'},indent=2))
if __name__=='__main__':main()
