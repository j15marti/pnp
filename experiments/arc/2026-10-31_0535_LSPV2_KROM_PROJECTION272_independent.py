#!/usr/bin/env python3
"""Independent finite verifier for KROM-RESOLUTION-PROJECTION272; no producer imports."""
import json,sys,itertools,collections,hashlib

def normalized(clause):
    v=set(clause)
    assert not any(-x in v for x in v),'tautological clause in canonical projection'
    return tuple(sorted(v,key=lambda x:(abs(x),x<0)))

def satisfied(c,assignment):
    return any(assignment[abs(l)]==(l>0) for l in c)

def exact_solver(clauses,n):
    stack=[{}];nodes=0
    while stack:
        a=stack.pop();nodes+=1
        while True:
            progress=False;incomplete=[];bad=False
            for c in clauses:
                if any(abs(l) in a and a[abs(l)]==(l>0) for l in c):continue
                openl=[l for l in c if abs(l) not in a]
                if not openl:bad=True;break
                if len(openl)==1:
                    v=abs(openl[0]);z=openl[0]>0
                    if v in a and a[v]!=z:bad=True;break
                    if v not in a:a[v]=z;progress=True
                incomplete.append(openl)
            if bad:break
            if not progress:break
        if bad:continue
        if not incomplete:return True,nodes
        choice=min(incomplete,key=len)
        v=abs(choice[0])
        for z in (True,False):
            b=a.copy();b[v]=z;stack.append(b)
    return False,nodes

