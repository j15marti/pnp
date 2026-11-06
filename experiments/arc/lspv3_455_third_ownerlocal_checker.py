#!/usr/bin/env python3
"""Independent owner-LOCAL checker for a PROPOSED grammar, not native R_mix341.
Each owner facet is first emitted in a paid LOCAL node before RES can cite it.
"""
import json,argparse,copy
from lspv3_455_third_checker import norm,read_cnf,expected_family,facets_for_def

def verify(doc,cnf):
    ell=doc['ell'];v,clauses,sha=read_cnf(cnf)
    ev,exp=expected_family(ell)
    if (v,clauses)!=(ev,exp):raise ValueError('original source mismatch')
    if doc['original_variables']!=v or doc['n']!=2**ell or doc['m']!=2**ell+1:raise ValueError('metadata mismatch')
    ids={};defs={};derived={};deps={};last_id=0;last_var=v
    nsrc=ndef=nlocal=nres=0
    for node in doc['events']:
        i=node['id']
        if i<=last_id:raise ValueError('topological order violation')
        last_id=i
        typ=node['type']
        if typ=='SOURCE':
            if nsrc>=len(clauses) or norm(node['clause'])!=clauses[nsrc]:raise ValueError('source mutation')
            derived[i]=clauses[nsrc];deps[i]=set();nsrc+=1
        elif typ=='DEF':
            z=node['output'];a,b=node['inputs']
            if z<=v or z!=last_var+1 or a>=z or b>=z or a<1 or b<1 or a==b:raise ValueError('gate freshness')
            if node['values'] not in ([0,0],[1,0],[0,1],[1,1]):raise ValueError('invalid gate tag')
            last_var=z;facet=facets_for_def(node)
            if [norm(f) for f in node['facets']]!=facet:raise ValueError('fake owner facets')
            defs[i]=facet;ids[z]=i;deps[i]=set(ids[j] for j in (a,b) if j in ids);ndef+=1
        elif typ=='LOCAL':
            parent=node['parent']
            if set(parent)!={'ref'}:raise ValueError('unauthorized local parent type')
            owner=parent['ref'];k=node['facet']
            if type(k)!=int or k not in (0,1,2) or owner not in defs or owner>=i:raise ValueError('wrong local owner')
            if norm(node['clause'])!=defs[owner][k]:raise ValueError('invalid paid local facet')
            derived[i]=defs[owner][k];deps[i]={owner};nlocal+=1
        elif typ=='RES':
            parents=node['parents'];refs=[]
            if len(parents)!=2:raise ValueError('wrong RES arity')
            for p in parents:
                if set(p)!={'ref'}:raise ValueError('DIRECT OWNER FACET not authorized in OWNER-LOCAL grammar')
                if p['ref'] not in derived or p['ref']>=i:raise ValueError('not a prior clause')
                refs.append(p['ref'])
            C,D=[derived[r] for r in refs];k=node['pivot']
            if type(k)!=int or k<1:raise ValueError('bad pivot')
            if k in C and -k in D:out=[x for x in C if x!=k]+[x for x in D if x!=-k]
            elif -k in C and k in D:out=[x for x in C if x!=-k]+[x for x in D if x!=k]
            else:raise ValueError('not an oriented RES')
            out=norm(list(set(out)))
            if norm(node['clause'])!=out:raise ValueError('fake RES conclusion')
            derived[i]=out;deps[i]=set(refs);nres+=1
        else:raise ValueError('unrecognized inference type')
    if nsrc!=len(clauses) or last_var!=doc['variables']:raise ValueError('incomplete source')
    expected={'sources':nsrc,'definitions':ndef,'resolutions':nres,'paid':ndef+nlocal+nres,'all_events':nsrc+ndef+nlocal+nres,'local':nlocal}
    if doc['counts']!=expected:raise ValueError('paid accounting')
    root=doc.get('root');visited=set()
    if root is not None:
        r=root['ref']
        if derived.get(r,None)!=():raise ValueError('root not empty')
        stack=[r]
        while stack:
            j=stack.pop()
            if j not in visited:
                visited.add(j);stack.extend(deps[j])
        if len(visited)!=len(doc['events']):raise ValueError('counted orphan nodes')
    return {'source_sha256':sha,'clauses':nsrc,'original_vars':v,'paid_defs':ndef,'paid_locals':nlocal,'paid_res':nres,'paid_total':ndef+nlocal+nres,'root_empty':root is not None,'ancestry_nodes':len(visited),'typed_facet_policy':'EVERY owner facet requires separate paid LOCAL; RES takes clauses only'}

def hostile(doc,cnf):
    result={}
    def check(name,f):
        d=copy.deepcopy(doc);f(d)
        try:verify(d,cnf)
        except (ValueError,AssertionError,KeyError,IndexError,TypeError):result[name]='REJECTED'
        else:raise AssertionError('mutated OWNER-LOCAL accepted '+name)
    check('LOCAL_facet_clausal_mutation',lambda d:next(x for x in d['events'] if x['type']=='LOCAL')['clause'].__setitem__(0,99999))
    check('LOCAL_nonowner_parent',lambda d:next(x for x in d['events'] if x['type']=='LOCAL').update(parent={'ref':555555}))
    check('DIRECT_DEF_facet_in_RES',lambda d:next(x for x in d['events'] if x['type']=='RES')['parents'][0].update(facet=0))
    check('LOCAL_facet_index_corrupt',lambda d:next(x for x in d['events'] if x['type']=='LOCAL').update(facet=3))
    check('wrong_RES_pivot',lambda d:next(x for x in d['events'] if x['type']=='RES').update(pivot=555555))
    check('paid_LOCAL_count_tamper',lambda d:d['counts'].update(local=0))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('raw');p.add_argument('cnf');p.add_argument('--hostile',action='store_true');a=p.parse_args()
    obj=json.load(open(a.raw));x=verify(obj,a.cnf)
    if a.hostile:x['hostile']=hostile(obj,a.cnf)
    print(json.dumps(x,indent=2))
