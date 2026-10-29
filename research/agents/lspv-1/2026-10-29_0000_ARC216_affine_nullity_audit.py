#!/usr/bin/env python3
"""ARC216: dependency-free exact mixed 2CNF/GF(2) projection and nullity audit.
This is a mathematical control implementation, NOT a charged physical TM simulator.
"""
import itertools, json, random, hashlib
from collections import defaultdict
from pathlib import Path

SEED = 2026102900
rng = random.Random(SEED)


def canonical(clause):
    s = set(clause)
    if any(-a in s for a in s):
        return None  # tautology
    assert all(x and isinstance(x,int) for x in s)
    assert len(s) <= 2
    return tuple(sorted(s, key=lambda x:(abs(x),x)))


def evaluate(cnf, rows, bits):
    c = all(any(((bits >> (abs(l)-1)) & 1) == (l > 0) for l in cl) for cl in cnf)
    a = all(((bits & mask).bit_count() & 1) == rhs for mask,rhs in rows)
    return c and a


def source_variables(cnf,rows):
    cvars = {abs(l)-1 for cl in cnf for l in cl}
    avars = {i for mask,_ in rows for i in range(mask.bit_length()) if mask & (1<<i)}
    return cvars, avars


def project_cnf(cnf, private, stats):
    clauses = {v for cl in cnf if (v:=canonical(cl)) is not None}
    for v in sorted(private):
        lit = v+1
        pos = [tuple(z for z in cl if z!=lit) for cl in clauses if lit in cl]
        neg = [tuple(z for z in cl if z!=-lit) for cl in clauses if -lit in cl]
        rest = {cl for cl in clauses if lit not in cl and -lit not in cl}
        for a in pos:
            for b in neg:
                stats['resolvent_trials'] += 1
                p = canonical(a+b)
                if p is not None: rest.add(p)
        clauses = rest
        stats['peak_clause_count'] = max(stats['peak_clause_count'],len(clauses))
    return sorted(clauses, key=lambda c:(len(c),c))


def project_rows(rows,private,stats):
    a = list(rows)
    for v in sorted(private):
        pivot = next((j for j,(mask,_) in enumerate(a) if mask & (1<<v)),None)
        if pivot is None: continue
        pm,pr = a.pop(pivot)
        new=[]
        for mask,rhs in a:
            if mask & (1<<v):
                mask ^= pm
                rhs ^= pr
                stats['xor_ops'] += 1
            new.append((mask,rhs))
        a = new
    return a


def rref(rows,b,stats):
    a = list(rows)
    pivots=[]
    h=0
    for col in range(b):
        pivot = next((j for j in range(h,len(a)) if a[j][0]&(1<<col)),None)
        if pivot is None: continue
        a[h],a[pivot] = a[pivot],a[h]
        pm,pr = a[h]
        for j in range(len(a)):
            if j!=h and (a[j][0]&(1<<col)):
                a[j]=(a[j][0]^pm,a[j][1]^pr)
                stats['xor_ops'] += 1
        pivots.append(col)
        h+=1
    if any(mask==0 and rhs for mask,rhs in a):
        return None,[],[]
    a=a[:h]
    z0=sum(rhs<<col for (mask,rhs),col in zip(a,pivots))
    free=[i for i in range(b) if i not in pivots]
    basis=[]
    for j in free:
        v=1<<j
        for (mask,rhs),col in zip(a,pivots):
            if mask & (1<<j): v|=1<<col
        basis.append(v)
    return z0,basis,a


def decide(cnf,rows, n, return_relation=False):
    stats={'resolvent_trials':0,'peak_clause_count':len(cnf),'xor_ops':0,'checked_candidates':0}
    cv,av=source_variables(cnf,rows)
    shared=sorted(cv & av)
    cproj=project_cnf(cnf, cv-set(shared),stats)
    aproj=project_rows(rows,av-set(shared),stats)
    rep={v:i for i,v in enumerate(shared)}
    zcnf=[]
    for cl in cproj:
        zcnf.append(tuple((1 if l>0 else -1)*(rep[abs(l)-1]+1) for l in cl))
    zrows=[]
    for mask,rhs in aproj:
        zmask=0
        for old,new in rep.items():
            if mask&(1<<old):zmask|=1<<new
        zrows.append((zmask,rhs))
    z0,basis,rred=rref(zrows,len(shared),stats)
    stats['shared_bits']=len(shared)
    stats['nullity']=len(basis)
    stats['rank']=len(shared)-len(basis) if z0 is not None else None
    stats['n']=n
    stats['source_encoded_bytes']=len(json.dumps({'n':n,'cnf':cnf,'xor':rows},separators=(',',':')).encode())
    stats['projection_encoded_bytes']=len(json.dumps({'n':len(shared),'cnf':zcnf,'xor':rred},separators=(',',':')).encode())
    if z0 is None:
        if return_relation:
            stats['projected_cnf']=zcnf
            stats['projected_xor']=zrows
            stats['shared_names']=shared
        stats['answer']=False
        stats['affine_inconsistent']=True
        return stats
    stats['affine_inconsistent']=False
    if return_relation:
        stats['projected_cnf']=zcnf
        stats['projected_xor']=zrows
        stats['shared_names']=shared
    for i in range(1<<len(basis)):
        zz=z0
        for j,v in enumerate(basis):
            if i&(1<<j): zz^=v
        stats['checked_candidates']+=1
        if evaluate(zcnf,[],zz):
            stats['answer']=True
            break
    else:
        stats['answer']=False
    return stats


def brute(cnf,rows,n):
    return any(evaluate(cnf,rows,x) for x in range(1<<n))


