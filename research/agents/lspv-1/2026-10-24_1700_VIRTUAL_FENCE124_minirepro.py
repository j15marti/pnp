#!/usr/bin/env python3
"""Finite mixed-label controls for VIRTUAL-FRONTIER-FENCE124. Python objects are
NOT FLMV random-access TM measurements; this reproduces finite semantic tests."""
import itertools, json, random
from collections import Counter

SEED=202610241700

def brute(n,clauses):
    for values in itertools.product((False,True),repeat=n):
        if all(any(values[abs(x)-1]==(x>0) for x in c) for c in clauses):
            return True
    return False

def source_virtual(n,clauses):
    m=len(clauses)
    stats={'event_queries':0,'source_fields':0}
    def read(i):
        assert 0<=i<2*n+m
        stats['event_queries']+=1
        if i<n:return ('OPEN',i+1)
        if i<n+m:
            stats['source_fields']+=len(clauses[i-n])
            return ('CLAUSE',clauses[i-n])
        return ('CLOSE',i-n-m+1)
    return 2*n+m,read,stats

def materialized(n,clauses):
    return [('OPEN',i+1) for i in range(n)]+[('CLAUSE',c) for c in clauses]+[('CLOSE',i+1) for i in range(n)]

def frontier_dp(event_count,read):
    live=[];states={0};peak=1;steps=0
    for i in range(event_count):
        op,arg=read(i)
        if op=='OPEN':
            assert arg not in live
            b=1<<len(live)
            states=states|{v|b for v in states}
            live.append(arg);steps+=len(states)
        elif op=='CLAUSE':
            positions={v:k for k,v in enumerate(live)}
            keep=set()
            for bits in states:
                if any(bool(bits&(1<<positions[abs(lit)]))==(lit>0) for lit in arg):
                    keep.add(bits)
            states=keep;steps+=len(positions)+len(keep)
        else:
            p=live.index(arg);mask=(1<<p)-1
            states={(v&mask)|((v>>(p+1))<<p) for v in states}
            live.pop(p);steps+=len(states)
        peak=max(peak,len(states))
    assert not live
    return bool(states),{'peak_states':peak,'table_ops':steps}

def horn(clauses,n):
    x=[False]*(n+1);visits=0
    while True:
        change=False
        for c in clauses:
            visits+=1
            pos=[v for v in c if v>0]
            neg=[-v for v in c if v<0]
            if all(x[v] for v in neg):
                if not pos:return False,visits
                if not x[pos[0]]:x[pos[0]]=True;change=True
        if not change:return True,visits

def twosat(clauses,n):
    def node(lit):return 2*(abs(lit)-1)+(lit<0)
    graph=[[] for _ in range(2*n)];rev=[[] for _ in range(2*n)]
    edges=0
    for c in clauses:
        if not c:return False,0
        if len(c)==1:c=(c[0],c[0])
        a,b=c
        for u,v in ((node(-a),node(b)),(node(-b),node(a))):
            graph[u].append(v);rev[v].append(u);edges+=1
    visited=set();order=[]
    for root in range(2*n):
        if root in visited:continue
        stack=[(root,0)];visited.add(root)
        while stack:
            v,i=stack[-1]
            if i<len(graph[v]):
                q=graph[v][i];stack[-1]=(v,i+1)
                if q not in visited:visited.add(q);stack.append((q,0))
            else:order.append(v);stack.pop()
    comp=[-1]*(2*n);cc=0
    for root in reversed(order):
        if comp[root]!=-1:continue
        stack=[root];comp[root]=cc
        while stack:
            v=stack.pop()
            for q in rev[v]:
                if comp[q]==-1:comp[q]=cc;stack.append(q)
        cc+=1
    return all(comp[2*v]!=comp[2*v+1] for v in range(n)),edges

def adaptive(n,clauses):
    acquisition=sum(len(c) for c in clauses)
    if all(sum(v>0 for v in c)<=1 for c in clauses):
        ans,steps=horn(clauses,n)
        return ans,{'rule':'Horn','recognition_reads':acquisition,'rule_ops':steps,'peak_states':n+1}
    if all(len(c)<=2 for c in clauses):
        ans,steps=twosat(clauses,n)
        return ans,{'rule':'SCC','recognition_reads':acquisition,'rule_ops':steps,'peak_states':2*n}
    m,read,stats=source_virtual(n,clauses)
    ans,ledger=frontier_dp(m,read)
    return ans,{'rule':'virtual-DP','recognition_reads':acquisition,'event_queries':stats['event_queries'],'source_fields':stats['source_fields'],**ledger}

