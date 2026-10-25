#!/usr/bin/env python3
"""ARC-EXPANDER-SCOPE172: exact graph padding, two real SAT levels, and scope checks.
Pure standard library, deterministic seed; each invocation <30 seconds.
The asymptotic expansion theorem is from Gabber--Galil, NOT proved by finite tests.
"""
from __future__ import annotations
import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

SEED = 202610250800
OUT = Path(__file__).with_name('2026-10-25_0800_ARC_EXPANDER_SCOPE172_results.json')
assertions = 0

def check(p, message='check failed'):
    global assertions
    assertions += 1
    if not p:
        raise AssertionError(message)

def slots(q):
    """Four forward permutation slots per vertex; undirected multigraph degree 8."""
    arr = []
    for x in range(q):
        for y in range(q):
            u = x*q+y
            for xx,yy in (((x+2*y)%q,y), ((x+2*y+1)%q,y),
                          (x,(y+2*x)%q), (x,(y+2*x+1)%q)):
                arr.append((u,xx*q+yy))
    return arr

def padding(q, source_nvars=3):
    n=q*q
    e=slots(q)
    clauses=[]
    for i,(u,v) in enumerate(e):
        # z_i and w_i are private to each slot. For loops, both ensure
        # a proper 3-variable clause. Never add a fake graph edge.
        uu=source_nvars+1+u
        vv=source_nvars+1+v
        aa=source_nvars+1+n+2*i
        bb=aa+1
        row=(uu,vv,aa) if u!=v else (uu,aa,bb)
        check(len(row)==3 and len(set(row))==3)
        clauses.append(row)
    return clauses, source_nvars+n+2*len(e)

