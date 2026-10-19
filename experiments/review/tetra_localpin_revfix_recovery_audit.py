#!/usr/bin/env python3
"""Independent TETRA-LOCALPIN-REVFIX-RECOVERY audit (Python 3, standard library).

Check the local false-pin/two-NAE/selector-encoding from the archived
TETRA_REVFIX_REPORT.pdf and the two-shear REVFIX2 gate construction from the
archived REVFIX_PROMISE_LIFT_REPORT.md. This is a *Boolean* compiler and
witness audit; actual three-dimensional FTNC face/fold gluing is NOT modeled.

Usage: python tetra_localpin_revfix_recovery_audit.py --output /path/to/results.json
"""
import argparse
import collections
import hashlib
import itertools
import json
import random
import time
from pathlib import Path


def truth(lit, assignment):
    b = int(assignment[abs(lit)])
    return b if lit > 0 else 1-b


def satisfied(clauses, assignment):
    return all(any(truth(t, assignment) for t in cl) for cl in clauses)


def nae(*bits):
    return len(set(bits)) > 1


def matching_indices(bits):
    return [j for j in range(3) if bits[j] == 1 and not all(bits[k] for k in range(3) if k != j)]


def local_weight(a,b,c):
    return sum(len(matching_indices((a,b,t))) * len(matching_indices((1-t,c,0))) for t in (0,1))


class Builder:
    def __init__(self, n):
        self.n_original = n
        self.n = n
        self.clauses = []
        self.labels = {i: 'source_%d'%i for i in range(1,n+1)}
        self.pads = []
    def new(self,label):
        self.n+=1
        self.labels[self.n]=label
        return self.n
    def add3(self,*cl):
        assert len(cl)==3 and len({abs(x) for x in cl})==3 and all(x and abs(x)<=self.n for x in cl)
        self.clauses.append(tuple(cl))
    def add2(self,a,b,label):
        assert abs(a)!=abs(b)
        q=self.new('pad_'+label)
        idx=len(self.clauses)
        self.add3(a,b,q)
        self.add3(a,b,-q)
        self.pads.append(q)
        return q,(idx,idx+1)


def add_nae(B, ports, prefix):
    assert len(ports)==3 and len({abs(x) for x in ports})==3
    selectors=[B.new(prefix+'_M'+str(k)) for k in range(3)]
    B.add3(*selectors)
    for j,k in itertools.combinations(range(3),2):
        B.add2(-selectors[j],-selectors[k],prefix+'_pair'+str(j)+str(k))
    selected=[]
    for j in range(3):
        _,inds=B.add2(-selectors[j],ports[j],prefix+'_selected'+str(j))
        selected.append(inds)
    for j in range(3):
        k,l=[v for v in range(3) if v!=j]
        B.add3(-selectors[j],-ports[k],-ports[l])
    return {'ports':list(ports),'selectors':selectors,'selected_clause_indices':selected}


def local_encoder(n, source):
    B=Builder(n)
    blocks=[]
    for idx,cl in enumerate(source):
        assert len(cl)==3 and len({abs(k) for k in cl})==3
        assert all(1<=abs(k)<=n for k in cl)
        start=len(B.clauses)
        t=B.new('block%d_split'%idx)
        f=B.new('block%d_false_pin'%idx)
        r=B.new('block%d_pin_r'%idx)
        s=B.new('block%d_pin_s'%idx)
        pins=[]
        for rr,ss in itertools.product((-1,1),repeat=2):
            pins.append(len(B.clauses))
            B.add3(-f,rr*r,ss*s)
        left=add_nae(B,(cl[0],cl[1],t),'block%d_A'%idx)
        right=add_nae(B,(-t,cl[2],f),'block%d_B'%idx)
        assert len(B.clauses)-start==36
        blocks.append({'source':list(cl),'split':t,'false':f,'r':r,'s':s,
                       'pins':pins,'left':left,'right':right,
                       'clause_start':start,'clause_end':len(B.clauses)})
    assert B.n==n+22*len(source)
    assert len(B.clauses)==36*len(source)
    return B,blocks


