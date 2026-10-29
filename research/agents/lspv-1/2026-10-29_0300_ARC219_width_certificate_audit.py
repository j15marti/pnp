#!/usr/bin/env python3
"""ARC219: fully charged width-parameterized source resolution and guarded proof lift.
No general SAT algorithm: arbitrary-width runs may be exponential.
No treewidth FPT discovery implemented: supplied elimination order charged/verified.
Reproducible computational checks are independent of the mathematical proof.
"""
import itertools, json, random, hashlib, sys
from pathlib import Path
from collections import defaultdict

SEED=21920261029
rng=random.Random(SEED)
ROOT=Path(__file__).resolve().parent
STATS=defaultdict(int)


def canon(c):
    s=set(c)
    if 0 in s or any(-u in s for u in s):
        raise ValueError('tautology or zero')
    return tuple(sorted(s,key=lambda z:(abs(z),z<0)))


def resolvent(pos,neg,pivot):
    assert pivot in pos and -pivot in neg
    rem=set(pos)-{pivot}
    rem|=set(neg)-{-pivot}
    if any(-x in rem for x in rem):return None
    return canon(rem)


def value(lit,assignment):
    return assignment[abs(lit)]==(1 if lit>0 else 0)


def sat_bruteforce(source,n):
    for bits in itertools.product((0,1),repeat=n):
        a={i+1:bits[i] for i in range(n)}
        if all(any(value(z,a) for z in c) for c in source):return a
    return None


class Proof:
    def __init__(self):self.rows=[]
    def ax(self,c,src):
        i=len(self.rows);self.rows.append({'kind':'axiom','clause':list(canon(c)),'owner':src});return i
    def res(self,a,b,pivot):
        C=resolvent(tuple(self.rows[a]['clause']),tuple(self.rows[b]['clause']),pivot)
        assert C is not None
        i=len(self.rows);self.rows.append({'kind':'res','clause':list(C),'a':a,'b':b,'pivot':pivot});return i


def verify_source_proof(source,proof,require_unsat=False):
    for i,r in enumerate(proof.rows):
        try:C=canon(r['clause'])
        except ValueError:return False
        if tuple(r['clause'])!=C:return False
        if r['kind']=='axiom':
            j=r.get('owner')
            if not isinstance(j,int) or not 0<=j<len(source) or C!=canon(source[j]):return False
        elif r['kind']=='res':
            a,b,p=r['a'],r['b'],r['pivot']
            if type(a)!=int or type(b)!=int or not 0<=a<i or not 0<=b<i:return False
            if p not in proof.rows[a]['clause'] or -p not in proof.rows[b]['clause']:return False
            if resolvent(tuple(proof.rows[a]['clause']),tuple(proof.rows[b]['clause']),p)!=C:return False
        else:return False
    return bool(proof.rows) and (not require_unsat or proof.rows[-1]['clause']==[])


def primal(n,clauses):
    E={i:set() for i in range(1,n+1)}
    for c in clauses:
        for a,b in itertools.combinations({abs(l) for l in c},2):
            E[a].add(b);E[b].add(a)
    return E


def eliminate_graph(n,source,order):
    assert sorted(order)==list(range(1,n+1))
    G=primal(n,source)
    bags={};parents={};w=0
    position={v:i for i,v in enumerate(order)}
    for v in order:
        ne=sorted(G[v],key=lambda x:position[x]);w=max(w,len(ne))
        bags[v]={v,*ne};parents[v]=ne[0] if ne else None
        for x,y in itertools.combinations(ne,2):
            G[x].add(y);G[y].add(x)
        for x in ne:G[x].remove(v)
        del G[v]
    return w,bags,parents


