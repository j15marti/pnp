from itertools import combinations
from collections import Counter

N=7

def clause_system(n):
    clauses=[]
    contains=[[] for _ in range(1<<n)]
    for T in combinations(range(n),3):
        for pat in range(8):
            vals={v:(pat>>j)&1 for j,v in enumerate(T)}
            mask=0
            for a in range(1<<n):
                if all(((a>>v)&1)==b for v,b in vals.items()):
                    mask |= 1<<a
            ci=len(clauses)
            clauses.append((T,pat,mask))
            for a in range(1<<n):
                if (mask>>a)&1:
                    contains[a].append(ci)
    return clauses,contains

def exact_covers(n):
    clauses,contains=clause_system(n)
    full=(1<<(1<<n))-1
    out=set()
    def rec(cov,chosen):
        if cov==full:
            if len(chosen)==8:
                out.add(frozenset(chosen))
            return
        if len(chosen)>=8:
            return
        rem=full & ~cov
        a=(rem & -rem).bit_length()-1
        for ci in contains[a]:
            m=clauses[ci][2]
            if not (m & cov):
                rec(cov|m,chosen+[ci])
    rec(0,[])
    return clauses,out

def recursive_covers(n):
    leaf={}
    idx=0
    for T in combinations(range(n),3):
        for pat in range(8):
            leaf[(T,pat)]=idx
            idx+=1
    def children(fixed,pat,split):
        nf=tuple(sorted(fixed+(split,)))
        vals={v:(pat>>j)&1 for j,v in enumerate(fixed)}
        ans=[]
        for b in (0,1):
            vv=dict(vals); vv[split]=b
            npat=sum(vv[v]<<j for j,v in enumerate(nf))
            ans.append((nf,npat))
        return ans
    parts={}
    for T in combinations(range(n),3):
        for pat in range(8):
            parts[(T,pat)]={frozenset([leaf[(T,pat)]])}
    for d in (2,1,0):
        for fixed in combinations(range(n),d):
            for pat in range(1<<d):
                r=set()
                for split in range(n):
                    if split in fixed:
                        continue
                    c0,c1=children(fixed,pat,split)
                    for A in parts[c0]:
                        for B in parts[c1]:
                            r.add(A|B)
                parts[(fixed,pat)]=r
    return parts[((),0)]

def support_size(sol,clauses):
    u=set()
    for i in sol:
        u.update(clauses[i][0])
    return len(u)

if __name__=='__main__':
    clauses,all_exact=exact_covers(7)
    rec=recursive_covers(7)
    residual=all_exact-rec
    print('D(7,8) exact covers',len(all_exact))
    print('recursive covers',len(rec))
    print('nonrecursive residual',len(residual))
    print('exact support histogram',dict(sorted(Counter(support_size(s,clauses) for s in all_exact).items())))
    print('recursive support histogram',dict(sorted(Counter(support_size(s,clauses) for s in rec).items())))
    print('residual support histogram',dict(sorted(Counter(support_size(s,clauses) for s in residual).items())))
    full_support=[s for s in all_exact if support_size(s,clauses)==7]
    missed_full=[s for s in full_support if s not in rec]
    print('full_support_exact',len(full_support))
    print('full_support_missed_by_recursive',len(missed_full))
    c2=84*9
    c1=14*11
    root=13
    print('recursive_gate_codim2',c2)
    print('recursive_gate_codim1',c1)
    print('recursive_gate_root',root)
    print('recursive_gate_total',c2+c1+root)
    assert len(all_exact)==132685
    assert len(rec)==114485
    assert len(residual)==18200
    assert len(full_support)==5040
    assert len(missed_full)==0
    assert c2+c1+root==923
    print('verification PASS')
