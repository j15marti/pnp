#!/usr/bin/env python3
"""Independent raw-record checker for ARC-KRAFT-CERTIFIED-COVER252.
Does not import the producing module; reconstructs formulas from the raw data.
"""
import itertools,json,math,random,collections
from pathlib import Path
from fractions import Fraction
raw=Path(__file__).with_name('2026-10-30_1300_LSPV-1_ARC_KRAFT_CERTIFIED_COVER252_raw.json')
data=json.loads(raw.read_text())
checks=collections.Counter()
for row in data['cases']:
    F=[tuple(c['clause']) for c in row['extremes']['all_occurrences']]
    n=row['UP']['n'];m=len(F)
    assert m==row['source_clause_count']
    for j,c in enumerate(F):
        assert len({abs(x) for x in c})==len(c)
        for l,d in zip(c,row['extremes']['all_occurrences'][j]['occurrences']):
            assert abs(l)==d['x']
            assert d['S']==int(l>0) and d['invert_S_is_U']==int(l<0)
            assert d['U']==int(l<0) and d['invert_U_is_S']==int(l>0)
            checks['signed_occurrence']+=1
    for p in row['extremes']['matrix']:
        C,D=F[p['j']],F[p['i']]
        for mode in ('SS','SU','US','UU'):
            forced=[]
            for clause,stage in ((C,mode[0]),(D,mode[1])):
                forced += [(abs(l),(l>0)==(stage=='S')) for l in clause]
            possible=all(v1!=v2 or b1==b2 for (v1,b1),(v2,b2) in itertools.combinations(forced,2))
            assert possible == p[mode]
            checks['matrix']+=1
    models=0
    for bits in itertools.product((False,True),repeat=n):
        a={i+1:bits[i] for i in range(n)}
        sat=all(any(a[abs(l)]==(l>0) for l in c) for c in F)
        models+=sat
        checks['full_assignments']+=1
    assert models==row['models']
    for trial in row['extremes']['flip_trails']:
        a={v:bool(trial['base']) for v in range(1,n+1)}
        for v in trial['flips']:
            if v<=n:a[v]=not a[v]
        counts=[sum(a[abs(l)]==(l>0) for l in c) for c in F]
        assert counts==trial['clause_counts']
        assert [counts.count(i) for i in range(4)]==trial['N']
        assert trial['SAT']==all(c>0 for c in counts)
        inv=[len(c)-k for c,k in zip(F,counts)]
        assert [inv.count(i) for i in range(4)]==trial['complement_N']
        checks['flip_trails']+=1
    cert=row['resolvent_certificate']
    if cert:
        j,k=cert['source_clause_indices'];pivot=cert['pivot_variable'];R=set(cert['resolvent'])
        candidates=[]
        for z in (pivot,-pivot):
            if z in F[j] and -z in F[k]:
                candidates.append(set(F[j]+F[k])-{z,-z})
        assert R in candidates and not any(-l in R for l in R)
        cube=dict(cert['falsifying_cube'])
        assert all(cube[abs(l)]==(l<0) for l in R)
        checks['derived_resolvent']+=1
    for mode in ('bare','UP'):
        d=row[mode];assert d['SAT']==(models>0)
        total=sum((Fraction(d[k]) for k in ('source_cert_NO_mass','source_cert_YES_mass',
              'guest_NO_mass','guest_YES_mass')),Fraction(0))
        assert total==1
        ctr=d['ledger'];q=ctr.get('guest_completed_calls',0)
        deg=collections.Counter(abs(l) for c in F for l in c)
        Delta=max(deg.values()) if deg else 0
        h=2+3*(1+math.ceil(math.log2(n+1)))
        k=max(0,math.ceil((m-(math.isqrt(m*h)//h))/Delta)) if Delta else 0
        assert d['k_floor']==k and d['max_variable_clause_degree']==Delta
        assert Fraction(d['guest_NO_mass'])+Fraction(d['guest_YES_mass'])<=Fraction(q,2**k)
        if not d['SAT']:
            assert Fraction(d['source_cert_NO_mass'])>=1-Fraction(q,2**k)
        else:
            w=dict(d['witness'])
            assert all(any(w[abs(l)]==(l>0) for l in c) for c in F)
        checks['mass_decompositions']+=1
# Confirm gadget source-independent pattern and exact 3-step resolution.
for item in data['gadget_forced_literals']:
    x=item['forced_variable'];j=(x-4)//3;u=x+1;v=x+2
    sources=[(x,u,v),(x,u,-v),(x,-u,v),(x,-u,-v)]
    assert set(sources[0]+sources[1])-{v,-v}=={x,u}
    assert set(sources[2]+sources[3])-{v,-v}=={x,-u}
    assert {x,u,-u}-{u,-u}=={x}
    checks['gadget_resolution']+=1
# Recreate seeded randomized cases independently and compare SAT labels.
rng=random.Random(data['random_seed']);sat=0
for expected in data['random_controls']:
    n=rng.randint(3,8);m=rng.randint(3,18)
    F=[tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),3)) for _ in range(m)]
    value=any(all(any(((mask>>(abs(l)-1))&1)==(l>0) for l in c) for c in F)
              for mask in range(1<<n))
    assert value==expected['SAT'] and (n,m)==(expected['n'],expected['m'])
    sat+=value;checks['randomized_labels']+=1
assert sat==data['randomized_sat_count']
# Independent recomputation of caching aliases for a proper 3CNF example.
SATW=[(1,2,3),(-1,2,3),(-1,-2,3)]
HIT8=[tuple((-(i+1) if mask>>i&1 else i+1) for i in range(3)) for mask in range(8)]
for control,G in zip(data['cached_guest_alias_controls'],(SATW,HIT8)):
    t=control['t'];F=list(G)
    for j in range(t):
        z,p,q=4+3*j,5+3*j,6+3*j
        F += [(z,p,q),(-z,p,q)]
    signatures=[]
    for state in itertools.product((False,True),repeat=t):
        pins={4+3*j:state[j] for j in range(t)}
        out=[]
        for c in F:
            if any(abs(l) in pins and pins[abs(l)]==(l>0) for l in c):continue
            out.append(tuple(sorted(l for l in c if abs(l) not in pins)))
        signatures.append(tuple(sorted(out)))
    assert len(set(signatures))==1
    assert control['unique_guest_queries']==1
    assert control['logical_leaf_occurrences']==2**t
    checks['cached_aliases']+=2**t
print(json.dumps({'verdict':'PASS','independent_checks':dict(checks)},indent=2))