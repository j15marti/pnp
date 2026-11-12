#!/usr/bin/env python3
"""LSPV-1/592. Independent declared-grammar extended-Resolution/native compilation audit.
NOT a replay of R_mix341 or a historical accepted-byte checker.
Python >=3.9, standard library only. Output deterministic JSON summary.
"""
import json, copy, hashlib, itertools, sys

def canon(clause):
    if any(type(x) is not int or x == 0 for x in clause):
        raise ValueError('bad literal')
    ans=tuple(sorted(set(clause),key=lambda x:(abs(x),x)))
    if any(-x in ans for x in ans):
        raise ValueError('tautological')
    return ans

def facets(z,a,b):
    return tuple(canon(c) for c in ((-z,a),(-z,b),(z,-a,-b)))

def eval_c(clause,assignment):
    return any((assignment[abs(lit)] if lit>0 else not assignment[abs(lit)]) for lit in clause)

def verified_packet(F,packet):
    """A separate *declared* source-bound, paid-owner, no-assumptions calculus."""
    F=[canon(c) for c in F]
    seen=[]; defs={}; owners=set(); made=set(); ns=nr=nfac=0
    orig_vars={abs(l) for C in F for l in C}
    for (id,z,a,b) in packet['definitions']:
        if any(type(t) is not int for t in (id,z,a,b)) or id in owners or z in made or z in orig_vars or z<=0 or a==0 or b==0 or abs(a)==z or abs(b)==z or any(abs(t) not in orig_vars|made for t in (a,b)):
            raise ValueError('invalid or nonfresh owner')
        defs[id]=(z,a,b);made.add(z);owners.add(id)
    source_idx=[]
    for r in packet['records']:
        c=canon(r['clause']); kind=r['kind']
        if kind=='SOURCE':
            if r.get('parents',[]) or r['source']>=len(F) or r['source']<0 or c!=F[r['source']]:
                raise ValueError('source mismatch')
            source_idx.append(r['source']);ns+=1
        elif kind=='FACET':
            if r.get('parents',[]) or r['owner'] not in defs or c not in facets(*defs[r['owner']]):
                raise ValueError('forged facet')
            nfac+=1
        elif kind=='RES':
            p=r['pivot']; par=r['parents'];
            if type(p) is not int or len(par)!=2 or any(type(j) is not int or j<0 or j>=len(seen) for j in par):
                raise ValueError('invalid parents')
            A,B=(seen[j] for j in par)
            if p not in A or -p not in B:
                raise ValueError('pivot sign')
            derived=canon([l for l in A if l!=p]+[l for l in B if l!=-p]);
            if derived!=c: raise ValueError('resolution mismatch')
            nr+=1
        else:
            raise ValueError('unrecognized rule')
        if any(abs(x) not in orig_vars|made for x in c):
            raise ValueError('unknown literal')
        seen.append(c)
    if sorted(source_idx)!=list(range(len(F))): raise ValueError('missing source')
    if not seen or seen[-1]!=(): raise ValueError('missing sink')
    if packet['paid'] != nr+len(defs): raise ValueError('paid mismatch')
    return {'paid':nr+len(defs),'source':ns,'facets':nfac,'resolution':nr,'definitions':len(defs)}

def add(R,kind,clause,**kwargs):
    R.append({'kind':kind,'clause':list(canon(clause)),**kwargs})
    return len(R)-1

def generate():
    F=[[1],[2],[-1,-2]]
    R=[]
    s0=add(R,'SOURCE',F[0],source=0,parents=[])
    s1=add(R,'SOURCE',F[1],source=1,parents=[])
    s2=add(R,'SOURCE',F[2],source=2,parents=[])
    z,a,b=3,1,2
    f1=add(R,'FACET',[-3,1],owner=0,parents=[])
    f2=add(R,'FACET',[-3,2],owner=0,parents=[])
    f3=add(R,'FACET',[3,-1,-2],owner=0,parents=[])
    r1=add(R,'RES',[-2,3],parents=[s0,f3],pivot=1)
    r2=add(R,'RES',[3],parents=[s1,r1],pivot=2)
    r3=add(R,'RES',[-3,-2],parents=[f1,s2],pivot=1)
    r4=add(R,'RES',[-3],parents=[s1,r3],pivot=2)
    r5=add(R,'RES',[],parents=[r2,r4],pivot=3)
    return F,{'definitions':[[0,z,a,b]],'records':R,'paid':5+1}

def main():
    F,p=generate()
    verified=verified_packet(F,p)
    checks=0
    for xx,yy,zz in itertools.product((False,True),repeat=3):
        d={1:xx,2:yy,3:zz}
        for c in facets(3,1,2):
            if zz==(xx and yy): assert eval_c(c,d)
            checks+=1
        assert all(eval_c(c,d) for c in facets(3,1,2))==(zz==(xx and yy));checks+=1
    assert not any(all(eval_c(c,{1:x,2:y}) for c in F) for x,y in itertools.product((False,True),repeat=2));checks+=4
    tests=[]
    def trial(name,mut,external=None):
        q=copy.deepcopy(p);mut(q)
        try:
            verified_packet(F if external is None else external,q)
            outcome='ACCEPT'
        except (ValueError,KeyError,TypeError,IndexError): outcome='REJECT'
        tests.append({'name':name,'outcome':outcome})
        if outcome!='REJECT':raise AssertionError('hostile accepted '+name)
    trial('forged-source',lambda q:q['records'][0].update(clause=[-1]))
    trial('external-root-switch',lambda q:None,[[1],[2],[1,-2]])
    trial('missing-owner',lambda q:q['definitions'].clear())
    trial('free-owner-charge',lambda q:q.update(paid=5))
    trial('wrong-AND-facet',lambda q:q['records'][3].update(clause=[-3,-1]))
    trial('wrong-pivot',lambda q:q['records'][-1].update(pivot=999999))
    trial('bad-parent',lambda q:q['records'][-1].update(parents=[11,9]))
    trial('missing-source',lambda q:q['records'].pop(2))
    trial('forged-rule',lambda q:q['records'][6].update(kind='LOCAL-CONVERT'))
    trial('nonfresh-definition',lambda q:q['definitions'][0].__setitem__(1,1))
    trial('unsupported-gate-parent',lambda q:q['definitions'][0].__setitem__(2,99))
    trial('wrong-terminal',lambda q:q['records'][-1].update(clause=[3]))
    out={'experiment':'LSPV1-592-ER-SIMULATION-FIREWALL','status':'PROVED/CONDITIONAL theorem; COMPUTATIONAL illustrative finite controls',
         'model':'declared unrestricted signed CNF SOURCE, arbitrary fresh binary AND2 definitions, all 3 free facets, exact strict RES, one paid owner and one paid RES record; NOT native R_mix341',
         'F':F,'F_UNSAT_exhaustive':True,'packet':p,'verified':verified,'facet_assignment_checks':checks,
         'negative_controls':tests,'all_pass':True,'historical_native_acceptance':'NOT CLAIMED'}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
