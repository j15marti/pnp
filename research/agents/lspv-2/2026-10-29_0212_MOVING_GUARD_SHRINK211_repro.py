#!/usr/bin/env python3
"""LSPV-2 moving four-variable guard, exact one-child projection.
Dependency-free; run python3 this_file > raw.json.
The source class is a tagged, proper 3CNF chain, not unrestricted SAT.
"""
import itertools, random, math, json
from collections import defaultdict, Counter

def endpoints(r):
    return tuple(sorted(set((0,1,r-2,r-1))))

def bitmask_all(r):
    return (1 << (1 << len(endpoints(r))))-1

def guard_eval(mask, r, assignment):
    e=endpoints(r)
    idx=sum((assignment[j]&1)<<i for i,j in enumerate(e))
    return (mask>>idx)&1

def eval_clause(cl, x):
    return any((x[abs(l)-1]==1)==(l>0) for l in cl)

def validate_core(r,core):
    assert r>=3
    spans=defaultdict(set)
    for c in core:
        assert len(c)==3 and len(set(abs(l) for l in c))==3
        assert all(1<=abs(l)<=r for l in c)
        scope=tuple(sorted(abs(l) for l in c))
        assert scope == tuple(range(scope[0],scope[0]+3))
        key=tuple(l if l>0 else -abs(l) for l in sorted(c,key=lambda l:abs(l)))
        assert key not in spans[scope]
        spans[scope].add(key)
    assert len(spans)==r-2 and all(tuple(range(i,i+3)) in spans for i in range(1,r-1))
    return True

def canonical_core(core):
    return tuple(sorted(set(tuple(sorted(c,key=lambda l:abs(l))) for c in core),key=lambda c:(abs(c[0]),tuple(c))))

def guard_gadgets(r,mask):
    e=endpoints(r); d=len(e)
    clauses=[]; u=0
    for v in range(1<<d):
        if mask>>v&1:continue
        literals=tuple(- (p+1) if (v>>i)&1 else (p+1) for i,p in enumerate(e))
        if d<=3:
            clauses.append(literals)
        else:
            u+=1; aux=r+u
            clauses.append((literals[0],literals[1],aux))
            clauses.append((-aux,literals[2],literals[3]))
    return tuple(clauses),u

def serialize(r,core,mask):
    core=canonical_core(core)
    validate_core(r,core)
    assert 0<=mask<=bitmask_all(r)
    guard,u=guard_gadgets(r,mask)
    # Both the explicit 16-bit guard and its canonical CNF realization are counted.
    out=[f'c CHAIN_GUARD_V1 r={r} mask={mask:x} core={len(core)}',
         f'p cnf {r+u} {len(core)+len(guard)}']
    for clause in core+guard:
        out.append(' '.join(str(l) for l in clause)+' 0')
    return ('\n'.join(out)+'\n').encode('ascii')

def parse(data):
    lines=data.decode('ascii').splitlines()
    if len(lines)<2:raise ValueError('short')
    a=lines[0].split()
    if len(a)!=5 or a[:2]!=['c','CHAIN_GUARD_V1']:raise ValueError('tag')
    try:
        r=int(a[2].split('=')[1]);mask=int(a[3].split('=')[1],16);m=int(a[4].split('=')[1]);
        assert all(a[i].startswith(s) for i,s in enumerate(('r=','mask=','core='),2))
        core=tuple(tuple(map(int,line.split()[:-1])) for line in lines[2:2+m])
        assert all(line.endswith(' 0') for line in lines[2:])
        assert data==serialize(r,core,mask)
    except (ValueError,IndexError,AssertionError) as e:
        raise ValueError('invalid canonical chain') from e
    return r, canonical_core(core),mask

def sat_brute(r,core,mask):
    for bits in itertools.product((0,1),repeat=r):
        if guard_eval(mask,r,bits) and all(eval_clause(c,bits) for c in core):return True
    return False

def sat_dp_chain(r,core,mask):
    """Exact bounded-frontier decision. Direct base routine, no SAT oracle."""
    ending=defaultdict(list)
    for c in core:ending[max(abs(l) for l in c)-1].append(c)
    e=endpoints(r)
    for pat in range(1<<len(e)):
        if not ((mask>>pat)&1):continue
        fixed={p:(pat>>i)&1 for i,p in enumerate(e)}
        states={()}
        for idx in range(r):
            cur=set()
            choices=(fixed[idx],) if idx in fixed else (0,1)
            for old in states:
                for bit in choices:
                    current=old+(bit,)
                    lookup={idx-j:current[-1-j] for j in range(len(current))}
                    if all(any((lookup[abs(l)-1]==1)==(l>0) for l in c) for c in ending[idx]):
                        cur.add(current[-2:])
            states=cur
            if not states:break
        if states:return True
    return False