def dimacs(clauses, nvar):
    return 'p cnf %d %d\n'%(nvar,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def parse(data):
    lines=[s.strip() for s in data.splitlines() if s.strip() and not s.startswith('c ')]
    if not lines: raise ValueError('empty')
    hdr=lines[0].split()
    if len(hdr)!=4 or hdr[:2]!=['p','cnf']: raise ValueError('header')
    try: nvar,m=map(int,hdr[2:])
    except Exception as e: raise ValueError('counts') from e
    if not (nvar>=0 and m>=0 and len(lines)==m+1): raise ValueError('count')
    out=[]
    for line in lines[1:]:
        try: seq=[int(x) for x in line.split()]
        except Exception as e: raise ValueError('literal') from e
        if not seq or seq[-1]!=0 or any(x==0 for x in seq[:-1]): raise ValueError('zero')
        if any(abs(x)>nvar for x in seq[:-1]): raise ValueError('range')
        out.append(tuple(seq[:-1]))
    return out,nvar

def restrict(clauses,v,val):
    want=v if val else -v
    anti=-want
    out=[]
    for row in clauses:
        if want in row: continue
        out.append(tuple(x for x in row if x!=anti))
    return out

def dpll(clauses):
    # Genuine ordinary-CNF decision, including empty clause and both labels.
    cls=tuple(tuple(c) for c in clauses)
    while True:
        if not cls: return True
        if any(not c for c in cls): return False
        units={c[0] for c in cls if len(c)==1}
        if any(-x in units for x in units):return False
        if units:
            x=min(units,key=lambda z:(abs(z),z<0))
            cls=tuple(restrict(cls,abs(x),x>0))
            continue
        signs={x for c in cls for x in c}
        pure=[x for x in signs if -x not in signs]
        if pure:
            x=min(pure,key=lambda z:(abs(z),z<0))
            cls=tuple(restrict(cls,abs(x),x>0))
            continue
        break
    # Branch on a shortest row's first variable, deterministic.
    row=min(cls,key=lambda c:(len(c),tuple(abs(x) for x in c)))
    x=abs(row[0])
    return dpll(restrict(cls,x,True)) or dpll(restrict(cls,x,False))

def frontier(q,order):
    es=slots(q)
    n=q*q
    rem=Counter()
    for u,v in es:
        rem[u]+=1
        if v!=u:rem[v]+=1
    seen=set(); max_width=0; cross=None; visit=None; width_cut=None
    for idx in order:
        u,v=es[idx]
        seen.add(u);seen.add(v)
        rem[u]-=1
        if v!=u: rem[v]-=1
        active={a for a in seen if rem[a]>0}
        max_width=max(max_width,len(active))
        if visit is None and len(seen)>=n/2:
            # Each undirected multigraph slot crossing this visited set is
            # an as-yet-unemitted clause involving an already-touched name.
            cross=sum((a in seen)!=(b in seen) for a,b in es)
            visit=len(seen);width_cut=len(active)
            check(cross<=8*len(active),'incident edge charge violated')
            lo=(8-5*math.sqrt(2))*visit*(n-visit)/n
            check(cross+1e-9>=lo,'spectral-expansion check violated')
        check(all(x>=0 for x in rem.values()),'negative incidence')
    check(sum(rem.values())==0)
    return {'max_live':max_width,'balanced_visited':visit,'active_at_cut':width_cut,
            'cross_slots':cross,'spectral_edge_bound':round((8-5*math.sqrt(2))*visit*(n-visit)/n,7)}

def pad_bit(q,source_nvars,position):
    """Indexed bit of fixed-width positive 3-CNF padding without emitting it."""
    n=q*q; M=4*n; width=(source_nvars+n+2*M+1).bit_length()
    record=3*(width+1)
    if not 0<=position<M*record:raise IndexError(position)
    edge_no,local=divmod(position,record)
    u_index,slot=divmod(edge_no,4)
    x,y=divmod(u_index,q)
    dest=(((x+2*y)%q,y),((x+2*y+1)%q,y),
          (x,(y+2*x)%q),(x,(y+2*x+1)%q))[slot]
    v_index=dest[0]*q+dest[1]
    U=source_nvars+1+u_index
    V=source_nvars+1+v_index
    A=source_nvars+1+n+2*edge_no
    B=A+1
    row=(U,V,A) if u_index!=v_index else (U,A,B)
    litidx,bit=divmod(local,width+1)
    if bit==0:return '0'   # fixed sign bit for positive literal
    return format(row[litidx],f'0{width}b')[bit-1]

def packed_pad(q,source_nvars):
    rows,_=padding(q,source_nvars)
    n=q*q; M=4*n; width=(source_nvars+n+2*M+1).bit_length()
    return ''.join(''.join('0'+format(x,f'0{width}b') for x in row) for row in rows)

def run():
    rng=random.Random(SEED)
    results={'run_id':'ARC-EXPANDER-SCOPE172','seed':SEED,
             'mode':'deterministic finite audit; no spectral theorem inferred from samples',
             'graph_convention':'four forward Margulis--Gabber--Galil slots per vertex; loops have separately SAT private clause variables',
             'graphs':[], 'roots':[], 'malformed':0, 'assertions':0}
    for q in (3,4,5,6,7,8,10,12):
        n=q*q; es=slots(q)
        check(len(es)==4*n)
        incidence=Counter()
        for u,v in es:
            incidence[u]+=1; incidence[v]+=1  # loop has two stubs
        check(all(incidence[x]==8 for x in range(n)), 'not 8-regular')
        orders={'forward':list(range(len(es))), 'reverse':list(range(len(es)-1,-1,-1))}
        for j in range(5):
            a=list(range(len(es)));rng.shuffle(a);orders[f'shuffle_{j}']=a
        stats={label:frontier(q,order) for label,order in orders.items()}
        raw=packed_pad(q,3)
        pos=[0,1,len(raw)-1,len(raw)//3,len(raw)//2]
        pos.extend(rng.randrange(len(raw)) for _ in range(min(160,len(raw))))
        for i in pos:check(pad_bit(q,3,i)==raw[i],'addressed bit mismatch')
        results['graphs'].append({'q':q,'vertices':n,'edge_slots':len(es),
                                  'loops':sum(u==v for u,v in es),'packed_bits':len(raw),
                                  'random_bit_probes':len(pos),'order_checks':stats,
                                  'min_sample_max_live':min(z['max_live'] for z in stats.values()),
                                  'min_sample_active_cut':min(z['active_at_cut'] for z in stats.values())})
    # Both SAT and UNSAT proper ternary roots. These are always
    # independently decided from serialized whole ordinary formulas.
    sat_roots=[[(1,2,3)],[(1,-2,3),(-1,2,3)],[(1,2,3),(-1,2,-3)]]
    unsat_roots=[list(itertools.product(*((i,-i) for i in (1,2,3)))),
                 [(1,2,3),(-1,2,3),(1,-2,3),(-1,-2,3),
                  (1,2,-3),(-1,2,-3),(1,-2,-3),(-1,-2,-3)]]
    # all eight sign triples exclude all assignments
    for i,F in enumerate(sat_roots+unsat_roots):
        expect=i<len(sat_roots)
        check(dpll(F)==expect,'source truth label wrong')
        for q in (3,4,6,8):
            G,nvar=padding(q)
            root=F+G
            root2,num=parse(dimacs(root,nvar))
            check(num==nvar and root2==root)
            check(dpll(root2)==expect,'whole root status')
            # Two REAL Shannon levels on *distinct* original graph vertices.
            x=4+0; y=4+q*q-1
            first=[]; second=[]
            for b in (0,1):
                F1=restrict(root2,x,b)
                text1=dimacs(F1,nvar)
                D1,_=parse(text1)
                check(dpll(D1)==expect,'child SAT/UNSAT mismatch')
                first.append(bool(dpll(D1)))
                for c in (0,1):
                    F2=restrict(D1,y,c)
                    D2,_=parse(dimacs(F2,nvar))
                    check(dpll(D2)==expect,'grandchild SAT/UNSAT mismatch')
                    second.append(bool(dpll(D2)))
            check(any(first)==expect)
            check(any(second)==expect)
            check(all(len(row)<=3 for row in root2))
            results['roots'].append({'q':q,'source_case':i,'source_label':'SAT' if expect else 'UNSAT',
                                      'root_clauses':len(root),'first_children':2,'grandchildren':4,
                                      'first_truths':first,'grandchild_truths':second,
                                      'root_encoded_bytes':len(dimacs(root,nvar).encode())})
    malformed=['p cnf 2 1\n1 2\n','p cna 3 1\n1 2 3 0\n',
               'p cnf 3 1\n1 4 3 0\n','p cnf 3 2\n1 2 3 0\n']
    for x in malformed:
        try:parse(x)
        except ValueError: check(True);results['malformed']+=1
        else:check(False,'malformed input accepted')
    results['assertions']=assertions
    results['two_level_children']=len(results['roots'])*2
    results['two_level_grandchildren']=len(results['roots'])*4
    OUT.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'assertions':assertions,'graphs':len(results['graphs']),
           'root_cases':len(results['roots']),'first_children':results['two_level_children'],
           'grandchildren':results['two_level_grandchildren'],'malformed':results['malformed'],
           'min_live_by_q':[(g['q'],g['min_sample_max_live']) for g in results['graphs']]},indent=2))

if __name__=='__main__':run()