def dp_refute_or_witness(source,n,order):
    width,bags,parents=eliminate_graph(n,source,order)
    proof=Proof()
    active={}
    for j,c in enumerate(source):
        c=canon(c)
        idx=proof.ax(c,j)
        if c not in active:active[c]=idx
    history=[];maxactive=len(active);pairs=0;derivations=0
    if () in active:
        # Source may already contain an empty axiom. Re-emit that indexed
        # original axiom last so the verified proof terminates in [].
        j=next(j for j,c in enumerate(source) if not c)
        proof.ax((),j)
        assert verify_source_proof(source,proof,True)
        return {'sat':False,'proof':proof,'width':width,'pairs':0,'derived':0,'max_active':maxactive,'bags':bags,'parents':parents}
    for v in order:
        p=[(c,i) for c,i in active.items() if v in c]
        neg=[(c,i) for c,i in active.items() if -v in c]
        history.append((v,[c for c,_ in p],[c for c,_ in neg]))
        nxt={c:i for c,i in active.items() if v not in c and -v not in c}
        for pc,pid in p:
            for nc,nid in neg:
                pairs+=1
                C=resolvent(pc,nc,v)
                if C is None:continue
                if C not in nxt:
                    idx=proof.res(pid,nid,v)
                    assert tuple(proof.rows[idx]['clause'])==C
                    nxt[C]=idx;derivations+=1
                    if C==():
                        assert verify_source_proof(source,proof,True)
                        return {'sat':False,'proof':proof,'width':width,'pairs':pairs,'derived':derivations,'max_active':max(maxactive,len(nxt)),'bags':bags,'parents':parents}
        active=nxt;maxactive=max(maxactive,len(active))
    assert () not in active
    assignment={}
    for v,p,neg in reversed(history):
        req1=any(not any(value(x,assignment) for x in c if x!=v) for c in p)
        req0=any(not any(value(x,assignment) for x in c if x!=-v) for c in neg)
        assert not (req1 and req0)
        assignment[v]=1 if req1 else 0
    assert all(any(value(z,assignment) for z in c) for c in source)
    assert verify_source_proof(source,proof,False)
    return {'sat':True,'witness':assignment,'proof':proof,'width':width,'pairs':pairs,'derived':derivations,'max_active':maxactive,'bags':bags,'parents':parents}


def parity3_even(a,b,c):
    return [canon((a if i==0 else -a,b if j==0 else -b,c if k==0 else -c))
            for i,j,k in itertools.product((0,1),repeat=3) if (i^j^k)==1]


def guarded_pinned(source,n):
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in source)
    pr=Proof();g=n+1;pin=pr.ax((-g,),('pin',))
    child=[]
    for j,c in enumerate(source):
        y1,y2,y3,t=[n+2+4*j+i for i in range(4)]
        bins=[pr.ax((ell,y),('binary',j,k)) for k,(ell,y) in enumerate(zip(c,(y1,y2,y3)))]
        xa=[pr.ax(u,('xor-a',j,k)) for k,u in enumerate(parity3_even(y1,y2,t))]
        xb=[pr.ax(u,('xor-b',j,k)) for k,u in enumerate(parity3_even(t,y3,g))]
        child.append((c,(y1,y2,y3,t),bins,xa,xb))
    return pr,g,pin,child


def guard_lift(source,n,source_proof):
    p,g,pin,children=guarded_pinned(source,n)
    mapping={}
    for j,(C,(y1,y2,y3,t),bins,xa,xb) in enumerate(children):
        def find(ids,c):
            matches=[i for i in ids if tuple(p.rows[i]['clause'])==canon(c)]
            assert len(matches)==1
            return matches[0]
        z=p.res(find(xb,(-y3,t,g)),pin,g)
        z=p.res(z,find(xa,(-y1,-y2,-t)),t)
        z=p.res(bins[2],z,y3)
        z=p.res(bins[1],z,y2)
        z=p.res(bins[0],z,y1)
        assert tuple(p.rows[z]['clause'])==canon(C)
        mapping[j]=z
    for idx,row in enumerate(source_proof.rows):
        if row['kind']=='axiom':mapping[idx]=mapping[row['owner']]
        else:
            mapping[idx]=p.res(mapping[row['a']],mapping[row['b']],row['pivot'])
            assert p.rows[mapping[idx]]['clause']==row['clause']
    assert p.rows[-1]['clause']==[]
    return p


