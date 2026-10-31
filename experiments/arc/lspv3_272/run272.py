#!/usr/bin/env python3
"""LSPV-3 finite original-source interface controller, GATE272. Python 3 stdlib."""
import itertools, json, random, hashlib, argparse, tracemalloc, time, collections
from pathlib import Path
SEED = 202610310324

class Meter:
    def __init__(self): self.x=collections.Counter()
    def add(self,key,n=1): self.x[key]+=n
    def val(self): return dict(self.x)

def lit_true(lit,assn):
    b=assn.get(abs(lit));return None if b is None else (b if lit>0 else (not b))

def counts(clauses,assign):
    return [sum(bool(lit_true(l,assign)) for l in c) for c in clauses]

def check(clauses,assign):
    return all(any(lit_true(l,assign) is True for l in c) for c in clauses)

def simplify(clauses,a,meter=None):
    out=[]
    for c in clauses:
        if meter: meter.add('literal_scan',len(c))
        if any(lit_true(l,a) is True for l in c): continue
        nc=tuple(l for l in c if lit_true(l,a) is None)
        if not nc: return None
        out.append(nc)
    return out

def propagate(clauses,a,meter):
    a=dict(a)
    while True:
        meter.add('propagation_pass')
        f=simplify(clauses,a,meter)
        if f is None:
            meter.add('conflict'); return None,None
        units=[c[0] for c in f if len(c)==1]
        if not units:return f,a
        anynew=False
        for lit in units:
            meter.add('unit_visits')
            v=abs(lit); want=lit>0
            if v in a and a[v]!=want:
                meter.add('conflict');return None,None
            if v not in a:
                a[v]=want;meter.add('forced_assignments');anynew=True
        if not anynew: raise AssertionError('propagation stalled')

def dpll(clauses,n,assumptions=None,meter=None):
    meter=meter or Meter();assumptions=assumptions or {}
    def rec(a):
        meter.add('dpll_nodes')
        f,a=propagate(clauses,a,meter)
        if f is None:return None
        if not f:
            model={i:a.get(i,False) for i in range(1,n+1)}
            if not check(clauses,model):raise AssertionError('witness')
            return model
        v=abs(f[0][0])
        for bit in (False,True):
            meter.add('branches')
            aa=dict(a);aa[v]=bit
            ans=rec(aa)
            if ans is not None:return ans
        return None
    return rec(dict(assumptions))

def pin(l,p,q):
    return [tuple((l,a*p,b*q)) for a,b in ((1,1),(1,-1),(-1,1),(-1,-1))]

def instance(b,sat,rename=False,seed=SEED):
    """G extends every boundary assignment; H singleton for SAT and empty for UNSAT."""
    clauses=[]; left=[];right=[]; m=0;n=b
    def add(part,c):
        nonlocal m
        clauses.append(tuple(c));m+=1;part.append(m)
    G=[];H=[]
    for i in range(1,b+1):
        p=n+1;q=n+2;n+=2
        add(G,(i,p,q));add(G,(-i,p,q))
    pattern=[((i*7+3)%3!=0) for i in range(1,b+1)]
    for i in range(1,b+1):
        p=n+1;q=n+2;n+=2
        l=i if pattern[i-1] else -i
        for c in pin(l,p,q):add(H,c)
    if not sat:
        p=n+1;q=n+2;n+=2
        l=(-1 if pattern[0] else 1)
        for c in pin(l,p,q):add(H,c)
    if rename:
        rng=random.Random(seed+b+int(sat)); perm=list(range(1,n+1));rng.shuffle(perm)
        sgn={i:(-1 if rng.randrange(2) else 1) for i in range(1,n+1)}
        cls=[tuple((1 if l>0 else -1)*sgn[abs(l)]*perm[abs(l)-1] for l in c) for c in clauses]
        shuffled=list(zip(cls,[('G' if j+1 in G else 'H') for j in range(len(clauses))]))
        rng.shuffle(shuffled)
        clauses=[tuple(random.Random(seed+11*j).sample(list(c),len(c))) for j,(c,p) in enumerate(shuffled)]
        G=[j+1 for j,(c,p) in enumerate(shuffled) if p=='G']
        H=[j+1 for j,(c,p) in enumerate(shuffled) if p=='H']
    return dict(name=f"PIN_b{b}_{'SAT' if sat else 'UNSAT'}{'_RENAMED' if rename else ''}",n=n,b=b,clauses=clauses,G=G,H=H,source_kind='pin',expected_sat=sat)

