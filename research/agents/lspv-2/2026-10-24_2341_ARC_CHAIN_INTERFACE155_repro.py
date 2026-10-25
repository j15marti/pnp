#!/usr/bin/env python3
"""ARC-CHAIN-INTERFACE155: finite exact tests, Python 3 standard library.
All source/gadget clauses are ordinary 3CNF with distinct variables.
Physical FLMV time/space measurements are NOT claimed.
"""
import json, math
from pathlib import Path


def encode(cnf):
    n = max((abs(x) for c in cnf for x in c), default=0)
    m = len(cnf)
    w = max(3, (2*n+1).bit_length(), (m+1).bit_length())
    out = ['1'*w+'0', format(n, f'0{w}b'), format(m, f'0{w}b')]
    for c in cnf:
        assert 1 <= len(c) <= 3 and len(set(map(abs,c))) == len(c)
        vals = [len(c)] + [2*abs(x)+(x<0) for x in c] + [0]*(3-len(c))
        out += [format(int(v), f'0{w}b') for v in vals]
    return ''.join(out)


def decode(bits):
    w = bits.find('0')
    assert w >= 3 and bits[:w] == '1'*w
    payload = bits[w+1:]
    assert len(payload) >= 2*w and len(payload) % w == 0
    fields = [int(payload[i:i+w],2) for i in range(0,len(payload),w)]
    n, m = fields[:2]
    assert len(fields) == 2 + 4*m
    cnf=[]
    for j in range(m):
        cfields=fields[2+4*j:6+4*j]
        a=cfields[0]
        assert 1 <= a <= 3 and all(t==0 for t in cfields[1+a:])
        clause=tuple((-1 if t&1 else 1)*(t//2) for t in cfields[1:1+a])
        assert all(0<abs(x)<=n for x in clause)
        assert len(set(map(abs,clause)))==a
        cnf.append(clause)
    assert n == max((abs(x) for c in cnf for x in c),default=0)
    return cnf


def proper3(clauses, auxiliary_base):
    """Exact existential gadget, keeps original variable IDs unchanged."""
    out=[]
    a=auxiliary_base
    for c in clauses:
        if len(c)==3:
            out.append(tuple(c))
        elif len(c)==2:
            a+=1
            out += [tuple(c)+(a,),tuple(c)+(-a,)]
        elif len(c)==1:
            a+=1; p=a
            a+=1; q=a
            out += [(c[0], p, q),(c[0], p, -q),
                    (c[0], -p, q),(c[0], -p, -q)]
        else: raise ValueError('requires nonempty <=3 CNF')
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in out)
    assert len(set(out))==len(out)
    return out


def chain(n, ending):
    assert n>=3 and ending in (0,1)
    return [(1,)]+[(-i,i+1) for i in range(1,n)]+[((n if ending else -n),)]


def root(n, ending):
    return proper3(chain(n,ending),n)


def dpll(cnf):
    cls=[tuple(c) for c in cnf]
    def solve(clauses):
        while True:
            if not clauses: return True
            if () in clauses: return False
            units = [c[0] for c in clauses if len(c)==1]
            if not units: break
            lit = units[0]
            if ( -lit,) in clauses: return False
            clauses=[tuple(v for v in c if v!=-lit) for c in clauses if lit not in c]
        v=min(abs(x) for c in clauses for x in c)
        for lit in (v,-v):
            nxt=[tuple(x for x in c if x!=-lit) for c in clauses if lit not in c]
            if solve(nxt): return True
        return False
    return solve(cls)


def segment_edges(start, stop):
    # x_start -> ... -> x_stop
    return [(-i,i+1) for i in range(start,stop)]


def pin(v,bit): return (v if bit else -v,)


def pinned_segment(start,stop,a,b,n):
    return proper3([pin(start,a)]+segment_edges(start,stop)+[pin(stop,b)],n)


def multiply(left,right):
    return [[int(any(left[a][b] and right[b][c] for b in (0,1)))
             for c in (0,1)] for a in (0,1)]


def identity(): return [[1,0],[0,1]]


def chunks(start,stop,span):
    return [(i,min(stop,i+span)) for i in range(start,stop,span)]


def group_solve(start,stop,a,b,n,stats):
    # First-level complete ordinary 3CNF child. Actual serialize and parse.
    group_bits=encode(pinned_segment(start,stop,a,b,n))
    group=decode(group_bits)
    assert group == pinned_segment(start,stop,a,b,n)
    stats['group_calls']+=1
    stats['max_group_bits']=max(stats['max_group_bits'],len(group_bits))
    stats['serialized_group_bits']+=len(group_bits)
    group_matrix=identity()
    span=max(1,math.ceil(math.sqrt(stop-start)))
    for l,r in chunks(start,stop,span):
        table=[]
        for u in (0,1):
            row=[]
            for v in (0,1):
                # Second-level complete proper 3CNF child, via generic total DPLL.
                bits=encode(pinned_segment(l,r,u,v,n))
                child=decode(bits)
                ok=int(dpll(child))
                row.append(ok)
                stats['leaf_calls']+=1
                stats['max_leaf_bits']=max(stats['max_leaf_bits'],len(bits))
                stats['serialized_leaf_bits']+=len(bits)
            table.append(row)
        group_matrix=multiply(group_matrix,table)
    # True group-pinned formula semantics checked against generic direct SAT.
    answer=bool(group_matrix[a][b])
    assert answer == dpll(group)
    return int(answer)


def nested_decider(n,ending):
    stats={'group_calls':0,'leaf_calls':0,'max_group_bits':0,'max_leaf_bits':0,
           'serialized_group_bits':0,'serialized_leaf_bits':0}
    entire=root(n,ending)
    source_bits=encode(entire)
    assert decode(source_bits)==entire
    group_count=math.ceil(math.sqrt(n-1))
    root_matrix=identity()
    for l,r in chunks(1,n,group_count):
        table=[[group_solve(l,r,a,b,n,stats) for b in (0,1)] for a in (0,1)]
        root_matrix=multiply(root_matrix,table)
    result=bool(root_matrix[1][ending])
    assert result==dpll(entire)
    stats.update({'n':n,'ending':ending,'root_bits':len(source_bits),
                  'root_clauses':len(entire),'result':int(result),
                  'semantic_relation':root_matrix,
                  'all_one_clause_deletion_statuses':all(dpll(entire[:j]+entire[j+1:]) for j in range(len(entire))),
                  'all_first_group_unpinned_sat':all(dpll(proper3(segment_edges(l,r),n)) for l,r in chunks(1,n,group_count))})
    assert stats['all_one_clause_deletion_statuses']
    assert stats['all_first_group_unpinned_sat']
    return stats


def route_all_input(cnf):
    # Concrete total wrapper: if a rigid chain gadget, nested; otherwise generic full-source fallback.
    if all(len(c)==3 for c in cnf) and (len(cnf)-6)%2==0:
        n=(len(cnf)-6)//2
        if n>=3:
            for e in (0,1):
                if cnf==root(n,e): return nested_decider(n,e)['result'],'nested'
    return int(dpll(cnf)),'full_parent_fallback'


def main():
    results=[]
    for n in (3,4,5,8,9,16,25,36,49,64):
        for end in (0,1):
            x=nested_decider(n,end)
            x['route_all_input']=route_all_input(root(n,end))[1] if n in (3,16,64) else 'nested_checked_by_dispatch_definition'
            assert x['result']==end
            results.append(x)
    nonpromised=[('eight_signs', [tuple((-v if (mask>>(v-1))&1 else v) for v in (1,2,3)) for mask in range(8)],False),
                 ('seven_signs',[tuple((-v if (mask>>(v-1))&1 else v) for v in (1,2,3)) for mask in range(7)],True),
                 ('contradict_units',[(1,),(-1,)],False),
                 ('easy_horn',[(1,),(-1,2)],True)]
    fallbacks=[]
    for name,cnf,expected in nonpromised:
        ans,route=route_all_input(cnf)
        assert bool(ans)==expected and route=='full_parent_fallback'
        fallbacks.append({'name':name,'sat':ans,'route':route,'bits':len(encode(cnf))})
    assert all((x['result']==x['ending'] and x['all_one_clause_deletion_statuses']) for x in results)
    out={'run_id':'ARC-CHAIN-INTERFACE155','source_gadget':'2-clause binary / 4-clause unit exact 3CNF','seed':None,
         'finite_claim_only':True,'tested_formula_count':len(results),'tests':results,
         'fallbacks':fallbacks,'total_leaf_calls':sum(x['leaf_calls'] for x in results),
         'total_group_calls':sum(x['group_calls'] for x in results)}
    dest=Path('/mnt/data/ARC_CHAIN_INTERFACE155_raw.json')
    dest.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'tested_formula_count':out['tested_formula_count'],
                      'total_leaf_calls':out['total_leaf_calls'],
                      'total_group_calls':out['total_group_calls'],
                      'fallbacks':fallbacks,
                      'largest_unSAT':next(x for x in results if x['n']==64 and x['ending']==0),
                      'raw_path':str(dest)},indent=2))

if __name__=='__main__': main()
