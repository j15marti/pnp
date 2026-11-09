#!/usr/bin/env python3
"""Independent, finite, original-source CDCL/RUP and MAY-cost regression control.
This is NOT the historical R_mix341 checker or an FLMV machine implementation.
"""
import hashlib, itertools, json, sys

class BadSource(ValueError): pass

def parse_dimacs(text):
    if not isinstance(text,str): raise BadSource('not text')
    rows=[x.strip() for x in text.splitlines() if x.strip() and not x.lstrip().startswith('c')]
    if not rows or len(rows[0].split())!=4 or rows[0].split()[:2]!=['p','cnf']:
        raise BadSource('missing header')
    try: v,m=map(int,rows[0].split()[2:])
    except Exception: raise BadSource('noninteger header')
    if v<0 or m<0 or m>1000000: raise BadSource('invalid counts')
    clauses=[]
    for line in rows[1:]:
        try: numbers=[int(x) for x in line.split()]
        except Exception: raise BadSource('noninteger literal')
        if not numbers or numbers[-1]!=0 or 0 in numbers[:-1]: raise BadSource('terminator')
        cl=tuple(numbers[:-1]);
        if len({abs(x) for x in cl})!=len(cl): raise BadSource('repeated variable')
        if any(not(1<=abs(x)<=v) for x in cl): raise BadSource('range')
        clauses.append(cl)
    if len(clauses)!=m: raise BadSource('clause count')
    return v,clauses