def pin_grammar(clauses,meter):
    """Whole-source authenticated recognition. Only these two verified exact grammars accepted."""
    groups=collections.defaultdict(list)
    for j,c in enumerate(clauses,1):
        meter.add('source_clause_read');meter.add('source_literal_read',len(c))
        if len(c)!=3 or len({abs(x) for x in c})!=3:return None
        groups[tuple(sorted(abs(l) for l in c))].append((j,c))
    stable_used=[]; targets=set();pins=[];gpairs=[]
    for vs,records in groups.items():
        meter.add('grammar_group_checks',len(records))
        if len(records)==2:
            first,second=records
            d=[k for k in vs if next(l for l in first[1] if abs(l)==k)!=next(l for l in second[1] if abs(l)==k)]
            if len(d)!=1:return None
            flip=d[0]
            same=[next(l for l in first[1] if abs(l)==k) for k in vs if k!=flip]
            gpairs.append((first[0],second[0],flip,same))
            stable_used.extend(abs(l) for l in same)
            targets.add(flip)
        elif len(records)==4:
            candidates=[]
            for k in vs:
                signed=[next(l for l in c if abs(l)==k) for j,c in records]
                meter.add('grammar_pin_candidate',len(records))
                if len(set(signed))==1:
                    free=[v for v in vs if v!=k]
                    combos={tuple(1 if next(l for l in c if abs(l)==f)>0 else -1 for f in free) for j,c in records}
                    if len(combos)==4:candidates.append((signed[0],free))
            if len(candidates)!=1:return None
            target,free=candidates[0]
            pins.append((target,free,records))
            stable_used.extend(free)
            targets.add(abs(target))
        else: return None
    if len(stable_used)!=len(set(stable_used)) or targets.intersection(stable_used):return None
    return pins,gpairs

def resolve(c,d,pivot):
    """Valid genuine binary resolution with no hidden SAT oracle."""
    if pivot not in c or -pivot not in d:raise ValueError('invalid pivot')
    r=set(c)|set(d);r.remove(pivot);r.remove(-pivot)
    if any(-l in r for l in r):raise ValueError('tautological resolvent')
    return tuple(sorted(r,key=lambda l:(abs(l),l<0)))

def unsat_pin_proof(clauses,pins):
    seen={};pair=None
    for target,free,records in pins:
        if -target in seen:
            pair=(seen[-target],(target,free,records));break
        seen[target]=(target,free,records)
    if pair is None:return None
    dag={j:tuple(c) for j,c in enumerate(clauses,1)}; steps=[];nextid=len(clauses)
    def step(a,b,pivot):
        nonlocal nextid
        x=resolve(dag[a],dag[b],pivot)
        nextid+=1;dag[nextid]=x
        steps.append(dict(id=nextid,parents=[a,b],pivot=pivot,clause=list(x)))
        return nextid
    ends=[]
    for target,free,records in pair:
        u,v=sorted(free)
        def src(su,sv):
            for idx,c in records:
                signs={abs(l):1 if l>0 else -1 for l in c}
                if signs[u]==su and signs[v]==sv:return idx
            raise AssertionError('missing signed extrema')
        rp=step(src(1,1),src(1,-1),v)
        rn=step(src(-1,1),src(-1,-1),v)
        end=step(rp,rn,u)
        assert dag[end]==(target,)
        ends.append((target,end))
    if ends[0][0]>0: final=step(ends[0][1],ends[1][1],ends[0][0])
    else: final=step(ends[1][1],ends[0][1],ends[1][0])
    assert dag[final]==()
    return steps

def verify_proof(clauses,steps):
    dag={j:tuple(c) for j,c in enumerate(clauses,1)}
    for s in steps:
        if s['id'] in dag:return False
        if not all(p in dag for p in s['parents']):return False
        try: val=resolve(dag[s['parents'][0]],dag[s['parents'][1]],s['pivot'])
        except ValueError:return False
        if val!=tuple(s['clause']):return False
        dag[s['id']]=val
    return bool(steps) and dag[steps[-1]['id']]==()

