#!/usr/bin/env python3
"""AFFINE-PROFILE-CROSSOVER234: connected exact22 XOR3 profile and resource controls.

Python 3.10+, standard library for core calculations; optional SciPy/HiGHS for
finite syntactic hitting-set optima. Retains exact source template/connector.
Usage: python 2026-10-29_1715_LSPV-2_AFFINE_PROFILE_CROSSOVER234_repro.py > raw234.json
"""
import itertools, json, math, time, tracemalloc, hashlib, random
from collections import Counter, defaultdict
from pathlib import Path
from connector231 import (validate, join, W1, G, local_profile, simple_models,
                          select_slot, shift_clause, eval_clause, renamed)


def parity_block(rhs=0):
    assert rhs in (0, 1)
    clauses=[]
    for bits in itertools.product((0,1),repeat=3):
        if (sum(bits) & 1)!=rhs:
            clauses.append(tuple(-j if val else j for j,val in enumerate(bits,1)))
    assert len(clauses)==4
    validate(clauses)
    for bits in itertools.product((0,1),repeat=3):
        satisfied=all(any(bits[abs(l)-1]==int(l>0) for l in c) for c in clauses)
        assert satisfied == ((sum(bits) & 1)==rhs)
    return clauses


def compile_chain(k, table, witness, anchor=None):
    """Canonical left-associative connector; returns full formula, SAT model, Y and decomposition."""
    assert k>=1
    source=parity_block(0)
    model={1:0,2:0,3:0}
    y=[1,2,3]
    bags=[set(range(1,4))]; edges=[]
    def attached(H,K,modelH,modelK,bags,edges):
        nH=max(abs(l) for c in H for l in c)
        ix,slx,x=select_slot(H,'last'); iy,sly,z=select_slot(K,'last')
        oldvars={abs(l) for l in H[ix]}
        newvars={nH+abs(l) for l in K[iy]}
        oldattach=next(i for i,B in enumerate(bags) if oldvars<=B)
        bagK={nH+j for j in range(1,max(abs(l) for c in K for l in c)+1)}
        idxK=len(bags); bags.append(bagK)
        idxC=len(bags)
        m=len(K); nk=max(abs(l) for c in K for l in c)
        bagC=oldvars | newvars | set(range(nH+nk+1,nH+nk+31))
        assert len(bagC)<=36
        bags.append(bagC)
        edges.extend([(oldattach,idxC),(idxK,idxC)])
        out,mod,info=join(H,K,modelH,modelK,mode='last',witness=witness)
        return out,mod,info,bags,edges,nH
    for i in range(2,k+1):
        source,model,info,bags,edges,nH=attached(source,parity_block(0),model,{j:0 for j in (1,2,3)},bags,edges)
        y.extend([nH+j for j in range(1,4)])
    if anchor is not None:
        assert anchor in ('SAT','UNSAT')
        core=G if anchor=='SAT' else W1
        core_model=next(simple_models(G)) if anchor=='SAT' else None
        md={j:int((core_model>>(j-1))&1) for j in range(1,16)} if core_model is not None else None
        source,model,info,bags,edges,nH=attached(source,core,model,md,bags,edges)
    validate(source)
    assert len(y)==3*k
    assert len(bags)==(2*k-1)+(2 if anchor else 0)
    return source,model,y,bags,edges


def verify_decomposition(cs,bags,edges):
    n=max(abs(l) for c in cs for l in c)
    assert len(edges)==len(bags)-1
    adj=[[] for _ in bags]
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    def bfs(initial,allow):
        seen={initial};todo=[initial]
        while todo:
            for v in adj[todo.pop()]:
                if v in allow and v not in seen:seen.add(v);todo.append(v)
        return seen
    assert len(bfs(0,set(range(len(bags)))))==len(bags)
    assert all(any(set(map(abs,c))<=B for B in bags) for c in cs)
    for v in range(1,n+1):
        owns={i for i,B in enumerate(bags) if v in B}
        assert owns and bfs(next(iter(owns)),owns)==owns
    return max(map(len,bags))-1


def linear_rank(rows):
    basis={}
    for row in rows:
        a=row
        while a:
            j=a.bit_length()-1
            if j not in basis:basis[j]=a;break
            a^=basis[j]
    return len(basis)


