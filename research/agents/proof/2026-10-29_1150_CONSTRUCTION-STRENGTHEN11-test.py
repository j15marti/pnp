#!/usr/bin/env python3
"""Fixed-parity closure terminal; semantic prototype, not a native RAM meter."""
import argparse, hashlib, itertools, json, random, signal, time
from pathlib import Path

def holds(cnf, x):
    return all(any(bool(x >> (abs(l)-1) & 1) == (l > 0) for l in c) for c in cnf)

def parity_ok(rows, x):
    return all((mask & x).bit_count() % 2 == b for mask, b in rows)

def brute(n, cnf, rows):
    return next((x for x in range(1 << n) if holds(cnf,x) and parity_ok(rows,x)), None)

def least_horn(n, cnf, pins, meter):
    x = pins
    for _ in range(n + 1):
        changed = False
        meter['passes'] += 1
        for c in cnf:
            meter['clauses'] += 1
            positives = [l for l in c if l > 0]
            assert len(positives) <= 1
            meter['literals'] += len(c)
            if all(x >> (-l-1) & 1 for l in c if l < 0):
                if not positives:
                    return None
                bit = 1 << (positives[0]-1)
                if not x & bit:
                    x |= bit
                    changed = True
        if not changed:
            return x
    raise AssertionError('closure exceeded n+1 scans')

def base_2sat(n, cnf, meter):
    # Dense reachability, no adjacency-list assumption or hidden SAT call.
    def idx(l): return 2*(abs(l)-1) + (l < 0)
    reach = [1 << i for i in range(2*n)]
    for c in cnf:
        meter['base_clause_reads'] += 1
        if not c: return None
        assert len(c) <= 2
        a,b = (c[0],c[0]) if len(c)==1 else c
        reach[idx(-a)] |= 1 << idx(b)
        reach[idx(-b)] |= 1 << idx(a)
    for k in range(2*n):
        for i in range(2*n):
            meter['reach_row_tests'] += 1
            if reach[i] >> k & 1: reach[i] |= reach[k]
    def conflict(bits):
        return any(bits >> (2*i) & 1 and bits >> (2*i+1) & 1 for i in range(n))
    if any(reach[2*i] >> (2*i+1) & 1 and reach[2*i+1] >> (2*i) & 1 for i in range(n)):
        return None
    chosen = 0
    for i in range(n):
        if chosen >> (2*i) & 3: continue
        trial = chosen | reach[2*i+1]
        chosen = chosen | reach[2*i] if conflict(trial) else trial
        assert not conflict(chosen)
    x = sum((bool(chosen >> (2*i) & 1)) << i for i in range(n))
    assert holds(cnf,x)
    return x

def solve(n, cnf, rows, kind='2sat', cap=None):
    meter = dict(passes=0, clauses=0, literals=0, candidates=0,
                 parity_bits=0, base_clause_reads=0, reach_row_tests=0,
                 recursive_sat_calls=0, executed_child_bits=0)
    if kind == '2sat':
        a = base_2sat(n,cnf,meter)
        if a is None: return 'UNSAT', None, meter
        horn = tuple(tuple(-l if a >> (abs(l)-1) & 1 else l for l in c) for c in cnf)
        shifted = tuple((mask,b ^ ((mask & a).bit_count()%2)) for mask,b in rows)
    else:
        a,horn,shifted = 0,cnf,rows
    assert all(sum(l>0 for l in c)<=1 for c in horn)
    for size in range(min(len(rows),n)+1):
        for subset in itertools.combinations(range(n),size):
            if cap is not None and meter['candidates'] >= cap:
                return 'UNKNOWN',None,meter
            meter['candidates'] += 1
            y = least_horn(n,horn,sum(1<<i for i in subset),meter)
            if y is None: continue
            meter['parity_bits'] += n*len(rows)
            if parity_ok(shifted,y):
                x = a ^ y
                assert holds(cnf,x) and parity_ok(rows,x)
                return 'SAT',x,meter
    return 'UNSAT',None,meter

def lin_solve(n, rows):
    basis = {}
    for mask,b in rows:
        while mask:
            p=mask.bit_length()-1
            if p not in basis:
                basis[p]=(mask,b); break
            q,c=basis[p]; mask^=q; b^=c
        if not mask and b: return None
    x=0
    for p,(mask,b) in sorted(basis.items()):
        if ((mask & x).bit_count()%2)^b: x ^= 1<<p
    return x