def source_controller(clauses,n,meter):
    # Phase 1: globally consistent, independently verified extreme assignments.
    for bit,tag in ((False,'zero'),(True,'one')):
        a={i:bit for i in range(1,n+1)}
        meter.add('phase1_endpoint_clause_evaluations',len(clauses))
        meter.add('phase1_endpoint_literal_tests',sum(len(c) for c in clauses))
        if check(clauses,a):
            meter.add('phase1_verified_witness'); return a,None,'endpoint-verified',[]
    # Phase 2: source-certified 3CNF pin deductions, or a charged failed recognition.
    info=pin_grammar(clauses,meter)
    if info is None:
        meter.add('recognition_fails');meter.add('policy_switches')
        return dpll(clauses,n,meter=meter),None,'fallback-dpll',[]
    pins,gpairs=info
    deduced=[]
    for target,free,records in pins:
        # The four source clauses resolve twice on free[1], then on free[0]
        # to the entailed unit target. Setting target FALSE is a forbidden cube.
        deduced.append(dict(unit_literal=target,
                           forbidden_cube={str(abs(target)):int(target<0)},
                           source_clause_ids=[idx for idx,c in records],
                           free_variables=free))
        meter.add('pin_resolution_template_checks',3)
    force={}; conflict=False
    for target,free,records in pins:
        meter.add('policy_pin_visits')
        if abs(target) in force and force[abs(target)]!=(target>0): conflict=True
        force[abs(target)]=target>0
    if conflict:
        proof=unsat_pin_proof(clauses,pins)
        assert proof and verify_proof(clauses,proof)
        meter.add('resolution_steps',len(proof));meter.add('proof_source_checks',sum(len(x['clause'])+2 for x in proof))
        return None,proof,'authenticated-resolution',deduced
    model={i:force.get(i,False) for i in range(1,n+1)}
    for j,k,v,same in gpairs:
        model[abs(same[0])]=same[0]>0
        meter.add('witness_lift_steps')
    meter.add('witness_clause_checks',len(clauses));meter.add('witness_literal_checks',sum(map(len,clauses)))
    assert check(clauses,model)
    return model,None,'authenticated-witness',deduced

def interface_dp(inst,meter):
    G=[inst['clauses'][i-1] for i in inst['G']];H=[inst['clauses'][i-1] for i in inst['H']]
    n=inst['n'];b=inst['b']
    boundary=sorted({abs(l) for c in G for l in c}&{abs(l) for c in H for l in c})
    assert len(boundary)==b, (inst['name'],boundary)
    for bits in itertools.product((False,True),repeat=b):
        meter.add('boundary_candidates');a=dict(zip(boundary,bits))
        gm=dpll(G,n,assumptions=a,meter=meter)
        if gm is None:continue
        hm=dpll(H,n,assumptions=a,meter=meter)
        if hm is None:continue
        merged={i:False for i in range(1,n+1)}; merged.update({abs(l):gm[abs(l)] for c in G for l in c}); merged.update({abs(l):hm[abs(l)] for c in H for l in c}); merged.update(a)
        if not check(inst['clauses'],merged):raise AssertionError('merge')
        return merged
    return None


def recognized_fast_classes(clauses,n):
    """Independent instrumented algebraic controls; not silently free in ARC."""
    solvers={}
    if all(sum(l>0 for l in c)<=1 for c in clauses):
        a={i:False for i in range(1,n+1)};passes=0;checks=0;contradict=False
        while True:
            passes+=1;changed=False
            for c in clauses:
                checks+=len(c)
                pos=[l for l in c if l>0];neg=[-l for l in c if l<0]
                if all(a[j] for j in neg):
                    if not pos:contradict=True;break
                    if not a[pos[0]]:a[pos[0]]=True;changed=True
            if contradict or not changed:break
        if not contradict:assert check(clauses,a)
        solvers['horn_forward']=dict(sat=not contradict,source_literal_checks=checks,passes=passes)
    if all(len(c)<=2 for c in clauses):
        nodes=list(range(-n,0))+list(range(1,n+1));g={l:[] for l in nodes};r={l:[] for l in nodes};edges=0
        for c in clauses:
            if not c:return {'krom_scc':dict(sat=False,graph_edges=0)}
            c=(c[0],c[0]) if len(c)==1 else c
            a,b=c
            for u,v in ((-a,b),(-b,a)):
                g[u].append(v);r[v].append(u);edges+=1
        seen=set();post=[]
        def dfs(u):
            seen.add(u)
            for v in g[u]:
                if v not in seen:dfs(v)
            post.append(u)
        for u in nodes:
            if u not in seen:dfs(u)
        comp={}
        def dfs2(u,k):
            comp[u]=k
            for v in r[u]:
                if v not in comp:dfs2(v,k)
        k=0
        for u in reversed(post):
            if u not in comp:dfs2(u,k);k+=1
        solvers['krom_scc']=dict(sat=all(comp[i]!=comp[-i] for i in range(1,n+1)),graph_edges=edges,vertices=2*n)
    groups=collections.defaultdict(list)
    for c in clauses:
        if len(c)!=3 or len(set(map(abs,c)))!=3:break
        groups[tuple(sorted(map(abs,c)))].append(tuple(c))
    else:
        eqs=[];bad=False
        for vs,cset in groups.items():
            # Full 8-clause block enforces immediate contradiction.
            if len(cset)==8:
                if len({tuple(sorted(c)) for c in cset})!=8:bad=True;break
                eqs.extend([(sum(1<<(v-1) for v in vs),0),(sum(1<<(v-1) for v in vs),1)])
                continue
            if len(cset)!=4:bad=True;break
            goodbits=[]
            for bits in itertools.product([False,True],repeat=3):
                a=dict(zip(vs,bits))
                if all(any(lit_true(l,a) for l in c) for c in cset):goodbits.append((sum(bits)%2))
            if len(goodbits)!=4 or len(set(goodbits))!=1:bad=True;break
            eqs.append((sum(1<<(v-1) for v in vs),goodbits[0]))
        if not bad and eqs:
            rows={};rank=0;contradict=False
            for mask,rhs in eqs:
                while mask:
                    p=mask.bit_length()-1
                    if p not in rows:rows[p]=(mask,rhs);rank+=1;break
                    z,t=rows[p];mask^=z;rhs^=t
                if not mask and rhs:contradict=True;break
            solvers['xor_gf2']=dict(sat=not contradict,rank=rank,equations=len(eqs),source_clause_reads=len(clauses))
    return solvers

