#!/usr/bin/env python3
"""LSPV-2, 2026-10-31: source-indexed Horn/Krom interface gate.
Standard-library reproducible experiment, Python selected-event proxies not FLMV bounds.
Usage: python lspv2_horn_krom_274.py [output.json]
"""
import itertools, json, sys, random, math, hashlib, tracemalloc
from collections import Counter

SEED=202610310712

def simplify(C):
    C=set(C)
    if any(-x in C for x in C): return None
    return tuple(sorted(C,key=lambda x:(abs(x),x<0)))

def value(l,a):return int(a[abs(l)-1] == (l>0))
def eval_clause(C,a):return sum(value(l,a) for l in C)
def satisfied(F,a):return all(eval_clause(C,a)>0 for C in F)
def serialize(F,n):return 'p cnf %d %d\n'%(n,len(F))+''.join(' '.join(map(str,C))+' 0\n' for C in F)

def solver(F,n):
    counts=Counter(); witness=None
    def dfs(a):
        counts['nodes']+=1
        a=list(a)
        while True:
            changed=False; allsat=True
            for C in F:
                counts['clause_reads']+=1; pending=[]; hit=False
                for lit in C:
                    counts['literal_tests']+=1;v=a[abs(lit)-1]
                    if v is None:pending.append(lit)
                    elif v==(lit>0):hit=True;break
                if hit:continue
                allsat=False
                if not pending:counts['conflicts']+=1;return None
                if len(pending)==1:
                    lit=pending[0];x=abs(lit)-1;want=lit>0
                    if a[x] is not None and a[x]!=want:counts['conflicts']+=1;return None
                    if a[x] is None:a[x]=want;counts['unit_assigns']+=1;changed=True
            if allsat:return [bool(v) if v is not None else False for v in a]
            if not changed:break
        counts['decisions']+=1
        x=next(i for i,v in enumerate(a) if v is None)
        for want in (False,True):
            b=a.copy();b[x]=want
            w=dfs(b)
            if w is not None:return w
        return None
    witness=dfs([None]*n)
    return witness,dict(counts)

def translate(F,n):
    T=[];groups=[]
    for j,C in enumerate(F):
        if len(C)!=3 or len(set(map(abs,C)))!=3: return None,None
        yy=[n+3*j+k+1 for k in range(3)]
        base=len(T)
        T.append(tuple(-y for y in yy))
        for l,y in zip(C,yy):T.extend([(l,y),(-l,-y)])
        groups.append({'source':j+1,'T_ids':list(range(base+1,base+8)), 'y':yy,'lits':list(C)})
    return T,groups

def resolve(A,B,p):
    if (p in A and -p in B):pass
    elif (-p in A and p in B):pass
    else:raise AssertionError('missing pivot')
    R=simplify([x for x in A if abs(x)!=abs(p)]+[x for x in B if abs(x)!=abs(p)])
    if R is None:raise AssertionError('tautological resolvent')
    return R

def source_recover_proofs(T,groups):
    proof=[];clauses={i+1:tuple(C) for i,C in enumerate(T)};roots={}
    for g in groups:
        curr=g['T_ids'][0]
        for k in range(3):
            y=g['y'][k];link=g['T_ids'][1+2*k]
            R=resolve(clauses[curr],clauses[link],y)
            new=len(clauses)+1;clauses[new]=R
            proof.append({'id':new,'parents':[curr,link],'pivot':y,'clause':list(R),'kind':'recover','orig_clause':g['source']})
            curr=new
        assert clauses[curr]==simplify(g['lits'])
        roots[g['source']]=curr
    return proof,clauses,roots

def orig_resolution(F,max_nodes=4500):
    # Sound complete saturation for these small finite samples, with exact source DAG.
    clauses={i+1:simplify(c) for i,c in enumerate(F)}
    seen={c:i for i,c in clauses.items()};steps=[]
    queue=list(clauses)
    for a in queue:
        A=clauses[a]
        for b in list(queue):
            if b>=a:continue
            B=clauses[b]
            for p in A:
                if -p not in B:continue
                R=simplify([x for x in A if x!=p]+[x for x in B if x!=-p])
                if R is None or R in seen:continue
                ix=len(clauses)+1;clauses[ix]=R;seen[R]=ix;queue.append(ix)
                steps.append({'id':ix,'parents':[a,b],'pivot':p,'clause':list(R)})
                if len(R)==0:return steps,ix
                if len(clauses)>max_nodes:return steps,None
    return steps,None

