#!/usr/bin/env python3
"""SOURCE-SUPPORT-PRIVATE-WITNESS126: exact independent finite verifier.
Run: python3 this_file.py. No dependencies, no timing/lower-bound claims.
"""
from collections import Counter
from functools import lru_cache
import json

W='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;
5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;
-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;
2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W1=tuple(tuple(map(int,c.split())) for c in W.replace('\n','').split(';'))
def tseitin(n,edges,charges):
    inc=[[] for _ in range(n)]
    for k,(u,v) in enumerate(edges):inc[u].append(k+1);inc[v].append(k+1)
    assert all(len(e)==3 for e in inc)
    return tuple(tuple(x if ((mask>>j)&1)==0 else -x for j,x in enumerate(inc[v]))
      for v in range(n) for mask in range(8)
      if ((mask&1)^((mask>>1)&1)^((mask>>2)&1))!=charges[v])
def supports(F,n):
    priv={};models=0
    for a in range(1<<n):
        bad=[k for k,c in enumerate(F) if all(((a>>(abs(x)-1))&1)!=int(x>0) for x in c)]
        if not bad:models+=1
        if len(bad)==1:priv.setdefault(bad[0],a)
    return priv,models
def serialize(F,n):
    s='p cnf %d %d\n'%(n,len(F))+''.join(' '.join(map(str,c))+' 0\n' for c in F)
    lines=s.strip().splitlines(); h=lines.pop(0).split()
    assert h==['p','cnf',str(n),str(len(F))]
    reread=tuple(tuple(map(int,l.split()[:-1])) for l in lines)
    assert reread==F and all(l.split()[-1]=='0' for l in lines)
    return len(s)
def optimal(F,n):
    @lru_cache(None)
    def rec(s):
        for i,c in enumerate(F):
            if all(s[abs(x)-1]>=0 and s[abs(x)-1]!=int(x>0) for x in c):
                return 1,0,('leaf',i)
        opts=[]
        for i,x in enumerate(s):
            if x<0:
                z=list(s);z[i]=0; L=rec(tuple(z))
                z[i]=1;R=rec(tuple(z))
                opts.append((L[0]+R[0],1+max(L[1],R[1]),('node',i,L[2],R[2])))
        assert opts,'would be satisfiable'
        return min(opts,key=lambda a:(a[0],a[1]))
    ans=rec((-1,)*n);return ans,rec.cache_info().currsize
def check_tree(F,t,n):
    def recur(t,s):
        if t[0]=='leaf':
            k=t[1]
            return 0<=k<len(F) and all(s[abs(x)-1]>=0 and s[abs(x)-1]!=int(x>0) for x in F[k])
        if t[0]!='node' or not 0<=t[1]<n or s[t[1]]>=0:return False
        z=list(s);z[t[1]]=0;a=recur(t[2],tuple(z));z[t[1]]=1;b=recur(t[3],tuple(z))
        return a and b
    return recur(t,(-1,)*n)
def run():
    cases={
      'odd_K4':(tseitin(4,[(i,j) for i in range(4) for j in range(i+1,4)],[1,0,0,0]),6,16),
      'odd_K33':(tseitin(6,[(i,j) for i in range(3) for j in range(3,6)],[1,0,0,0,0,0]),9,24),
      'exact_2P2N_W1':(W1,15,20)}
    recs={}
    for name,(F,n,m) in cases.items():
        p,count=supports(F,n)
        assert count==0 and len(F)==len(p)==m and len(set(p.values()))==m
        assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
        assert len(set(F))==len(F)
        root=serialize(F,n);one=serialize(F[1:],n);two=serialize(F[2:],n)
        assert supports(F[1:],n)[1]>0 and supports(F[2:],n)[1]>0
        for k,w in p.items():
            assert all(any(((w>>(abs(z)-1))&1)==int(z>0) for z in c)
                       for j,c in enumerate(F) if j!=k)
            assert all(((w>>(abs(z)-1))&1)!=int(z>0) for z in F[k])
        recs[name]=dict(variables=n,clauses=m,essential=len(p),root_bytes=root,
                        child_bytes=one,grandchild_bytes=two)
    count=Counter(x for clause in W1 for x in clause)
    assert all(count[i]==2 and count[-i]==2 for i in range(1,16))
    K=cases['odd_K4'][0]
    opt,states=optimal(K,6)
    assert opt[:2]==(28,6) and states==697 and check_tree(K,opt[2],6)
    even=tseitin(4,[(i,j) for i in range(4) for j in range(i+1,4)],[0,0,0,0])
    assert supports(even,6)[1]>0 and not check_tree(even,opt[2],6)
    forged=tuple(((-c[0],*c[1:]) if k==0 else c) for k,c in enumerate(K))
    assert supports(forged,6)[1]>0 and not check_tree(forged,opt[2],6)
    D=K+tuple(tuple((abs(x)+6)*(1 if x>0 else -1) for x in c) for c in K)
    assert supports(D,12)==({},0)
    assert supports(((1,),(-1,)),1)[1]==0
    assert supports(((1,2),(-1,2)),2)[1]>0
    return dict(run_id='SOURCE-SUPPORT-PRIVATE-WITNESS126',cases=recs,
                K4_optimal_branch_leaves=28,K4_min_leaf_max_depth=6,
                K4_dynamic_states=697,strict_W1=True,
                disconnected_essential=0,
                forged_proof_rejected=True,SAT_proof_rejected=True,
                all_checks_passed=True,
                scope='exact small-control computation; no FLMV-time measurement')
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
