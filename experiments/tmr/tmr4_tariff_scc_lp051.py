#!/usr/bin/env python3
"""TMR-4 fusion-Lipschitz tariff lab 051. Exact Fraction LP and zero-cost SCC.

A qualified 2-bit parity *oracle-access protocol*, not an arbitrary SAT TM.
No third-party runtime dependencies. Python 3.12+.
Usage: python tmr4_tariff_scc_lp051.py [output.json]
"""
from __future__ import annotations
from collections import deque, Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from heapq import heappush, heappop
from itertools import product
import json, sys

COLS = ("CNF", "XOR", "sep", "fusion", "Gamma", "interface", "machine")
assert len(COLS) == 7

@dataclass(frozen=True, order=True)
class State:
    source: str
    mask: int
    tag: int
    halt: bool

    def key(self): return (self.source, self.mask, self.tag, self.halt)
    def label(self):
        return (int(self.source[0]) ^ int(self.source[1])) if self.halt else None

@dataclass(frozen=True)
class Edge:
    src: State
    dst: State
    rule: str
    cost: int
    def key(self): return (self.src.key(),self.dst.key(),self.rule,self.cost)


def build(extra_compact=False, extra_zero=False):
    sources = ('00','01','10','11')
    states = [State(b,m,t,False) for b,m,t in product(sources,range(4),range(2))]
    states += [State(b,3,0,True) for b in sources]
    edges=[]
    def add(a,b,r,w):
        assert a in states and b in states and w in (0,1)
        edges.append(Edge(a,b,r,w))
    for a in states:
        if a.halt: continue
        add(a,State(a.source,a.mask,1-a.tag,False),'free_tag_swap',0)
        for i in range(2):
            add(a,State(a.source,a.mask|(1<<i),a.tag,False),'read_'+str(i),1)
        add(a,a,'bad_index_2',1)
        if a.mask == 3:
            add(a,State(a.source,3,0,True),'free_affine_xor_finish',0)
        if extra_compact and a.mask==0:
            add(a,State(a.source,3,0,True),'compact_parity_hint',1)
        if extra_zero and a.mask==0:
            add(a,State(a.source,3,0,True),'free_omniscient_hint',0)
    return tuple(states),tuple(edges)


def tarjan(states,edges):
    adj={s:[] for s in states}
    for e in edges:
        if e.cost == 0: adj[e.src].append(e.dst)
    index={};low={};st=[];in_st=set();comp=[]
    def visit(v):
        index[v]=low[v]=len(index);st.append(v);in_st.add(v)
        for u in adj[v]:
            if u not in index:
                visit(u);low[v]=min(low[v],low[u])
            elif u in in_st: low[v]=min(low[v],index[u])
        if low[v] == index[v]:
            grp=[]
            while True:
                u=st.pop();in_st.remove(u);grp.append(u)
                if u==v:break
            comp.append(tuple(sorted(grp)))
    for s in states:
        if s not in index:visit(s)
    return tuple(comp)


def epsilon_closure(states,edges):
    adj={s:[] for s in states}
    for e in edges:
        if e.cost==0:adj[e.src].append(e.dst)
    closure={}
    for s in states:
        seen={s};q=deque([s])
        while q:
            for t in adj[q.popleft()]:
                if t not in seen:seen.add(t);q.append(t)
        closure[s]=frozenset(seen)
    return closure


def features(s):
    residual=2-s.mask.bit_count()
    return (0,0,0,0,residual,residual,0)


def closed_features(states,closure):
    p={}
    for s in states:
        p[s]=tuple(min(features(t)[j] for t in closure[s]) for j in range(len(COLS)))
    return p


def dot(x,y):return sum((a*b for a,b in zip(x,y)),Q(0))


def constraints(states,edges,p):
    allrows=[]
    for i,e in enumerate(edges):
        d=tuple(Q(a-b) for a,b in zip(p[e.src],p[e.dst]))
        allrows.append((d,Q(e.cost),f'{i}:{e.rule}:{e.src.key()}->{e.dst.key()}'))
    for s in states:
        if s.halt:
            allrows.append((tuple(map(Q,p[s])),Q(0),f'goal:{s.key()}'))
    assert all(b>=0 for _,b,_ in allrows)
    return allrows