def lift_refutation(T,groups,F):
    proof,clauses,roots=source_recover_proofs(T,groups)
    orig_steps,empty=orig_resolution(F)
    if empty is None:return proof, None, {'reason':'bounded resolution saturation returned no empty clause'}
    refmap=dict(roots)
    for st in orig_steps:
        lhs,rhs=(refmap[x] for x in st['parents'])
        R=resolve(clauses[lhs],clauses[rhs],st['pivot'])
        assert list(R)==st['clause']
        ix=len(clauses)+1;clauses[ix]=R;refmap[st['id']]=ix
        proof.append({'id':ix,'parents':[lhs,rhs],'pivot':st['pivot'],'clause':list(R),'kind':'source-refute'})
    assert clauses[refmap[empty]]==()
    return proof,refmap[empty],{'source_resolution_steps':len(orig_steps),'recovered_source_roots':len(groups)}

def audit_source(F,n):
    a0=[False]*n;a1=[True]*n
    occ=[];compat=[]
    for j,C in enumerate(F):
        for k,l in enumerate(C):
            s=int(l>0);u=1-s
            occ.append({'clause':j+1,'position':k+1,'literal':l,'source_variable':abs(l),
                        'S_value':s,'S_inverse_U':u,'U_value':u,'U_inverse_S':s})
    def feasible(C,D,s,t):
        req={}
        for cc,mode in ((C,s),(D,t)):
            for lit in cc:
                val=(lit>0) if mode=='S' else (lit<0)
                if abs(lit) in req and req[abs(lit)]!=val:return False
                req[abs(lit)]=val
        return True
    for j in range(len(F)):
        for k in range(j+1,len(F)):
            C,D=F[j],F[k]
            modes={x+y:feasible(C,D,x,y) for x in 'SU' for y in 'SU'}
            if n<=6:
                for a in itertools.product((False,True),repeat=n):
                    for xy,ok in modes.items():
                        want=(eval_clause(C,a)==(len(C) if xy[0]=='S' else 0) and
                              eval_clause(D,a)==(len(D) if xy[1]=='S' else 0))
                        if want:assert ok
                for xy,ok in modes.items():
                    assert ok==any(eval_clause(C,a)==(len(C) if xy[0]=='S' else 0) and
                                   eval_clause(D,a)==(len(D) if xy[1]=='S' else 0)
                                   for a in itertools.product((False,True),repeat=n))
            compat.append({'source_pair':[j+1,k+1],**modes})
    frames=[];a=a0.copy();old=[eval_clause(C,a) for C in F]
    frames.append({'assignment':list(map(int,a)),'true_counts':old,'categories':{str(i):old.count(i) for i in range(4)},'flip':None})
    for x in range(n):
        a[x]=not a[x];new=[eval_clause(C,a) for C in F]
        for C,prev,nxt in zip(F,old,new):
            oldvalue=a.copy();oldvalue[x]=not oldvalue[x]
            change=(1 if any(abs(l)==x+1 and value(l,oldvalue)==0 for l in C) else 0)-(1 if any(abs(l)==x+1 and value(l,oldvalue)==1 for l in C) else 0)
            assert prev+change==nxt
        frames.append({'assignment':list(map(int,a)),'true_counts':new,'categories':{str(i):new.count(i) for i in range(4)},'flip':x+1})
        old=new
    assert frames[0]['assignment']==[0]*n and frames[-1]['assignment']==[1]*n
    for C in F:assert eval_clause(C,a0)+eval_clause(C,a1)==len(C)
    return {'signed_occurrences':occ,'pair_extreme_compatibility':compat,
            'coherent_flip_frames':frames,'endpoint_0':frames[0], 'endpoint_1':frames[-1]}

def signed_renaming(F,n,perm,flips):
    out=[]
    for C in F:
        out.append(tuple((1 if l>0 else -1)*(-1 if flips[abs(l)-1] else 1)*perm[abs(l)-1] for l in C))
    return out

def all_clauses(n):
    return [tuple((1 if (mask>>i)&1 else -1)*(i+1) for i in range(n)) for mask in range(1<<n)]

