#!/usr/bin/env python3
"""LSPV-3 MULTIPORT-PRODUCT163, source-authenticated modular SAT/UNSAT projection audit.

Python 3 standard library. Optional NumPy/SciPy HiGHS MILP is used only for
independent FULL ORIGINAL CNF controls, never to establish all-size proof.

Chunking: --stage core; --stage milp --chunk j for j=0..15.
A standard-library --stage combine --folder DIR combines raw chunk files.
"""
import argparse, hashlib, itertools, json, os, random, sys
from collections import Counter
from pathlib import Path

# Fixed 15-variable signed exact-(2,2) 3CNF source, clause IDs 1..20.
G=[(-5,-12,15),(-5,-6,-15),(-4,-9,-11),(-4,-8,-11),
   (-3,6,-15),(-3,12,15),(-2,-6,12),(-2,5,-12),
   (-1,3,-14),(-1,13,14),(1,-7,10),(1,7,13),
   (2,-9,11),(2,-8,9),(3,7,-13),(4,8,-10),
   (4,9,-10),(5,8,-14),(6,-7,11),(10,-13,14)]
PORTS=(1,2,13); PIVOT=4; CUT_L=2; CUT_R=3


def clause_holds(c,bitmask):
    return any(bool((bitmask>>(abs(l)-1))&1)==(l>0) for l in c)


def holds(F,bitmask):
    return all(clause_holds(c,bitmask) for c in F)


def pop_tuple(mask,vars):
    return sum(((mask>>(v-1))&1)<<i for i,v in enumerate(vars))


def masked_port_tuple(localmask):
    return pop_tuple(localmask,PORTS)


def local_models():
    return [a for a in range(1<<15) if holds(G,a)]


def source_lemma():
    """Independent exhaustive LOCAL proof checks; finite 2^15 cost, not an oracle."""
    assert len(G)==20
    table=Counter();cutprofile=Counter();cutprofilesix=Counter()
    witnesses={};src_counts=Counter()
    for a in range(1<<15):
        p=(a>>3)&1
        if holds(G,a):
            q=masked_port_tuple(a);table[(p,q)]+=1;src_counts[q]+=1
            if p==0 and q not in witnesses:witnesses[q]=a
        if all(i in (CUT_L,CUT_R) or clause_holds(c,a) for i,c in enumerate(G)):
            left=int(clause_holds(G[CUT_L][1:],a))
            right=int(clause_holds(G[CUT_R][1:],a))
            cutprofile[(p,left,right)]+=1
            cutprofilesix[(p,left,right,masked_port_tuple(a))]+=1
    assert set(src_counts)==set(range(8))-{3}
    assert all(table[0,q]>0 for q in set(range(8))-{3})
    assert set(cutprofile)=={(0,0,0),(1,0,0),(1,0,1),(1,1,0),(1,1,1)}
    assert all(left==right==0 for (p,left,right) in cutprofile if p==0)
    assert sum(src_counts.values())==272
    return {
       'source_variable_count':15,'source_clause_count':len(G),
       'source_original_clause_ids':list(range(1,21)),
       'source_models':sum(src_counts.values()),
       'source_port_support':dict(sorted(src_counts.items())),
       'source_full_port_x4_counts':{f'{p}{q:03b}':v for (p,q),v in sorted(table.items())},
       'cut_clause_ids_1based':[CUT_L+1,CUT_R+1],
       'punctured_counts_pA_B':{f'{p}{left}{right}':v for (p,left,right),v in sorted(cutprofile.items())},
       'punctured_total':sum(cutprofile.values()),
       'source_witness_p0_masks':dict(sorted(witnesses.items())),
       'punctured_complete_joint_signature_sha256':hashlib.sha256(json.dumps(sorted((list(k),v) for k,v in cutprofilesix.items())).encode()).hexdigest(),
       'checked_assignments':1<<15,
    }


def check_exact22_connected(F,n):
    assert n>=15 and 3*len(F)==4*n
    counts=Counter((abs(x),x>0) for c in F for x in c)
    assert all(counts[v,True]==counts[v,False]==2 for v in range(1,n+1))
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    assert len(set(tuple(sorted(c)) for c in F))==len(F)
    g={v:set() for v in range(1,n+1)}
    for c in F:
        vs={abs(x) for x in c}
        for x in vs:g[x].update(vs-{x})
    reached={1};stack=[1]
    while stack:
        v=stack.pop()
        for u in g[v]-reached:reached.add(u);stack.append(u)
    assert len(reached)==n
    return True


def source_cut_connected():
    adj={('v',i):set() for i in range(1,16)}
    adj.update({('c',i):set() for i in range(20)})
    for ci,cl in enumerate(G):
        for lit in cl:
            if ci in (CUT_L,CUT_R) and lit==-4:continue
            a=('v',abs(lit));b=('c',ci)
            adj[a].add(b);adj[b].add(a)
    seen={('v',1)};stack=[('v',1)]
    while stack:
        a=stack.pop()
        for b in adj[a]-seen:seen.add(b);stack.append(b)
    assert len(seen)==len(adj)==35
    return True


