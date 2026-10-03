from itertools import combinations
import csv, hashlib, sys

# D(5,8) exhaustive pair-witness certificate generator and verifier.
# Clause index = 8*triple_index + falsifying_sign_pattern,
# with variable triples in lexicographic order.
# Promise: exactly eight of the 80 clause-presence bits are 1.

N=5
TRIPLES=list(combinations(range(N),3))
CLAUSES=[]
CONTAINS=[[] for _ in range(1<<N)]
for T in TRIPLES:
    for pat in range(8):
        mask=0
        for a in range(1<<N):
            if all(((a>>v)&1)==((pat>>j)&1) for j,v in enumerate(T)):
                mask |= 1<<a
        ci=len(CLAUSES)
        CLAUSES.append(mask)
        for a in range(1<<N):
            if (mask>>a)&1:
                CONTAINS[a].append(ci)

FULL=(1<<(1<<N))-1
assert len(CLAUSES)==80

def is_unsat(F):
    cov=0
    for x in F:
        cov |= CLAUSES[x]
    return cov==FULL

def exact_unsat_sets():
    out=set()
    def rec(cov, chosen):
        if cov==FULL:
            if len(chosen)==8:
                out.add(tuple(sorted(chosen)))
            return
        if len(chosen)>=8:
            return
        rem=(~cov)&FULL
        a=(rem & -rem).bit_length()-1
        for ci in CONTAINS[a]:
            m=CLAUSES[ci]
            if m&cov:
                continue
            rec(cov|m, chosen+(ci,))
    rec(0,())
    return sorted(out)

def generate(path):
    unsat_sets=exact_unsat_sets()
    assert len(unsat_sets)==4380
    witness={}
    for F in unsat_sets:
        FS=set(F)
        for i in F:
            base=tuple(x for x in F if x!=i)
            for j in range(80):
                if j in FS:
                    continue
                p=tuple(sorted((i,j)))
                if p in witness:
                    continue
                G=base+(j,)
                if not is_unsat(G):
                    witness[p]=(i,j,base)
    assert len(witness)==3160
    with open(path,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["pair_a","pair_b","unsat_add","sat_add",
                    "b0","b1","b2","b3","b4","b5","b6"])
        for a,b in combinations(range(80),2):
            i,j,base=witness[(a,b)]
            w.writerow([a,b,i,j,*base])
    raw=open(path,"rb").read()
    print("generated_rows",len(witness))
    print("sha256",hashlib.sha256(raw).hexdigest())

def verify(path):
    seen=set()
    rows=0
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            a,b,i,j=map(int,[r["pair_a"],r["pair_b"],r["unsat_add"],r["sat_add"]])
            base=tuple(int(r["b"+str(k)]) for k in range(7))
            assert 0<=a<b<80
            assert {i,j}=={a,b}
            assert len(set(base))==7
            assert all(0<=x<80 for x in base)
            assert i not in base and j not in base
            Fu=base+(i,)
            Fs=base+(j,)
            assert len(set(Fu))==8 and len(set(Fs))==8
            assert is_unsat(Fu)
            assert not is_unsat(Fs)
            assert (a,b) not in seen
            seen.add((a,b))
            rows+=1
    expected=set(combinations(range(80),2))
    assert seen==expected
    raw=open(path,"rb").read()
    print("PASS rows",rows)
    print("pairs",len(seen))
    print("sha256",hashlib.sha256(raw).hexdigest())
    print("CERTIFIED_LOWER_BOUND_QUERY_NODES 79")

if __name__=="__main__":
    if len(sys.argv)!=3 or sys.argv[1] not in {"generate","verify"}:
        raise SystemExit("usage: python d5_m8_pair_certificate.py generate|verify certificate.csv")
    if sys.argv[1]=="generate":
        generate(sys.argv[2])
    else:
        verify(sys.argv[2])
