#!/usr/bin/env python3
"""LSPV-2/526: original-variable RAT^- vs RUP, source-bound test controls.
No dependencies. This is a local experimental calculus, NOT R_mix341.
"""
from __future__ import annotations
import hashlib, json, itertools

class CheckError(ValueError): pass

def formula(k):
    assert k >= 1
    clauses=[]
    for i in range(k):
        b,c=2*i+2, 2*i+3
        clauses.extend([(1,b,c),(-1,b,c)])
    return tuple(clauses),2*k+1

def serialize(clauses, v):
    return (f'p cnf {v} {len(clauses)}\n' + ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()

def parse(data):
    try:
        if not isinstance(data,bytes): raise CheckError('bytes required')
        lines=data.decode('ascii').splitlines()
        if not lines: raise CheckError('empty')
        top=lines[0].split()
        if len(top)!=4 or top[:2]!=['p','cnf']: raise CheckError('bad header')
        v,m=map(int,top[2:])
        if v<=0 or m<0 or len(lines)!=m+1: raise CheckError('bad dimensions')
        clauses=[]
        for s in lines[1:]:
            nums=tuple(map(int,s.split()))
            if len(nums)!=4 or nums[-1]!=0 or 0 in nums[:3]:raise CheckError('not proper 3cnf')
            c=nums[:3]
            if len({abs(a) for a in c})!=3 or any(abs(x)>v for x in c):raise CheckError('invalid literal')
            clauses.append(c)
        return tuple(clauses),v
    except (UnicodeError, ValueError) as e: raise CheckError(str(e)) from e

def up(clauses, assumptions, stat=None):
    if stat is None: stat={'scans':0,'literals':0,'units':0}
    assign={}
    for a in assumptions:
        if abs(a) in assign and assign[abs(a)]!=(a>0):return True,stat
        assign[abs(a)]=a>0
    while True:
        changed=False
        for clause in clauses:
            stat['scans']+=1
            alive=[]; satisfied=False
            for lit in clause:
                stat['literals']+=1
                x=assign.get(abs(lit))
                if x is None: alive.append(lit)
                elif x==(lit>0):satisfied=True;break
            if satisfied:continue
            if not alive: return True,stat
            if len(alive)==1:
                u=alive[0]; x=assign.get(abs(u))
                if x is None:
                    assign[abs(u)]=u>0
                    stat['units']+=1;changed=True
                elif x!=(u>0): return True,stat
        if not changed:return False,stat

def rup(clauses,C,stat=None):
    return up(clauses,[-x for x in C],stat)[0]

def rat(clauses,C,pivot,stat=None):
    if pivot not in C: return False,0,stat
    checks=0
    for D in clauses:
        if -pivot not in D: continue
        checks+=1
        res=tuple(dict.fromkeys(x for x in C if x!=pivot))+tuple(x for x in D if x!=-pivot)
        if any(-x in res for x in res):continue
        if not rup(clauses,res,stat): return False,checks,stat
    return True,checks,stat

def sat(clauses, a):
    return all(any(a[abs(l)] == (l>0) for l in C) for C in clauses)

def replay(clauses,v,src_sha,cert):
    if hashlib.sha256(serialize(clauses,v)).hexdigest()!=src_sha: return False
    for rec in cert:
        kind=rec.get('rule'); C=tuple(rec['clause'])
        if not C or any(x==0 or abs(x)>v for x in C):return False
        if kind=='RUP': valid=rup(clauses,C)
        elif kind=='RAT':valid=rat(clauses,C,rec.get('pivot'))[0]
        else: return False
        if not valid:return False
        clauses=clauses+(C,)
    return True

def rpar(n, perm):
    """Two opposed standard XOR-3 chains with disjoint auxiliaries, n>=4."""
    assert n>=4 and sorted(perm)==list(range(1,n+1))
    A=list(range(1,n+1)); B=list(perm)
    F=[]
    for q, order in enumerate((A,B)):
        t=[n + q*(n-3)+i for i in range(1,n-2)]
        triples=[(order[0],order[1],t[0])]
        triples.extend((t[i],order[i+2],t[i+1]) for i in range(n-4))
        triples.append((t[-1],order[-2],order[-1]))
        for idx, triple in enumerate(triples):
            charge=int(q==1 and idx==len(triples)-1)
            for bits in itertools.product((False,True), repeat=3):
                if (sum(bits)&1)!=charge:
                    F.append(tuple(-lit if bit else lit for lit,bit in zip(triple,bits)))
    return tuple(F),3*n-6

def main():
    runs=[]; assertions=0; fingerprints=[]; tot={'scans':0,'literals':0,'units':0}
    for k in range(1,25):
        F,v=formula(k)
        data=serialize(F,v); G,w=parse(data)
        assert G==F and w==v;assertions+=2
        digest=hashlib.sha256(data).hexdigest();fingerprints.append(digest)
        stat={'scans':0,'literals':0,'units':0}
        israt,nchecks,_=rat(F,(1,),1,stat)
        assert israt and nchecks==k;assertions+=2
        assert not rup(F,(1,));assertions+=1
        assert replay(F,v,digest,[{'rule':'RAT','clause':[1],'pivot':1}]);assertions+=1
        assert not replay(F,v,digest,[{'rule':'RUP','clause':[1]}]);assertions+=1
        assert not replay(F,v,'0'*64,[{'rule':'RAT','clause':[1],'pivot':1}]);assertions+=1
        assert not replay(F,v,digest,[{'rule':'RAT','clause':[1],'pivot':-1}]);assertions+=1
        m0={i:True for i in range(1,v+1)}; m1=m0|{1:False}
        assert sat(F,m0) and sat(F,m1) and sat(F+((1,),),m0) and not sat(F+((1,),),m1);assertions+=4
        bad=tuple(C for idx,C in enumerate(F) if idx!=0)
        assert not rat(bad,(1,),1)[0];assertions+=1
        assert not replay(F,v,digest,[{'rule':'RAT','clause':[1],'pivot':1}, {'rule':'RAT','clause':[-1],'pivot':-1}]);assertions+=1
        if k<=5:
            count=0
            for bits in itertools.product((False,True),repeat=v):
                assn={i+1:bits[i] for i in range(v)}
                if sat(F,assn):count+=1
            assert count==2*3**k;assertions+=1
        for key in tot:tot[key]+=stat[key]
        runs.append({'k':k,'variables':v,'original_clauses':len(F),'sha256':digest,'rat_pivot':1,'rat_resolvent_checks':nchecks,'rup_a':False,'rat_a':True,'models_before':f'2*3^{k}','checker_operations':stat})
    bad_frames=[b'',b'p cnf 1 1\n1 2 3 0\n',b'p cnf 3 1\n1 1 2 0\n',b'p cnf 3 1\n1 2 3\n',b'p cnf 3 1\n1 2 3 0\n1 2 3 0\n',b'p cnf X 1\n1 2 3 0\n',b'p cnf 3 1\n1 2 3 0\n\xff']
    for data in bad_frames:
        try:parse(data)
        except CheckError: assertions+=1
        else: raise AssertionError('malformed accepted')
    rpar_controls=[]
    for n in (4,5,6):
        perms=[tuple(range(1,n+1)),tuple(reversed(range(1,n+1))),tuple(range(2,n+1))+ (1,)]
        for perm in perms:
            F,v=rpar(n,perm);data=serialize(F,v)
            assert parse(data)==(F,v);assertions+=1
            assert len(F)==8*(n-2) and v==3*n-6;assertions+=2
            assert all(not sat(F,{i+1:bits[i] for i in range(v)}) for bits in itertools.product((False,True),repeat=v));assertions+=1
            rpar_controls.append({'n':n,'permutation':list(perm),'variables':v,'clauses':len(F),'sha256':hashlib.sha256(data).hexdigest(),'classification':'UNSAT'})
    output={'experiment':'LSPV2_526_RAT_MINUS_VS_RUP','scope':'Original signed strict 3CNF; RAT one-record non-RUP satisfiability-preserving, model-changing addition','parameters':'k=1..24 exhaustive enumeration k<=5','assertions':assertions,'malformed_rejections':len(bad_frames),'runs':runs,'rpar_controls':rpar_controls,'total_checker_ops':tot,'not_a_Rmix341_certificate':True}
    print(json.dumps(output,sort_keys=True,indent=2))

if __name__=='__main__': main()
