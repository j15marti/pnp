#!/usr/bin/env python3
"""ARC218: source-authenticated five-step resolution lift for guarded mixed 2CNF-XOR3.

Independent deterministic proof verifier, signed-clause controls and archive replay evidence.
No SAT, UNSAT, proof, or summary oracle is used to construct the local derivations.
A full UNSAT refutation requires a SOURCE resolution proof, supplied separately.
"""
import itertools
import json
import random
import hashlib
from pathlib import Path

SEED = 21820261029
ROOT = Path(__file__).parent


def canon(xs):
    s=set(xs)
    if 0 in s or any(-v in s for v in s):
        raise ValueError('zero or tautological clause')
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))


def parity3_even(a,b,c):
    return [canon((a if i==0 else -a,b if j==0 else -b,c if k==0 else -c))
            for i,j,k in itertools.product((0,1),repeat=3) if (i^j^k)==1]


def resolvent(c,d,p):
    assert p in c and -p in d,('not a valid oriented pivot',p,c,d)
    return canon(tuple(x for x in c if x!=p)+tuple(x for x in d if x!=-p))


class Trace:
    def __init__(self):
        self.rows=[]
    def axiom(self, c, owner):
        c=canon(c)
        self.rows.append({'kind':'axiom','clause':list(c),'owner':owner})
        return len(self.rows)-1
    def res(self, a, b, p, label=''):
        c=resolvent(tuple(self.rows[a]['clause']),tuple(self.rows[b]['clause']),p)
        self.rows.append({'kind':'resolution','clause':list(c),'a':a,'b':b,'pivot':p,'label':label})
        return len(self.rows)-1


def compile_guarded_pinned(source,n):
    """Construct CNF for ARC217 H_F plus -g, retaining each original source clause ID."""
    tr=Trace()
    g=n+1
    guard=tr.axiom((-g,),{'source':'pin-g-zero'})
    children=[]
    for ci,cl in enumerate(source):
        assert len(cl)==3 and len({abs(v) for v in cl})==3
        y1,y2,y3,t=(n+2+4*ci+i for i in range(4))
        bins=[tr.axiom((ell,y),{'source':ci,'kind':'binary','position':i})
              for i,(ell,y) in enumerate(zip(cl,(y1,y2,y3)))]
        one=[tr.axiom(c,{'source':ci,'kind':'xor-a','row':i}) for i,c in enumerate(parity3_even(y1,y2,t))]
        two=[tr.axiom(c,{'source':ci,'kind':'xor-b','row':i}) for i,c in enumerate(parity3_even(t,y3,g))]
        children.append({'ci':ci,'lits':list(cl),'binary':bins,'xor_a':one,'xor_b':two,'ys':[y1,y2,y3],'t':t})
    return tr,g,guard,children


def locate(tr,ids,needle):
    x=canon(needle)
    hits=[i for i in ids if tuple(tr.rows[i]['clause'])==x]
    assert len(hits)==1,(x,hits)
    return hits[0]


def lift_local(tr,g,guard,ch):
    """Five resolution inferences yielding EXACTLY the original 3-clause, no solver call."""
    l1,l2,l3=ch['lits']
    y1,y2,y3=ch['ys']; t=ch['t']
    # y3 -> t when g=0, from the second parity row and literal pin.
    z=tr.res(locate(tr,ch['xor_b'],(-y3,t,g)),guard,g,label=f'C{ch["ci"]}:5a')
    # If y1=y2=1 and t=1, parity row y1 xor y2 xor t=0 is violated.
    z=tr.res(z,locate(tr,ch['xor_a'],(-y1,-y2,-t)),t,label=f'C{ch["ci"]}:5b')
    # Sequentially substitute the three binary clauses; no existential guessing.
    z=tr.res(ch['binary'][2],z,y3,label=f'C{ch["ci"]}:5c')
    z=tr.res(ch['binary'][1],z,y2,label=f'C{ch["ci"]}:5d')
    z=tr.res(ch['binary'][0],z,y1,label=f'C{ch["ci"]}:5e')
    assert tuple(tr.rows[z]['clause'])==canon(ch['lits'])
    return z