def verify_one(row):
    F=row['proof']['source'];G=row['child'];proof=row['proof']
    n=row['n'];B=proof['boundary'];P=proof['private'];assert not set(B)&set(P)
    assert set(B)|set(P)=={abs(l) for c in F for l in c}
    assert all(any(abs(l) in B for l in c) for c in F if len(c)>2)
    nodes=proof['nodes'];assert len(nodes)>=len(F)
    values=[];resolve_count=0
    for j,node in enumerate(nodes):
        assert node['id']==j
        c=normalized(node['clause'])
        if j<len(F):
            assert node['kind']=='source' and c==normalized(F[j]);values.append(c)
        else:
            assert node['kind']=='resolve';pa,pb=node['parents'];p=node['pivot']
            assert pa<j and pb<j and p in values[pa] and -p in values[pb]
            target=normalized([x for x in values[pa] if x!=p]+[x for x in values[pb] if x!=-p])
            assert c==target,'resolution step incorrect'
            values.append(c);resolve_count+=1
    if row['label']=='UNSAT':
        root=proof.get('refutation_root')
        assert isinstance(root,int) and 0<=root<len(values)
        assert values[root]==(),'missing or invalid original-source resolution refutation'
        assert proof['refutation_stage'] in ('projected_source','original_source')
    else:
        assert proof.get('refutation_root') is None
    # Every saved pivot stage is a complete Davis-Putnam stage, verified without trusting the producer.
    working={normalized(c) for c in F if len(c)<=2}
    for item in proof['histories']:
        p=item['pivot'];assert p in P
        expected_pos={c for c in working if p in c}
        expected_neg={c for c in working if -p in c}
        assert expected_pos=={normalized(c) for c in item['positive']}
        assert expected_neg=={normalized(c) for c in item['negative']}
        rest={c for c in working if p not in c and -p not in c}
        for c in expected_pos:
            for d in expected_neg:
                resolvent=set(c)-{p}|(set(d)-{-p})
                if not any(-x in resolvent for x in resolvent):rest.add(normalized(resolvent))
        working=rest
    assert all(not any(abs(l) in P for l in c) for c in working)
    expected={normalized(c) for c in F if len(c)>2}|working
    actual={normalized(c) for c in proof['source_final_clauses']}
    assert actual==expected
    for c,idx in zip(proof['source_final_clauses'],proof['proof_ids']):
        assert values[idx]==normalized(c),'output lacks source proof'
    map_id={v:i+1 for i,v in enumerate(B)}
    expected_G={normalized([map_id[abs(l)]*(1 if l>0 else -1) for l in c]) for c in expected}
    assert expected_G=={normalized(c) for c in G}
    cn=len(B)
    valid_child,nn=exact_solver(G,cn)
    assert valid_child==(row['label']=='SAT')
    assert valid_child==(row['source_witness'] is not None)
    if valid_child:
        w={int(k):v for k,v in row['source_witness'].items()}
        assert all(satisfied(c,w) for c in F)
        q={int(k):v for k,v in row['child_witness'].items()}
        assert all(satisfied(c,q) for c in G)
        assert all(w[old]==q[new] for old,new in map_id.items())
    # Independent exhaustive cofactor checks for bounded original-variable instances.
    count_profile=0
    if n<=11:
        for x in itertools.product((False,True),repeat=cn):
            bv={B[j]:x[j] for j in range(cn)}
            projection=False
            for p in itertools.product((False,True),repeat=len(P)):
                a=bv.copy();a.update({P[j]:p[j] for j in range(len(P))})
                if all(satisfied(c,a) for c in F):projection=True;break
            g={j+1:x[j] for j in range(cn)}
            assert projection==all(satisfied(c,g) for c in G)
            count_profile+=1
    # Test physical indexed output, without importing the producer's accessor.
    expected_text=f'p cnf {cn} {len(G)}\n'+''.join(' '.join(map(str,c))+(' ' if c else '')+'0\n' for c in G)
    assert expected_text==row['child_serialization']
    # Source S/U pairs are checked against an independent sign requirement map.
    for r in row.get('audit',{}).get('occurrences',[]):
        j=r['clause'];sgn=r['sign'];v=r['variable']
        assert sgn*v in F[j] and r['S']==(sgn>0) and r['U']==(sgn<0)
        assert r['S']==r['invert_U'] and r['U']==r['invert_S']
    for rec in row.get('audit',{}).get('pairs',[]):
        c,d=F[rec['j']],F[rec['k']]
        for key,declared in rec['modes'].items():
            want={};good=True
            for clause,symbol in ((c,key[0]),(d,key[1])):
                for l in clause:
                    v=abs(l);val=(l>0) if symbol=='S' else (l<0)
                    if v in want and want[v]!=val:good=False
                    want[v]=val
            assert good==declared
    for title,z in row.get('audit',{}).get('endpoint',{}).items():
        a={i: title=='ones' for i in range(1,n+1)}
        assert z==[sum(a[abs(l)]==(l>0) for l in c) for c in F]
    a={i:False for i in range(1,n+1)}
    for t in row.get('audit',{}).get('flips',[]):
        old=[sum(a[abs(l)]==(l>0) for l in c) for c in F]
        assert old==t['before'];a[t['flip']]=not a[t['flip']]
        assert [sum(a[abs(l)]==(l>0) for l in c) for c in F]==t['after']
    return resolve_count,count_profile,nn

def main():
    path=sys.argv[1] if len(sys.argv)>1 else '/mnt/data/lspv2_272/raw272.json'
    blob=open(path,'rb').read();D=json.loads(blob)
    counts=collections.Counter()
    for r in D['cases']:
        p,q,n=verify_one(r);counts['cases']+=1;counts['resolution_nodes']+=p
        counts['independent_boundary_profiles']+=q;counts['child_DPLL_nodes']+=n
    # Mutation resistance: an authenticated proof node cannot lie about the pivot.
    copied=json.loads(json.dumps(D['cases'][0]));bad=next(x for x in copied['proof']['nodes'] if x['kind']=='resolve')
    bad['pivot']+=1000
    rejected=False
    try:verify_one(copied)
    except (AssertionError,KeyError,ValueError):rejected=True
    assert rejected;counts['corrupt_resolution_rejected']=1
    print(json.dumps({'source_sha256':hashlib.sha256(blob).hexdigest(),'result':'PASS', 'counts':dict(counts)},sort_keys=True))
if __name__=='__main__':main()