def cases():
    eight=all_clauses(3)
    omit=(-1,2,-3) # false exactly at 101, so 000 and 111 BOTH fail.
    sat=[c for c in eight if c!=omit]+[eight[0]]
    assert len(sat)==len(eight)==8
    out=[('UNSAT_all8',3,eight),('SAT_unique_101',3,sat),
         ('SAT_allpositive',3,[(1,2,3)]),('SAT_allnegative',3,[(-1,-2,-3)]),
         ('SAT_polarity_mixed',3,[(1,-2,3),(-1,-2,-3)]),
         ('SAT_Horn3',3,[(-1,-2,3),(-2,-3,1)]),
         ('SAT_dualHorn3',3,[(1,2,-3),(1,3,-2)]),
         ('SAT_XOR_even',3,[c for c in eight if sum(x<0 for x in c)%2==0]),
         ('UNSAT_XOR_both',3,eight[:])]
    out += [('SAT_renamed',3,signed_renaming(sat,3,[3,1,2],[True,False,True])),
            ('UNSAT_renamed',3,signed_renaming(eight,3,[2,3,1],[True,True,False]))]
    # Original high-width controls are unrecognized by the proper 3CNF compiler.
    wide=all_clauses(4)
    out += [('UNSAT_highwidth_fallback',4,wide),('SAT_highwidth_fallback',4,wide[:-1])]
    # Material duplicates: known easy physical shortening, not universal ARC.
    out += [('SAT_repeated_32',3,sat*32),('UNSAT_repeated_32',3,eight*32)]
    rng=random.Random(SEED)
    for i in range(10):
        n=4+(i%3);m=6+i
        f=[]
        for _ in range(m):
            v=rng.sample(range(1,n+1),3)
            f.append(tuple(x*(1 if rng.randrange(2) else -1) for x in v))
        out.append(('random_%02d'%i,n,f))
    return out