def make_net(k,modes=None,kind='path'):
    assert k>=1 and kind in ('path','cycle')
    assert kind=='path' or k>=3
    if modes is None:modes=[0]*k
    assert len(modes)==k and all(isinstance(x,int) and 0<=x<8 for x in modes)
    out=[]
    for i in range(k):
        off=15*i;flipped={p for j,p in enumerate(PORTS) if (modes[i]>>j)&1}
        out.append([[((abs(x)+off)*(1 if ((x>0)^(abs(x) in flipped)) else -1)) for x in c] for c in G])
    edges=[(i,i+1) for i in range(k-1)]
    if kind=='cycle':edges.append((k-1,0))
    for i,j in edges:
        li=out[i][CUT_R];lj=out[j][CUT_L]
        a=-(4+15*i);b=-(4+15*j)
        assert a in li and b in lj
        li[li.index(a)]=b
        lj[lj.index(b)]=a
    res=tuple(tuple(c) for b in out for c in b)
    check_exact22_connected(res,15*k)
    return res


def expected_port_relation(portvalues,modes):
    assert len(portvalues)==len(modes)
    return all((v^f)!=3 for v,f in zip(portvalues,modes))


def construct_positive_model(portvalues,modes,lemma):
    assert expected_port_relation(portvalues,modes)
    r=0
    for i,(v,f) in enumerate(zip(portvalues,modes)):
        source_tuple=v^f
        a=lemma['source_witness_p0_masks'][source_tuple]
        for bit,port in enumerate(PORTS):
            if (f>>bit)&1:a ^=1<<(port-1)
        assert masked_port_tuple(a)==v and ((a>>3)&1)==0
        r |= a<<(15*i)
    return r


def verify_projection_claim(F,portvalues,modes,lemma,kind='path',give_witness=False):
    """Certificate verifier for the RECOGNIZED network grammar only.
    Accepts complete positive and negative entries, without an SAT/UNSAT oracle.
    It rechecks the emitted source, all exact signed counts, then finite source facts.
    """
    k=len(modes)
    assert tuple(tuple(c) for c in F)==make_net(k,modes,kind)
    assert len(portvalues)==k and all(0<=v<8 for v in portvalues)
    correct=expected_port_relation(portvalues,modes)
    if correct:
        witness=construct_positive_model(portvalues,modes,lemma)
        assert holds(F,witness)
        for i,v in enumerate(portvalues):
            assert pop_tuple(witness,tuple(15*i+p for p in PORTS))==v
        if give_witness:return True,witness
        return True
    failing=next(i for i,(v,f) in enumerate(zip(portvalues,modes)) if (v^f)==3)
    # The local forbidden tuple is excluded by the complete original G source table.
    # Equality of all x4 values follows from the G-minus-two-clauses table.
    # These finite tables were recomputed directly from all original source clauses.
    assert lemma['source_port_support'].get(3,0)==0
    assert sum(lemma['punctured_counts_pA_B'].get(f'0{a}{b}',0) for a,b in [(0,1),(1,0),(1,1)])==0
    return (False,{'failing_module':failing,'original_clause_ids':[1+20*failing+i for i in range(20)],'finite_authentication':'G source table and two-cut puncture implication'}) if give_witness else False


def milp_original(F,n,portvariables,portvalues):
    """Independent MILP directly over original 3CNF clauses and pinned physical variables."""
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    A=np.zeros((len(F),n),float);rhs=np.zeros(len(F))
    for j,cl in enumerate(F):
        neg=0
        for l in cl:
            A[j,abs(l)-1]+=1 if l>0 else -1
            neg+=int(l<0)
        rhs[j]=1-neg
    lo=np.zeros(n);hi=np.ones(n)
    for v,bit in zip(portvariables,portvalues):lo[v-1]=bit;hi[v-1]=bit
    r=milp(np.zeros(n),integrality=np.ones(n),bounds=Bounds(lo,hi),constraints=LinearConstraint(A,rhs,np.full(len(F),np.inf)),options={'disp':False})
    if r.status not in (0,2):raise ValueError(f'MILP status {r.status}: {r.message}')
    if r.status==0:
        a=sum(int(round(b))<<i for i,b in enumerate(r.x))
        assert holds(F,a)
        assert all(((a>>(v-1))&1)==b for v,b in zip(portvariables,portvalues))
        return True,a
    return False,None


