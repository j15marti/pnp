#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-04: tight local ER2 compilation of AND_k-substituted
Tseitin CNFs F_{G,k} (LSPV-3 ANDK-LIFT-POLYNOMIAL365 family).

Builds F_{G,k}, emits an explicit signed-ER2 refutation (paid fresh AND2
definitions + strict binary Resolution), and checks it with an independent
replay routine. Also checks UNSAT (small cases), the clause-deletion witnesses,
the restriction to Tseitin(G), and the closed-form node counts.
Usage: python3 andk_tight.py  (deterministic; no arguments)
"""
import itertools, json, hashlib, sys

# ---------------- graphs (simple, cubic, 2-vertex-connected) ----------------
def K4(): return 4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
def K33(): return 6, [(a,b) for a in range(3) for b in range(3,6)]
def Q3():
    E=[]
    for u in range(8):
        for b in range(3):
            v=u^(1<<b)
            if u<v: E.append((u,v))
    return 8, E
def Petersen():
    E=[(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)]
    return 10, [tuple(sorted(e)) for e in E]
GRAPHS={'K4':K4,'K33':K33,'Q3':Q3,'Petersen':Petersen}

# ---------------- instance ----------------
def build(G, k):
    h, E = GRAPHS[G]()
    assert all(sum(v in e for e in E)==3 for v in range(h))
    z = {(ei,j): 1+ei*k+j for ei in range(len(E)) for j in range(k)}   # z[e,j], j=0..k-1
    nvar = len(E)*k
    inc = {v:[ei for ei,e in enumerate(E) if v in e] for v in range(h)}
    s = {v:(1 if v==0 else 0) for v in range(h)}
    src = []   # list of (clause, (v,a,jtuple))
    for v in range(h):
        es = inc[v]
        for a in itertools.product((0,1),repeat=3):
            if (a[0]^a[1]^a[2]) == s[v]: continue
            zero = [i for i in range(3) if a[i]==0]
            for jt in itertools.product(range(k),repeat=len(zero)):
                cl=set()
                for idx,i in enumerate(zero): cl.add(z[(es[i],jt[idx])])
                for i in range(3):
                    if a[i]==1:
                        for t in range(k): cl.add(-z[(es[i],t)])
                src.append((frozenset(cl),(v,a,jt)))
    return dict(h=h,E=E,k=k,z=z,nvar=nvar,inc=inc,s=s,src=src)

def m_formula(h,k): return k**3+3*k+(h-1)*(3*k*k+1)

# ---------------- proof producer ----------------
class Proof:
    def __init__(s, nvar): s.lines=[]; s.next=nvar+1; s.idx={}
    def add(s, line, clause):
        if clause in s.idx: return s.idx[clause]
        s.lines.append((line, clause)); s.idx[clause]=len(s.lines)-1; return s.idx[clause]
    def src(s, c): return s.add(('src',), c)
    def define(s, a, b):
        u=s.next; s.next+=1
        s.lines.append((('def',u,a,b), None))
        sl=[frozenset({-u,a}),frozenset({-u,b}),frozenset({u,-a,-b})]
        ids=[]
        for c in sl:
            s.lines.append((('slot',len(s.lines)-1 - (len(ids))), c))
            s.idx.setdefault(c,len(s.lines)-1); ids.append(len(s.lines)-1)
        return u, ids
    def res(s, i, j, p):
        ci, cj = s.lines[i][1], s.lines[j][1]
        r = (ci-{p}) | (cj-{-p})
        return s.add(('res',i,j,p), frozenset(r))
    def clause(s,i): return s.lines[i][1]

def produce(I):
    k, E, z = I['k'], I['E'], I['z']
    P = Proof(I['nvar'])
    g, imp, wide = {}, {}, {}
    for ei in range(len(E)):
        zs=[z[(ei,j)] for j in range(k)]
        # chain t2=z1&z2, t_j=t_{j-1}&z_j
        t, ids = P.define(zs[0], zs[1])
        T=[None,None,t]; Tslots={2:ids}
        for j in range(2,k):
            t, ids = P.define(T[-1], zs[j]); T.append(t); Tslots[j+1]=ids
        gk=T[k]; g[ei]=gk
        # (-t_k v t_i) for i=k-1..2
        down={k: None}
        if k>=3:
            down[k-1]=Tslots[k][0]                      # (-t_k v t_{k-1}) slot
            for i in range(k-2,1,-1):
                down[i]=P.res(down[i+1], Tslots[i+1][0], T[i+1])   # 1 RES each
        # implications (-g v z_j)
        imp[ei]={}
        imp[ei][k-1]=Tslots[k][1]                       # (-t_k v z_k) slot
        for j in range(k-1):                            # j = 0..k-2  (z_1..z_{k-1})
            jj=j+1                                      # 1-based
            host=max(jj,2)
            slot = Tslots[host][1] if jj==host else Tslots[2][0]   # (-t_host v z_jj)
            if host==k: imp[ei][j]=slot
            else: imp[ei][j]=P.res(down[host], slot, T[host])
        # wide clause (g v -z_1 ... -z_k)
        w=Tslots[k][2]
        for i in range(k,2,-1):
            w=P.res(Tslots[i-1][2], w, T[i-1])
        wide[ei]=w
    # blockers: eliminate zero groups FIRST, then convert one-groups
    srcid={c:P.src(c) for c,_ in I['src']}
    blockers={}
    for v in range(I['h']):
        es=I['inc'][v]
        for a in itertools.product((0,1),repeat=3):
            if (a[0]^a[1]^a[2])==I['s'][v]: continue
            zero=[i for i in range(3) if a[i]==0]
            # current: dict index-tuple -> line id
            cur={}
            for c,(vv,aa,jt) in I['src']:
                if vv==v and aa==a: cur[jt]=srcid[c]
            for gi in range(len(zero)-1,-1,-1):   # eliminate last zero group
                e=es[zero[gi]]; nxt={}
                for pre in itertools.product(range(k),repeat=gi):
                    acc=wide[e]
                    for j in range(k):
                        acc=P.res(cur[pre+(j,)], acc, z[(e,j)])
                    nxt[pre]=acc
                cur=nxt
            line=cur[()]
            for i in range(3):
                if a[i]==1:
                    e=es[i]
                    for t in range(k):
                        line=P.res(line, imp[e][t], -z[(e,t)])
            blockers[(v,a)]=line
    return P, g, blockers

def dp_refute(P, clause_ids, order):
    """Davis-Putnam elimination on given clause line ids; returns empty-clause id."""
    pool=set(clause_ids)
    for x in order:
        pos=[i for i in pool if x in P.clause(i)]; neg=[i for i in pool if -x in P.clause(i)]
        rest=pool-set(pos)-set(neg); new=set()
        for i in pos:
            for j in neg:
                r=(P.clause(i)-{x})|(P.clause(j)-{-x})
                if any(-l in r for l in r): continue
                new.add(P.res(i,j,x))
        pool=rest|new
        for i in pool:
            if len(P.clause(i))==0: return i
    raise RuntimeError('no empty clause')

def prune(P, root):
    need=set(); st=[root]
    while st:
        i=st.pop()
        if i in need: continue
        need.add(i); L=P.lines[i][0]
        if L[0]=='res': st+= [L[1],L[2]]
        if L[0]=='slot': st.append(L[1])
    return need

# ---------------- independent checker ----------------
def check(I, lines, keep):
    srcset={c for c,_ in I['src']}
    used=set(range(1,I['nvar']+1)); C={}; nres=ndef=0
    defs_of={}
    for i,(L,c) in enumerate(lines):
        if i not in keep: continue
        if L[0]=='src':
            assert c in srcset, 'unauthenticated source'; C[i]=c
        elif L[0]=='def':
            _,u,a,b=L; assert u not in used and a in used and b in used and a!=b and a>0 and b>0
            used.add(u); ndef+=1; defs_of[i]=(u,a,b)
        elif L[0]=='slot':
            u,a,b=defs_of[L[1]]
            assert c in (frozenset({-u,a}),frozenset({-u,b}),frozenset({u,-a,-b})); C[i]=c
        elif L[0]=='res':
            _,p,q,x=L; assert p<i and q<i and p in C and q in C
            assert x in C[p] and -x in C[q]
            r=(C[p]-{x})|(C[q]-{-x}); assert not any(-l in r for l in r), 'tautology'
            assert r==c; C[i]=c; nres+=1
    return nres, ndef

def brute_unsat(I):
    n=I['nvar']; cls=[c for c,_ in I['src']]
    for bits in range(1<<n):
        if all(any(((bits>>(abs(l)-1))&1)==(l>0) for l in c) for c in cls): return False
    return True

def deletion_witnesses(I):
    """For each source clause, build the LSPV-3 witness and check it falsifies exactly that clause."""
    h,E,k,z=I['h'],I['E'],I['k'],I['z']; ok=0
    import collections
    for c,(v,a,jt) in I['src']:
        # outputs: fix incident edges of v to a, solve parity on G-v by spanning-tree fix
        es=I['inc'][v]; out={es[i]:a[i] for i in range(3)}
        others=[ei for ei in range(len(E)) if ei not in out]
        # solve linear system over GF(2) for other edges: for u!=v, sum = s_u
        rows=[u for u in range(h) if u!=v]
        # gaussian elimination
        var=others; M=[]
        for u in rows:
            row=[1 if u in E[ei] else 0 for ei in var]
            rhs=I['s'][u]^(sum(out[ei] for ei in out if u in E[ei])%2)
            M.append(row+[rhs])
        nv=len(var); r=0; piv=[]
        for col in range(nv):
            pr=next((i for i in range(r,len(M)) if M[i][col]),None)
            if pr is None: continue
            M[r],M[pr]=M[pr],M[r]
            for i in range(len(M)):
                if i!=r and M[i][col]: M[i]=[x^y for x,y in zip(M[i],M[r])]
            piv.append(col); r+=1
        assert all(any(row[:-1]) or row[-1]==0 for row in M), 'inconsistent'
        sol=[0]*nv
        for i,col in enumerate(piv): sol[col]=M[i][-1]
        for i,ei in enumerate(var): out[ei]=sol[i]
        asg={}
        zero_idx={es[i]:jt[n] for n,i in enumerate([i for i in range(3) if a[i]==0])}
        for ei in range(len(E)):
            for t in range(k): asg[z[(ei,t)]]=1
            if out[ei]==0: asg[z[(ei,zero_idx.get(ei,0))]]=0
        fals=[cc for cc,_ in I['src'] if not any((asg[abs(l)]==1)==(l>0) for l in cc)]
        assert fals==[c], (len(fals))
        ok+=1
    return ok

def restriction_is_tseitin(I):
    """Set z[e,j]=1 for j>=1: residual CNF equals Tseitin(G,s) on z[e,0]."""
    k,z,E=I['k'],I['z'],I['E']; res=set()
    for c,_ in I['src']:
        if any(l>0 and (abs(l)-1)%k!=0 for l in c): continue   # satisfied
        res.add(frozenset(l for l in c if (abs(l)-1)%k==0))
    ts=set()
    for v in range(I['h']):
        es=I['inc'][v]
        for a in itertools.product((0,1),repeat=3):
            if (a[0]^a[1]^a[2])==I['s'][v]: continue
            ts.add(frozenset(z[(es[i],0)] if a[i]==0 else -z[(es[i],0)] for i in range(3)))
    return res==ts

def formulas(h,k):
    chain=(3*h//2)*(3*k-6)
    blk=(k**3+k*k+10*k)+(h-1)*(3*k*k+9*k)
    return chain, blk, (3*h//2)*(k-1)

def hostile_controls():
    """Corrupt a valid K4,k=3 proof in several ways; the checker must reject each."""
    I=build('K4',3); P,g,bl=produce(I)
    root=dp_refute(P,list(bl.values()),[g[e] for e in range(len(I['E']))])
    keep=prune(P,root)
    for i in list(keep):
        if P.lines[i][0][0]=='slot': keep.add(P.lines[i][0][1])
    import copy
    rejected=0
    res_ids=[i for i in sorted(keep) if P.lines[i][0][0]=='res']
    src_ids=[i for i in sorted(keep) if P.lines[i][0][0]=='src']
    def_ids=[i for i in sorted(keep) if P.lines[i][0][0]=='def']
    muts=[]
    L=list(P.lines); i=res_ids[5]; (t,a,b,p),c=L[i]; L[i]=((t,a,b,-p),c); muts.append(L)          # wrong pivot sign
    L=list(P.lines); i=res_ids[7]; L[i]=(L[i][0], L[i][1]|{1}); muts.append(L)                       # wrong resolvent
    L=list(P.lines); i=src_ids[3]; L[i]=(L[i][0], frozenset(set(L[i][1])-{max(L[i][1])})); muts.append(L)  # forged source
    L=list(P.lines); i=def_ids[2]; (t,u,a,b),c=L[i]; L[i]=((t,1,a,b),c); muts.append(L)              # non-fresh definition
    L=list(P.lines); i=res_ids[-1]; (t,a,b,p),c=L[i]; L[i]=((t,i+1,b,p),c); muts.append(L)          # forward reference
    for M in muts:
        try: check(I,M,keep)
        except (AssertionError,KeyError,TypeError): rejected+=1
    return rejected, len(muts)

if __name__=='__main__':
    print('hostile controls rejected/total', hostile_controls())
    out=[]
    for G in ['K4','K33','Q3','Petersen']:
        for k in ([2,3,4,5,6] if G=='K4' else [2,3,4]):
            I=build(G,k); h=I['h']; m=len(I['src'])
            assert m==m_formula(h,k)
            P,g,bl=produce(I)
            # local counts
            nl_before=len(P.lines)
            # global: pure RES DP refutation of the 4h blockers (Tseitin on g)
            order=[g[ei] for ei in range(len(I['E']))]
            root=dp_refute(P, list(bl.values()), order)
            keep=prune(P,root)
            # include def lines for kept slots
            for i in list(keep):
                if P.lines[i][0][0]=='slot': keep.add(P.lines[i][0][1])
            nres,ndef=check(I,P.lines,keep)
            # local-only count: RES lines that are ancestors of blockers
            lk=set()
            for b in bl.values(): lk|=prune(P,b)
            nres_local=sum(1 for i in lk if P.lines[i][0][0]=='res')
            chain,blk,dd=formulas(h,k)
            srcs_used=sum(1 for i in keep if P.lines[i][0][0]=='src')
            row=dict(graph=G,h=h,k=k,m=m,sources_used=srcs_used,DEF=ndef,RES_local=nres_local,
                     RES_local_formula=chain+blk,RES_total=nres,RES_global=nres-nres_local,
                     W_upper=nres+ndef,W_lower=m-1,
                     restriction_is_tseitin=restriction_is_tseitin(I))
            assert ndef==dd and nres_local==chain+blk and srcs_used==m
            if G in ('K4','K33','Q3') and k<=3:
                row['deletion_witnesses_ok']=deletion_witnesses(I)
            if G=='K4' and k<=3: row['brute_unsat']=brute_unsat(I)
            out.append(row); print(json.dumps(row)); sys.stdout.flush()
    js=json.dumps(out,indent=1,sort_keys=True)
    open('andk_tight_results.json','w').write(js+'\n')
    print('SHA256', hashlib.sha256((js+'\n').encode()).hexdigest())