def xor3_source(sat):
    x=(1,2,3)
    def four(rhs):
        out=[]
        for bits in itertools.product([False,True],repeat=3):
            if sum(bits)%2 !=rhs:
                out.append(tuple(-v if bit else v for v,bit in zip(x,bits)))
        return out
    c=four(0) if sat else four(0)+four(1)
    return dict(name='XOR3_'+('SAT' if sat else 'UNSAT'),n=3,clauses=c,source_kind='adversarial',expected_sat=sat)

def endpoint_and_extrema(inst,trail_max=10):
    clauses=inst['clauses'];n=inst['n']; m=len(clauses)
    endpoints={}
    for name,bit in (('all_zero',False),('all_one',True)):
        c=counts(clauses,{i:bit for i in range(1,n+1)})
        endpoints[name]=dict(satisfied=all(x>0 for x in c),clause_true_counts=c,histogram=[c.count(r) for r in range(4)])
    extrema=[]
    for j,c in enumerate(clauses,1):
        local_sat={str(abs(l)):int(l>0) for l in c}
        local_unsat={str(abs(l)):int(l<0) for l in c}
        extrema.append(dict(j=j,occurrences=[dict(variable=abs(l),signed_literal=l,local_S_value=int(l>0),invert_S_value=int(l<0),local_U_value=int(l<0),invert_U_value=int(l>0)) for l in c],S=local_sat,U=local_unsat,inv_S=local_unsat,inv_U=local_sat))
    pair=[]
    for j,c in enumerate(clauses):
        d1={abs(l):1 if l>0 else -1 for l in c}
        for k in range(j+1,len(clauses)):
            d2={abs(l):1 if l>0 else -1 for l in clauses[k]}
            shared=set(d1)&set(d2)
            same=any(d1[v]==d2[v] for v in shared)
            opp=any(d1[v]!=d2[v] for v in shared)
            flags=dict(SS=not opp,SU=not same,US=not same,UU=not opp)
            # An extreme target combination is feasible exactly when no overlapping target conflict.
            for a in ('S','U'):
                for b in ('S','U'):
                    vals={v:d1[v]*(1 if a=='S' else -1) for v in d1}
                    valid=all((v not in vals or vals[v]==d2[v]*(1 if b=='S' else -1)) for v in d2)
                    assert valid==flags[a+b]
            pair.append(dict(j=j+1,k=k+1,same=same,opposite=opp,flags=flags))
    gray=[];a={i:False for i in range(1,n+1)};prev=0
    for step in range(min(trail_max,1<<min(n,30))):
        cur=step^(step>>1); changed=(cur^prev)
        if changed:
            i=changed.bit_length();a[i]=not a[i]
        v=counts(clauses,a)
        comp={i:not val for i,val in a.items()}
        vc=counts(clauses,comp)
        assert all(vc[j]==len(clauses[j])-v[j] for j in range(m))
        gray.append(dict(step=step,flipped=i if changed else None,assignment_int=cur,true_counts=v,complement_true_counts=vc,sat=all(x>0 for x in v)))
        prev=cur
    return dict(endpoints=endpoints,extrema=extrema,compatibility=pair,gray=gray)