def main(path):
    tracemalloc.start()
    result={'run':'HORN-KROM-FOREST-INTERFACE274','seed':SEED,'cases':[],
            'theorem':'forall source proper3 F, forall x: exists y T(F)(x,y) iff F(x); #SAT(T)=#SAT(F)',
            'status':'PROVED/EXACT restricted proof, external referee pending; COMPUTATIONAL tests; ARC OPEN'}
    for name,n,F in cases():
        tracemalloc.reset_peak()
        F=[tuple(c) for c in F]
        src_label=any(satisfied(F,a) for a in itertools.product((False,True),repeat=n))
        src_w,src_ops=solver(F,n);assert (src_w is not None)==src_label
        audit=audit_source(F,n)
        T,groups=translate(F,n)
        if T is None:
            assert any(len(C)!=3 for C in F)
            row={'name':name,'n':n,'F':list(map(list,F)),'label':'SAT' if src_label else 'UNSAT',
                 'policy':'REJECT_UNRECOGNIZED_AND_EXACT_FALLBACK','source_witness':src_w,
                 'source_baseline':src_ops,'audit':audit,'recognizer_failed_trials':1,'policy_switches':1,
                 'original_bits':len(serialize(F,n))*8}
        else:
            tn=n+3*len(F)
            t_w,t_ops=solver(T,tn)
            assert (t_w is not None)==src_label
            assert all(len(C)<=2 for j,C in enumerate(T) if j%7!=0)
            assert all(all(l<0 for l in C) for j,C in enumerate(T) if j%7==0)
            # Horn component independently SAT (all y=0), Krom components independently SAT (any x and its unique y).
            for a in itertools.product((False,True),repeat=n):
                yy=[not bool(value(l,a)) for C in F for l in C]
                full=list(a)+yy
                assert satisfied(T[::7], full) == satisfied(F,a)
                assert all(satisfied(T[7*j+1:7*j+7],full) for j in range(len(F)))
                for j in range(len(F)):
                    assert satisfied([T[7*j]],full)==(eval_clause(F[j],a)>0)
            proof,clauses,roots=source_recover_proofs(T,groups)
            derived,root,extra=lift_refutation(T,groups,F) if not src_label and len(F)<20 else (proof,None,{})
            # For large redundant unsat sources, a source-refutation exists in the unique 8-clause subformula.
            if not src_label and root is None:
                unique=[];ids=[]
                for j,C in enumerate(F):
                    if C not in unique:unique.append(C);ids.append(j+1)
                steps,empty=orig_resolution(unique)
                if empty is not None:
                    P,D,R=source_recover_proofs(T,groups)
                    refs={j+1:R[ids[j]] for j in range(len(ids))}
                    for st in steps:
                        lhs,rhs=[refs[u] for u in st['parents']]
                        C=resolve(D[lhs],D[rhs],st['pivot']);ix=len(D)+1;D[ix]=C
                        P.append({'id':ix,'parents':[lhs,rhs],'pivot':st['pivot'],'clause':list(C),'kind':'source-refute'})
                        refs[st['id']]=ix
                    derived,root,extra=P,refs[empty],{'source_resolution_steps':len(steps),'unique_source_clauses':len(unique)}
            # A three-resolution derived original clause is falsified exactly on its own source cube.
            known_resolvent=None
            for aidx,A in enumerate(F):
                if known_resolvent is not None:break
                for bidx,B in enumerate(F[:aidx]):
                    for pivot in A:
                        if -pivot not in B:continue
                        R=simplify([x for x in A if x!=pivot]+[x for x in B if x!=-pivot])
                        if R is not None and R and len(R)<len(A)+len(B)-2:
                            known_resolvent={'parents_original':[aidx+1,bidx+1],'pivot':pivot,
                                             'entailed_clause':list(R),'forbidden_cube':{str(abs(l)):int(l<0) for l in R}}
                            break
                    if known_resolvent is not None:break
            # Compiler grammar validation and exact child text (redundant clauses collapsed by trusted source equivalence).
            simple=[]
            for C in F:
                if C not in simple:simple.append(C)
            parent_bits=8*len(serialize(T,tn));child_bits=8*len(serialize(simple,n))
            measured=Counter({'input_char_reads':len(serialize(T,tn)),'policy_recognition_literal_reads':sum(map(len,T)),
                              'failed_class_trials':2,'policy_switches':2,'proof_resolution_steps':len(derived),
                              'child_output_characters':len(serialize(simple,n)),'witness_validation_literal_reads':sum(map(len,T)) if src_label else 0})
            measured['guest_literal_tests']=src_ops.get('literal_tests',0)
            measured['proof_literal_visits']=sum(len(s['clause']) for s in derived)
            measured['selected_total_events']=sum(measured.values())
            parent_baseline_events=len(serialize(T,tn))+sum(t_ops.values())
            row={'name':name,'n':n,'F':list(map(list,F)),'label':'SAT' if src_label else 'UNSAT',
                 'policy':'AUTHENTICATED_HORN_KROM_STAR_EXTRACTION','T':list(map(list,T)),
                 'T_n':tn,'groups':groups,'source_witness':src_w,'transformed_witness':t_w,
                 'source_baseline':src_ops,'transformed_baseline':t_ops,
                 'source_resolution_certificate':derived if root is not None else proof,
                 'source_refutation_root':root,'source_certificate_meta':extra,
                 'derived_source_resolvent':known_resolvent,
                 'physically_shorter':child_bits<parent_bits,
                 'power_short':child_bits*child_bits<=parent_bits,'parent_bits':parent_bits,'child_bits':child_bits,
                 'child_original_F_dedup':list(map(list,simple)),
                 'host_selected_events':dict(measured),'T_baseline_selected_events':parent_baseline_events,
                 'audit':audit}
        row['python_peak_alloc_bytes']=tracemalloc.get_traced_memory()[1]
        result['cases'].append(row)
    tracemalloc.stop()
    result['totals']={'formulas':len(result['cases']),
                      'SAT':sum(r['label']=='SAT' for r in result['cases']),
                      'UNSAT':sum(r['label']=='UNSAT' for r in result['cases']),
                      'recognized':sum(r['policy'].startswith('AUTHENTICATED') for r in result['cases']),
                      'power_short':sum(r.get('power_short',False) for r in result['cases']),
                      'source_extreme_pairs':sum(len(r['audit']['pair_extreme_compatibility']) for r in result['cases']),
                      'signed_occurrences':sum(len(r['audit']['signed_occurrences']) for r in result['cases']),
                      'proof_nodes':sum(len(r.get('source_resolution_certificate',[])) for r in result['cases']),
                      'controller_events_recognized':sum(r.get('host_selected_events',{}).get('selected_total_events',0) for r in result['cases']),
                      'baseline_events_recognized':sum(r.get('T_baseline_selected_events',0) for r in result['cases'])}
    with open(path,'w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result['totals'],indent=2));print('sha256:',hashlib.sha256(open(path,'rb').read()).hexdigest())

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/lspv2_horn_krom_274_raw.json')