def test():
    random.seed(SEED)
    cases=[]
    def add(name,n,c):cases.append((name,n,tuple(tuple(z) for z in c)))
    add('horn_sat',3,[(-1,2),(-2,3)])
    add('horn_unsat',3,[(1,),(-1,)])
    add('two_sat',2,[(1,2),(-1,2)])
    add('two_unsat',2,[(1,2),(1,-2),(-1,2),(-1,-2)])
    q0=[(s[0]*1,s[1]*2,s[2]*3) for s in itertools.product((-1,1),repeat=3) if sum(x<0 for x in s)%2==0]
    q1=[(s[0]*1,s[1]*2,s[2]*3) for s in itertools.product((-1,1),repeat=3) if sum(x<0 for x in s)%2==1]
    add('affine_sat',3,q0)
    add('affine_unsat',3,q0+q1)
    add('disconnected_sat',6,[(1,2,3),(4,5,6)])
    add('disconnected_unsat',6,q0+q1+[(4,5,6)])
    add('connected_sat',4,[(1,2,3),(-2,3,4)])
    add('connected_unsat',4,q0+q1+[(1,3,4)])
    for k in range(220):
        n=random.choice([3,4,5,6]);m=random.randint(1,12);c=[]
        for _ in range(m):
            vs=random.sample(range(1,n+1),3)
            c.append(tuple(v if random.getrandbits(1) else -v for v in vs))
        add('random_'+str(k),n,c)
    for k in range(100):
        n=random.choice([3,4,5,6]);m=random.randint(3,12)
        target=[False]+[bool(random.getrandbits(1)) for _ in range(n)];c=[]
        for _ in range(m):
            vs=random.sample(range(1,n+1),3)
            while True:
                trial=tuple(v if random.getrandbits(1) else -v for v in vs)
                if any(target[abs(x)]==(x>0) for x in trial):break
            c.append(trial)
        add('planted_sat_'+str(k),n,c)
    for k in range(100):
        n=random.choice([3,4,5,6]);m=random.randint(0,5)
        vs=random.sample(range(1,n+1),3)
        c=[tuple(s*v for s,v in zip(signs,vs)) for signs in itertools.product((-1,1),repeat=3)]
        for _ in range(m):
            v=random.sample(range(1,n+1),3)
            c.append(tuple(z if random.getrandbits(1) else -z for z in v))
        add('planted_unsat_'+str(k),n,c)
    counts=Counter();checks=0;max_peak=0;max_queries=0;controls={}
    for name,n,c in cases:
        truth=brute(n,c)
        got,detail=adaptive(n,c)
        assert got==truth,(name,c);checks+=1
        count,reader,source=source_virtual(n,c)
        events=materialized(n,c)
        assert [reader(j) for j in range(count)]==events;checks+=1
        mat,table=frontier_dp(count,lambda j:events[j])
        assert mat==truth;checks+=1
        if detail['rule']=='virtual-DP':
            assert detail['source_fields']==sum(len(row) for row in c)
            checks+=1
        counts[detail['rule']+('_SAT' if truth else '_UNSAT')]+=1
        max_peak=max(max_peak,table['peak_states'])
        max_queries=max(max_queries,source['event_queries'])
        if name in ('affine_sat','affine_unsat','horn_unsat','two_unsat','disconnected_sat','connected_unsat'):
            controls[name]={'label':truth,**detail,'independent_dp_peak':table['peak_states']}
    return {'title':'VIRTUAL-FRONTIER-FENCE124','seed':SEED,'cases':len(cases),
            'SAT':sum(v for k,v in counts.items() if k.endswith('_SAT')),
            'UNSAT':sum(v for k,v in counts.items() if k.endswith('_UNSAT')),
            'checks':checks,'failures':0,'methods':dict(sorted(counts.items())),
            'max_dp_peak_states':max_peak,'max_virtual_event_queries':max_queries,
            'controls':controls,'model_warning':'Python event counts are not FLMV bit-machine time/space; asymptotic result is symbolic.'}

if __name__=='__main__':
    print(json.dumps(test(),indent=2,sort_keys=True))