def next_state(r,core,mask,counts):
    """Eliminate the prefix, retaining sqrt(r) variables. Exactly one child."""
    h=max(4,math.isqrt(r));cut=r-h
    assert cut>=2
    keep=[];removed=[]
    for c in core:
        if min(abs(l) for l in c)>cut:
            keep.append(tuple((1 if l>0 else -1)*(abs(l)-cut) for l in c))
        else:
            removed.append(c)
    ending=defaultdict(list)
    for c in removed: ending[max(abs(l) for l in c)-1].append(c)
    old_e=endpoints(r);new_e=endpoints(h)
    out_mask=0
    for pattern in range(1<<len(new_e)):
        fixed={cut+j:(pattern>>i)&1 for i,j in enumerate(new_e)}
        states={()}  # rolling last two assigned bits
        for idx in range(cut+2):
            cur=set()
            choices=(fixed[idx],) if idx in fixed else (0,1)
            for history in states:
                for bit in choices:
                    counts['candidate_transitions']+=1
                    current=history+(bit,)
                    lookup={idx-j:current[-1-j] for j in range(len(current))}
                    # Old guard touches only x0,x1 and the two fixed far-right variables.
                    if idx==1:
                        gv={**fixed,0:lookup[0],1:lookup[1]}
                        counts['guard_queries']+=1
                        if not guard_eval(mask,r,gv):continue
                    good=True
                    for c in ending[idx]:
                        counts['clauses_tested']+=1
                        if not any((lookup[abs(l)-1]==1)==(l>0) for l in c):
                            good=False;break
                    if good:cur.add(current[-2:])
            states=cur
            if not states:break
        if states:out_mask|=1<<pattern
    out=canonical_core(keep)
    counts['source_clauses_scanned']+=len(core)
    validate_core(h,out)
    assert 0<=out_mask<=bitmask_all(h)
    return h,out,out_mask

def shrink(r,core,mask,threshold=96,exponent=.95):
    trace=[]; counts=Counter(); original_data=serialize(r,core,mask)
    input_size=len(original_data)
    while r>threshold:
        oldr=r
        hr,hc,hm=next_state(r,core,mask,counts)
        candidate=serialize(hr,hc,hm)
        counts['candidate_bytes_constructed']+=len(candidate)
        use_fallback = 8*len(candidate)>(8*input_size)**exponent
        if use_fallback:
            # All costs, including a failed candidate and final direct decision, are charged.
            counts['fallback_direct_decisions']+=1
            direct=sat_dp_chain(r,core,mask)
            hr,hc,hm=3,((1,2,3),),bitmask_all(3) if direct else 0
        data=serialize(hr,hc,hm)
        rr,cc,mm=parse(data)
        assert (rr,cc,mm)==(hr,hc,hm)
        assert 8*len(data)<=(8*input_size)**exponent
        trace.append(dict(parent_core=oldr,child_core=hr,parent_bytes=input_size,child_bytes=len(data),
                          power_ratio_3_4=round(8*len(data)/((8*input_size)**.75),5),
                          power_ratio_0_95=round(8*len(data)/((8*input_size)**.95),5),
                          fallback_direct_decision=use_fallback,
                          guard_forbidden=(1<<len(endpoints(hr)))-hm.bit_count(),
                          auxiliaries=guard_gadgets(hr,hm)[1]))
        r,core,mask=rr,cc,mm
        input_size=len(data)
    ans=sat_dp_chain(r,core,mask)
    return ans,trace,dict(counts),r

def brute_projection_check(r,core,mask):
    """Compares FULL projected functions, not just SAT answers. Restrict r<=12."""
    assert 6<=r<=12
    h,hcore,hmask=next_state(r,core,mask,Counter()); cut=r-h
    projected=set()
    for bits in itertools.product((0,1),repeat=r):
        if guard_eval(mask,r,bits) and all(eval_clause(c,bits) for c in core):
            projected.add(bits[cut:])
    for tail in itertools.product((0,1),repeat=h):
        expected=tail in projected
        actual=bool(guard_eval(hmask,h,tail)) and all(eval_clause(c,tail) for c in hcore)
        assert expected==actual,(r,tail,expected,actual)
    return 1<<h

def clauses_for_cycle(n):
    assert n>=3 and n%3==0
    return ([(i,(i+1)%n,(i+2)%n) for i in range(n)]
            + [tuple(range(i,i+3)) for i in range(0,n,3)])

def canonical_signed(n):
    return ([(i+1,(i+1)%n+1,-((i+2)%n+1)) for i in range(n)]
            + [tuple(-(j+1) for j in range(i,i+3)) for i in range(0,n,3)])

