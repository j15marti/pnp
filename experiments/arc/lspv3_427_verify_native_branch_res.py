#!/usr/bin/env python3
"""Independent, exact-original-source RES certificate verifier for LSPV-3/427.
Usage: python branch_lift427_verify_compact.py branch_lift427_raw.json
Does not import or trust the producing solver.
"""
import json,sys

def C(xs):return tuple(sorted(set(xs),key=lambda x:(abs(x),x)))

def R(a,b,p):
    assert p in a and -p in b, ('pivot',p,a,b)
    c=C([x for x in a if x!=p]+[x for x in b if x!=-p])
    assert not any(-x in c for x in c),'tautological resolvent'
    return c

def parse(text):
    lines=text.splitlines();head=lines[0].split()
    assert len(head)==4 and head[:2]==['p','cnf']
    n,m=map(int,head[2:]); assert len(lines)==m+1
    out=[]
    for line in lines[1:]:
        z=list(map(int,line.split()));assert z[-1]==0 and z.count(0)==1
        assert len(z)==4 and all(1<=abs(x)<=n for x in z[:-1]);assert len(set(map(abs,z[:-1])))==3
        out.append(C(z[:-1]))
    return n,out

def restrict(c,lit):
    return None if lit in c else C(x for x in c if x!=-lit)

def check(entry):
    n,src=parse(entry['source_dimacs']);assert n==entry['variable_count']
    assert len(src)==entry['clause_count'];x=entry['branchvar']
    assert [b['literal'] for b in entry['branches']]==[x,-x]
    total=0
    for b in entry['branches']:
        d={};byid={}
        def get(ref):
            if ref[0]=='s':
                c=restrict(src[int(ref[1:])],b['literal']);assert c is not None
                return c
            return d[ref]
        for line in b['nodes']:
            assert abs(line['pivot'])!=x and line['id'] not in d
            a,z=(get(t) for t in line['parents']);assert R(a,z,line['pivot'])==C(line['clause'])
            d[line['id']]=C(line['clause']);byid[line['id']]=line
        assert get(b['terminal'])==()
        stack=[b['terminal']];used=set()
        while stack:
            t=stack.pop()
            if t[0]=='s' or t in used:continue
            used.add(t);stack.extend(byid[t]['parents'])
        total+=len(used)
    assert total==entry['branch_used_nodes']
    d={};byid={}
    def orig(ref):
        if ref[0]=='s':return src[int(ref[1:])]
        return d[ref]
    for line in entry['compiled']['nodes']:
        assert line['id'] not in d
        a,z=(orig(t) for t in line['parents'])
        assert R(a,z,line['pivot'])==C(line['clause'])
        d[line['id']]=C(line['clause']);byid[line['id']]=line
    assert orig(entry['compiled']['terminal'])==()
    for v in (x,-x):
        z=entry['compiled']['branch_terminals'][str(v)]
        assert orig(z['ref'])==C(z['clause'])
        assert orig(z['ref']) in ((),(-v,))
    stack=[entry['compiled']['terminal']];used=set()
    while stack:
        t=stack.pop()
        if t[0]=='s' or t in used:continue
        used.add(t);stack.extend(byid[t]['parents'])
    assert len(used)==len(entry['compiled']['nodes'])==entry['compiled_used_nodes']
    assert total+1-len(used)==entry['possible_node_savings']
    return entry['name'],len(src),total,len(used),entry['possible_node_savings']

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else 'branch_lift427_raw.json'
    data=json.load(open(path))
    for row in data['sources']:print(*check(row))
    print('PASS: original-source native binary RES; no case-split/discharge rule')