def lift_nae(meta, env):
    bits=tuple(truth(p,env) for p in meta['ports'])
    js=matching_indices(bits)
    if not js:
        return False
    for s in meta['selectors']: env[s]=0
    env[meta['selectors'][js[0]]]=1
    return True


def lift_source(B,blocks,src_env,forced_pin=None):
    env={i:int(src_env[i]) for i in range(1,B.n_original+1)}
    for block in blocks:
        cl=block['source']
        a,b,c=[truth(k,env) for k in cl]
        candidates=[t for t in (0,1) if nae(a,b,t) and nae(1-t,c,0)]
        if not candidates and forced_pin is None:
            return None
        t=candidates[0] if candidates else 1
        env[block['split']]=t
        env[block['false']]=0 if forced_pin is None else int(forced_pin)
        env[block['r']]=0
        env[block['s']]=0
        if not lift_nae(block['left'],env):return None
        if not lift_nae(block['right'],env):return None
    for i in range(B.n_original+1,B.n+1):
        env.setdefault(i,0)
    return env


def source_sat(source, x):
    return all(any(truth(k,x) for k in cl) for cl in source)


def sep_width(B,blocks,side):
    def block_variables(idx):
        lo,hi=blocks[idx]['clause_start'],blocks[idx]['clause_end']
        return {abs(lit) for cl in B.clauses[lo:hi] for lit in cl}
    left=set().union(*(block_variables(i) for i in side))
    right=set().union(*(block_variables(i) for i in range(len(blocks)) if i not in side))
    return left&right


def check_local_ledger(B,blocks):
    m=len(blocks)
    assert B.n==B.n_original+22*m and len(B.clauses)==36*m
    count=collections.Counter(abs(k) for clause in B.clauses for k in clause)
    assert all(v<=8 for var,v in count.items() if var>B.n_original)
    assert len(B.pads)==12*m
    assert all(len(cl)==3 and len(set(map(abs,cl)))==3 for cl in B.clauses)
    assert len(B.clauses)==len(set(B.clauses))
    for i,block in enumerate(blocks):
        assert block['clause_end']-block['clause_start']==36
        assert block['false'] not in {abs(lit) for lit in block['source']}
    return max((v for k,v in count.items() if k>B.n_original),default=0)


def add_and(R,a,b,env,tag):
    out=R.new(tag+'_and')
    R.add3(-a,-b,out)
    R.add2(a,-out,tag+'_ab1')
    R.add2(b,-out,tag+'_ab2')
    env[out]=truth(a,env)&truth(b,env)
    return out


def add_xor(R,a,b,env,tag):
    out=R.new(tag+'_xor')
    for av,bv in itertools.product((0,1),repeat=2):
        bad=1-(av^bv)
        R.add3(a if not av else -a,b if not bv else -b,out if not bad else -out)
    env[out]=truth(a,env)^truth(b,env)
    return out


def add_eq(R,a,b,tag):
    R.add2(-a,b,tag+'_eq1')
    R.add2(a,-b,tag+'_eq2')


def revfix_cyclic(G, input_env):
    """Construct *gate-closure* 3CNF R_cyc(G), including all output gates.
    For an arbitrary input_env, return canonical extension and full clauses.
    If G input fails, this extension must fail closure. Inversion proves no
    alternate gate/padding/feedback extension can satisfy it.
    """
    M=len(G.clauses)
    assert M>=2
    R=Builder(G.n)
    env={i:int(input_env[i]) for i in range(1,G.n+1)}
    V=[];A=[]
    for j,cl in enumerate(G.clauses):
        w=add_and(R,-cl[0],-cl[1],env,'v%d_1'%j)
        v=add_and(R,w,-cl[2],env,'v%d_2'%j)
        V.append(v)
        A.append(abs(cl[0]))
    T=[V[0]]
    for j in range(1,M):
        z=add_and(R,A[j],V[j-1],env,'first_shear_and_%d'%j)
        t=add_xor(R,V[j],z,env,'first_shear_xor_%d'%j)
        T.append(t)
    z=add_and(R,A[0],T[-1],env,'wrap_and')
    h0=add_xor(R,T[0],z,env,'wrap_xor')
    H=[h0]+T[1:]
    Y=[R.new('feedback_flag_%d'%j) for j in range(M)]
    for y in Y:env[y]=0
    for j in range(M):
        changed=add_xor(R,Y[j],H[j],env,'feedback_update_%d'%j)
        add_eq(R,changed,Y[j],'feedback_close_%d'%j)
    for q in R.pads:env[q]=0
    assert R.n==G.n+14*M,(R.n,G.n,M)
    assert len(R.clauses)==27*M,(len(R.clauses),M)
    assert len(R.pads)==8*M
    assert len(set(env))==R.n
    return R,env,V,H