def project_affine(n, cnf, rows):
    # Explicit Gaussian parametrization. This stage retains polynomial state.
    particular=lin_solve(n,rows)
    if particular is None: return None
    basis={}
    for mask,b in rows:
        while mask:
            p=mask.bit_length()-1
            if p not in basis: basis[p]=(mask,b); break
            q,c=basis[p]; mask^=q; b^=c
    free=[i for i in range(n) if i not in basis]
    vectors=[0]*n
    for j,i in enumerate(free): vectors[i]=1<<j
    for p,(mask,b) in sorted(basis.items()):
        v=0
        for i in range(p):
            if mask>>i&1: v ^= vectors[i]
        vectors[p]=v
    obs=sorted({vectors[abs(l)-1] for c in cnf for l in c} - {0})
    ids={v:j+1 for j,v in enumerate(obs)}
    converted=[]
    for c in cnf:
        new=[]; satisfied=False
        for l in c:
            i=abs(l)-1; const=bool(particular>>i&1); v=vectors[i]
            if not v:
                if const == (l>0): satisfied=True; break
            else:
                new.append(ids[v] if (l>0)^const else -ids[v])
        if not satisfied: converted.append(tuple(new))
    deps=[]; vbasis={}
    for j,v in enumerate(obs):
        comb=1<<j
        while v:
            p=v.bit_length()-1
            if p not in vbasis: vbasis[p]=(v,comb); break
            q,c=vbasis[p]; v^=q; comb^=c
        if not v: deps.append((comb,0))
    return len(obs),tuple(converted),tuple(deps),particular,vectors,obs,len(free)

