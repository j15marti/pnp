import itertools, random, json
from collections import deque

def basis(xs):
    B={}
    for x in xs:
        for p in sorted(B,reverse=True):
            if (x>>p)&1: x ^= B[p]
        if x: B[x.bit_length()-1]=x
    return B

def red(x,B):
    for p in sorted(B,reverse=True):
        if (x>>p)&1: x ^= B[p]
    return x

def parity(x): return x.bit_count()&1
def span(owners, S): return basis(v for i in S for v in owners[i][:2])

def independent_transversal(owners, ids, quotient):
    E=[(i,red(v,quotient)) for i in ids for v in (*owners[i][:2],owners[i][0]^owners[i][1])]
    I=set()
    def lin(S): return len(basis(E[e][1] for e in S))==len(S)
    def part(S): return len({E[e][0] for e in S})==len(S)
    while True:
        O=set(range(len(E)))-I
        P={e:None for e in O if lin(I|{e})}; Q=deque(P)
        end=None
        while Q:
            v=Q.popleft()
            if v in O and part(I|{v}): end=v; break
            nbr=(e for e in I if part((I-{e})|{v})) if v in O else (e for e in O if lin((I-{v})|{e}))
            for e in nbr:
                if e not in P: P[e]=v;Q.append(e)
        if end is None: return [E[e] for e in sorted(I)]
        path=set()
        while end is not None: path.add(end);end=P[end]
        I ^= path
        assert lin(I) and part(I)

def sat(owners, ids, x):
    return all((parity(owners[i][0]&x),parity(owners[i][1]&x))!=owners[i][2:] for i in ids)

def subs(S):
    return (tuple(i for i,j in zip(S, bits) if j) for bits in itertools.product((0,1),repeat=len(S)))

def audit():
    rng=random.Random(20261125); counts=dict(root_hall=0, root_sat=0,root_unsat=0, guard_jobs=0, guard_sat=0,guard_unsat=0, no_tight_guards=0,tight_guards=0, core_checks=0, lift_checks=0, compiler_source_assignments=0,selector_assignments=0)
    for n in range(2,7):
        for _ in range(80):
            m=rng.randint(1,n+2); owners=[]
            for i in range(m):
                a,b=rng.sample(range(1,1<<n),2)
                owners.append((a,b,rng.randrange(2),rng.randrange(2)))
            ids=tuple(range(m)); words=range(1<<n)
            F=[x for x in words if sat(owners,ids,x)]
            counts['root_sat' if F else 'root_unsat']+=1
            hall=all(len(span(owners,S))>=len(S) for S in subs(ids))
            assert (len(independent_transversal(owners,ids,{}))==m)==hall
            if not hall: continue
            counts['root_hall']+=1
            assert F
            for h in range(1,1<<n):
                Q=basis([h]); bad=lambda S:len(independent_transversal(owners,S,Q))<len(S)
                T=list(ids) if bad(ids) else []
                if T:
                    for i in ids:
                        if i in T and bad([j for j in T if j!=i]): T.remove(i)
                    counts['tight_guards']+=1
                    tights=[set(S) for S in subs(ids) if len(span(owners,S))==len(S) and red(h,span(owners,S))==0]
                    assert set(T)==set.intersection(*tights)
                    assert len(independent_transversal(owners,[i for i in ids if i not in T],span(owners,T)))==m-len(T)
                else: counts['no_tight_guards']+=1
                for t in (0,1):
                    orig=[x for x in F if parity(h&x)==t]
                    core=[x for x in words if parity(h&x)==t and sat(owners,T,x)]
                    assert bool(orig)==bool(core)
                    counts['guard_jobs']+=1;counts['guard_sat' if orig else 'guard_unsat']+=1
                    counts['core_checks']+=1
                    B=span(owners,T)
                    for x in core:
                        assert any(all(parity(v&(x^y))==0 for v in B.values()) for y in orig)
                        counts['lift_checks']+=1
    for signs in itertools.product((0,1),repeat=3):
        for x in itertools.product((0,1),repeat=3):
            l=tuple(a^b for a,b in zip(signs,x)); s=(l[0],(1^l[0])&l[1],(1^l[0])&(1^l[1]));
            assert s[0]^s[1]^s[2]==1
            assert tuple(si&(1^li) for si,li in zip(s,l))==(0,0,(1^l[0])&(1^l[1])&(1^l[2]))
            for t in itertools.product((0,1),repeat=3):
                legal=(t[0]^t[1]^t[2])==1 and all(not ti or li for ti,li in zip(t,l))
                if legal: assert any(l)
                counts['selector_assignments']+=1
            assert (any(l))==all(not si or li for si,li in zip(s,l))
            counts['compiler_source_assignments']+=1
    print(json.dumps(counts,indent=2))

def strict_control():
    F=[(2,4,0,0),(1,6,0,1),(2,5,1,1),(1,4,1,1)]
    I=tuple(range(4)); assert not any(sat(F,I,x) for x in range(8))
    for S in subs(I):
        assert len(span(F,S))>=len(S) if len(S)<4 else len(span(F,S))==3
    for i in I:
        J=tuple(j for j in I if j!=i)
        for h in (F[i][0],F[i][1],F[i][0]^F[i][1]):
            T=[S for S in subs(J) if len(span(F,S))==len(S) and red(h,span(F,S))==0]
            assert T==[J]
    print('Strict deficiency-one UNSAT partition example: all 12 direction cores retain all 3 remaining owners.')

if __name__=='__main__':
    audit()
    strict_control()