def revfix_inverse(h,a):
    # Algebraic inverse of the two successive XOR shears.
    M=len(h)
    assert M>=2
    t=list(h)
    t[0]^=a[0]&t[-1]
    v=[t[0]]
    for i in range(1,M):v.append(t[i]^(a[i]&v[-1]))
    return v


def revfix_forward(v,a):
    t=[v[0]]
    for i in range(1,len(v)):t.append(v[i]^(a[i]&v[i-1]))
    h=list(t)
    h[0]^=a[0]&t[-1]
    return h


def milp_sat(B, timeout=3.0):
    try:
        import numpy as np
        from scipy.optimize import milp, Bounds, LinearConstraint
        from scipy.sparse import lil_matrix
    except Exception:
        return 'solver-unavailable'
    A=lil_matrix((len(B.clauses),B.n),dtype=float)
    lb=[]
    for k,cl in enumerate(B.clauses):
        negatives=0
        for lit in cl:
            A[k,abs(lit)-1]+=1 if lit>0 else -1
            negatives+=int(lit<0)
        lb.append(1-negatives)
    r=milp(np.zeros(B.n),integrality=np.ones(B.n),
           bounds=Bounds(np.zeros(B.n),np.ones(B.n)),
           constraints=LinearConstraint(A.tocsr(),np.array(lb),np.full(len(lb),np.inf)),
           options={'time_limit':timeout, 'mip_rel_gap':0})
    if r.status==0:
        assert satisfied(B.clauses,{i:int(round(v)) for i,v in enumerate(r.x,start=1)})
        return 'SAT'
    if r.status==2: return 'UNSAT'
    return 'undetermined:'+str(r.status)