def check_trace(source,n,tr,require_empty=False):
    """Independently checks each axiom's SOURCE and both actual parent clauses.
    Does not trust labels or use original builder's intermediate computation.
    """
    if not tr.rows:return False
    g=n+1
    key=lambda c,owner:(canon(c),json.dumps(owner,sort_keys=True))
    valid={key((-g,),{'source':'pin-g-zero'})}
    for ci,cl in enumerate(source):
        ys=[n+2+4*ci+j for j in range(3)];t=n+5+4*ci
        for pos,(ell,y) in enumerate(zip(cl,ys)):
            valid.add(key((ell,y),{'source':ci,'kind':'binary','position':pos}))
        for row,c in enumerate(parity3_even(ys[0],ys[1],t)):
            valid.add(key(c,{'source':ci,'kind':'xor-a','row':row}))
        for row,c in enumerate(parity3_even(t,ys[2],g)):
            valid.add(key(c,{'source':ci,'kind':'xor-b','row':row}))
    checked=[]
    for row in tr.rows:
        c=canon(row['clause'])
        if tuple(row['clause'])!=c:return False
        if row['kind']=='axiom':
            if key(c,row.get('owner')) not in valid:return False
        elif row['kind']=='resolution':
            a,b,p=row['a'],row['b'],row['pivot']
            if not (isinstance(a,int) and isinstance(b,int) and a<len(checked) and b<len(checked)):return False
            if p not in checked[a] or -p not in checked[b]:return False
            if c!=resolvent(checked[a],checked[b],p):return False
        else:return False
        checked.append(c)
    return not require_empty or checked[-1]==()


def all_eight_3sat():
    return [tuple((i+1) if (k>>i)&1 else -(i+1) for i in range(3)) for k in range(8)]


def append_all_eight_resolution(tr,source_line):
    """Exact seven-step source proof on all eight proper 3-clauses."""
    pairs2={}
    for a,b in itertools.product((-1,1),repeat=2):
        cpos=(a,2*b,3);cneg=(a,2*b,-3)
        pairs2[(a,b)]=tr.res(source_line[canon(cpos)],source_line[canon(cneg)],3,label='source-x3')
    pairs1={}
    for a in (-1,1):
        pairs1[a]=tr.res(pairs2[(a,1)],pairs2[(a,-1)],2,label='source-x2')
    return tr.res(pairs1[1],pairs1[-1],1,label='source-x1')


def source_sat(source,n):
    return any(all(any(((assignment>>(abs(l)-1))&1)==(l>0) for l in c) for c in source)
               for assignment in range(1<<n))


def guarded_clause_exists(lits,g):
    for a,b,c,t in itertools.product((0,1),repeat=4):
        if all(u or y for u,y in zip(lits,(a,b,c))) and (a^b^t)==0 and (t^c^g)==0:
            return True
    return False


