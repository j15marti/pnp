#!/usr/bin/env python3
"""Independent LSPV-3/455 original-source strict-3 BPHP proof audit.
Uses no producer/verifier code. Certifies declared FACET-A semantic grammar,
not historical accepted-byte R_mix341 grammar.
"""
import argparse, copy, hashlib, json, sys
from pathlib import Path


def norm(cl):
    if not isinstance(cl,list) or any(type(v)!=int or v==0 for v in cl):
        raise ValueError('bad clause atoms')
    unique=set(cl)
    if len(unique)!=len(cl) or any(-v in unique for v in unique):
        raise ValueError('duplicate/tautological clause')
    return tuple(sorted(cl, key=lambda v:(abs(v),v)))


def read_cnf(path):
    data=Path(path).read_bytes(); lines=data.decode('ascii').splitlines()
    if not lines or not lines[0].startswith('p cnf '):raise ValueError('header')
    h=lines[0].split()
    if len(h)!=4:raise ValueError('header arity')
    v,m=map(int,h[2:]); clauses=[]
    for line in lines[1:]:
        if not line.strip():continue
        parts=list(map(int,line.split()))
        if not parts or parts[-1]!=0 or 0 in parts[:-1]:raise ValueError('terminator')
        cl=norm(parts[:-1])
        if len(cl)!=3 or any(abs(x)>v for x in cl):raise ValueError('source width/range')
        clauses.append(cl)
    if len(clauses)!=m:raise ValueError('clause count')
    return v,clauses,hashlib.sha256(data).hexdigest()


def expected_family(e):
    n=2**e; pigeons=n+1; orig=pigeons*e; clauses=[]; nextvar=orig
    for p in range(pigeons):
      for q in range(p+1,pigeons):
       for hole in range(n):
        b=[(hole >> (e-1-t))&1 for t in range(e)]
        terms=[]
        for i in (p,q):
         for t in range(e):
          var=i*e+t+1
          terms.append(var if b[t]==0 else -var)
        k=len(terms)
        assert k>=4
        wires=list(range(nextvar+1,nextvar+(k-3)+1));nextvar+=k-3
        clauses.append(norm([terms[0],terms[1],wires[0]]))
        for j in range(1,k-3):
          clauses.append(norm([-wires[j-1],terms[j+1],wires[j]]))
        clauses.append(norm([-wires[-1],terms[-2],terms[-1]]))
    return nextvar,clauses


def facets_for_def(node):
    a,b=node['inputs']; c,d=node['values']; z=node['output']
    # z = (a equals c) AND (b equals d)
    x=a if c else -a; y=b if d else -b
    return [norm([-z,x]),norm([-z,y]),norm([z,-x,-y])]


