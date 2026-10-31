#!/usr/bin/env python3
"""LSPV-2 HORN-FRONTIER273, standalone stdlib finite falsification.
Every source clause carries an index.  All proof nodes are ordinary resolution.
The projection may be exponentially long; accessor does not materialize it.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, time, tracemalloc
from collections import Counter
from pathlib import Path

SEED=202610310612

def source(k, no=False):
    # q_i=1+i, a_i=k+2+2*i, b_i=k+3+2*i
    q=lambda i:i+1
    a=lambda i:k+2+2*i
    b=lambda i:k+3+2*i
    C=[(q(0),),(-q(k),)]
    idx={}
    for i in range(k):
        idx[i]={}
        for s,v in [('a',a(i)),('b',b(i))]:
            idx[i][s]=len(C)
            C.append((-q(i),-v,q(i+1)))
    if no:
        for i in range(k):
            idx[i]['h']=len(C)
            C.append((a(i),b(i)))
    return C,idx,3*k+1

def norm(cl):
    d=set(cl)
    if any(-v in d for v in d):
        raise ValueError('tautological resolvent')
    return tuple(sorted(d,key=lambda x:(abs(x),x<0)))

def resolve(a,b,p):
    a,b=set(a),set(b)
    if p in a and -p in b: pass
    elif -p in a and p in b: a,b=b,a
    else: raise AssertionError(('bad pivot',p,a,b))
    return norm((a-{p})|(b-{-p}))

def make_proof(C,k,idx,word=None):
    """If word is set, derive boundary blocker; else derive empty for NO."""
    steps=[]; terms=[norm(c) for c in C]
    def add(left,right,p):
        cl=resolve(terms[left],terms[right],p)
        steps.append({'parents':[left,right],'pivot':p,'clause':list(cl)})
        terms.append(cl)
        return len(terms)-1
    if word is not None:
        assert len(word)==k
        root=0
        for i,bit in enumerate(word):
            v=k+2+2*i+bit
            root=add(root,idx[i]['b' if bit else 'a'],i+1)
        root=add(root,1,k+1)
        assert len(terms[root])==k and (k>0)
    else:
        root=0
        for i in range(k):
            a=k+2+2*i; b=a+1
            s=add(idx[i]['h'],idx[i]['a'],a)
            t=add(s,idx[i]['b'],b)
            root=add(root,t,i+1)
        root=add(root,1,k+1)
        assert terms[root]==()
    return {'root':root,'steps':steps,'root_clause':list(terms[root])}

def verify_proof(C,proof):
    terms=[norm(c) for c in C]
    for step in proof['steps']:
        a,b=step['parents'];p=step['pivot']
        if not (0<=a<len(terms) and 0<=b<len(terms)):raise AssertionError('forward proof ref')
        derived=resolve(terms[a],terms[b],p)
        if list(derived)!=step['clause']:raise AssertionError('bad derived clause')
        terms.append(derived)
    assert proof['root']==len(terms)-1
    assert list(terms[-1])==proof['root_clause']
    return len(terms)-len(C)

def clauses_true(C,bits):
    return all(any(bits[abs(l)-1]==(l>0) for l in c) for c in C)

def tcounts(C,bits):
    return [sum(bits[abs(l)-1]==(l>0) for l in c) for c in C]

def ext_modes(c,d):
    a={abs(l):(l>0) for l in c};b={abs(l):(l>0) for l in d}
    same=any(a[x]==b[x] for x in a.keys()&b.keys())
    opp=any(a[x]!=b[x] for x in a.keys()&b.keys())
    return {'SS':not opp,'SU':not same,'US':not same,'UU':not opp}

def flip_controls(C,n):
    traces={}
    for start in [0,1]:
        bits=[bool(start)]*n
        flips=[0,min(1,n-1),min(2,n-1)] if n else []
        frames=[]
        for z in [-1]+flips:
            if z>=0: bits[z]=not bits[z]
            counts=tcounts(C,bits)
            frames.append({'flip':z if z>=0 else None,'true_counts':counts,'N0_N1_N2_N3':[counts.count(i) for i in range(4)],'SAT':all(c>=1 for c in counts)})
        traces[str(start)]=frames
    # Compact signed occurrence targets: each clause and each literal targets
    local=[]
    for j,c in enumerate(C):
        local.append({'clause_id':j,'targets':[{'occurrence':h,'literal':l,'variable':abs(l),
        'S':int(l>0),'invert_S_U':int(l<0),'U':int(l<0),'invert_U_S':int(l>0)} for h,l in enumerate(c)]})
    pair=[{'i':i,'j':j,'matrix':ext_modes(C[i],C[j])} for i in range(len(C)) for j in range(i+1,len(C))]
    return {'endpoint_flip_trails':traces,'signed_occurrence_targets':local,'pair_extremes':pair}

def boundary_projection_feasible(k,bb):
    return any(not bb[2*i] and not bb[2*i+1] for i in range(k))

def proj(k,no):
    d=[]
    for bits in itertools.product([0,1],repeat=k):
        # original signed variables and remapped boundary variables
        clause=tuple(-(2*i+1+bit) for i,bit in enumerate(bits))
        d.append(clause)
    if no:d.extend((2*i+1,2*i+2) for i in range(k))
    return d

def text_child(k,no):
    clauses=proj(k,no)
    return ('p cnf %d %d\n'%(2*k,len(clauses)))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def prefix_len(k,R):
    # length of first R lexicographic choice clauses without materializing them
    assert 0<=R<=2**k
    s=R*(2+2*k)
    for i in range(k):
        half=1<<(k-i-1)
        ones=(R//(2*half))*half+max(0,R%(2*half)-half)
        s+=(R-ones)*len(str(2*i+1))+ones*len(str(2*i+2))
    return s

def character(k,no,pos):
    M=1<<k
    header=f'p cnf {2*k} {M+(k if no else 0)}\n'
    full=prefix_len(k,M)
    if pos <len(header):return header[pos]
    pos-=len(header)
    if pos>=full:
        pos-=full
        for i in range(k):
            row=f'{2*i+1} {2*i+2} 0\n'
            if pos<len(row):return row[pos]
            pos-=len(row)
        raise IndexError
    low,high=0,M
    while low+1<high:
        middle=(low+high)//2
        if prefix_len(k,middle)<=pos: low=middle
        else:high=middle
    bitword=[(low>>(k-i-1))&1 for i in range(k)]
    row=' '.join('-'+str(2*i+1+bit) for i,bit in enumerate(bitword))+' 0\n'
    return row[pos-prefix_len(k,low)]

def run_dpll(C,n):
    counts=Counter();memo={}
    def rec(partial):
        counts['nodes']+=1
        part=dict(partial)
        while True:
            change=False;opencl=[]
            for c in C:
                counts['source_clauses_scanned']+=1
                und=[];sat=False
                for l in c:
                    counts['literal_probes']+=1
                    if abs(l) in part:
                        if part[abs(l)]==(l>0):sat=True;break
                    else:und.append(l)
                if sat:continue
                if not und:counts['conflict_nodes']+=1;return None
                opencl.append(und)
                if len(und)==1:
                    l=und[0];v=abs(l);vval=l>0
                    if v in part and part[v]!=vval:counts['conflict_nodes']+=1;return None
                    if v not in part:
                        part[v]=vval;counts['propagations']+=1;change=True
            if not change:break
        if not opencl:return part
        v=abs(opencl[0][0]);counts['decisions']+=1
        for val in [False,True]:
            r=rec(part|{v:val})
            if r is not None:return r
        return None
    sol=rec({});return sol,dict(counts)

def audit(k,no,random_source=False):
    C,idx,n=source(k,no)
    rng=random.Random(SEED+k*71+no)
    mapping=list(range(1,n+1));rng.shuffle(mapping)
    flips={v:rng.getrandbits(1) for v in range(1,n+1)}
    if random_source:
        S=[tuple((1 if l>0 else -1)*(-1 if flips[abs(l)] else 1)*mapping[abs(l)-1] for l in c) for c in C]
    else:S=C
    t0=time.monotonic();sol,base=run_dpll(S,n)
    if random_source:
        expected=not no
        assert (sol is not None)==expected
        # The structural proof is renaming-invariant; map proof literals and pivots.
        def convert(proof):
            def signed(x):return (1 if x>0 else -1)*(-1 if flips[abs(x)] else 1)*mapping[abs(x)-1]
            return {'root':proof['root'],'steps':[{'parents':s['parents'],'pivot':mapping[s['pivot']-1],
              'clause':list(norm(signed(l) for l in s['clause']))} for s in proof['steps']],
              'root_clause':list(norm(signed(l) for l in proof['root_clause']))}
    else:convert=lambda x:x
    if no:
        P=convert(make_proof(C,k,idx,None));verify_proof(S,P)
        proofs=[P]
    else:
        proofs=[]
        for bits in itertools.product([0,1],repeat=k):
            P=convert(make_proof(C,k,idx,bits))
            verify_proof(S,P);proofs.append(P)
    assert (sol is None)==no
    if sol is not None:assert clauses_true(S,[sol.get(v,False) for v in range(1,n+1)])
    child=text_child(k,no)
    for p in range(len(child)):
        if child[p]!=character(k,no,p):raise AssertionError(('accessor',k,no,p))
    if k<=5:
        for tup in itertools.product([False,True],repeat=2*k):
            # direct exhaustive existential test of same original source
            ext=False
            for qs in itertools.product([False,True],repeat=k+1):
                bits=list(qs)+list(tup)
                if clauses_true(C,bits):ext=True;break
            assert ext==(boundary_projection_feasible(k,tup) and (not no or all(tup[2*i] or tup[2*i+1] for i in range(k))))
            actual=all(any(tup[abs(l)-1]==(l>0) for l in c) for c in proj(k,no))
            assert actual==ext,('projection',k,no,tup)
    checks=flip_controls(S,n)
    N=len(('p cnf %d %d\n'%(n,len(S)))+''.join(' '.join(map(str,c))+' 0\n' for c in S))
    return {'k':k,'SAT':not no,'renamed':random_source,'n':n,'source_clauses':len(S),'original_bits':N,
      'child_bits':len(child),'sqrtN':N**.5,'child_power_short':len(child)<=N**.5,
      'resolution_steps':sum(len(p['steps']) for p in proofs),'proof_count':len(proofs),
      'baseline':base,'controller':{'recognition_clause_reads':len(S),'policy_trials':1,'policy_switches':int(len(child)>N**.5),'prefix_length_queries':len(child),
      'proof_resolution_steps':sum(len(p['steps']) for p in proofs),'output_char_checks':len(child),'source_clauses_scanned':len(S),
      'size_first_gate':{'prefix_rank_arithmetic':k*k,'precomputed_length':prefix_len(k,1<<k)+len(f'p cnf {2*k} {(1<<k)+(k if no else 0)}\n')+sum(len(f'{2*i+1} {2*i+2} 0\n') for i in range(k) if no),'fallback_nodes':base.get('nodes',0)}},
      'phase_seconds':round(time.monotonic()-t0,4),'source_sha256':hashlib.sha256(str(S).encode()).hexdigest(),
      'child_sha256':hashlib.sha256(child.encode()).hexdigest(),
      'pair_extreme_checks':len(checks['pair_extremes'])*4,'endpoint_frames':sum(map(len,checks['endpoint_flip_trails'].values())),
      'signed_occurrences':sum(map(len,(x['targets'] for x in checks['signed_occurrence_targets']))),
      'witness':{str(v):int(sol.get(v,False)) for v in range(1,n+1)} if sol is not None else None,
      'certificates':proofs,
      'renaming':{'mapping':mapping,'flips':flips} if random_source else None,'source_clauses_indexed':S,'controls':checks}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='/mnt/data/lspv2_horn_frontier273/raw.json');a=ap.parse_args()
    tracemalloc.start()
    runs=[]
    for k in range(1,7):
        for no in (False,True):
            runs.append(audit(k,no,False))
            if k<=4:runs.append(audit(k,no,True))
    host_current,host_peak=tracemalloc.get_traced_memory()
    tracemalloc.stop()
    raw={'host_peak_allocated_bytes':host_peak,'host_current_allocated_bytes':host_current,
         'id':'HORN-FRONTIER273','seed':SEED,'mode':'deterministic finite exhaustive for k<=5; derived proof checks k<=6',
         'test_cases':len(runs),'results':runs}
    path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':len(runs),'SAT':sum(r['SAT'] for r in runs),'UNSAT':sum(not r['SAT'] for r in runs),
      'certificates':sum(r['proof_count'] for r in runs),'proof_steps':sum(r['resolution_steps'] for r in runs),
      'child_short':sum(r['child_power_short'] for r in runs),
      'max_child_ratio':round(max(r['child_bits']/r['original_bits'] for r in runs),2),
      'baseline_nodes':sum(r['baseline']['nodes'] for r in runs),'host_peak_allocated_bytes':host_peak,
      'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()