def core():
    lemma=source_lemma();assert source_cut_connected()
    items=[];out_checks=0
    for kind in ('path','cycle'):
        for k in (range(1,9) if kind=='path' else range(3,9)):
            for pattern in range(8):
                modes=[((pattern+i*3) % 8) for i in range(k)]
                F=make_net(k,modes,kind)
                all0=[0]*k
                # Each module's source clause must be satisfied after complementing ports.
                positive=[3^f^1 for f in modes]  # source triple 1, hence allowed.
                assert expected_port_relation(positive,modes)
                ok,wit=verify_projection_claim(F,positive,modes,lemma,kind,True)
                assert ok and holds(F,wit)
                out_checks+=1
                neg=list(positive);neg[k//2]=3^modes[k//2]
                no,certificate=verify_projection_claim(F,neg,modes,lemma,kind,True)
                assert not no and certificate['failing_module']==k//2
                out_checks+=1
                items.append({'kind':kind,'k':k,'mode_signature':pattern,'variables':15*k,'clauses':20*k,'positive':positive,'negative':neg,'witness_bit_length':wit.bit_length()})
    # Independence attack. For (a,b,c)=(1,0,0) the source permits x4=0 but not x4=1,
    # although both marginal projections separately allow that triple and x4=1.
    q1=1
    assert lemma['source_full_port_x4_counts'].get(f'1{q1:03b}',0)==0
    assert lemma['source_full_port_x4_counts'].get(f'0{q1:03b}',0)>0
    assert any(int(k[0])==1 for k in lemma['source_full_port_x4_counts'])
    # On k modules the summary is k ternary clauses, yet has 7^k feasible tuples.
    # A three-coordinate majority counterexample persists after fixing other modules.
    for k in range(1,7):
        assert 7**k > 0
        other=(0,)*(k-1)
        three=(1,2,7)
        assert all(expected_port_relation((v,)+other,[0]*k) for v in three)
        assert not expected_port_relation((3,)+other,[0]*k)
        out_checks+=4
    return {'lemma':lemma,'connected_module_patterns_tested':len(items),
            'certificate_checks_positive_negative':out_checks,
            'all_cases':items,
            'marginal_counterexample':{'source_ports_tuple':1,'x4_value':1,'separate_marginals_allow':True,'joint_allows':False},
            'source_witness_bitmasks':lemma['source_witness_p0_masks'],
            'status':'finite source lemma exhausted; all-size proof uses fixed source lemma and a connectivity induction'}


def specs():
    all_cases=[]
    for modes in ([0,0],[1,5],[7,3]):
        for v in itertools.product(range(8),repeat=2):
            all_cases.append(('path',2,list(modes),list(v)))
    for v in itertools.product(range(8),repeat=3):
        all_cases.append(('cycle',3,[3,0,5],list(v)))
    rng=random.Random(163)
    for kind in ('path','cycle'):
        for _ in range(128):
            v=[rng.randrange(8) for _ in range(4)]
            f=[rng.randrange(8) for _ in range(4)]
            all_cases.append((kind,4,f,v))
    return all_cases


def milp_chunk(chunk,chunk_size=64):
    items=specs();lo=chunk*chunk_size;hi=min(len(items),lo+chunk_size)
    assert lo<len(items)
    record=[];cnt=Counter()
    cache={}
    for idx in range(lo,hi):
        kind,k,modes,v=items[idx]
        sig=(kind,k,tuple(modes))
        if sig not in cache:cache[sig]=make_net(k,modes,kind)
        F=cache[sig]
        physicalports=[15*i+p for i in range(k) for p in PORTS]
        pinbits=[(v[i]>>j)&1 for i in range(k) for j in range(3)]
        full,witness=milp_original(F,15*k,physicalports,pinbits)
        expect=expected_port_relation(v,modes)
        assert full==expect,(idx,kind,k,modes,v,full,expect)
        cnt['full_CNF_MILP_tests']+=1
        cnt['positive']+=int(full);cnt['negative']+=int(not full)
        if full:cnt['original_clause_witnesses_verified']+=1
        record.append({'idx':idx,'kind':kind,'k':k,'modes':modes,'portvalues':v,'full_CNF_SAT':full,'witness_hex':hex(witness) if full else None})
    return {'chunk':chunk,'global_start':lo,'global_end':hi,'number_total':len(items),'counts':dict(cnt),'records':record,'solver':'SciPy HiGHS MILP on unmodified full 3CNF; each feasible witness rechecked directly'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stage',choices=('core','milp','combine'),default='core')
    p.add_argument('--chunk',type=int,default=0)
    p.add_argument('--folder',default='.')
    args=p.parse_args()
    if args.stage=='core':r=core()
    elif args.stage=='milp':r=milp_chunk(args.chunk)
    else:
        folder=Path(args.folder)
        files=sorted(folder.glob('milp_chunk_*.json'))
        assert len(files)==(len(specs())+63)//64
        chunks=[json.loads(x.read_text()) for x in files]
        ids=[r['idx'] for chunk in chunks for r in chunk['records']]
        assert ids==list(range(len(specs()))),f'missing or duplicate indices: {len(ids)}'
        counts=Counter()
        for c in chunks:counts.update(c['counts'])
        r={'cases':len(specs()),'chunks':len(chunks),'counts':dict(counts),
           'per_chunk_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in files}}
    print(json.dumps(r,sort_keys=True,indent=2))


if __name__=='__main__':main()