def run():
    stats={'local_proof_steps':0,'local_axioms':0,'local_proof_source_cases':0,'source_subsets':0,
           'pointwise_guard_rows':0,'source_assignments':0,'full_refutation_steps':0,
           'full_refutation_axioms':0,'full_refutation_checked':0,'negative_controls':0,
           'random_sources':0,'random_sat':0,'random_unsat':0,'random_guard_checks':0}
    all8=all_eight_3sat()
    # Local pointwise truth proof, including two distinct negative controls.
    for bits in itertools.product((0,1),repeat=3):
        for g in (0,1):
            assert guarded_clause_exists(bits,g)==(bool(g) or any(bits))
            stats['pointwise_guard_rows']+=1
    assert guarded_clause_exists((0,0,0),1)
    assert not guarded_clause_exists((0,0,0),0)
    stats['negative_controls']+=2
    # Every subset: the guard family is ALWAYS satisfiable, but pinned g=0 agrees with source SAT.
    for mask in range(1<<8):
        src=[all8[i] for i in range(8) if (mask>>i)&1]
        tr,g,pin,ch=compile_guarded_pinned(src,3)
        stats['local_axioms']+=len(tr.rows)
        lifted=[lift_local(tr,g,pin,c) for c in ch]
        assert check_trace(src,3,tr)
        stats['local_proof_steps']+=5*len(src)
        stats['local_proof_source_cases']+=len(src)
        for ass in itertools.product((0,1),repeat=3):
            x=[int(v) for v in ass]
            form_ok=all(any((x[abs(l)-1] if l>0 else 1-x[abs(l)-1]) for l in c) for c in src)
            ext_ok=all(guarded_clause_exists(tuple(x[abs(l)-1] if l>0 else 1-x[abs(l)-1] for l in c),0) for c in src)
            assert form_ok==ext_ok
            stats['source_assignments']+=1
        assert source_sat(src,3)==(mask!=255)
        stats['source_subsets']+=1
    # Actual full 8-clause refutation. 11m+1 axioms, 5m+7 resolution steps.
    tr,g,pin,ch=compile_guarded_pinned(all8,3)
    source_line={canon(c['lits']):lift_local(tr,g,pin,c) for c in ch}
    last=append_all_eight_resolution(tr,source_line)
    assert tr.rows[last]['clause']==[]
    assert check_trace(all8,3,tr,require_empty=True)
    stats['full_refutation_axioms']=sum(r['kind']=='axiom' for r in tr.rows)
    stats['full_refutation_steps']=sum(r['kind']=='resolution' for r in tr.rows)
    stats['full_refutation_checked']=1
    assert stats['full_refutation_axioms']==89
    assert stats['full_refutation_steps']==47
    # Falsifiers: mutation of ANY derived pivot or an input axiom must be rejected.
    old=tr.rows[-1]['pivot'];tr.rows[-1]['pivot']=2
    assert not check_trace(all8,3,tr,require_empty=True)
    tr.rows[-1]['pivot']=old
    old=tr.rows[1]['clause'];tr.rows[1]['clause']=[999999]
    assert not check_trace(all8,3,tr,require_empty=True)
    tr.rows[1]['clause']=old
    assert check_trace(all8,3,tr,require_empty=True)
    old=tr.rows[1]['owner'];tr.rows[1]['owner']={'source':999,'kind':'binary','position':0}
    assert not check_trace(all8,3,tr,require_empty=True)
    tr.rows[1]['owner']=old
    assert check_trace(all8,3,tr,require_empty=True)
    stats['negative_controls']+=4
    # Random original SAT/UNSAT controls. No SAT oracle, exhaust small source only for tests.
    rng=random.Random(SEED)
    for j in range(160):
        n=4+j%2;m=6+j%19
        src=[]
        for _ in range(m):
            names=rng.sample(range(1,n+1),3)
            src.append(tuple(name if rng.randrange(2) else -name for name in names))
        actual=source_sat(src,n)
        tr2,g2,pin2,ch2=compile_guarded_pinned(src,n)
        for c in ch2:lift_local(tr2,g2,pin2,c)
        assert check_trace(src,n,tr2)
        projected=any(all(guarded_clause_exists(tuple(int((ass>>(abs(l)-1))&1)==int(l>0) for l in c),0) for c in src)
                      for ass in range(1<<n))
        assert actual==projected
        stats['random_guard_checks']+=1
        stats['random_sources']+=1
        stats['random_sat' if actual else 'random_unsat']+=1
    # Archive replay should be independently performed as a separate file step.
    data={'status':'PASS','classification':{'five_step_lift':'PROVED/RESTRICTED',
        'Cook_Reckhow_barrier':'PROVED/CONDITIONAL_CLASSICAL',
        'all_input_affordable_certificates':'OPEN','P_versus_NP':'OPEN'},
          'seed':SEED,'counts':stats,
          'example':{'source_vars':3,'source_clauses':8,
                     'pinned_mixed_cnf_axioms':stats['full_refutation_axioms'],
                     'local_resolution_steps':40,'source_resolution_steps':7,
                     'complete_steps':47,
                     'encoding':{'all_source_ids_retained':True,'full_rows':len(tr.rows),
                                  'max_clause_width':max(len(row['clause']) for row in tr.rows)}},
          'limitations':['Constructs short local clause derivations, not global UNSAT proofs for arbitrary F.',
                         'A resolution refutation of arbitrary F is required as additional input.',
                         'No kernel-verified proof, only explicit source-aware Python checker.',
                         'No unrestricted SAT compression or native TM lower bound.']}
    (ROOT/'ARC218_guarded_certificate_raw.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    (ROOT/'ARC218_eight_clause_refutation.json').write_text(json.dumps({'source':all8,'n':3,'rows':tr.rows},sort_keys=True,indent=2)+'\n')
    print(json.dumps(data,sort_keys=True,indent=2))

if __name__=='__main__':run()