def simplex_nonnegative(rows, objective):
    """Exact rational simplex for max c.x: A.x<=b, x>=0, b>=0.
    Initial slack basis feasible, Bland pivot rule, full rational dual check.
    """
    m=len(rows);n=len(objective);width=n+m+1
    a=[]
    for i,(coeff,b,_) in enumerate(rows):
        line=list(map(Q,coeff))+[Q(int(j==i)) for j in range(m)]+[Q(b)]
        assert len(line)==width
        a.append(line)
    a.append([-Q(c) for c in objective]+[Q(0)]*m+[Q(0)])
    basis=[n+i for i in range(m)]
    iterations=0
    while True:
        entering=next((j for j in range(n+m) if a[m][j]<0),None)
        if entering is None:break
        candidates=[(a[i][-1]/a[i][entering],basis[i],i) for i in range(m) if a[i][entering]>0]
        if not candidates:raise ValueError(f'UNBOUNDED entering column {entering}')
        _,_,pivot=min(candidates)
        z=a[pivot][entering]
        a[pivot]=[v/z for v in a[pivot]]
        for i in range(m+1):
            if i==pivot:continue
            f=a[i][entering]
            if f:a[i]=[a[i][k]-f*a[pivot][k] for k in range(width)]
        basis[pivot]=entering
        iterations+=1
        if iterations>10000:raise AssertionError('simplex pivot guard')
    x=[Q(0) for _ in range(n+m)]
    for i,j in enumerate(basis):x[j]=a[i][-1]
    lam=x[:n]
    dual=a[m][n:n+m]
    assert all(v>=0 for v in lam+dual)
    val=dot(objective,lam)
    assert val==dot([r[1] for r in rows],dual)==a[m][-1]
    for coeff,b,_ in rows:assert dot(coeff,lam)<=b
    for j in range(n):
        assert sum((dual[i]*rows[i][0][j] for i in range(m)),Q(0))>=objective[j]
    return {'weights':lam,'dual':dual,'value':val,'pivots':iterations}


def shortest_path(states,edges,start):
    adj={s:[] for s in states}
    for e in edges:adj[e.src].append(e)
    seq=0;h=[(0,seq,start)];d={start:0};parent={}
    while h:
        cost,_,state=heappop(h)
        if cost!=d[state]:continue
        if state.halt:
            path=[];cur=state
            while cur!=start:
                e=parent[cur];path.append(e);cur=e.src
            return cost,list(reversed(path))
        for e in adj[state]:
            v=cost+e.cost
            if v<d.get(e.dst,10**100):
                d[e.dst]=v;parent[e.dst]=e;seq+=1;heappush(h,(v,seq,e.dst))
    raise ValueError('unreachable terminal')


def independent_audit(states,edges,closure,p,rows,weights):
    checked=0;violations=[]
    for e in edges:
        before=dot(weights,p[e.src]);after=dot(weights,p[e.dst]);checked+=1
        if before > e.cost+after:
            violations.append({'rule':e.rule,'before':str(before),'cost':e.cost,'after':str(after),'src':e.src.key()})
        if e.cost==0:
            assert closure[e.dst].issubset(closure[e.src])
            assert all(p[e.src][j]<=p[e.dst][j] for j in range(len(COLS)))
    for s in states:
        if s.halt:
            checked+=1
            if dot(weights,p[s])>0: violations.append({'goal':s.key()})
    return checked,violations


def strq(q):return str(q.numerator) if q.denominator==1 else f'{q.numerator}/{q.denominator}'
def printable(xs):return [strq(x) for x in xs]


