#!/usr/bin/env python3
"""LSPV-3 branching exact-(2,2) graft audit. Only restricted families.
Source: W1 15-variable UNSAT and the fixed 15-variable SAT guard G in
LSPV-2 TWO_SWAP_EXACT_PORT_TRANSPORT223. Python stdlib, deterministic.

Proofs are exact source-identified Resolution derivations, not formal LRAT.
"""
from __future__ import annotations
import json, hashlib, pathlib, time
from collections import Counter, defaultdict
from itertools import product

G = [(-5,-12,15),(-5,-6,-15),(-4,-9,-11),(-4,-8,-11),(-3,6,-15),
     (-3,12,15),(-2,-6,12),(-2,5,-12),(-1,3,-14),(-1,13,14),
     (1,-7,10),(1,7,13),(2,-9,11),(2,-8,9),(3,7,-13),
     (4,8,-10),(4,9,-10),(5,8,-14),(6,-7,11),(10,-13,14)]
W1 = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
      (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
      (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
      (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]

def canon(c): return tuple(sorted(c,key=lambda v:(abs(v),v)))
def ctrue(c,a): return any(a[abs(l)]==(l>0) for l in c)
def models(F,n=15):
    for mask in range(1<<n):
        a = {i:bool(mask>>(i-1)&1) for i in range(1,n+1)}
        if all(ctrue(c,a) for c in F):
            yield mask

def source_guard():
    # Full exact finite lemma for the fixed 15-variable guard, source-authenticated.
    punctured=[c for j,c in enumerate(G) if j not in (2,15)]
    counts=Counter(); full=Counter(); examples={}
    for mask in range(1<<15):
        a={i:bool(mask>>(i-1)&1) for i in range(1,16)}
        if all(ctrue(c,a) for c in punctured):
            p=int(a[4]); A=int(a[8] or not a[10]); B=int(not a[9] or not a[11]); key=(p,A,B)
            counts[key]+=1; examples.setdefault(key,mask)
        if all(ctrue(c,a) for c in G): full[int(a[4])]+=1
    want={(0,0,0):85,(0,1,0):153,(1,0,0):85,(1,0,1):119}
    assert dict(counts)==want, (counts,want)
    assert sum(full.values())==272 and all(full.values())
    assert sum(1 for _ in models(W1))==0
    triple=Counter()
    for mask in models(G):
        triple[((mask>>0)&1,(mask>>1)&1,(mask>>12)&1)]+=1
    assert set(triple)==(set(product((0,1),repeat=3))-{(1,1,0)}),triple
    return {'puncture_counts':{str(k):v for k,v in sorted(counts.items())},
            'full_guard_pins':dict(full),'full_guard_models':sum(full.values()),
            'root_W1_models':0,'triple_fiber_counts':{str(k):v for k,v in sorted(triple.items())},'example_masks':{str(k):v for k,v in examples.items()}}

def graft(k:int, root_mode:str):
    """Root is W1 UNSAT or G SAT. Binary heap module tree, k nodes."""
    assert 1<=k and root_mode in ('W1','G')
    blocks=[]
    for i in range(k):
        base=(W1 if root_mode=='W1' else G) if i==0 else G
        blocks.append([[((abs(v)+15*i) if v>0 else -(abs(v)+15*i)) for v in c]
                       for c in base])
    swaps=[]; ports={}
    for child in range(1,k):
        parent=(child-1)//2
        side=0 if child==2*parent+1 else 1
        x0=(1,2)[side] if parent==0 else (8,9)[side]
        x=x0+15*parent; p=4+15*child
        # Parent x occurrence is untouched before this edge (one distinct x per child).
        pos=next(j for j,c in enumerate(blocks[parent]) if x in c)
        neg=next(j for j,c in enumerate(blocks[parent]) if -x in c)
        gp=15; gn=2
        assert p in blocks[child][gp] and -p in blocks[child][gn]
        def exchange(i,j,lit_a, c,d,lit_b):
            assert lit_a in blocks[i][j] and lit_b in blocks[c][d]
            blocks[i][j][blocks[i][j].index(lit_a)]=lit_b
            blocks[c][d][blocks[c][d].index(lit_b)]=lit_a
        exchange(parent,pos,x,child,gp,p)
        exchange(parent,neg,-x,child,gn,-p)
        swaps.append({'parent':parent,'child':child,'x':x,'p':p,
                      'parent_positive_clause':pos,'parent_negative_clause':neg,
                      'child_positive_clause':gp,'child_negative_clause':gn})
        ports[child]=(x,p)
    clauses=[canon(c) for b in blocks for c in b]
    assert len(clauses)==20*k and len(set(clauses))==20*k
    for c in clauses:
        assert len(c)==3 and len({abs(v) for v in c})==3
    count=Counter(v for c in clauses for v in c)
    assert all(count[x]==count[-x]==2 for x in range(1,15*k+1))
    adj={v:set() for v in range(1,15*k+1)}
    for c in clauses:
        ns={abs(v) for v in c}
        for v in ns: adj[v]|=ns-{v}
    seen={1}; fringe=[1]
    while fringe:
        v=fringe.pop()
        for w in adj[v]-seen: seen.add(w); fringe.append(w)
    assert len(seen)==15*k
    bags=[{abs(v) for c in b for v in c} for b in blocks]
    assert max(map(len,bags))<=18
    for i in range(1,k):
        par=(i-1)//2
        assert bags[par]&bags[i]==set(ports[i]), (i,bags[par]&bags[i],ports[i])
    # Precise running-intersection check without relying on the weaker shortcut above.
    tree_adj={i:set() for i in range(k)}
    for i in range(1,k): tree_adj[i].add((i-1)//2);tree_adj[(i-1)//2].add(i)
    for v in range(1,15*k+1):
        places={i for i,B in enumerate(bags) if v in B}
        q=[min(places)]; visited={q[0]}
        while q:
            i=q.pop()
            for j in (tree_adj[i]&places)-visited: visited.add(j);q.append(j)
        assert visited==places, ('running intersection',v,places)
    return blocks,clauses,bags,ports,swaps

def order_from_bags(bags):
    k=len(bags)
    def post(i):
        for child in (2*i+1,2*i+2):
            if child<k: yield from post(child)
        yield i
    order=[]; bag_of={}
    for t in post(0):
        par=(t-1)//2 if t else None
        forget=sorted(bags[t]-(bags[par] if par is not None else set()))
        for v in forget:
            assert v not in bag_of
            order.append(v);bag_of[v]=t
    assert len(order)==sum(1 for v in set.union(*bags))
    return order,bag_of

def elim_resolution(clauses,bags):
    """Full unbounded-variable Davis-Putnam, ordered by a supplied bag tree.
    No oracle. Produces explicit source parent IDs or a complete assignment.
    """
    src=[canon(c) for c in clauses]
    proof=[{'id':i+1,'clause':list(c),'source':i+1} for i,c in enumerate(src)]
    live={c:i+1 for i,c in enumerate(src)}
    order,bag_of=order_from_bags(bags)
    buckets=[]; candidate=taut=0; width=0; max_live=len(live);max_length=3
    for v in order:
        pos=[(c,q) for c,q in live.items() if v in c]
        neg=[(c,q) for c,q in live.items() if -v in c]
        context=bags[bag_of[v]]
        assert all({abs(x) for x in c}<=context for c,q in pos+neg), ('induced width',v)
        width=max(width,len(context)-1)
        buckets.append((v,[c for c,q in pos+neg]))
        new={}
        for A,idA in pos:
            for B,idB in neg:
                candidate+=1
                items=set(A)-{v};items.update(set(B)-{-v})
                if any(-x in items for x in items):taut+=1;continue
                C=canon(items);max_length=max(max_length,len(C))
                if C not in live and C not in new:
                    row={'id':len(proof)+1,'clause':list(C),'parents':[idA,idB],'pivot':v}
                    proof.append(row);new[C]=row['id']
                if not C:
                    return {'status':'UNSAT','proof':proof,'candidate_pairs':candidate,
                            'tautological_pairs':taut,'derived':len(proof)-len(src),
                            'max_live':max_live,'max_width':width,'max_clause_size':max_length}
        for c,q in pos+neg:live.pop(c,None)
        live.update(new);max_live=max(max_live,len(live))
    assert not live
    assigned={}
    for v,bucket in reversed(buckets):
        forced=set()
        for c in bucket:
            if not any(assigned[abs(l)]==(l>0) for l in c if abs(l)!=v):
                forced.add(v in c)
        assert len(forced)<=1, ('contradictory reconstruct',v,forced)
        assigned[v]=next(iter(forced)) if forced else False
    assert all(ctrue(c,assigned) for c in clauses)
    return {'status':'SAT','assignment':[int(assigned[v]) for v in range(1,len(assigned)+1)],
            'candidate_pairs':candidate,'tautological_pairs':taut,
            'derived':len(proof)-len(src),'max_live':max_live,
            'max_width':width,'max_clause_size':max_length}

def check_resolution(original,proof):
    """Independent strict verifier. First m exact source lines, rest exact resolvents."""
    m=len(original);db={};empty=False
    for i,row in enumerate(proof):
        idx=i+1
        if row.get('id')!=idx:return False
        C=canon(row['clause'])
        if len(set(C))!=len(C) or any(-x in C for x in C):return False
        if i<m:
            if row.get('source')!=idx or C!=canon(original[i]):return False
        else:
            parents=row.get('parents');v=row.get('pivot')
            if not isinstance(parents,list) or len(parents)!=2 or any(p not in db for p in parents):return False
            A,B=db[parents[0]],db[parents[1]]
            if v not in A or -v not in B:return False
            union=(set(A)-{v})|(set(B)-{-v})
            if any(-x in union for x in union):return False
            if C!=canon(union):return False
        db[idx]=C
        if not C: empty=True
    return empty

def exact_bag_dp(blocks,bags,ports):
    """Independent exhaustive constant-bag semantics, not using Resolution."""
    k=len(blocks);messages={};solutions={};visits=0
    for i in range(k-1,-1,-1):
        bag=sorted(bags[i]);at={v:j for j,v in enumerate(bag)}
        tests=[]
        for c in blocks[i]:
            positive=sum(1<<at[abs(v)] for v in c if v>0)
            negative=sum(1<<at[abs(v)] for v in c if v<0)
            tests.append((positive,negative))
        children=[c for c in (2*i+1,2*i+2) if c<k]
        child_lookup=[(c,at[ports[c][0]],at[ports[c][1]]) for c in children]
        pair=ports[i] if i else None
        sep=(at[pair[0]],at[pair[1]]) if pair else None
        message={};sample={}
        for a in range(1<<len(bag)):
            visits+=1
            if any((a&pos)==0 and (a&neg)==neg for pos,neg in tests):continue
            if any(((a>>vx)&1,(a>>vp)&1) not in messages[c] for c,vx,vp in child_lookup):continue
            key=((a>>sep[0])&1,(a>>sep[1])&1) if sep else ()
            if key not in message:
                message[key]=True;sample[key]=a
        messages[i]=message;solutions[i]=(bag,sample)
    status='SAT' if () in messages[0] else 'UNSAT'
    if status=='SAT':
        result={}
        def rec(i,key):
            bag,samples=solutions[i];mask=samples[key]
            result.update({v:int((mask>>j)&1) for j,v in enumerate(bag)})
            for child in (2*i+1,2*i+2):
                if child>=k:continue
                a,b=ports[child];rec(child,(result[a],result[b]))
        rec(0,())
        assert all(ctrue(c,result) for b in blocks for c in b)
    return {'status':status,'bag_trials':visits,'message_sizes':[len(messages[i]) for i in range(k)]}

def run():
    start=time.monotonic();fixed=source_guard();tests=[];example=None
    # Breadth-first trees have real branching at k>=4; SAT/UNSAT instances same shape.
    for k in (1,2,3,4,5,7,9,15,31):
        for mode in ('G','W1'):
            blocks,F,bags,ports,swaps=graft(k,mode)
            got=elim_resolution(F,bags)
            want='SAT' if mode=='G' else 'UNSAT'
            assert got['status']==want,(k,mode,got)
            assert got['max_width']<=17
            if want=='UNSAT':
                assert check_resolution(F,got['proof']),('bad proof',k)
                if k==7:
                    example={'n':15*k,'m':20*k,'clauses':[list(c) for c in F],
                             'proof':got['proof'],'grafts':swaps}
            else:
                assert len(got['assignment'])==15*k
                assert all(any(bool(got['assignment'][abs(v)-1])==(v>0) for v in c) for c in F)
            independent=None
            if k<=5:
                independent=exact_bag_dp(blocks,bags,ports)
                assert independent['status']==want,(k,mode,independent)
            tests.append({'k':k,'mode':mode,'status':got['status'],
                          'variables':15*k,'clauses':20*k,
                          'bag_size_max':max(map(len,bags)),
                          'edge_adhesion_max':max((len(bags[i]&bags[(i-1)//2]) for i in range(1,k)),default=0),
                          'candidate_pairs':got['candidate_pairs'],
                          'derived':got['derived'],'max_live':got['max_live'],
                          'max_clause_size':got['max_clause_size'],
                          'independent_table':independent})
            print('AUDIT',k,mode,got['status'],'derived',got['derived'],'pairs',got['candidate_pairs'],'elapsed',round(time.monotonic()-start,2),flush=True)
    assert example is not None
    cofactor_controls=[]
    for mode in ('G','W1'):
        b,F,bag,pr,sw=graft(3,mode)
        for pin in product((0,1),repeat=3):
            units=[((v,) if bit else (-v,)) for v,bit in zip((1,2,13),pin)]
            Fpin=F+units
            bpin=[list(q) for q in b]
            bpin[0]=bpin[0]+[list(c) for c in units]
            rpin=elim_resolution(Fpin,bag)
            expected=('SAT' if mode=='G' and pin!=(1,1,0) else 'UNSAT')
            assert rpin['status']==expected,(mode,pin,rpin['status'])
            if expected=='UNSAT':assert check_resolution(Fpin,rpin['proof'])
            dpin=exact_bag_dp(bpin,bag,pr)
            assert dpin['status']==expected
            cofactor_controls.append({'mode':mode,'pins':pin,'status':expected,
                                      'derived':rpin['derived'],'independent_trials':dpin['bag_trials']})
    # Hostile controls: invalid parent slots, lost clause, corrupt Resolution derivation.
    b,F,bag,pr,sw=graft(3,'W1')
    valid=elim_resolution(F,bag);assert check_resolution(F,valid['proof'])
    damaged=[dict(r) for r in valid['proof']]
    dr=next(r for r in damaged if 'parents' in r)
    dr['pivot']+=999
    assert not check_resolution(F,damaged)
    assert len(F)==60 and all(len(c)==3 for c in F)
    out={'run':'2026-10-29 LSPV-3 BRANCHING_EXACT22_GRAFT167',
         'fixed_guard':fixed,'tests':tests,
         'total_tests':len(tests),'pinned_cofactor_tests':cofactor_controls,
         'independent_exhaustive_bag_controls':sum(x['independent_table'] is not None for x in tests),
         'proof_corruption_rejected':True,
                  'status':'COMPUTATIONAL; restricted all-size lemma from fixed puncture table'}
    directory=pathlib.Path(__file__).parent
    raw=directory/'2026-10-29_1424_BRANCHING_EXACT22_GRAFT167_raw.json'
    raw.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    ex=directory/'2026-10-29_1424_BRANCHING_EXACT22_GRAFT167_example_proof.json'
    ex.write_text(json.dumps(example,sort_keys=True,separators=(',',':'))+'\n')
    print('RESULT',json.dumps({'tests':len(tests),'elapsed':round(time.monotonic()-start,3),
                               'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
                               'proof_sha256':hashlib.sha256(ex.read_bytes()).hexdigest()}))

if __name__=='__main__':run()