def parity_rows(k):
    return [7 << (3*j) for j in range(k)]


def sat_profile(i,k):
    for j in range(k):
        v=(i>>(3*j))&7
        if v.bit_count()&1:return False
    return True


def check_canonical(cs,k,table,witness):
    # One uniform recognizer; SAT/UNSAT labels are NOT supplied.
    for label in ('SAT','UNSAT'):
        want,*_=compile_chain(k,table,witness,anchor=label)
        if cs==want:return label
    return 'UNKNOWN'


def bdd_nodes(k):
    """A reduced ordered decision diagram with 5k internal nodes, 0/1 terminal ids."""
    nodes={};ok=1
    # Build from last block to first; prefix partial parity 0/1 is state.
    for j in range(k-1,-1,-1):
        a,b,c=(3*j+1,3*j+2,3*j+3)
        # c: for even prefix bit 0, c=0 continues; for prefix 1, c=1 continues.
        evenC=len(nodes)+2;nodes[evenC]=(c,ok,0)
        oddC =len(nodes)+2;nodes[oddC] =(c,0,ok)
        # b: state after a, branches between evenC and oddC.
        evenB=len(nodes)+2;nodes[evenB]=(b,evenC,oddC)
        oddB =len(nodes)+2;nodes[oddB] =(b,oddC,evenC)
        root=len(nodes)+2;nodes[root]=(a,evenB,oddB)
        ok=root
    assert len(nodes)==5*k
    return ok,nodes


def eval_bdd(root,nodes,mask):
    state=root
    while state>=2:
        v,low,hi=nodes[state];state=hi if ((mask>>(v-1))&1) else low
    return bool(state)


def encode_lengths(k):
    b=3*k;w=math.ceil(math.log2(b+1));h=math.ceil(math.log2(5*k+2))
    header=2*w
    return {'w':w,'h':h,'dense_bits':header+(1<<b),
            'sparse_affine_bits':header+k*(3*w+1),
            'robdd_bits':header+5*k*(w+2*h),
            'robdd_nonterminals':5*k}


def read_counts(cs,y):
    Y=set(y);Z={abs(l) for c in cs for l in c}-Y
    internal=[c for c in cs if all(abs(l) not in Y for l in c)]
    # One private module Z, Y global. Clause-hitting objective defined only on internal clauses.
    degree4_lower=math.ceil(len(internal)/4)
    # Greedy upper is NOT claimed optimum.
    uncovered=set(range(len(internal)));hit=set()
    while uncovered:
        scores=Counter(abs(l) for i in uncovered for l in internal[i]);best=max(scores,key=lambda z:(scores[z],-z))
        hit.add(best);uncovered={i for i in uncovered if best not in set(map(abs,internal[i]))}
    return {'boundary_b':len(Y),'private_vars':len(Z),'private_only_clauses':len(internal),
            'q_lower_4degree':degree4_lower,'q_greedy_upper':len(hit),'q_greedy_witness':sorted(hit)}


def exact_hitting_milp(cs,y):
    try:
        import numpy as np
        from scipy.optimize import milp, Bounds, LinearConstraint
    except ImportError:return None
    Y=set(y);Z=sorted({abs(l) for c in cs for l in c}-Y)
    private=[c for c in cs if not any(abs(l) in Y for l in c)]
    from scipy.sparse import lil_matrix
    A=lil_matrix((len(private),len(Z)),dtype=float);col={v:i for i,v in enumerate(Z)}
    for row,c in enumerate(private):
        for l in c:A[row,col[abs(l)]]=1
    r=milp(np.ones(len(Z)),integrality=np.ones(len(Z)),bounds=Bounds(0,1),
        constraints=LinearConstraint(A.tocsr(),np.ones(len(private)),np.full(len(private),np.inf)),
        options={'time_limit':6.0,'mip_rel_gap':0.0})
    if r.x is None:return {'status':str(r.message),'proven_optimal':False}
    chosen={Z[i] for i,x in enumerate(r.x) if x>.5}
    assert all(any(abs(l) in chosen for l in c) for c in private)
    return {'size':len(chosen),'witness':sorted(chosen),'proven_optimal_solver_status':bool(r.status==0),
            'solver_message':str(r.message),'mip_gap':float(getattr(r,'mip_gap',math.nan))}


