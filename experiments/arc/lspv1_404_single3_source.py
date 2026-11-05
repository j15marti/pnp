#!/usr/bin/env python3
"""LSPV-1/404 exact 3-CNF single-clause source-retention checks; Python 3 stdlib.
Symbolic Pi_1 completeness is proved in report, NOT by this finite toy threshold.
Run: python3 lspv1_404_single3_source.py [out.json]
"""
import itertools, json, sys

def block(i):
    a,b,c=3*i-2,3*i-1,3*i
    return [tuple([a, s*b, t*c]) for s,t in itertools.product((1,-1),repeat=2)]
def source(n):return [cl for i in range(1,n+1) for cl in block(i)]
def append():return (-1,-4,-7)
def lit(l, assignment):return assignment[abs(l)] == (l>0)
def sat(formula, assignment):return all(any(lit(l,assignment) for l in cl) for cl in formula)
def witness(n, deletion):
    a={v:False for v in range(1,3*n+1)}
    for j in range(1,n+1):a[3*j-2]=True
    if deletion==12:return a
    i=deletion//4+1; sig=deletion%4
    cl=block(i)[sig]
    a[3*i-2]=False
    a[3*i-1]=cl[1]<0
    a[3*i]=cl[2]<0
    return a

def resolve(c1,c2,p):
    if p not in c1 or -p not in c2: raise ValueError('invalid pivot')
    out=set(c1)-{p};out|=set(c2)-{-p}
    if any(-v in out for v in out): raise ValueError('tautological resolvent')
    return tuple(sorted(out,key=lambda z:(abs(z),z<0)))

def proof_for(n):
    orig=source(n)+[append()]; nodes=[]
    db={f'S{j}':c for j,c in enumerate(orig)}
    for i in range(1,4):
        j=4*(i-1);a,b,c=3*i-2,3*i-1,3*i
        for left,right,piv in [(f'S{j}',f'S{j+1}',c), (f'S{j+2}',f'S{j+3}',c), (f'R{len(nodes)}',f'R{len(nodes)+1}',b)]:
            r=resolve(db[left],db[right],piv)
            name=f'R{len(nodes)}';db[name]=r;nodes.append({'left':left,'right':right,'pivot':piv,'out':r})
    prev=f'S{4*n}'
    for i in range(1,4):
        parent=f'R{3*i-1}'
        p=-(3*i-2)
        r=resolve(db[prev],db[parent],p)
        name=f'R{len(nodes)}';db[name]=r;nodes.append({'left':prev,'right':parent,'pivot':p,'out':r})
        prev=name
    assert len(nodes)==12 and db[prev]==()
    return nodes

def strict(s):
    lines=s.splitlines()
    if not lines or not lines[0].startswith('p cnf '):raise ValueError
    p=lines[0].split()
    if len(p)!=4:raise ValueError
    try:n,m=int(p[2]),int(p[3])
    except ValueError:raise ValueError
    if n<1 or m<1 or len(lines)!=m+1:raise ValueError
    for line in lines[1:]:
        t=line.split()
        if len(t)!=4 or t[-1]!='0':raise ValueError
        try:c=[int(x) for x in t[:3]]
        except ValueError:raise ValueError
        if any(v==0 or abs(v)>n for v in c) or len({abs(v) for v in c})!=3:raise ValueError
    return True

def main():
    rows=[];checks=0
    for n in range(3,10):
        F=source(n);G=F+[append()]
        assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in G);checks+=1
        true_assignment={j:(j%3==1) for j in range(1,3*n+1)}
        assert sat(F,true_assignment) and not sat(G,true_assignment);checks+=2
        for d in range(13):
            deleted=G[:d]+G[d+1:] if d<12 else G[:-1]
            a=witness(n,d)
            assert sat(deleted,a) and not sat(G,a);checks+=2
        proof=proof_for(n)
        assert len(proof)==12 and proof[-1]['out']==();checks+=2
        for h in (None,1,3,5,12):
            for bound in (n,n-1):
                enabled=h is not None and h<=bound
                out=G if enabled else F
                assert sat(out,true_assignment)==(not enabled);checks+=1
                rows.append({'n':n,'halt_threshold':h,'test_steps':bound,'changed':enabled,'num_source_clauses':len(F),'num_output_clauses':len(out),'source_sat':True,'output_sat':not enabled})
        if n<=5:
            sm=gm=0
            for bits in itertools.product((False,True),repeat=3*n):
                a={i+1:bits[i] for i in range(3*n)}
                sm+=sat(F,a);gm+=sat(G,a);checks+=2
            assert sm==4**n and gm==0;checks+=2
        else:sm=4**n;gm=0
        rows.append({'n':n,'kind':'core','original_satisfying_assignments':sm,'triggered_satisfying_assignments':gm,'indispensable_source_clauses':13,'certified_mixed_paid_nodes':12,'source_clauses':len(F)})
    for bad in ('','p cnf nope','p cnf 3 1\n1 2 3','p cnf 3 1\n1 2 4 0\n','p cnf 3 1\n1 2 0\n','p cnf 3 2\n1 2 3 0\n'):
        try:strict(bad)
        except ValueError:checks+=1
        else:raise AssertionError('malformed accepted')
    try:resolve((1,2),(1,-2),1)
    except ValueError:checks+=1
    else:raise AssertionError('bad pivot accepted')
    data={'theorem':'LSPV1 SINGLE3 SOURCE PRESERVATION404','classification':'finite checks only; Pi1 proof symbolic','seed':None,'runs':rows,'checks':checks,'malformed_rejected':6,'corrupted_pivot_rejected':1,'proof_system':'R_mix341 unchanged, strict RES subset, unit per derived binary step'}
    with open(sys.argv[1] if len(sys.argv)>1 else 'lspv1_404_raw.json','w') as f:json.dump(data,f,indent=2,sort_keys=True)
    print(json.dumps({'checks':checks,'rows':len(rows),'n_range':[3,9],'malformed':6,'bad_pivot':1}))
if __name__=='__main__':main()