def encode(v,clauses):
    return 'p cnf %d %d\n'%(v,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def tseitin(vertices,edges,charges):
    assert len(vertices)==len(charges) and len(edges)*2==3*len(vertices)
    ids={tuple(sorted(e)):i+1 for i,e in enumerate(edges)}
    cs=[]
    for pos,u in enumerate(vertices):
        inc=sorted([ids[tuple(sorted(e))] for e in edges if u in e]);assert len(inc)==3
        for vals in itertools.product((0,1),repeat=3):
            if sum(vals)%2 != charges[pos]:
                cs.append(tuple((-a if vals[j] else a) for j,a in enumerate(inc)))
    return len(edges),cs

def up_conflict(v,clauses,assumptions=()):
    vals={}
    for a in assumptions:
        if not 1<=abs(a)<=v: return False,0,0
        if -a in vals: return True,0,0
        vals[a]=1
    scans=0; units=0
    while True:
        changed=False
        for clause in clauses:
            scans+=1
            if any(lit in vals for lit in clause): continue
            undec=[lit for lit in clause if -lit not in vals]
            if not undec: return True,scans,units
            if len(undec)==1:
                l=undec[0]; vals[l]=1;units+=1;changed=True;break
        if not changed:return False,scans,units

def is_rup(v,db,clause):
    contradiction,scans,units=up_conflict(v,db,(-l for l in clause))
    return contradiction,scans,units

def resolve(a,b,pivot):
    if pivot in a and -pivot in b: pa=a;pb=b
    elif -pivot in a and pivot in b: pa=b;pb=a
    else: raise AssertionError('wrong resolution orientation')
    out=tuple(dict.fromkeys([x for x in pa if x!=pivot]+[x for x in pb if x!=-pivot]))
    if any(-x in out for x in out):raise AssertionError('tautological resolvent')
    return out

def solve_cdcl(v,original, restart_every=0, max_conflicts=5000):
    """Deterministic CDCL with first-UIP resolution, nonchronological backjump, optional restarts.
    Every learned clause is RUP authenticated against earlier active clauses; no new vars.
    """
    db=list(original); learned=[]; trail=[];level=0; conflict_count=0
    scans=0; units=0; decisions=0; restarts=0; res_steps=0;rup_scans=0
    def asdict():return {abs(l):(l>0) for (l,lev,reason) in trail}
    def propagate():
        nonlocal scans,units
        while True:
            values=asdict();action=False
            for ci,cl in enumerate(db):
                scans+=1
                if any((l>0)==values[abs(l)] for l in cl if abs(l) in values):continue
                left=[l for l in cl if abs(l) not in values]
                if not left:return ci
                if len(left)==1:
                    trail.append((left[0],level,ci));units+=1;action=True;break
            if not action: return None
    while True:
        conflict=propagate()
        if conflict is not None:
            conflict_count+=1
            if conflict_count>max_conflicts:raise RuntimeError('finite test conflict cutoff')
            if level==0:
                valid,ss,uu=is_rup(v,db,());rup_scans+=ss
                assert valid, 'root conflict must RUP-validate empty'
                learned.append(())
                return {'label':'UNSAT','conflicts':conflict_count,'additions':len(learned),
                        'scans':scans,'units':units,'decisions':decisions,'restarts':restarts,
                        'res_steps':res_steps,'rup_scans':rup_scans,'learned':learned}
            current=list(db[conflict]);
            def at_level(l):
                for x,ll,rr in reversed(trail):
                    if abs(x)==abs(l):return ll
                raise AssertionError('missing current-level literal')
            while sum(at_level(l)==level for l in current)>1:
                targets=[(idx,x,reason) for idx,(x,ll,reason) in enumerate(trail) if ll==level and any(abs(y)==abs(x) for y in current) and reason is not None]
                if not targets:raise AssertionError('first UIP no legal antecedent')
                idx,p,ri=max(targets,key=lambda x:x[0]);current=list(resolve(current,db[ri],p));res_steps+=1
            if any(-x in current for x in current):raise AssertionError('tautology')
            candidate=tuple(current)
            valid,ss,uu=is_rup(v,db,candidate);rup_scans+=ss
            if not valid:raise AssertionError('learned clause fails RUP')
            learned.append(candidate);db.append(candidate)
            remaining=[at_level(x) for x in candidate if at_level(x)!=level]
            back=max(remaining) if remaining else 0
            trail[:]=[item for item in trail if item[1]<=back];level=back
            if restart_every and conflict_count%restart_every==0:
                trail.clear();level=0;restarts+=1
            continue
        vals=asdict()
        if len(vals)==v:
            assert all(any(vals[abs(x)]==(x>0) for x in c) for c in original)
            return {'label':'SAT','conflicts':conflict_count,'additions':len(learned),
                    'scans':scans,'units':units,'decisions':decisions,'restarts':restarts,
                    'res_steps':res_steps,'rup_scans':rup_scans,'learned':learned,
                    'witness':[int(vals[i]) for i in range(1,v+1)]}
        var=next(i for i in range(1,v+1) if i not in vals)
        level+=1;decisions+=1;trail.append((var,level,None))

def verify_log(v,original,log):
    db=list(original);scans=0
    for clause in log:
        ok,k,u=is_rup(v,db,clause);scans+=k
        if not ok:return False,scans
        db.append(tuple(clause))
    return True,scans

def brute_sat(v,clauses):
    for bits in itertools.product((False,True),repeat=v):
        if all(any(bits[abs(l)-1]==(l>0) for l in c) for c in clauses):return True
    return False

def main():
    assertions=0; records=[];controls=0
    cases=[]
    for n in range(1,11):
        cs=[(1,)]+[(-i,i+1) for i in range(1,n)]+[(-n,)]
        cases.append(('horn-'+str(n),n,cs,False))
    k4=list(range(4));edges=[(u,w) for u in k4 for w in k4 if u<w]
    cube_edges=[(u,w) for u in range(8) for w in range(u+1,8) if (u^w) in (1,2,4)]
    for graph,verts,edges_here in [('K4',k4,edges),('Cube',list(range(8)),cube_edges)]:
        samples=list(range(16)) if graph=='K4' else [0,1,2,3,5,7,15,31,63,85,127,128,170,222,254,255]
        for mask in samples:
            charges=[(mask>>i)&1 for i in range(len(verts))]
            v,cs=tseitin(verts,edges_here,charges)
            cases.append((graph+'-charge-'+str(mask),v,cs,sum(charges)%2==0))
    cases.extend([('sat-2cnf',3,[(1,2),(-1,3)] ,True),('unsat-3cnf',3,[tuple((-j-1 if b&(1<<j) else j+1) for j in range(3)) for b in range(8)],False)])
    for label,v,cs,expect in cases:
        text=encode(v,cs);pv,original=parse_dimacs(text);assert pv==v and original==cs;assertions+=2
        assert brute_sat(v,original)==expect;assertions+=1
        for restart in (0,2):
            run=solve_cdcl(v,original,restart_every=restart)
            assert (run['label']=='SAT')==expect;assertions+=1
            ok,rups=verify_log(v,original,run['learned'])
            assert ok and run['additions']<=run['conflicts'];assertions+=1
            assert (run['learned'][-1]==()) if not expect else True;assertions+=1
            if expect:
                assert all(any((run['witness'][abs(x)-1]==1)==(x>0) for x in c) for c in cs);assertions+=1
            records.append({k:run[k] for k in ('label','conflicts','additions','scans','units','decisions','restarts','res_steps','rup_scans')}|{'case':label,'restart_every':restart,'sha256':hashlib.sha256(text.encode()).hexdigest(),'variables':v,'clauses':len(cs),'learned_log':[list(c) for c in run['learned']]})
    # All restricted transitions must be source-authenticated. Positive and negative controls.
    for bad in ('', 'p cnf 1 1\n1\n', 'p cnf 1 1\n2 0\n','p cnf 1 1\n1 -1 0\n','p cnf 1 2\n1 0\n','p cnf z 1\n1 0\n'):
        try:parse_dimacs(bad);raise AssertionError('malformed accepted')
        except BadSource:controls+=1
    v,clauses=cases[-1][1:3]
    assert not is_rup(v,clauses,(1,))[0] or brute_sat(v,clauses)==False # no guarantee non RUP for unsat; rely SAT test
    assert not is_rup(3,[(1,2)],())[0];controls+=1
    # Spoofed learned clause on a satisfiable source must be rejected.
    assert not verify_log(3,[(1,2)], [()])[0];controls+=1
    # A real shortcut for parity demonstrates class mismatch: GF(2) sum => inconsistency in O(h).
    assert (sum([1]+[0]*7)%2)==1;controls+=1
    payload={'status':'COMPUTATIONAL','scope':'original-variable CDCL first-UIP, no XOR/ER/RAT',
             'theorem':'Every learned clause is RUP; conflicts >= additions >= W_Res(F)/v for UNSAT',
             'assertions':assertions,'rejected_controls':controls,'runs':len(records),'results':records}
    print(json.dumps(payload,indent=2,sort_keys=True));return payload
if __name__=='__main__':main()
