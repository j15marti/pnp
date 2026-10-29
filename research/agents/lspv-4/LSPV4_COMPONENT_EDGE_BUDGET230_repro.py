#!/usr/bin/env python3
"""Independent LSPV-4 structural / resource audit, 29 Oct 2026.

PROVED component-edge theorem: k + h <= 3b+1 on a connected strict22
source with a supplied boundary and source-clause-separable private modules.
Known precursor: j15marti/pnp BOUNDARY_BURDEN1, not rediscovered here.
NEW explicit construction saturating k=3b+1 in strictly signed exact22,
with full 3CNF clauses, connected source, q_i=2 and known SAT witness.

Deterministic assertion tests are COMPUTATIONAL, not proof-assistant checks.
Resource proxies are for a specific supplied-decomposition strategy only.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from itertools import combinations, product
from math import ceil, log2, sqrt
from pathlib import Path
import csv
import hashlib
import json
import time

LEAF = [("Y", "a", "b")]
for v in ("a", "b"):
    LEAF.extend((v, x, y) for x, y in combinations("cde", 2))
CONNECTOR = [("L", "a", "b"), ("R", "c", "d")]
CONNECTOR += list(combinations("abcd", 3))
LEAF_POS = {"a": (0, 1), "b": (0, 4), "c": (1, 2),
            "d": (1, 3), "e": (5, 6)}
CONNECTOR_POS = {"a": (0, 2), "b": (0, 2),
                 "c": (1, 4), "d": (3, 5)}


def ceil_div(x: int, y: int) -> int:
    return -((-x) // y)


def old_q(n: int, b: int) -> int:
    return max(0, ceil_div(n - 3 * b, 12 * b))


def sharpened_q(n: int, b: int) -> int:
    return max(0, ceil_div(n - 3 * b, 9 * b + 3))


def integer_floor(n: int) -> int:
    s = 0
    while n > 3 * s + 9 * (s * s // 4):
        s += 1
    return s


def add_module(modules: list, typ: str, parents: tuple[int, ...]):
    mid = len(modules)
    clauses = LEAF if typ == "leaf" else CONNECTOR
    localpos = LEAF_POS if typ == "leaf" else CONNECTOR_POS
    symmap = {"Y": ("y", parents[0]),
              "L": ("y", parents[0]),
              "R": ("y", parents[-1])}
    for c in ("abcde" if typ == "leaf" else "abcd"):
        symmap[c] = ("z", mid, c)
    assert all(len([j for j, cl in enumerate(clauses) if name in cl]) == 4
               for name in localpos)
    assert all(any(j in localpos[name] for name in cl if name in localpos)
               for j, cl in enumerate(clauses)), "local all-ones witness failed"
    modules.append({"type": typ, "parent": parents,
                    "vars": [symmap[x] for x in localpos],
                    "clauses": [[symmap[t] for t in cl] for cl in clauses],
                    "localpos": localpos})


def construct(b: int):
    assert b >= 1
    modules = []
    for i in range(b-1):
        add_module(modules, "connector", (i, i+1))
    for i in range(b):
        leaves = 4 - int(i>0) - int(i<b-1)
        for _ in range(leaves):
            add_module(modules, "leaf", (i,))
    assert len(modules) == 3*b + 1
    names = [("y", i) for i in range(b)]
    for mod in modules:
        names.extend(mod["vars"])
    ids = {v: i+1 for i, v in enumerate(names)}
    unsigned = []
    var_inc = {}
    for modid, mod in enumerate(modules):
        for j, clause in enumerate(mod["clauses"]):
            ix = len(unsigned)
            unsigned.append((modid, j, clause))
            for sym in clause:
                var_inc.setdefault(sym, []).append((ix, modid, j))
    posocc = {}
    for sym, occ in var_inc.items():
        assert len(occ) == 4
        if sym[0] == 'y':
            posocc[sym] = set(ix for ix,_,_ in occ[:2])
        else:
            modid, name = sym[1], sym[2]
            posocc[sym] = {ix for ix,mi,j in occ
                           if j in modules[modid]["localpos"][name]}
            assert len(posocc[sym]) == 2
    numeric, assigned_modules = [], [[] for _ in modules]
    for ix, (mid, j, cl) in enumerate(unsigned):
        signed = tuple(ids[v] if ix in posocc[v] else -ids[v] for v in cl)
        assert len(set(map(abs,signed)))==3
        numeric.append(signed)
        assigned_modules[mid].append(signed)
    assert len(numeric)==20*b+8 and len(names)==15*b+6
    return {"n":len(names),"m":len(numeric),"b":b,
            "Y":set(range(1,b+1)), "clauses":numeric,
            "modules":assigned_modules,"module_vars": [
                {ids[v] for v in mod["vars"]} for mod in modules],
            "names":names}


def incidence_components(data):
    n=data["n"]; y=data["Y"]; clauses=data["clauses"]
    adj=[set() for _ in range(n+len(clauses)+1)]
    for j,cl in enumerate(clauses):
        node=n+j+1
        for lit in cl:
            x=abs(lit)
            adj[x].add(node);adj[node].add(x)
    # Connected prior to boundary deletion.
    reached={1}; todo=[1]
    while todo:
        u=todo.pop()
        for v in adj[u]:
            if v not in reached: reached.add(v);todo.append(v)
    assert len(reached)==n+len(clauses)
    remaining=(set(range(1,n+len(clauses)+1))-y)
    components=[]
    while remaining:
        root=min(remaining); remaining.remove(root);todo=[root]; comp={root}
        while todo:
            u=todo.pop()
            for v in adj[u]:
                if v in remaining:
                    remaining.remove(v);comp.add(v);todo.append(v)
        components.append(comp)
    private=[c for c in components if any(v<=n and v not in y for v in c)]
    lonely_clauses=[c for c in components if len(c)==1 and next(iter(c))>n]
    return len(private),len(lonely_clauses),len(components)


def local_hitting(module:list[tuple[int,...]], Y:set[int], budget:int):
    # Find clause-hitting set of private variables only for clauses disjoint Y.
    edges=[frozenset(map(abs,cl)) for cl in module
           if not any(abs(l) in Y for l in cl)]
    nodes=0
    def dfs(chosen:frozenset[int], remain:tuple[frozenset[int],...]):
        nonlocal nodes
        nodes+=1
        if not remain:return chosen
        if len(chosen)>=budget:return None
        edge=min(remain, key=lambda e:(len(e),tuple(sorted(e))))
        for v in sorted(edge):
            nxt=frozenset((*chosen,v))
            out=dfs(nxt, tuple(e for e in remain if v not in e))
            if out is not None:return out
        return None
    return dfs(frozenset(),tuple(edges)),nodes


def restrict(clauses, fixed:dict[int,bool]):
    residual=[]
    for clause in clauses:
        if any((lit>0)==fixed[abs(lit)] for lit in clause if abs(lit) in fixed):
            continue
        row=tuple(lit for lit in clause if abs(lit) not in fixed)
        if not row:return None
        residual.append(row)
    return residual


def two_sat(clauses):
    active=sorted({abs(l) for cl in clauses for l in cl})
    ids={v:i for i,v in enumerate(active)}
    num=len(active)
    if not num:return {}
    adj=[[] for _ in range(2*num)];rev=[[] for _ in adj]
    def node(lit):return 2*ids[abs(lit)]+(0 if lit>0 else 1)
    def edge(a,b):adj[a].append(b);rev[b].append(a)
    for cl in clauses:
        assert len(cl)<=2
        if len(cl)==0:return None
        if len(cl)==1:
            v=node(cl[0]);edge(v^1,v)
        else:
            a,b=map(node,cl);edge(a^1,b);edge(b^1,a)
    seen=set();order=[]
    def visit(v):
        seen.add(v)
        for w in adj[v]:
            if w not in seen:visit(w)
        order.append(v)
    for v in range(2*num):
        if v not in seen:visit(v)
    comp=[-1]*(2*num)
    def mark(v,c):
        comp[v]=c
        for w in rev[v]:
            if comp[w]==-1:mark(w,c)
    c=0
    for v in reversed(order):
        if comp[v]==-1:mark(v,c);c+=1
    solution={}
    for v,i in ids.items():
        if comp[2*i]==comp[2*i+1]:return None
        solution[v]=(comp[2*i]>comp[2*i+1])
    assert all(any((l>0)==solution[abs(l)] for l in cl) for cl in clauses)
    return solution


def static_solver(data, q:int):
    # ONE program, SAT and UNSAT; supplied boundary + authenticated partition.
    Y=sorted(data["Y"]); boundaries=0;tries=0;calls=0;nodes=0
    backs=[]
    for mod in data["modules"]:
        B,nbr=local_hitting(mod,set(Y),q)
        nodes+=nbr
        if B is None:return {"status":"UNKNOWN_NO_BACKDOOR","nodes":nodes}
        backs.append(sorted(B))
    for vals in product((False,True),repeat=len(Y)):
        boundaries+=1
        selected=dict(zip(Y,vals));joint=dict(selected);allgood=True
        for mod,B in zip(data["modules"],backs):
            localok=False
            for bits in product((False,True),repeat=len(B)):
                tries+=1
                fixed=dict(selected);fixed.update(zip(B,bits))
                res=restrict(mod,fixed)
                if res is None:continue
                assert all(len(cl)<=2 for cl in res)
                calls+=1
                extra=two_sat(res)
                if extra is not None:
                    fixed.update(extra);joint.update(fixed);localok=True;break
            if not localok: allgood=False;break
        if allgood:
            for cl in data["clauses"]:
                for lit in cl: joint.setdefault(abs(lit), False)
            assert all(any((lit>0)==joint[abs(lit)] for lit in cl)
                       for cl in data["clauses"])
            return {"status":"SAT","boundary_trials":boundaries,
                    "local_assignment_trials":tries,"two_sat_calls":calls,
                    "discovery_nodes":nodes,"witness_true_bits":sum(joint.values())}
    return {"status":"UNSAT","boundary_trials":boundaries,
            "local_assignment_trials":tries,"two_sat_calls":calls,
            "discovery_nodes":nodes}


def dimacs(path:Path):
    lines=path.read_text().splitlines();clauses=[]; n=0
    for line in lines:
        if not line or line[0]=='c':continue
        if line[0]=='p':n=int(line.split()[2]);continue
        vals=[int(x) for x in line.split()]
        assert vals[-1]==0
        clauses.append(tuple(vals[:-1]))
    assert len(clauses)==4*n//3
    return {"n":n,"m":len(clauses),"b":0,"Y":set(),
            "clauses":clauses,"modules":[clauses]}


def exhaustive_n15(data):
    assert data['n']==15
    satisfying=0
    for mask in range(1<<15):
        if all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in cl)
               for cl in data['clauses']):satisfying+=1
    return satisfying


def frontier(n):
    rows=[]; alpha=log2(3)
    for b in range(1,n+1):
        q=sharpened_q(n,b)
        rows.append({"b":b,"old_q":old_q(n,b),"new_q":q,
                     "new_log2_T_enum":b+q,"new_log2_T_discovery":alpha*q,
                     "paid_log2_time":max(alpha*q,b+q),
                     "table_log2_space":b,"streaming_exponential_space":0})
    minim=min(r['new_log2_T_enum'] for r in rows)
    feasible=[r for r in rows if r['new_log2_T_enum']==minim]
    cont_b=(sqrt(n+1)-1)/3
    paidmin=min(r['paid_log2_time'] for r in rows)
    out={"n":n,"old_min":min(b+old_q(n,b) for b in range(1,n+1)),
         "new_min":minim,"new_min_b": [r['b'] for r in feasible],
         "formula_integer_floor":integer_floor(n),
         "continuous_b":cont_b,
         "continuous_exponent":2*cont_b,
         "paid_min":paidmin,
         "paid_min_b":[r['b'] for r in rows if abs(r['paid_log2_time']-paidmin)<1e-10],
         "first_equal_log_proxy_b":ceil_div(n,3),
         "first_discovery_enum_cross_continuous":
           (-alpha+sqrt(alpha*alpha+4*(alpha-1)*n))/6}
    return out,rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='.')
    ap.add_argument('--w1',default='W1.cnf')
    a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    t0=time.perf_counter();tests=0;families=[]
    # Exact capacity floor: test all n<=6000 divisible by 3, with no floating-point assumptions.
    for n in range(3,6001,3):
        floor=integer_floor(n)
        best=min(b+sharpened_q(n,b) for b in range(1,min(n,floor+3)+1))
        assert best==floor;tests+=1
        assert n<=3*floor+9*(floor*floor//4);tests+=1
        if floor>0:
            prev=floor-1
            assert n>3*prev+9*(prev*prev//4);tests+=1
    for b in (1,2,3,4,8,16):
        data=construct(b)
        k,h,c=incidence_components(data)
        assert k==3*b+1 and h==0 and c==k;tests+=3
        sign=Counter(l for cl in data['clauses'] for l in cl)
        assert all(sign[i]==2 and sign[-i]==2 for i in range(1,data['n']+1));tests+=1
        assert all(any(l>0 for l in cl) for cl in data['clauses']);tests+=1
        assert len({tuple(sorted(map(abs,cl))) for cl in data['clauses']})==len(data['clauses']);tests+=1
        for mod in data['modules']:
            found1,_=local_hitting(mod,data['Y'],1)
            found2,_=local_hitting(mod,data['Y'],2)
            assert found1 is None and found2 is not None;tests+=2
        result=static_solver(data,2) if b in (1,2,3,4) else None
        if result:
            assert result['status']=='SAT';tests+=1
        source_bytes=len((f"p cnf {data['n']} {data['m']}\n"+"".join(" ".join(map(str,cl))+" 0\n" for cl in data['clauses'])).encode())
        families.append({"b":b,"n":data['n'],"m":data['m'],"N_dimacs_bytes":source_bytes,"k":k,
                         "h":h,"q":2,"all_true_witness":True,
                         "boundary_modules":len(data['modules']),
                         "solver":result})
    w1_path=Path(a.w1)
    if w1_path.exists():
        w1=dimacs(w1_path)
        w1_sign=Counter(l for cl in w1['clauses'] for l in cl)
        assert all(w1_sign[i]==2 and w1_sign[-i]==2 for i in range(1,16));tests+=1
        models=exhaustive_n15(w1);assert models==0;tests+=1
        ans=static_solver(w1,5);assert ans['status']=='UNSAT';tests+=1
    else:ans={"status":"NOT_RUN","reason":"W1 file missing"};models=None
    sat_variant=Path(a.w1).with_name("W1_SAT_signswap.cnf")
    if sat_variant.exists():
        w1sat=dimacs(sat_variant)
        satmodels=exhaustive_n15(w1sat)
        assert satmodels>0;tests+=1
        ans_sat=static_solver(w1sat,5)
        assert ans_sat['status']=='SAT';tests+=1
        # This is a same-scope signed exact22 pair, not a strict22 root after pinning.
        assert [tuple(sorted(map(abs,cl))) for cl in w1sat['clauses']] == [tuple(sorted(map(abs,cl))) for cl in w1['clauses']];tests+=1
    else: satmodels=None;ans_sat={"status":"NOT_RUN"}
    numeric,rows=frontier(1200)
    assert numeric['new_min']==23 and numeric['new_min_b']==list(range(9,15));tests+=1
    assert numeric['old_min']==20;tests+=1
    assert numeric['first_equal_log_proxy_b']==400;tests+=1
    assert all((3*r['b']+1)*(3*r['new_q']+1)>=1201 for r in rows);tests+=1
    assert all(r['new_q']==0 for r in rows if r['b']>=400);tests+=1
    with (out/'n1200_frontier.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    raw={"run_id":"COMPONENT_EDGE_BUDGET230","date":"2026-10-29",
         "prior_theorem":"BOUNDARY_BURDEN1 existing prior sharpening",
         "new_claim":"explicit strict22 k=3b+1 realization",
         "n1200":numeric,"families":families,"W1_UNSAT":ans,"W1_model_count":models,
         "W1_signswap_SAT":ans_sat,"W1_signswap_model_count":satmodels,
         "integer_floor_tests":6000//3,"assertions":tests,
         "elapsed_s":round(time.perf_counter()-t0,4)}
    (out/'results.json').write_text(json.dumps(raw,sort_keys=True,indent=2)+'\n')
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(figsize=(8.3,4.7))
        x=[r['b'] for r in rows if r['b']<=35]
        rr=rows[:35]
        ax.plot(x,[r['b']+r['old_q'] for r in rr],label='Original relaxed proxy $b+q$')
        ax.plot(x,[r['new_log2_T_enum'] for r in rr],label='Sharpened enumeration proxy')
        ax.plot(x,[r['paid_log2_time'] for r in rr],label='Charged $3^q$ discovery envelope')
        ax.plot(x,[r['table_log2_space'] for r in rr],label='Materialized table exponent $b$')
        ax.set_xlabel('Boundary size $b$');ax.set_ylabel('Base-2 exponent (poly factors omitted)')
        ax.set_title('n=1200: necessary static proxy parameters, NOT SAT lower bounds')
        ax.legend(fontsize=8);ax.grid(True,alpha=.2);fig.tight_layout()
        fig.savefig(out/'frontier.png',dpi=150);plt.close(fig)
    except ImportError:
        pass
    print(json.dumps(raw,indent=2,sort_keys=True))

if __name__=='__main__':main()