def produce(fixtures):
    results=[]
    for inst in fixtures:
        baseline=Meter();t=time.perf_counter();model0=dpll(inst['clauses'],inst['n'],meter=baseline)
        baseline_ns=time.perf_counter()-t
        cont=Meter();tracemalloc.start();t=time.perf_counter();model,proof,policy,deductions=source_controller(inst['clauses'],inst['n'],cont)
        elapsed=time.perf_counter()-t
        peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
        if (model is None)!=(model0 is None):raise AssertionError(inst['name'])
        if model is not None:assert check(inst['clauses'],model)
        if proof is not None:assert verify_proof(inst['clauses'],proof)
        diag=endpoint_and_extrema(inst,trail_max=10)
        special=recognized_fast_classes(inst['clauses'],inst['n'])
        for q,v in special.items():assert v['sat']==(model0 is not None),(inst['name'],q)
        dp_stats=None
        if inst.get('source_kind')=='pin':
            mdp=Meter();t=time.perf_counter();dp=interface_dp(inst,mdp)
            assert (dp is None)==(model0 is None)
            dp_stats=dict(events=mdp.val(),elapsed_sec=time.perf_counter()-t,witness={str(k):int(v) for k,v in (dp or {}).items()} if dp else None)
        results.append(dict(name=inst['name'],n=inst['n'],m=len(inst['clauses']),b=inst.get('b'),expected_sat=inst.get('expected_sat'),actual_sat=model is not None,policy=policy,clauses=[list(c) for c in inst['clauses']],G=inst.get('G'),H=inst.get('H'),baseline=dict(events=baseline.val(),elapsed_sec=baseline_ns),controller=dict(events=cont.val(),elapsed_sec=elapsed,peak_python_tracemalloc_allocated_bytes=peak,source_serialized_bits=8*len(('p cnf '+str(inst['n'])+' '+str(len(inst['clauses']))+'\n'+'\n'.join(' '.join(map(str,c))+' 0' for c in inst['clauses'])+'\n').encode()),retained_certificate_bits=8*len(json.dumps(dict(witness=model,proof=proof,deductions=deductions)).encode())),oracle_dp=dp_stats,algebraic_controls=special,certificate=dict(witness={str(k):int(v) for k,v in model.items()} if model is not None else None,resolution=proof,forbidden_cubes=deductions),source_controls=diag))
        print(inst['name'], 'SAT' if model else 'UNSAT','policy',policy,'baseline_nodes',baseline.x['dpll_nodes'],'DP',dp_stats['events']['boundary_candidates'] if dp_stats else '-')
    out=dict(date='2026-10-31 03:24 America/Los_Angeles',seed=SEED,model='Instrumented Python with original-source clauses; restricted membership-oracle theorem separately',theorem='b-interface membership-only singleton-vs-empty exact deterministic worst-case 2^b queries on empty; randomized error epsilon lower bound expected (1-2epsilon)*2^b',fixtures=len(results),results=results)
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='raw272.json');args=parser.parse_args()
    fixtures=[]
    for b in range(1,6):
        for sat in (True,False):fixtures.append(instance(b,sat))
    for b in (3,5):
        for sat in (True,False):fixtures.append(instance(b,sat,rename=True))
    fixtures.extend([xor3_source(True),xor3_source(False)])
    # Historical original clause controls loaded by independent archive, not used as answer oracles.
    import zipfile
    archive=Path('/mnt/data/2026-10-31_0219_LSPV-3_STRICT22_BACKDOOR_SELECTOR_GATE271_COMPLETE.zip')
    if archive.exists():
        with zipfile.ZipFile(archive) as z:old=json.loads(z.read('fixtures271.json'))
    elif Path(__file__).with_name('fixtures271.json').exists():
        old=json.loads(Path(__file__).with_name('fixtures271.json').read_text())
    else:
        old=None
    if old is not None:
        for name in ('W1_UNSAT','SWAP6_SAT','W1_RENAMED_UNSAT','SWAP6_RENAMED_SAT','KROM_SAT','KROM_UNSAT','HORN_CHAIN_SAT','HORN_CHAIN_UNSAT','RANDOM3_SEED11'):
            d=old[name]
            fixtures.append(dict(name=name,n=d['n'],clauses=[tuple(c) for c in d['original_clauses']],source_kind='adversarial',expected_sat=None))
    result=produce(fixtures)
    Path(args.out).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    checksum=hashlib.sha256(Path(args.out).read_bytes()).hexdigest()
    print('RAW_SHA256',checksum,'BYTES',Path(args.out).stat().st_size,'FORMULAS',result['fixtures'])
if __name__=='__main__':main()