def verify(doc,cnf):
    e=doc['ell'];assert 2<=e<=6
    n=2**e;m=n+1
    v,cs,sha=read_cnf(cnf)
    exp_v,exp_cs=expected_family(e)
    if (v,cs)!=(exp_v,exp_cs):raise ValueError('source not original indexed BPHP chain')
    if doc['original_variables']!=v or doc['n']!=n or doc['m']!=m:raise ValueError('metadata')
    cid={};gid={};deps={};owner={};last_id=0;last_var=v
    sources=0;defs=0;res=0;locals_=0
    for node in doc['events']:
        id_=node['id']
        if id_<=last_id:raise ValueError('topological order')
        last_id=id_
        kind=node['type']
        if kind=='SOURCE':
            if norm(node['clause'])!=cs[sources]:raise ValueError('source authenticity')
            cid[id_]=cs[sources];deps[id_]=set();sources+=1
        elif kind=='DEF':
            z=node['output'];a,b=node['inputs']
            if z!=last_var+1 or z<=v or a>=z or b>=z or a<=0 or b<=0 or a==b:
                raise ValueError('bad globally fresh definition')
            last_var=z
            if node['values'] not in ([0,0],[0,1],[1,0],[1,1]):raise ValueError('gate values')
            facets=facets_for_def(node)
            if [norm(x) for x in node['facets']]!=facets:raise ValueError('gate facets')
            deps[id_]=set(owner[x] for x in [a,b] if x in owner)
            gid[id_]=facets;owner[z]=id_;defs+=1
        elif kind=='RES':
            ref=[];anc=set()
            for parent in node['parents']:
                r=parent['ref']
                if r>=id_ or r not in deps:raise ValueError('parent ID scope')
                if 'facet' in parent:
                    if r not in gid:raise ValueError('not gate owner')
                    idx=parent['facet'];
                    if type(idx)!=int or not 0<=idx<3:raise ValueError('facet index')
                    ref.append(gid[r][idx])
                else:
                    if r not in cid:raise ValueError('not clause parent')
                    ref.append(cid[r])
                anc.add(r)
            if len(ref)!=2:raise ValueError('resolution arity')
            pivot=node['pivot']
            if type(pivot)!=int or pivot<=0:raise ValueError('pivot')
            a,b=ref
            if pivot in a and -pivot in b:
                tmp=[t for t in a if t!=pivot]+[t for t in b if t!=-pivot]
            elif -pivot in a and pivot in b:
                tmp=[t for t in a if t!=-pivot]+[t for t in b if t!=pivot]
            else:raise ValueError('incorrect oriented pivot')
            actual=norm(list(set(tmp)))
            if tuple(norm(node['clause']))!=actual:raise ValueError('resolvent mismatch')
            cid[id_]=actual;deps[id_]=anc;res+=1
        else:raise ValueError('undeclared rule '+str(kind))
    if sources!=len(cs):raise ValueError('incomplete original source')
    if last_var!=doc['variables']:raise ValueError('bad last variable')
    if doc['counts']!={'sources':sources,'definitions':defs,'resolutions':res,'paid':defs+res,'all_events':sources+defs+res}:raise ValueError('counts')
    root=doc.get('root');ancestry=set()
    if root is not None:
        r=root['ref']
        if r not in cid or cid[r]!=():raise ValueError('root not contradiction')
        stack=[r]
        while stack:
            a=stack.pop()
            if a not in ancestry:
                ancestry.add(a);stack.extend(deps[a])
        if sum(k in ancestry for k in gid)!=defs or sum(k in ancestry for k in cid if k not in gid)!=sources+res:
            raise ValueError('unused derivations in claimed full proof')
    return dict(original_source_sha256=sha,source_clauses=sources,original_vars=v,derived_defs=defs,paid_resolutions=res,paid_nodes=defs+res,root_empty=root is not None,ancestry=len(ancestry),verified_types='SOURCE/DEF/RES; owner-qualified clause facets')


def hostile(doc,cnf):
    tests={}
    def expect_bad(name, mut, source=None):
        d=copy.deepcopy(doc);mut(d)
        try:verify(d,source or cnf)
        except (ValueError,AssertionError,IndexError,KeyError,TypeError):tests[name]='REJECTED'
        else:raise AssertionError('accepted corruption: '+name)
    expect_bad('definition_output_collides_with_original',lambda d: d['events'][0].update(output=d['original_variables']))
    expect_bad('definition_facet_wrong_sign',lambda d: d['events'][0]['facets'][0].__setitem__(0,-d['events'][0]['facets'][0][0]))
    expect_bad('incorrect_resolution_pivot',lambda d:next(n for n in d['events'] if n['type']=='RES').update(pivot=999999))
    expect_bad('source_clause_sign_tamper',lambda d:next(n for n in d['events'] if n['type']=='SOURCE')['clause'].__setitem__(0,-next(n for n in d['events'] if n['type']=='SOURCE')['clause'][0]))
    expect_bad('corrupted_root',lambda d:d.update(root={'ref':1}))
    expect_bad('forward_parent_reference',lambda d:next(n for n in d['events'] if n['type']=='RES')['parents'][0].update(ref=d['events'][-1]['id']))
    return tests

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('raw');parser.add_argument('cnf');parser.add_argument('--hostile',action='store_true');args=parser.parse_args()
    doc=json.load(open(args.raw));data=verify(doc,args.cnf)
    if args.hostile:data['hostile']=hostile(doc,args.cnf)
    print(json.dumps(data,indent=2))