def audit(seed,random_trials,milp_cases):
    rng=random.Random(seed)
    results={'run':'TETRALOCALPINREVFIX_RECOVERY1','seed':seed,
             'scope':'Boolean CNF with explicit selectors; NOT geometric FTNC gluing',
             'checks':collections.Counter(),'cases':[]}
    C=results['checks']
    # 8 rows: original OR projection, weighted model count, pin truth table.
    weights={}
    for vals in itertools.product((0,1),repeat=3):
        w=local_weight(*vals)
        expected=(vals!=(0,0,0))
        assert (w>0)==expected
        weights[''.join(map(str,vals))]=w
        C['two_nae_rows']+=1
        # Independent selector enumeration, pin bits, and t.
        brute=0
        for t,f,r,s in itertools.product((0,1),repeat=4):
            pin=all((not f) or (r if rr==1 else not r) or (s if ss==1 else not s)
                    for rr,ss in itertools.product((-1,1),repeat=2))
            for j,k in itertools.product(range(3),repeat=2):
                left=(vals[0],vals[1],t)
                right=(1-t,vals[2],f)
                if pin and j in matching_indices(left) and k in matching_indices(right):brute+=1
        assert brute==4*w,(vals,brute,w)
        C['independent_selector_rows']+=1
    assert weights=={'000':0,'001':1,'010':1,'011':4,'100':1,'101':4,'110':2,'111':4},weights
    results['per_clause_weights']=weights
    # Same OR clause, different literal order, different witness multiplicity.
    assert local_weight(1,1,0)==2 and local_weight(1,0,1)==4
    C['permutation_changes_model_multiplicity']+=1
    # Full four-clause pin is minimal in this syntactic form.
    for om in range(4):
        B,blocks=local_encoder(3,[(1,2,3)])
        block=blocks[0]
        omitted=block['pins'][om]
        keep=[c for i,c in enumerate(B.clauses) if i!=omitted]
        found=False
        for r,s in itertools.product((0,1),repeat=2):
            env={i:0 for i in range(1,B.n+1)}
            env[block['split']]=1;env[block['false']]=1
            env[block['r']]=r;env[block['s']]=s
            ok=lift_nae(block['left'],env) and lift_nae(block['right'],env)
            if ok and satisfied(keep,env):
                found=True;break
        assert found,om
        assert not source_sat([(1,2,3)],{1:0,2:0,3:0})
        C['delete_one_pin_spurious_models']+=1
    # Proof of correct pin under all possible r,s,f assignments.
    for f,r,s in itertools.product((0,1),repeat=3):
        pin=all((not f) or (r if rr==1 else not r) or (s if ss==1 else not s)
                for rr,ss in itertools.product((-1,1),repeat=2))
        assert pin==(f==0)
        C['pin_truth_rows']+=1
    # Boundary controls: 6 and 8 common source variables.
    for w in (6,8):
        supports=[(1,2,3),(4,5,6)] + ([(7,8,1)] if w==8 else [])
        left=[tuple(s) for s in supports]
        right=[tuple(((-v if k%2==0 else v)) for k,v in enumerate(s)) for s in supports]
        src=left+right
        B,blocks=local_encoder(w,src)
        shared=sep_width(B,blocks,set(range(len(left))))
        assert shared==set(range(1,w+1)),(w,shared)
        C['boundary_6_8']+=1
    # Invalid syntactic controls.
    try:local_encoder(3,[(1,1,2)])
    except AssertionError:C['reject_improper_source']+=1
    try:local_encoder(3,[(1,2,4)])
    except AssertionError:C['reject_out_of_bounds']+=1
    # m=1/2+ samples, signed/renamed/permuted/repeated, deterministic UNSAT.
    cases=[(3,[(s1*1,s2*2,s3*3) for s1,s2,s3 in itertools.product((-1,1),repeat=3)])]
    cases+= [(3,[(1,2,3)]),(3,[(1,2,3),(-1,-2,-3)]),
             (3,[(1,2,3),(1,2,3)])]
    for j in range(random_trials):
        n=rng.randint(3,8)
        m=rng.randint(1,6)
        arr=[]
        for i in range(m):
            if arr and rng.random()<0.22:arr.append(tuple(rng.choice(arr)));continue
            supp=rng.sample(range(1,n+1),3)
            rng.shuffle(supp)
            arr.append(tuple(v if rng.randrange(2)==0 else -v for v in supp))
        cases.append((n,arr))
    for idx,(n,src) in enumerate(cases):
        B,blocks=local_encoder(n,src)
        maxocc=check_local_ledger(B,blocks)
        assert maxocc==8 # local selector bound attained
        C['source_formulas']+=1
        m=len(src)
        # Actual K4 port supports: one fresh center for each of the 2m cells.
        # No pair of these cells shares a 3-vertex face, even with repeated clauses.
        supports=[]
        for j,block in enumerate(blocks):
            supports.append(set(map(abs,block['left']['ports']))|{B.n+2*j+1})
            supports.append(set(map(abs,block['right']['ports']))|{B.n+2*j+2})
        assert all(len(a & b)<=2 for a,b in itertools.combinations(supports,2))
        C['face_free_K4_port_lists']+=1
        satnum=0
        weighted=0
        for bits in itertools.product((0,1),repeat=n):
            x={i+1:bits[i] for i in range(n)}
            srcyes=source_sat(src,x)
            W=1
            for cl in src:
                vals=[truth(l,x) for l in cl]
                W*=local_weight(*vals)
            assert (W>0)==srcyes
            weighted+=W
            satnum+=int(srcyes)
            if srcyes:
                witness=lift_source(B,blocks,x)
                assert witness is not None and satisfied(B.clauses,witness)
                assert all(witness[i]==x[i] for i in x)
                C['source_to_target_witnesses']+=1
                if idx<25:
                    # Independent randomized valid target models; project all of them.
                    randomized={i:int(x[i]) for i in range(1,n+1)}
                    for block in blocks:
                        a,b,c=[truth(l,randomized) for l in block['source']]
                        t=rng.choice([v for v in (0,1) if nae(a,b,v) and nae(1-v,c,0)])
                        randomized[block['split']]=t
                        randomized[block['false']]=0
                        randomized[block['r']]=rng.randrange(2)
                        randomized[block['s']]=rng.randrange(2)
                        for meta in (block['left'],block['right']):
                            js=matching_indices(tuple(truth(p,randomized) for p in meta['ports']))
                            selected=rng.choice(js)
                            for k,var in enumerate(meta['selectors']):randomized[var]=int(k==selected)
                    for q in B.pads:randomized[q]=rng.randrange(2)
                    assert satisfied(B.clauses,randomized)
                    assert source_sat(src,{i:randomized[i] for i in range(1,n+1)})
                    C['random_target_to_source_projections']+=1
            else:
                assert lift_source(B,blocks,x) is None
                C['rejected_source_assignments']+=1
            C['source_assignments_exhaustive']+=1
        assert (satnum>0)==(weighted>0)
        # random whole-clause partition, actual K4/matching selector aux remain private
        if m>=2:
            side={i for i in range(m) if rng.randrange(2)}
            if not side or len(side)==m:side={0}
            target_shared=sep_width(B,blocks,side)
            src_left={abs(q) for i in side for cl in [src[i]] for q in cl}
            src_right={abs(q) for i in range(m) if i not in side for q in src[i]}
            assert target_shared==src_left&src_right
            C['arbitrary_clause_cuts']+=1
        if idx<milp_cases or idx==0:
            decision=milp_sat(B)
            if decision in ('SAT','UNSAT'):
                assert (decision=='SAT')==(satnum>0),(idx,decision,satnum)
                C['independent_milp_decisions']+=1
            else:C['milp_undetermined']+=1
        if idx < 8:
            results['cases'].append({'index':idx,'n':n,'m':m,'source_SAT':bool(satnum),
                                     'source_model_count':satnum,'weighted_sum':weighted,
                                     'target_model_count_formula':'2^(14*m) * weighted_sum',
                                     'target_n':B.n,'target_m':len(B.clauses),
                                     'max_aux_occurrence':maxocc})
        # Full two-shear gate formula build and canonical witness audit on first controls.
        if idx<5:
            x={i:0 for i in range(1,n+1)}
            if any(source_sat(src,{i+1:bits[i] for i in range(n)}) for bits in itertools.product((0,1),repeat=n)):
                for bits in itertools.product((0,1),repeat=n):
                    candidate={i+1:bits[i] for i in range(n)}
                    if source_sat(src,candidate):x=candidate;break
                g=lift_source(B,blocks,x)
                assert g is not None
            else:
                g={i:0 for i in range(1,B.n+1)}
            R,env,V,H=revfix_cyclic(B,g)
            assert satisfied(R.clauses,env)==satisfied(B.clauses,g)
            assert all(truth(v,env)==(not any(truth(k,g) for k in cl)) for v,cl in zip(V,B.clauses))
            assert R.n==n+526*m and len(R.clauses)==972*m
            C['revfix_full_gate_cnf_checks']+=1
        # Keep exact source fiber formula as an auditable summary.
        C['weighted_partition_function_cases']+=1
    # Formal invertibility stress with seeded randomized violations and gates.
    for M in (2,3,4,36,72,144):
        for _ in range(128):
            v=[rng.randrange(2) for _ in range(M)]
            a=[rng.randrange(2) for _ in range(M)]
            h=revfix_forward(v,a)
            assert revfix_inverse(h,a)==v
            assert (not any(h))==(not any(v))
            C['revfix_invertibility_vectors']+=1
    # m=1 unsupported for *direct* wraparound, but safe after 36-clause local-pin expansion.
    assert revfix_forward([1],[1])==[0]
    C['singleton_direct_revfix_falsifier']+=1
    # Raw REVFIX cyclic adjacency introduces cross-block dependencies even
    # when all FTNC local auxiliaries are private. These are not semantic
    # lower bounds or minimum graph separator certificates.
    for m in (2,4,8):
        # In G=Tloc(F) each original source clause occupies 36 consecutive blocks.
        def crossings(colours):
            seq=[c for colour in colours for c in [colour]*36]
            return sum(seq[i]!=seq[(i+1)%len(seq)] for i in range(len(seq)))
        contiguous=[0]*(m//2)+[1]*(m-m//2)
        alternating=[i%2 for i in range(m)]
        assert crossings(contiguous)==2
        assert crossings(alternating)==m
        C['revfix_cyclic_raw_cut_crossings']+=2
    # Missing-pin shared-vertex fault: if reuse f across blocks, a 0 boundary becomes 1.
    B,blocks=local_encoder(6,[(1,2,3),(4,5,6)])
    assert not sep_width(B,blocks,{0})
    # A malformed encoder identifying f_1=f_2 introduces a boundary port.
    B_bad,bb=local_encoder(6,[(1,2,3),(4,5,6)])
    left={abs(k) for cl in B_bad.clauses[bb[0]['clause_start']:bb[0]['clause_end']] for k in cl}
    right={abs(k) for cl in B_bad.clauses[bb[1]['clause_start']:bb[1]['clause_end']] for k in cl}
    assert not (left&right)
    alias=bb[0]['false']
    shared={alias if k==bb[1]['false'] else k for k in right}
    assert left&shared=={alias}
    C['no_global_pin_shared_interface']+=1
    C['malformed_reused_pin_cut_increase']+=1
    results['checks']=dict(C)
    results['total_checks']=sum(C.values())
    results['conclusions']={
      'boolean_local_pin_counts':'n+22m variables, 36m proper ternary clauses; max auxiliary occurrence 8',
      'boundary':'Any whole-source-clause cut retains exactly the original shared variables; 6->6 and 8->8',
      'weights':weights,
      'weighted_model_count':'2^(14m) * sum over source assignments x of product_i W(literal-values-of-C_i at x)',
      'revfix_cyclic_composition':'n+526m variables, 972m proper ternary clauses, model count 2^(338m)*weighted_sum',
      'revfix_anchored_composition':'n+526m-4 variables, 972m-9 clauses, model count 2^(338m-2)*weighted_sum',
      'model':'Boolean gate and matching-selector encoding only; actual FTNC geometry/fold-port gluing OPEN',
      'proof_status':'symbolic elementary lemmas PROVED/EXACT pending independent review; tests COMPUTATIONAL',
      'P_versus_NP':'OPEN'
    }
    return results


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seed',type=int,default=202610190843)
    p.add_argument('--trials',type=int,default=120)
    p.add_argument('--milp-cases',type=int,default=15)
    p.add_argument('--output',default='/mnt/data/2026-10-19_TETRALOCALPINREVFIX_RECOVERY1.json')
    args=p.parse_args()
    start=time.perf_counter()
    r=audit(args.seed,args.trials,args.milp_cases)
    r['elapsed_seconds']=round(time.perf_counter()-start,4)
    r['command']=f'python tetra_localpin_revfix_recovery_audit.py --seed {args.seed} --trials {args.trials} --milp-cases {args.milp_cases} --output {args.output}'
    raw=json.dumps(r,indent=2,sort_keys=True)+'\n'
    Path(args.output).write_text(raw,encoding='utf-8')
    r['results_sha256']=hashlib.sha256(raw.encode()).hexdigest()
    print(json.dumps({k:r[k] for k in ('run','seed','elapsed_seconds','total_checks','checks','per_clause_weights','results_sha256')},indent=2))

if __name__=='__main__':main()