def case_random(n):
    cm=rng.randrange(0,n*3+1)
    xm=rng.randrange(0,n*2+1)
    cnf=[]
    for _ in range(cm):
        size=rng.choice((1,min(2,n)))
        vs=rng.sample(range(n),size)
        cnf.append(tuple((v+1)*rng.choice((-1,1)) for v in vs))
    rows=[]
    for _ in range(xm):
        length=rng.randrange(0,n+1)
        vs=rng.sample(range(n),length)
        mask=sum(1<<v for v in vs)
        rows.append((mask,rng.randrange(2)))
    return cnf,rows


def gadget(clauses):
    # arbitrary clauses use exactly three original signed literals on x1,x2,x3
    rows=[]; cnf=[]
    for k,cl in enumerate(clauses):
        yy=[4+3*k+j for j in range(3)]
        for l,y in zip(cl,yy):cnf.append((l,y))
        rows.append((sum(1<<(y-1) for y in yy),0))
    return cnf,rows,3+3*len(clauses)


def run():
    result={'status':'PASS','seed':SEED,'random_tests':0,'exact_projection_checks':0,'gadget_tests':[],
            'low_nullity_controls':[],'high_nullity_controls':[],'side_totals':{'SAT':0,'UNSAT':0}}
    # Every random case is compared with exhaustive 2^n source truth table.
    for n in range(1,9):
        for _ in range(90):
            c,a=case_random(n)
            got=decide(c,a,n)
            want=brute(c,a,n)
            assert got['answer']==want,(n,c,a,got)
            result['random_tests']+=1
            result['side_totals']['SAT' if want else 'UNSAT']+=1
    # Exhaustive truth of projected relation for one private-heavy case, using source assignments.
    for n in (4,5,6,7):
        for _ in range(40):
            c,a=case_random(n)
            cv,av=source_variables(c,a)
            shared=sorted(cv&av)
            projection=decide(c,a,n,return_relation=True)
            # Pointwise existential-extension comparison at EVERY shared assignment.
            # This is stricter than comparing only the final SAT bit.
            source_relation=set()
            for assignment in range(1<<n):
                if evaluate(c,a,assignment):
                    z=sum(((assignment>>old)&1)<<i for i,old in enumerate(shared))
                    source_relation.add(z)
            for z in range(1<<len(shared)):
                projected=evaluate(projection['projected_cnf'],projection['projected_xor'],z)
                assert projected==(z in source_relation),(n,c,a,shared,z)
                result['exact_projection_checks']+=1
            assert projection['answer']==bool(source_relation)
    eight=[tuple((v+1)*(1 if (mask>>v)&1 else -1) for v in range(3)) for mask in range(8)]
    for m in (1,2,3,4,8):
        c,a,n=gadget(eight[:m])
        got=decide(c,a,n)
        original_sat=any(all(any(((xb>>(abs(l)-1))&1)==(l>0) for l in cl) for cl in eight[:m]) for xb in range(8))
        assert got['answer']==original_sat
        assert got['shared_bits']==3*m and got['rank']==m and got['nullity']==2*m
        result['gadget_tests'].append({'clauses':m,'shared':3*m,'rank':m,'nullity':2*m,
                                       'SAT':got['answer'],'candidates_checked':got['checked_candidates']})
    for b,r in ((12,0),(20,0),(40,0),(40,1),(40,3)):
        # All b original interface names really occur in both languages.
        # For r private-paired variables, existential projection removes
        # the 2CNF and affine private auxiliaries, leaving r free shared bits.
        c=[(-(i+1),) for i in range(b-r)]
        a=[(1<<i, 1 if i==0 else 0) for i in range(b-r)]
        for j,i in enumerate(range(b-r,b)):
            c.append((i+1, b+j+1))
            a.append(((1<<i)|(1<<(b+r+j)),0))
        got=decide(c,a,b+2*r)
        assert got['shared_bits']==b
        assert got['rank']==b-r and got['nullity']==r
        assert not got['answer'] and got['checked_candidates']==1<<r
        result['low_nullity_controls'].append({'b_requested':b,'r_requested':r,'shared':got['shared_bits'],
                                                'nullity':got['nullity'],'candidates':got['checked_candidates'],
                                                'source_bytes':got['source_encoded_bytes'],'child_bytes':got['projection_encoded_bytes']})
    for b in (8,12):
        # affine parity odd, all shared bits forced zero in 2CNF. UNSAT but naive enumerator visits all 2^(b-1).
        c=[(-(i+1),) for i in range(b)]
        a=[((1<<b)-1,1)]
        got=decide(c,a,b)
        assert got['shared_bits']==b and got['nullity']==b-1
        assert not got['answer'] and got['checked_candidates']==1<<(b-1)
        result['high_nullity_controls'].append({'shared':b,'rank':1,'nullity':b-1,'candidates':got['checked_candidates']})
    # A single affine substitution can destroy bijunctive (2CNF) semantics.
    # Relation f(u,v,w) := (u XOR v) OR w is not closed under majority.
    witnesses=[(0,1,0),(1,0,0),(0,0,1)]
    def f(t): return bool((t[0]^t[1]) or t[2])
    majority=tuple(int(sum(t[i] for t in witnesses)>=2) for i in range(3))
    assert all(f(t) for t in witnesses) and not f(majority)
    result['majority_closure_falsifier']={'satisfying_witnesses':witnesses,'majority':majority,
        'majority_satisfies':f(majority),'conclusion':'not equivalent to any existential projection of 2CNF'}
    result['proof_status']=['PROVED/RESTRICTED by independent algebra (not by tests)',
                             'COMPUTATIONAL: controls only','OPEN: all-input polynomial nullity or universal contraction']
    Path(__file__).with_name('ARC216_affine_nullity_raw.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':run()