def dpll(cs, node_cap=400000):
    """Complete DPLL on arbitrary signed CNF, with full failed paths charged."""
    nodes=0;peak_depth=0
    def go(clauses,assign,depth):
        nonlocal nodes,peak_depth
        nodes+=1;peak_depth=max(peak_depth,depth)
        if nodes>node_cap:raise RuntimeError('DPLL node cap reached: not a decision')
        work=list(clauses);a=assign.copy()
        while True:
            work2=[];units=[]
            for c in work:
                if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
                d=tuple(l for l in c if abs(l) not in a)
                if not d:return False
                if len(d)==1:units.append(d[0])
                work2.append(d)
            work=work2
            if not work:return True
            if not units:break
            for l in units:
                v=abs(l);vv=int(l>0)
                if v in a and a[v]!=vv:return False
                a[v]=vv
        freq=Counter(abs(l) for c in work for l in c)
        v=max(freq,key=lambda x:(freq[x],-x))
        return go(work,{**a,v:0},depth+1) or go(work,{**a,v:1},depth+1)
    value=go(tuple(cs),{},0)
    return {'answer':value,'nodes':nodes,'max_depth':peak_depth}


def table_profile(k,active=True):
    size=1<<(3*k);bitpack=bytearray((size+7)//8);count=0
    for a in range(size):
        good=bool(active) and sat_profile(a,k)
        if good:bitpack[a>>3]|=1<<(a&7);count+=1
    return {'count':count,'bytes':len(bitpack),'sha256':hashlib.sha256(bitpack).hexdigest()}


def stream_profile(k,active=True):
    count=0
    for a in range(1<<(3*k)):
        if active and sat_profile(a,k):count+=1
    return {'count':count}


def compact_profile(k,active=True,format_name='affine'):
    header=2*math.ceil(math.log2(3*k+1))
    if not active:
        return {'rank':None,'row_count':0,'nodes':0,'encoded_bits':header+1,'active':False}
    if format_name=='affine':
        rows=parity_rows(k)
        return {'rank':linear_rank(rows),'row_count':len(rows),
                'encoded_bits':encode_lengths(k)['sparse_affine_bits'],'active':True}
    root,nodes=bdd_nodes(k)
    return {'root':root,'nodes':len(nodes),'encoded_bits':encode_lengths(k)['robdd_bits'],
            'active':True}


def authenticated_work(cs,k,method,table,witness):
    # A SINGLE deterministic program recognizes both SAT and UNSAT answers.
    # The experiment's true label is not passed to this solver.
    if method=='dpll':return dpll(cs)
    label=check_canonical(cs,k,table,witness)
    if label=='UNKNOWN':raise ValueError('outside authenticated canonical source class')
    if method=='recognize':return label
    active=(label=='SAT')
    if method=='table':return table_profile(k,active)
    if method=='stream':return stream_profile(k,active)
    if method=='affine':return compact_profile(k,active,'affine')
    if method=='robdd':return compact_profile(k,active,'robdd')
    raise ValueError(method)


def measured_pipeline(k,fixture_label,method,table,witness):
    cs,_,_,_,_=compile_chain(k,table,witness,fixture_label)
    return authenticated_work(cs,k,method,table,witness)


def timer(func):
    tracemalloc.start();start=time.perf_counter()
    try:
        output=func();error=None
    except Exception as exc:
        output={};error=repr(exc)
    seconds=time.perf_counter()-start;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return {'seconds':round(seconds,6),'peak_python_traced_bytes':peak,'output':output,'error':error}


def run():
    table,witness,guard=local_profile()
    assert guard['source_W1_models']==0
    assert guard['source_G_models']==272
    results={'id':'AFFINE_PROFILE_CROSSOVER234','date':'2026-10-29','guard':guard,
             'closed_form':{'n_chain':'33*k-30','m_chain':'44*k-40','n_paired':'33*k+15',
               'm_paired':'44*k+20','b':'3*k','affine_codimension_SAT':'k',
               'treewidth_upper':35},'records':[],'benchmark':[],'renamed_controls':[]}
    for k in (1,2,3,4,5,6,7,8,9,12):
        positive,model,Y,bags,edges=compile_chain(k,table,witness,'SAT')
        negative,_,Yn,bagsn,edgesn=compile_chain(k,table,witness,'UNSAT')
        assert Y==Yn
        n,m=validate(positive);assert validate(negative)==(n,m)
        assert n==33*k+15 and m==44*k+20
        assert model is not None and all(any(model[abs(l)]==int(l>0) for l in c) for c in positive)
        assert sorted(sorted(map(abs,c)) for c in positive)==sorted(sorted(map(abs,c)) for c in negative)
        signs=sum(1 for a,b in zip(sum(positive,()),sum(negative,())) if a!=-b and a!=b)
        differences=sum(1 for c,d in zip(positive,negative) for x,y in zip(c,d) if x!=y)
        assert differences==2
        wt=verify_decomposition(positive,bags,edges)
        assert verify_decomposition(negative,bagsn,edgesn)<=35
        assert wt<=35
        assert linear_rank(parity_rows(k))==k
        r={'k':k,'n':n,'m':m,'canonical_source_bits':(4*m+2)*math.ceil(math.log2(64*(n+m+1))),
           'boundary_b':len(Y),'affine_rank':k,'affine_codimension':k,
           'full_relation_cardinality_SAT':1<<(2*k),'full_relation_cardinality_UNSAT':0,
           'tw_upper':wt,'unsigned_scopes_match':True,'source_literal_sign_differences':differences,
           'encoding':encode_lengths(k),'hitting':read_counts(positive,Y)}
        if k<=9:r['hitting']['milp']=exact_hitting_milp(positive,Y)
        if k<=4:
            root,nodes=bdd_nodes(k)
            for a in range(1<<(3*k)):
                assert eval_bdd(root,nodes,a)==sat_profile(a,k)
        if k<=3:
            scrambled,permutation=renamed(positive,seed=234+k)
            assert validate(scrambled)==(n,m)
            permuted_model={permutation[v]:vv for v,vv in model.items()}
            assert all(any(permuted_model[abs(l)]==int(l>0) for l in c) for c in scrambled)
            assert check_canonical(scrambled,k,table,witness)=='UNKNOWN'
            results['renamed_controls'].append({'k':k,'seed':234+k,'n':n,
                   'signed_quotas':True,'witness_preserved':True,
                   'template_recognizer':'UNKNOWN'})
            for mask in range(1<<(3*k)):
                assert sat_profile(mask,k)==(sum((mask>>(3*j))&7 for j in range(k))>=0 and all(((mask>>(3*j))&7).bit_count()%2==0 for j in range(k)))
        results['records'].append(r)
        if k<=5:
            for label,formula in [('SAT',positive),('UNSAT',negative)]:
                for method in ('recognize','dpll','stream','table','affine','robdd'):
                    if method in ('stream','table') and k>4:continue
                    if method=='dpll' and (k>2 or (label=='UNSAT' and k>1)):continue
                    # Full same-run generator + source recognizer + method.
                    metric=timer(lambda: measured_pipeline(k,label,method,table,witness))
                    if method=='recognize':assert metric['output']==label
                    elif method=='dpll':assert metric['output'].get('answer')==(label=='SAT')
                    elif method in ('stream','table'):
                        assert metric['output'].get('count')== (1<<(2*k) if label=='SAT' else 0)
                    assert metric['error'] is None,metric
                    results['benchmark'].append({'k':k,'label':label,'method':method,**metric})
    for row in results['records']:
        k=row['k'];p=row['encoding']
        row['table_vs_bdd']='BDD-smaller' if p['robdd_bits']<p['dense_bits'] else 'TABLE-smaller'
        row['table_vs_affine']='AFFINE-smaller' if p['sparse_affine_bits']<p['dense_bits'] else 'TABLE-smaller'
        if k<=9:
            assert row['hitting']['milp'] is not None
    assert results['records'][1]['encoding']['robdd_bits']>results['records'][1]['encoding']['dense_bits']
    assert results['records'][2]['encoding']['robdd_bits']<results['records'][2]['encoding']['dense_bits']
    return results


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))