def verify_guard_proof(source,n,p,need_unsat=True):
    valid=set();g=n+1
    valid.add((canon((-g,)),('pin',)))
    for j,c in enumerate(source):
        y1,y2,y3,t=(n+2+4*j+i for i in range(4))
        for k,(ell,y) in enumerate(zip(c,(y1,y2,y3))):valid.add((canon((ell,y)),('binary',j,k)))
        for k,C in enumerate(parity3_even(y1,y2,t)):valid.add((C,('xor-a',j,k)))
        for k,C in enumerate(parity3_even(t,y3,g)):valid.add((C,('xor-b',j,k)))
    for i,row in enumerate(p.rows):
        try:C=canon(row['clause'])
        except ValueError:return False
        if C!=tuple(row['clause']):return False
        if row['kind']=='axiom':
            if (C,tuple(row['owner'])) not in valid:return False
        elif row['kind']=='res':
            a,b,t=row['a'],row['b'],row['pivot']
            if type(a)!=int or type(b)!=int or not 0<=a<i or not 0<=b<i:return False
            if t not in p.rows[a]['clause'] or -t not in p.rows[b]['clause']:return False
            if resolvent(tuple(p.rows[a]['clause']),tuple(p.rows[b]['clause']),t)!=C:return False
        else:return False
    return not need_unsat or p.rows[-1]['clause']==[]


def guard_primal(n,source):
    allvars=n+1+4*len(source)
    G={v:set() for v in range(1,allvars+1)};g=n+1
    def clique(xs):
        for a,b in itertools.combinations(xs,2):G[a].add(b);G[b].add(a)
    for j,c in enumerate(source):
        ys=[n+2+4*j+i for i in range(4)]
        for ell,y in zip(c,ys[:3]):clique((abs(ell),y))
        clique((ys[0],ys[1],ys[3]))
        clique((ys[3],ys[2],g))
    return G


def certificate_tree(source,n,order):
    w,original,parent=eliminate_graph(n,source,order)
    bags=[set()]+[original[v]|{n+1} for v in order]
    edges=[];position={v:i+1 for i,v in enumerate(order)}
    for v in order:edges.append((position[v],position[parent[v]] if parent[v] is not None else 0))
    g=n+1;bags[0]={g}
    for j,c in enumerate(source):
        assert len(c)==3 and len({abs(z) for z in c})==3
        a,b,d=[abs(z) for z in c]
        anchors=[i for i,B in enumerate(bags) if {a,b,d}.issubset(B)]
        assert anchors
        y1,y2,y3,t=[n+2+4*j+i for i in range(4)]
        newbags=[{a,b,d,g,y1},{b,d,g,y1,y2},{d,g,y1,y2,t},
                 {d,g,y2,t,y3},{d,g,t,y3}]
        previous=anchors[0]
        for B in newbags:
            idx=len(bags);bags.append(B);edges.append((previous,idx));previous=idx
    return (w,bags,edges)


def verify_decomposition(G,bags,edges):
    if len(edges)!=len(bags)-1:return False
    adj={i:set() for i in range(len(bags))}
    for a,b in edges:
        if a==b or a not in adj or b not in adj:return False
        adj[a].add(b);adj[b].add(a)
    seen={0};todo=[0]
    while todo:
        a=todo.pop()
        for b in adj[a]-seen:seen.add(b);todo.append(b)
    if len(seen)!=len(bags):return False
    for v,nb in G.items():
        containing={i for i,B in enumerate(bags) if v in B}
        if not containing:return False
        start=min(containing);reached={start};todo=[start]
        while todo:
            a=todo.pop()
            for b in (adj[a]&containing)-reached:reached.add(b);todo.append(b)
        if reached!=containing:return False
        for u in nb:
            if u<v:continue
            if not any(u in B and v in B for B in bags):return False
    return True


def guard_minor_equals_source(source,n):
    G=guard_primal(n,source)
    def contract(a,b):
        assert b in G[a]
        for x in list(G[b]):
            G[x].discard(b)
            if x!=a:G[x].add(a);G[a].add(x)
        G[a].discard(a);G[a].discard(b);del G[b]
    for j,c in enumerate(source):
        a,b,d=[abs(z) for z in c]
        y1,y2,y3,t=[n+2+4*j+i for i in range(4)]
        contract(a,y1);contract(b,y2);contract(d,y3);contract(d,t)
    g=n+1
    for x in list(G[g]):G[x].discard(g)
    del G[g]
    return G==primal(n,source)


