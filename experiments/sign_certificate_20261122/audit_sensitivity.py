#!/usr/bin/env python3
"""Exact finite controls for literal-sign sensitivity of strict 3-CNF UNSAT sources.
All formulas contain ordered three-literal clauses with three distinct variable IDs.
"""
import itertools, json, hashlib
from pathlib import Path

def sat(a, cs):
    for pos, neg in cs:
        if not ((a & pos) or ((~a) & neg)):
            return False
    return True

def masks(F):
    return [(sum(1 << (abs(l)-1) for l in cl if l > 0),
             sum(1 << (abs(l)-1) for l in cl if l < 0)) for cl in F]

def find_model(F, n, pins=None):
    fixed=pins or {}
    cm=masks(F)
    for a in range(1<<n):
        if any(bool((a>>(v-1))&1)!=bool(b) for v,b in fixed.items()):
            continue
        if sat(a,cm): return a
    return None

def flip(F,j,h):
    G=list(F); c=list(G[j]); c[h]=-c[h]; G[j]=tuple(c);return G

def strict(F):
    return all(len(c)==3 and len({abs(z) for z in c})==3 for c in F)

def chain(k):
    # k core vars, k-1 split implications, two independent four-row units
    F=[]
    a,b=k+1,k+2
    for sa,sb in itertools.product((1,-1),repeat=2):
        F.append((1,sa*a,sb*b))
    for i in range(1,k):
        z=k+2+i
        F.extend([(-i,i+1,z),(-i,i+1,-z)])
    c,d=2*k+2,2*k+3
    for sc,sd in itertools.product((1,-1),repeat=2):
        F.append((-k,sc*c,sd*d))
    return F, 2*k+3

def guard(H,n):
    p,x,a,b=range(n+1,n+5)
    F=[(p,x,a),(p,x,-a),(p,-x,b),(p,-x,-b)]
    for j,(l1,l2,l3) in enumerate(H):
        s=n+5+j
        F.extend([(-p,l1,s),(-s,l2,l3)])
    return F,n+len(H)+4, {'p':p,'x':x,'a':a,'b':b}

def sensitive_indices(F,n,pins):
    base=find_model(F,n,pins)
    assert base is None
    sensitive=[]
    for j in range(len(F)):
        for h in range(3):
            G=flip(F,j,h)
            a=find_model(G,n,pins)
            if a is not None:
                assert sat(a,masks(G))
                sensitive.append((j,h))
    return sensitive

def check_mu(F,n):
    assert find_model(F,n) is None
    witnesses=[]
    for j in range(len(F)):
        a=find_model(F[:j]+F[j+1:],n)
        assert a is not None
        assert not sat(a,masks([F[j]]))
        for h in range(3):
            assert sat(a,masks(flip(F,j,h)))
        witnesses.append(a)
    return witnesses

def certify_exhaustively(F,n,pins):
    """Enumerate all subsets of sign bits; test core-equivalence and construct SAT competitors."""
    total=3*len(F)
    assert total<=12
    min_c=None
    certs=0
    for Q in range(1<<total):
        K=[F[j] for j in range(len(F)) if all(Q&(1<<(3*j+h)) for h in range(3))]
        witness=find_model(K,n,pins)
        if witness is None:
            certs+=1
            count=Q.bit_count()
            if min_c is None or count<min_c:min_c=count
            continue
        # Preserve read signs, allow independent changes only at unread sign positions.
        G=[list(c) for c in F]
        for j,c in enumerate(F):
            if sat(witness,masks([c])):continue
            unread=[h for h in range(3) if not Q&(1<<(3*j+h))]
            assert unread,(Q,j)
            h=unread[0]
            G[j][h]=-G[j][h]
        assert sat(witness,masks(G))
        for j in range(len(F)):
            for h in range(3):
                if Q&(1<<(3*j+h)):
                    assert G[j][h]==F[j][h]
    return {'signs':total,'minimum_certificate_signs':min_c,'certificates':certs,
            'input_bit_masks_checked':1<<total}

def main():
    rows=[]
    for k in range(2,8):
        F,n=chain(k)
        assert strict(F) and n==2*k+3 and len(F)==2*k+6
        witnesses=check_mu(F,n)
        rows.append({'family':'implication_chain','k':k,'n':n,'m':len(F),
                     'sensitive_sign_bits':3*len(F), 'deletion_witness_count':len(witnesses)})
    H=[tuple(v*sgn for v,sgn in zip((1,2,3),signs))
       for signs in itertools.product((-1,1),repeat=3)]
    F,n,named=guard(H,3)
    assert n==15 and len(F)==20 and strict(F)
    check_mu(F,n)
    order=[named['a']]+[v for v in range(1,n+1) if v not in {named['a'],named['p'],named['x']}]+[named['x'],named['p']]
    assert len(order)==n and len(set(order))==n
    levels=[]
    for r in [0,1,6,13,14,15]:
        pins={v:0 for v in range(1,n+1) if v not in order[:r]}
        sens=sensitive_indices(F,n,pins)
        expected=3 if r==0 else 6 if 1<=r<=13 else 12 if r==14 else 60
        assert len(sens)==expected,(r,len(sens),expected)
        assert all(j<2 for j,h in sens) if 1<=r<=13 else True
        assert all(j<4 for j,h in sens) if r==14 else True
        levels.append({'unknowns':r,'remaining_pins':pins,'literal_sign_sensitivity':len(sens),
                       'sensitive_positions':sens})
    certificate_cases=[]
    for label, G, pins in [
        ('one_violated_guard',F[:1],{v:0 for v in range(1,n+1)}),
        ('two_guard_plateau',F[:2],{named['p']:0,named['x']:0}),
        ('duplicated_plateau',[F[0],F[0],F[1],F[1]],{named['p']:0,named['x']:0}),
        ('four_guard_penultimate',F[:4],{named['p']:0})]:
        assert find_model(G,n,pins) is None
        cert=certify_exhaustively(G,n,pins)
        if label=='duplicated_plateau':
            assert len(sensitive_indices(G,n,pins))==0
            assert cert['minimum_certificate_signs']==6
        elif label=='one_violated_guard':assert cert['minimum_certificate_signs']==3
        elif label=='two_guard_plateau':assert cert['minimum_certificate_signs']==6
        else:assert cert['minimum_certificate_signs']==12
        certificate_cases.append({'case':label,**cert})
    out={'status':'PASS','chain_cases':rows,'final_pin':{
        'n':n,'m':len(F),'levels':levels,'all_original_clauses_critical':True,
        'all_original_sign_bits_sensitive':True,
        'complete_all_32768_unsat_checked':find_model(F,n) is None},
        'certificate_cases':certificate_cases,
        'disclosure':'Exact finite control. All-size proofs are separate symbolic lemmas.'}
    path=Path(__file__).with_name('audit_sensitivity_results.json')
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','chains':len(rows),'samples':[(x['unknowns'],x['literal_sign_sensitivity']) for x in levels],
      'certificates':[(x['case'],x['minimum_certificate_signs']) for x in certificate_cases],'results':str(path)}))
if __name__=='__main__': main()