def mixed(n,cnf,rows,e_cap):
    p=project_affine(n,cnf,rows)
    if p is None: return 'UNSAT',None,{'affine_inconsistent':True}
    k,c,deps,a,vectors,obs,free=p
    if len(deps)>e_cap: return 'UNKNOWN',None,{'e':len(deps)}
    status,u,meter=solve(k,c,deps)
    meter['e']=len(deps)
    if status=='SAT':
        t=lin_solve(free,[(v,u>>j&1) for j,v in enumerate(obs)])
        assert t is not None
        x=a
        for i,v in enumerate(vectors):
            if (v&t).bit_count()%2: x ^= 1<<i
        assert holds(cnf,x) and parity_ok(rows,x)
        return status,x,meter
    return status,None,meter

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--suite',choices=['relations','solver','mixed','cost'],required=True)
    parser.add_argument('--output',required=True); args=parser.parse_args()
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('24-second budget')))
    signal.alarm(24); started=time.monotonic(); rng=random.Random(202610291150)
    result={'suite':args.suite,'seed':202610291150,'failures':0,'scope':'finite semantic tests, not native bit-cost benchmark'}
    if args.suite=='relations':
        families=checks=0
        for raw in range(1,256):
            rel=[x for x in range(8) if raw>>x&1]
            if any((x&y) not in rel for x in rel for y in rel): continue
            families+=1
            candidates=[]
            for s in range(8):
                if s.bit_count()>2: continue
                above=[x for x in rel if x&s==s]
                if above:
                    z=7
                    for x in above:z&=x
                    candidates.append(z)
            for m1,m2,b in itertools.product(range(8),range(8),range(4)):
                rows=((m1,b&1),(m2,b>>1))
                assert any(parity_ok(rows,x) for x in rel)==any(parity_ok(rows,x) for x in candidates)
                checks+=1
        result.update(meet_closed_families=families,two_parity_checks=checks)
    elif args.suite=='solver':
        totals={'SAT':0,'UNSAT':0}; cases=0; max_candidates=0
        for kind in ('2sat','horn'):
            for n in range(1,9):
                for _ in range(100):
                    cnf=[]
                    for j in range(rng.randrange(0,4*n+1)):
                        width=rng.randint(1,min(n,2 if kind=='2sat' else 3))
                        support=rng.sample(range(1,n+1),width)
                        c=tuple(i*rng.choice([-1,1]) for i in support)
                        if kind=='horn' and sum(l>0 for l in c)>1:
                            c=tuple(-abs(l) for l in c)
                        cnf.append(c)
                    rows=tuple((rng.randrange(1<<n),rng.randrange(2)) for _ in range(rng.randrange(4)))
                    expected=brute(n,cnf,rows)
                    status,x,met=solve(n,cnf,rows,kind)
                    assert (status=='SAT')==(expected is not None)
                    totals[status]+=1; cases+=1; max_candidates=max(max_candidates,met['candidates'])
        # Joint-feasibility and tight e=2 pin controls.
        cnf=((-1,-2),); rows=((1,1),(2,1))
        assert all(brute(2,cnf,[r]) is not None for r in rows)
        assert solve(2,cnf,rows)[0]=='UNSAT'
        s,x,met=solve(2,(),rows,'horn'); assert s=='SAT' and met['candidates']==4
        assert solve(2,(),rows,'horn',cap=3)[0]=='UNKNOWN'
        # Representation controls: duplication, order, complements, permutation.
        controls=0
        for _ in range(100):
            n=5; cnf=[tuple(rng.choice([-1,1])*i for i in rng.sample(range(1,6),2)) for j in range(8)]
            rows=[(rng.randrange(32),rng.randrange(2)) for j in range(2)]
            truth=solve(n,cnf,rows)[0]
            assert solve(n,cnf+list(reversed(cnf)),rows)[0]==truth; controls+=1
            flip=rng.randrange(32)
            cs=[tuple(-l if flip>>(abs(l)-1)&1 else l for l in c) for c in cnf]
            rs=[(m,b^((m&flip).bit_count()%2)) for m,b in rows]
            assert solve(n,cs,rs)[0]==truth; controls+=1
            perm=list(range(n));rng.shuffle(perm)
            cs=[tuple((1 if l>0 else -1)*(perm[abs(l)-1]+1) for l in c) for c in cnf]
            rs=[(sum(1<<perm[i] for i in range(n) if m>>i&1),b) for m,b in rows]
            assert solve(n,cs,rs)[0]==truth;controls+=1
        result.update(cases=cases,answers=totals,max_candidates=max_candidates,representation_controls=controls,
                      joint_marginal_false_positive_rejected=True,two_pins_necessary=True,capped_unknown_verified=True)
    elif args.suite=='cost':
        records=[]
        for n in (8,16,32,64,128,256,512):
            cnf=tuple((-i,) for i in range(1,n+1))
            rows=(((1<<n)-1,1),)
            status,_,met=solve(n,cnf,rows,'horn')
            assert status=='UNSAT' and met['clauses']==n*(n+3)//2
            assert met['candidates']==n+1
            records.append({'n':n,'clause_reads':met['clauses'],'candidates':met['candidates'],
                            'formula':'all negative units, odd global parity'})
        result.update(records=records,naive_near_linear_promotion='FALSIFIED for this implementation only')
    else:
        answers={'SAT':0,'UNSAT':0,'UNKNOWN':0}; cases=0; es={}
        for n in range(2,9):
            for _ in range(120):
                rows=[(rng.randrange(1<<n),rng.randrange(2)) for j in range(rng.randrange(n+1))]
                cnf=[tuple(i*rng.choice([-1,1]) for i in rng.sample(range(1,n+1),rng.randint(1,2))) for j in range(rng.randrange(3*n))]
                status,x,met=mixed(n,cnf,rows,2);expected=brute(n,cnf,rows)
                if status!='UNKNOWN':assert (status=='SAT')==(expected is not None)
                answers[status]+=1;cases+=1;e=str(met.get('e','inconsistent'));es[e]=es.get(e,0)+1
        # 2SAT + XOR3 selectors exactly encodes every subset of eight 3-clauses.
        source_clauses=list(itertools.product((-1,1),(-2,2),(-3,3)))
        for bits in range(256):
            source=[c for j,c in enumerate(source_clauses) if bits>>j&1]
            cnf=[];rows=[];n=3
            for c in source:
                sel=[n+1,n+2,n+3];n+=3
                rows.append((sum(1<<(s-1) for s in sel),1))
                cnf.extend((-s,-t) for s,t in itertools.combinations(sel,2))
                cnf.extend((-s,l) for s,l in zip(sel,c))
            # Verify every original assignment via independent local selector
            # extensions. Do not run the growing-e algorithm exponentially.
            for x in range(8):
                extendable=True
                for c in source:
                    local=any(s.bit_count()==1 and all(not(s>>j&1) or
                        bool(x>>(abs(l)-1)&1)==(l>0) for j,l in enumerate(c))
                        for s in range(8))
                    extendable &= local
                assert extendable == holds(source,x)
        result.update(cases=cases,answers=answers,dependency_distribution=es,unbounded_rank_selector_controls=256)
    result['elapsed_seconds']=round(time.monotonic()-started,6)
    result['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