def test_case(source,n,order,guarded=True):
    out=dp_refute_or_witness(source,n,order)
    ref=sat_bruteforce(source,n)
    assert out['sat']==(ref is not None)
    width=out['width'];assert out['derived']<=n*3**width
    assert out['pairs']<=n*9**width
    if out['sat']:
        assert all(any(value(z,out['witness']) for z in c) for c in source)
        STATS['sat_cases']+=1
    else:
        assert verify_source_proof(source,out['proof'],True)
        STATS['unsat_cases']+=1
    STATS['cases']+=1
    STATS['derived_total']+=out['derived']
    STATS['pairs_total']+=out['pairs']
    STATS['source_rows_total']+=len(out['proof'].rows)
    STATS['max_width']=max(width,STATS['max_width'])
    if guarded:
        w,bags,edges=certificate_tree(source,n,order)
        G=guard_primal(n,source)
        assert verify_decomposition(G,bags,edges)
        maxbag=max(len(B) for B in bags)
        assert maxbag-1<=max(w+1,4)
        assert guard_minor_equals_source(source,n)
        STATS['guard_decompositions']+=1
        STATS['guard_minor_controls']+=1
        if not out['sat']:
            lifted=guard_lift(source,n,out['proof'])
            assert verify_guard_proof(source,n,lifted)
            assert len(lifted.rows)==11*len(source)+1+5*len(source)+out['derived']
            STATS['guard_proof_rows']+=len(lifted.rows)
            STATS['guard_proof_checks']+=1
            return out,lifted
    return out,None


def run():
    src=[tuple((i+1) if (mask>>i)&1 else -(i+1) for i in range(3)) for mask in range(8)]
    x,cert=test_case(src,3,[1,2,3]);assert not x['sat']
    p=Proof();p.rows=json.loads(json.dumps(x['proof'].rows))
    t=next(i for i,r in enumerate(p.rows) if r['kind']=='res')
    p.rows[t]['pivot']=99;assert not verify_source_proof(src,p,True);STATS['corrupt_reject']+=1
    p=Proof();p.rows=json.loads(json.dumps(x['proof'].rows))
    p.rows[0]['owner']=7
    assert not verify_source_proof(src,p,True);STATS['corrupt_reject']+=1
    for n in (4,5,6,7,8,9,10):
        for j in range(12):
            cl=[]
            for a in range(1,n-1):
                for _ in range(1+(j%3==0)):
                    c=tuple(v if rng.randrange(2) else -v for v in (a,a+1,a+2))
                    cl.append(c)
            if j%4==0:cl=src+cl
            if j%5==0:cl=list(reversed(cl))
            out,_=test_case(cl,n,list(range(1,n+1)))
            if j%6==0:
                order=list(range(1,n+1));rng.shuffle(order)
                test_case(cl,n,order)
    for k in range(1,4):
        n=3*k
        allsrc=[]
        for j in range(k):
            allsrc.extend(tuple((i+1+3*j) if (mask>>i)&1 else -(i+1+3*j)
                            for i in range(3)) for mask in range(8))
        test_case(allsrc,n,list(range(1,n+1)))
    n=9
    cl=[(1,i,i+1) for i in range(2,n)]
    good=dp_refute_or_witness(cl,n,list(range(2,n+1))+[1])
    bad=dp_refute_or_witness(cl,n,list(range(1,n+1)))
    assert bad['width']>=good['width']+3
    STATS['order_bad_width']=bad['width'];STATS['order_good_width']=good['width']
    summary={k:int(v) for k,v in sorted(STATS.items())}
    summary['seed']=SEED
    summary['all8_source_proof_sha256']=hashlib.sha256(json.dumps(x['proof'].rows,sort_keys=True).encode()).hexdigest()
    summary['archive_original_sha256']='05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca'
    (ROOT/'ARC219_width_certificate_raw.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    (ROOT/'ARC219_eight_clause_source_resolution.json').write_text(json.dumps(x['proof'].rows,indent=2)+'\n')
    (ROOT/'ARC219_eight_clause_guarded_resolution.json').write_text(json.dumps(cert.rows,indent=2)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':run()