def exercise(widen=False, free_hint=False):
    states,edges=build(widen, free_hint)
    scc=tarjan(states,edges);closure=epsilon_closure(states,edges)
    for comp in scc:
        for s in comp:assert closure[s]==closure[comp[0]]
    p=closed_features(states,closure)
    rows=constraints(states,edges,p)
    initial=State('00',0,0,False);o=tuple(map(Q,p[initial]))
    lp=simplex_nonnegative(rows,o)
    manual=[Q(0)]*7;manual[4]=Q(1,2) if not widen else Q(1,4);manual[5]=manual[4]
    checks,errors=independent_audit(states,edges,closure,p,rows,manual)
    assert not errors
    if not free_hint: assert dot(o,manual)==lp['value']
    else: assert lp['value']==0 and all(v==0 for v in o)
    dist,path=shortest_path(states,edges,initial)
    assert Q(dist)==lp['value']
    assert path and sum(e.cost for e in path)==dist
    for b in ('00','01','10','11'):
        a=State(b,0,0,False)
        v,tr=shortest_path(states,edges,a)
        assert v==(0 if free_hint else (1 if widen else 2))
        assert tr[-1].dst.label()==(int(b[0])^int(b[1]))
    if widen and not free_hint:
        old=[Q(0)]*7;old[4]=old[5]=Q(1,2)
        c,v=independent_audit(states,edges,closure,p,rows,old)
        assert len(v)==8 and all(x['rule']=='compact_parity_hint' for x in v)
    if free_hint:
        violations=[e for e in edges if e.rule=='free_omniscient_hint' and features(e.src)[4]>features(e.dst)[4]]
        assert len(violations)==8
    naive=[Q(0)]*7;naive[4]=naive[5]=Q(1)
    _,naive_bad=independent_audit(states,edges,closure,p,rows,naive)
    assert naive_bad or free_hint
    rule_rows={}
    for e in edges:
        d=tuple(a-b for a,b in zip(p[e.src],p[e.dst]))
        key=(e.rule,e.cost,d)
        rule_rows[key]=rule_rows.get(key,0)+1
    return {
        'model':'exact deterministic two-source-bit read protocol; arbitrary adaptive read requests, not a full SAT TM',
        'widened_with_nonquery_compact_source_hint':widen,
        'widened_with_free_omniscient_hint':free_hint,
        'states':len(states),'legal_edges':len(edges),'zero_cost_edges':sum(e.cost==0 for e in edges),
        'zero_scc_count':len(scc),'nontrivial_zero_scc_count':sum(len(c)>1 for c in scc),
        'max_zero_closure':max(map(len,closure.values())),
        'columns':COLS,'initial_p':p[initial],
        'optimum':strq(lp['value']),'primal_simplex':printable(lp['weights']),
        'rational_certificate':printable(manual),'simplex_pivots':lp['pivots'],
        'nonzero_dual_row_multipliers':[{'row':rows[i][2],'value':strq(y)} for i,y in enumerate(lp['dual']) if y],
        'independently_checked_edge_and_goal_inequalities':checks,
        'minimum_actual_paid_path_cost':dist,
        'witness_shortest_path':[{'rule':e.rule,'cost':e.cost,'before':e.src.key(),'after':e.dst.key()} for e in path],
        'tariff_matrix':[{'rule':key[0],'cost':key[1],'delta':list(key[2]),'multiplicity':count} for key,count in sorted(rule_rows.items())],
        'naive_sum_violated_rows':len(naive_bad),
        'naive_first_violation':naive_bad[0] if naive_bad else None,
        'old_rational_certificate_violated_shortcut_rows':8 if widen else 0
    }


def main():
    basic=exercise(False);extended=exercise(True);free=exercise(False,True)
    assert basic['optimum']=='2' and extended['optimum']=='1' and free['optimum']=='0'
    assert basic['nontrivial_zero_scc_count']==16
    out={
        'experiment':'TMR4-TARIFF-SCC-LP051', 'status':'COMPUTATIONAL finite calibration + exact arithmetic',
        'timestamp_pacific':'2026-11-14 19:36 PST',
        'scope':'two-bit oracle protocol, not ordinary SAT, /341, /386, or any universal machine',
        'exact_rational_engine':'Python fractions.Fraction simplex, Bland-rule pivots; exact dual and independent path check',
        'qualified':basic, 'hostile_compact_extension':extended, 'hostile_free_oracle_extension':free,
        'facts':{'affine':'free XOR finish; XOR residual zero','sharing':'duplicate/cached read does not discharge again',
                 'malformed':'invalid read address charged, no source fact or terminal','compact':'source-aware primitive creates a new model and halves certified cost',
                 'zero_cost':'two-way tag swaps form authentic zero SCCs; free finalization is one-way zero edge; hypothetical free oracle collapses initial potential'},
        'asymptotic_or_unrestricted_claim':'NONE; P versus NP OPEN'
    }
    target=sys.argv[1] if len(sys.argv)>1 else None
    data=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if target:
        with open(target,'w',encoding='utf8') as f:f.write(data)
    print(json.dumps({'result':'PASS','basic':{'states':basic['states'],'edges':basic['legal_edges'],'scc':basic['zero_scc_count'],'optimum':basic['optimum'],'certificate':basic['rational_certificate'],'row_checks':basic['independently_checked_edge_and_goal_inequalities']},'compact_extension':{'edges':extended['legal_edges'],'optimum':extended['optimum'],'certificate':extended['rational_certificate'],'violating_shortcuts':8},'free_oracle_extension':{'optimum':free['optimum'],'collapsed_initial_potential':True}},sort_keys=True))

if __name__=='__main__':main()
