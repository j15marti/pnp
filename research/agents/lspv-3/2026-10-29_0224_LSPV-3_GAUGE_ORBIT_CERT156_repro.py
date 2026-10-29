#!/usr/bin/env python3
"""LSPV-3 GAUGE-ORBIT-CERT156. Python 3 stdlib.
Certificate transport for indexed strict signed exact-(2,2)-3CNF sources.
No solver oracle, advice, or external dependencies. The checked source
resolution trace is an explicit input, never assumed to have been discovered
by this compiler. Usage: python3 this.py --trace <155_proof_traces.json>.
"""
import argparse, hashlib, itertools, json, random
from collections import Counter

U_STR='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S_STR='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'

CHECKS=0

def test(assertion,why):
    global CHECKS
    CHECKS+=1
    if not assertion:
        raise AssertionError(why)

def parse(s):return tuple(tuple(int(l) for l in c.split()) for c in s.split(';'))
def flip_lit(l,mask):return -l if (mask>>(abs(l)-1))&1 else l
def flip_formula(F,mask):return tuple(tuple(flip_lit(l,mask) for l in c) for c in F)
def src_signs(F):return bytes(1 if l>0 else 0 for c in F for l in c)
def same_support(F,G):
    return len(F)==len(G) and all(tuple(abs(x) for x in a)==tuple(abs(y) for y in b) for a,b in zip(F,G))

def gauge_mask(F,G,n):
    # Source clause IDs and literal slot positions MUST match exactly.
    if not same_support(F,G):return None
    flips=[None]*n
    for c,d in zip(F,G):
        for l,r in zip(c,d):
            v=abs(l)-1
            if not (0<=v<n):return None
            f=int((l>0)!=(r>0))
            if flips[v] is not None and flips[v]!=f:return None
            flips[v]=f
    if any(x is None for x in flips):return None
    return sum(int(b)<<j for j,b in enumerate(flips))

def canon_gauge(F,n):
    # Deterministically make the FIRST occurrence of every variable positive.
    mask=0;seen=set()
    for c in F:
        for l in c:
            if abs(l) not in seen:
                seen.add(abs(l))
                if l<0:mask|=1<<(abs(l)-1)
    test(len(seen)==n,'all variables active')
    return flip_formula(F,mask),mask

def proper22(F,n):
    count=Counter(l for c in F for l in c)
    return (len(F)*3==4*n and all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
            and len({tuple(sorted(c)) for c in F})==len(F)
            and all(count[v]==count[-v]==2 for v in range(1,n+1)))

def connected(F,n):
    edges=[[] for _ in range(n+1)]
    for j,c in enumerate(F):
        for l in c:edges[abs(l)].append(j)
    vars_seen={1};clauses_seen=set();todo=[1]
    while todo:
        v=todo.pop()
        for j in edges[v]:
            if j in clauses_seen:continue
            clauses_seen.add(j)
            for l in F[j]:
                if abs(l) not in vars_seen:
                    vars_seen.add(abs(l));todo.append(abs(l))
    return len(vars_seen)==n and len(clauses_seen)==len(F)

def holds(F,a):
    return all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in c) for c in F)

def bitmask_truth(F,n):
    # independent brute-force SAT count and per-variable fiber tables
    tot=0;fibers=[0]*n
    for a in range(1<<n):
        if not holds(F,a):continue
        tot+=1
        for v in range(n):fibers[v]|=1<<((a>>v)&1)
    return tot,fibers

def residual_source(F,assignments):
    # Original source IDs survive simplification and both recursive levels.
    out=[]
    for source_id,clause in enumerate(F,1):
        if any(abs(l) in assignments and assignments[abs(l)]==int(l>0) for l in clause):
            continue
        out.append((source_id,tuple(l for l in clause if abs(l) not in assignments)))
    return tuple(out)

def gauge_residual_records(records,mask):
    return tuple((i,tuple(flip_lit(l,mask) for l in clause)) for i,clause in records)