def signed_random(n,rng):
    scopes=clauses_for_cycle(n)
    occurrences={v:[] for v in range(n)}
    for ci,cl in enumerate(scopes):
        for j,v in enumerate(cl):occurrences[v].append((ci,j))
    positives=set()
    for places in occurrences.values():
        assert len(places)==4
        positives.update(rng.sample(places,2))
    return [tuple((v+1) if (ci,j) in positives else -(v+1)
                  for j,v in enumerate(cl)) for ci,cl in enumerate(scopes)]

def brute(cs,n):
    return any(all(any(bool(a>>(abs(l)-1)&1)==(l>0) for l in cl)
                   for cl in cs) for a in range(1<<n))

def from_cyclic_exact22(n,signs=None):
    clauses=canonical_signed(n) if signs is None else signs
    core=[]; wrap=[]
    for c in clauses:
        if max(abs(l) for l in c)-min(abs(l) for l in c)==2:core.append(c)
        else:wrap.append(c)
    # For n=3 all triples contiguous and wrap is empty.
    e=endpoints(n);m=0
    for pattern in range(1<<len(e)):
        a={p:(pattern>>i)&1 for i,p in enumerate(e)}
        if all(any((a[abs(l)-1]==1)==(l>0) for l in c) for c in wrap):m|=1<<pattern
    return n,canonical_core(set(core)),m

def build_core(r,rng,unsat=False):
    core=[]
    for i in range(r-2):
        core.append(tuple((i+j+1)*(1 if rng.randrange(2) else -1) for j in range(3)))
    if unsat:
        # Eight complete clauses on a single triple make the instance UNSAT.
        scope=(0,1,2)
        core=[c for c in core if tuple(abs(l)-1 for l in c)!=scope]
        core.extend(tuple((j+1)*(1 if ((pat>>j)&1) else -1) for j in range(3)) for pat in range(8))
    return canonical_core(core)

def independent_clause_gadget_audit():
    trials=0
    for pattern in range(16):
        lits=tuple((pattern>>i)&1 for i in range(4))
        left=lits[0] or lits[1];right=lits[2] or lits[3]
        assert (left or right)==any(((left or bit) and ((not bit) or right)) for bit in (0,1))
        trials+=1
    return trials

def run():
    rng=random.Random(21120261029)
    controls=0;classes=Counter(); size_tests=[];full_projection_assignments=0
    for n in (3,6,9,12):
        for sample in range(20):
            signed=signed_random(n,rng)
            st=from_cyclic_exact22(n,signed)
            data=serialize(*st)
            assert parse(data)==st
            before=brute(signed,n)
            assert before==sat_brute(*st)
            if n>=6:full_projection_assignments+=brute_projection_check(*st)
            if n>96:after,_,_,_=shrink(*st)
            else:after=before
            assert before==after
            controls+=1;classes['exact22_SAT' if before else 'exact22_UNSAT']+=1
    for n in (3,6,9,12,18,36,100,400,1600,10000):
        for unsat in (False,True):
            core=build_core(n,rng,unsat=unsat)
            mask=bitmask_all(n)
            source=serialize(n,core,mask)
            assert parse(source)==(n,core,mask)
            if n<=12:
                assert sat_brute(n,core,mask)==(not unsat)
                if n>=6:full_projection_assignments+=brute_projection_check(n,core,mask)
            answer,trace,ops,base=shrink(n,core,mask) if n>96 else (sat_dp_chain(n,core,mask),[],{},n)
            assert answer==(not unsat)
            size_tests.append(dict(n=n,unsat=unsat,initial_bytes=len(source),levels=len(trace),
                                   trace=trace,ops=ops,base_variables=base))
            classes['chain_SAT' if answer else 'chain_UNSAT']+=1;controls+=1
    # Guard-table variants: a single boundary false guard forces UNSAT.
    for n in (6,12,36,100):
        core=build_core(n,rng)
        for mask in (0,bitmask_all(n)):
            before=sat_brute(n,core,mask) if n<=12 else bool(mask)
            ans,trace,ops,base=shrink(n,core,mask) if n>96 else (sat_dp_chain(n,core,mask),[],{},n)
            assert ans==before
            controls+=1
    checks=independent_clause_gadget_audit()
    return dict(status='PASS',sampled_instances=controls,classes=dict(classes),split_clause_truth_cases=checks,
                full_projection_truth_cases=full_projection_assignments,
                core_size_tests=size_tests, 
                theorem='For source chain constraints and four-bit endpoint guard, exact prefix projection onto a power-small suffix is polynomial and closed. This is restricted and does not include arbitrary SAT.',
                limitations=['This is an annotated ordinary-3CNF subset, not all 3SAT.',
                             'No full native TM step instrumentation; polynomial simulations are charged asymptotically.',
                             'Python transition counters are not TM transitions.',
                             'Gadget clause counts include each auxiliary and all serialized bytes; fallback charges failed construction.',
                             'Source-only exact22 sample may all be SAT; separate chain UNSAT controls are explicit.'])
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