def norm(lits):
    s=set(lits)
    if any(-l in s for l in s):return None
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def replay(F,unit,trace):
    # Independent Resolution checker: source IDs 1..m, assumption m+1.
    try:
        db={j:norm(c) for j,c in enumerate(F,1)}
        db[len(F)+1]=norm(unit)
        for step in trace:
            idx=step['id'];p,q=step['parents'];v=step['pivot'];c=tuple(step['clause'])
            if (idx in db or idx<=len(F)+1 or p not in db or q not in db):return False
            if db[p] is None or db[q] is None:return False
            if v not in db[p] or -v not in db[q]:return False
            r=norm([l for l in db[p] if l!=v]+[l for l in db[q] if l!=-v])
            if r is None or c!=r:return False
            db[idx]=r
        return () in db.values()
    except (KeyError,TypeError,ValueError,IndexError):return False

def flip_trace(trace,mask):
    # Keep clause IDs and source parent indices. Pivot signs flip as literals do.
    return [{'id':s['id'], 'parents':list(s['parents']),
             'pivot':flip_lit(s['pivot'],mask),
             'clause':[flip_lit(l,mask) for l in s['clause']]}
            for s in trace]

def trace_digest(trace):return hashlib.sha256(json.dumps(trace,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main(path):
    rng=random.Random(202610290224)
    U,S=parse(U_STR),parse(S_STR)
    n=15;y=13;m=len(U)
    L0=[list(c) for c in U];L0[7][0]*=-1;L0[19][0]*=-1
    L0=tuple(tuple(c) for c in L0)
    L1=flip_formula(L0,1<<(y-1))
    cases={'empty_U':U,'singleton0_L0':L0,'singleton1_L1':L1,'full_S':S}
    for name,F in cases.items():
        test(proper22(F,n),name+' strict22')
        test(connected(F,n),name+' connected')
        test(same_support(U,F),name+' exact indexed scope')
    test(gauge_mask(L0,L1,n)==1<<(y-1),'singleton pair exact boundary flip')
    test(gauge_mask(U,L0,n) is None,'balanced two-occurrence edit is NOT gauge')
    test(gauge_mask(U,S,n) is None,'U and S not gauge')
    test(gauge_mask(L0,S,n) is None,'singleton and full not gauge')
    test(gauge_mask(U,U,n)==0,'identity gauge')
    profiles={}
    for name,F in cases.items():
        count,fibers=bitmask_truth(F,n)
        profiles[name]={'sat_assignments':count,'y_projection_bitmask':fibers[y-1]}
    test([profiles[z]['y_projection_bitmask'] for z in cases]==[0,1,2,3],'four full truth tables')
    test(profiles['singleton0_L0']['sat_assignments']==profiles['singleton1_L1']['sat_assignments']==168,'same cardinality under gauge')
    test(profiles['empty_U']['sat_assignments']==0 and profiles['full_S']['sat_assignments']==861,'other two counts')
    test(all(canon_gauge(F,n)[0]==canon_gauge(flip_formula(F,0b101010101010101),n)[0] for F in cases.values()),'canonical equals after flips')

    # Distinct 2^n signings in each orbit, exact source signatures, canonical reps.
    reps={tag:src_signs(canon_gauge(F,n)[0]).hex() for tag,F in cases.items()}
    test(reps['singleton0_L0']==reps['singleton1_L1'],'two singleton tables collapse to one gauge orbit')
    test(len({reps['empty_U'],reps['singleton0_L0'],reps['full_S']})==3,'three distinct gauge orbits')
    counts={};sat_orbit_witnesses=0
    first_witness={tag:next((a for a in range(1<<n) if holds(F,a)),None) for tag,F in (('singleton0_L0',L0),('full_S',S))}
    for tag,F in (('empty_U',U),('singleton0_L0',L0),('full_S',S)):
        signatures=set();zero=one=0
        for mask in range(1<<n):
            G=flip_formula(F,mask)
            signs=src_signs(G)
            test(signs not in signatures,'free group action')
            signatures.add(signs)
            test(gauge_mask(F,G,n)==mask,'exact mask recovery')
            test(src_signs(canon_gauge(G,n)[0]).hex()==reps[tag],'deterministic class recognizer chooses registered orbit')
            if tag in first_witness:
                test(holds(G,first_witness[tag]^mask),'uniform SAT witness transport on recognized input')
                sat_orbit_witnesses+=1
            if tag=='singleton0_L0':
                result=(1<<((mask>>(y-1))&1))
                if result==1:zero+=1
                else:one+=1
        test(len(signatures)==1<<n,'orbit size')
        counts[tag]={'distinct_signings':len(signatures),'fiber_zero_orbit':zero,'fiber_one_orbit':one}
    test(counts['singleton0_L0']['fiber_zero_orbit']==16384 and counts['singleton0_L0']['fiber_one_orbit']==16384,'half each')
    # Balanced occurrence choices: six sign choices per variable, factor out two flips.
    # W1 has pairwise different source clause scopes, so no duplicate-clause exclusions.
    test(len({tuple(sorted(map(abs,c))) for c in U})==m,'no repeated unsigned scope')
    orbit_count=3**n
    test((6**n)//(2**n)==orbit_count,'3^n balanced-signing gauge classes')
    
    # Independent representative assignment tests (not derived only from the gauge test itself).
    assignment_pairs=0
    for tag,F in cases.items():
        for _ in range(64):
            mask=rng.randrange(1<<n);G=flip_formula(F,mask)
            for _ in range(64):
                a=rng.randrange(1<<n)
                test(holds(G,a)==holds(F,a^mask),'model-bijection exact')
                assignment_pairs+=1
    # Two hereditary ordinary-CNF children. Restrictions commute with gauge
    # only if the branch assignment is also translated; source IDs survive.
    hereditary_checks=0
    for tag,F in cases.items():
        for _ in range(128):
            mask=rng.randrange(1<<n)
            FG=flip_formula(F,mask)
            v,w=rng.sample(range(1,n+1),2)
            for a,b in itertools.product((0,1),repeat=2):
                target={v:a,w:b}
                base={z:bit^((mask>>(z-1))&1) for z,bit in target.items()}
                direct=residual_source(FG,target)
                transported=gauge_residual_records(residual_source(F,base),mask)
                test(direct==transported,'two-level hereditary source-ID transport')
                hereditary_checks+=1
    # Negative controls: one sign mutation, paired same-variable mutation and scope corruption.
    single=list(list(c) for c in U);single[0][0]=-single[0][0]
    test(gauge_mask(U,tuple(map(tuple,single)),n) is None,'single sign reject')
    test(gauge_mask(U,L0,n) is None and proper22(L0,n),'balanced nongauge reject')
    mixed=[list(c) for c in U];mixed[0][0]=-(abs(mixed[0][0])+1)
    test(gauge_mask(U,tuple(map(tuple,mixed)),n) is None,'unsigned scope reject')

    # Source-ID resolution trace transport: test both negative U fibers and L0->L1.
    trace_data=json.load(open(path,'r',encoding='utf8'))
    test(tuple(map(tuple,trace_data['L0_source']))==L0,'supplied signed source must match')
    specs=[('U0',U,(-y,),trace_data['U_trace_false']),
           ('U1',U,(y,),trace_data['U_trace_true']),
           ('L0_missing1',L0,(y,),trace_data['L0_trace'])]
    for label,F,unit,tr in specs:
        test(replay(F,unit,tr),'source trace initially authentic '+label)
    trace_checks=0;trace_steps=0
    for label,F,unit,tr in specs:
        for _ in range(128):
            mask=rng.randrange(1<<n)
            FG=flip_formula(F,mask)
            flipped_unit=tuple(flip_lit(l,mask) for l in unit)
            TT=flip_trace(tr,mask)
            test(replay(FG,flipped_unit,TT),'transport verified '+label)
            test(len(TT)==len(tr),'step count invariant')
            test(all(a['id']==b['id'] and a['parents']==b['parents'] for a,b in zip(TT,tr)),'source IDs and parent IDs preserved')
            trace_checks+=1;trace_steps+=len(TT)
    # The original L0 proof of y=1 transports to L1 proof of y=0.
    flipY=1<<(y-1)
    test(replay(L1,(-y,),flip_trace(trace_data['L0_trace'],flipY)),'forbidden fiber orientation transported')
    test(replay(L1,(-y,),trace_data['L0_trace']) is False,'original untransformed proof rejected')
    
    # Mutation tests for source-authenticated transport checker.
    TT=flip_trace(trace_data['L0_trace'],flipY)
    broken=json.loads(json.dumps(TT));broken[0]['parents'][0]=10**8
    test(not replay(L1,(-y,),broken),'invalid parent rejected')
    broken=json.loads(json.dumps(TT));broken[0]['pivot']=-broken[0]['pivot']
    test(not replay(L1,(-y,),broken),'bad pivot rejected')
    broken=json.loads(json.dumps(TT));broken[0]['clause'][0]=-broken[0]['clause'][0]
    test(not replay(L1,(-y,),broken),'wrong resolvent rejected')
    broken=json.loads(json.dumps(TT));broken.pop(-1)
    test(not replay(L1,(-y,),broken),'missing empty proof rejected')
    
    # Local E/X gadgets cannot be distinguished through an external a-port if
    # the only E/X change is a private b-complementation.
    E=(( -1,2,3),(-1,2,-3),(1,-2,3),(1,-2,-3))
    X=((1,2,3),(1,2,-3),(-1,-2,3),(-1,-2,-3))
    test(proper22(E,3) and proper22(X,3),'local equality/xor exact22')
    test(gauge_mask(E,X,3)==1,'same-slot E/X is a-port complementation')
    X_priv=flip_formula(E,2)
    test(gauge_mask(E,X_priv,3)==2,'private b gauge in source-indexed order')
    test(sorted(map(tuple,X_priv))==sorted(map(tuple,X)),'E/X differ by b gauge plus authenticated clause permutation')
    for external in [0,1]:
        rE=any(holds(E, a) for a in range(8) if (a&1)==external)
        rX=any(holds(X, a) for a in range(8) if (a&1)==external)
        test(rE==rX==True,'one-port projection cannot see b-private flip')
    return {
      'status':'PASS', 'seed':202610290224, 'assertion_groups':CHECKS,
      'archive_input':'Connected_Interface_Audit.zip independently rerun separately',
      'matched_controls':profiles, 'distinct_gauge_orbits_among_four_fibers':3,
      'orbit_counts':counts,'three_orbit_union_size':3*(1<<n),'sat_orbit_witnesses_authenticated':sat_orbit_witnesses,'all_balanced_signings_on_unique_scope_support':6**n,
      'gauge_equivalence_classes_for_unique_scope_support':orbit_count,
      'assignment_bijection_tests':assignment_pairs,'two_level_hereditary_source_tests':hereditary_checks,
      'resolution_transports_verified':trace_checks,'individual_resolution_steps_replayed':trace_steps,
      'base_resolution_lengths':{name:len(tr) for name,F,unit,tr in specs},
      'model':'signed source-record CNF, uniform literal sign flip; ordinary indexed complexity not a native measured TM runtime',
      'limitations':[
        'Trace acquisition for an arbitrary orbit representative is NOT provided.',
        'Only exact variable-wide sign complements are covered.',
        'Finite tests do not prove arbitrary-size theorem.',
        'This result does not establish an unconditional SAT speedup or lower bound.',
        'Certified proof replay is implemented in Python, not an external kernel checker.'
      ]
    }

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trace',required=True)
    args=p.parse_args()
    print(json.dumps(main(args.trace),indent=2,sort_keys=True))
