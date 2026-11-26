"""C07 mobile-neuron finite audit, 2026-11-26. Python 3, stdlib only."""
from itertools import product, combinations
from random import Random
from collections import defaultdict, deque
import json, math
P=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
class DSU:
    def __init__(self,n): self.p=list(range(n)); self.s=[1]*n; self.x=[0]*n
    def find(self,i):
        r=i; a=0
        while self.p[r]!=r: a^=self.x[r];r=self.p[r]
        return r,a
    def union(self,i,j,b):
        r,a=self.find(i);s,c=self.find(j)
        if r==s: return 0 if a^c==b else -1
        if self.s[r]>self.s[s]:r,s=s,r
        self.p[r]=s;self.x[r]=a^c^b;self.s[s]+=self.s[r];return 1

def score(n,F,ss):
    d=DSU(n);return sum(d.union(C[i],C[j],1)==-1 for C,t in zip(F,ss) for i,j in P[t])

def valid(F,x,pins={}): return all(x[i]==v for i,v in pins.items()) and all(sum(x[i] for i in C)==2 for C in F)

def hub(n,F):
    # All source-derived pair groups, no supplied wheel decomposition.
    G=defaultdict(list)
    for C in F:
        for a,b in combinations(sorted(C),2):
            u,v=[x for x in C if x not in (a,b)];G[a,b].append((u,v))
    eq=[]; odd=0
    for (a,b),edges in G.items():
        adj=defaultdict(set)
        for u,v in edges:adj[u].add(v);adj[v].add(u)
        color={}; comps=[];bad=False
        for u in sorted(adj):
            if u in color:continue
            color[u]=0; q=deque([u]);K=[]
            while q:
                i=q.popleft();K.append(i)
                for j in adj[i]:
                    if j not in color:color[j]=1-color[i];q.append(j)
                    elif color[j]==color[i]:bad=True
            comps.append(K)
        if bad:
            odd+=1;eq.append((a,b,0));eq.extend((a,u,1) for u in adj)
        else:
            for K in comps:
                for v in (0,1):
                    L=[u for u in K if color[u]==v]
                    eq.extend((L[0],u,0) for u in L[1:])
    return eq,odd

def close(n,F,eq):
    """Exact local tables and all local unary/binary forced consequences. Const vertex n."""
    d=DSU(n+1)
    for i,j,b in eq:
        if d.union(i,j,b)<0:return None,[]
    while True:
        changed=False; unresolved=[]
        for C in F:
            # Include the constant root in the table to obtain unary facts.
            roots=sorted({d.find(i)[0] for i in (*C,n)})
            const,cp=d.find(n);free=[r for r in roots if r!=const];rows=[]
            fs=[d.find(i) for i in C]
            for bits in product((0,1),repeat=len(free)):
                z=dict(zip(free,bits));z[const]=cp
                if sum(z[r]^s for r,s in fs)==2:rows.append(z)
            if not rows:return None,[]
            if len(rows)==2**len(free):continue
            unresolved.append(C)
            for i,j in combinations(roots,2):
                b=rows[0][i]^rows[0][j]
                if all(r[i]^r[j]==b for r in rows):
                    v=d.union(i,j,b)
                    if v<0:return None,[]
                    changed|=bool(v)
        if not changed:return d,unresolved

def solver(n,F,pins={},use_hub=True,probe=True):
    eq=[(i,n,v) for i,v in pins.items()];stats={'nodes':0,'probes':0,'odd_groups':0,'joins':0}
    if use_hub:
        ex,o=hub(n,F);eq+=ex;stats['odd_groups']=o
    def rec(E):
        stats['nodes']+=1
        while True:
            d,U=close(n,F,E)
            if d is None:return None
            if not U:
                r,c=d.find(n);x=[(c if d.find(i)[0]==r else 0)^d.find(i)[1] for i in range(n)]
                assert valid(F,x,pins);return x
            # Carry the entire exact parity forest into descendants (guard provenance).
            E=[(i,r,b) for i in range(n+1) for r,b in [d.find(i)] if i!=r]
            if not probe:break
            # Sound opposite-pin probes relative to E, then repeat closure after any deduction.
            cr,_=d.find(n);R=sorted({d.find(i)[0] for i in range(n)}-{cr});ded=None
            for r in R:
                for b in (0,1):
                    stats['probes']+=1
                    a,_=close(n,F,E+[(r,n,b)])
                    if a is None:ded=(r,n,b^1);break
                if ded:break
            if ded is None:break
            E=E+[ded]
        a,b,c,e=U[0];assert len({d.find(i)[0] for i in (a,b,c,e)})==4
        x=rec(E+[(a,b,1),(c,e,1)])
        if x is not None:return x
        return rec(E+[(a,b,0),(c,e,0),(a,c,1)])
    x=rec(eq);return x,stats

def brute(n,F,pins={}):return next((x for x in product((0,1),repeat=n) if valid(F,x,pins)),None)

def parity_wheel(k):
    # XOR all actual occupancy rows mod 2. All rim coefficients cancel.
    F=[(0,1,2+i,2+(i+1)%k) for i in range(k)];mask=0
    for C in F:
        for i in C:mask^=1<<i
    assert mask==3 if k%2 else mask==0
    return F,mask

def main():
    rng=Random(20261126);counts={'random':0,'SAT':0,'UNSAT':0,'nodes':0,'probes':0,'hub_certificate_relations_checked':0}; rings=[]
    # Fixed small controls: compare independent enumeration and complete guarded solver.
    for _ in range(240):
        n=rng.randrange(4,11);A=list(combinations(range(n),4));F=rng.sample(A,rng.randrange(1,min(len(A),16)+1));pins={i:rng.randrange(2) for i in range(n) if rng.randrange(6)==0}
        w=brute(n,F,pins);x,s=solver(n,F,pins)
        assert (w is None)==(x is None)
        if x is not None:assert valid(F,x,pins)
        counts['random']+=1;counts['SAT' if w is not None else 'UNSAT']+=1;counts['nodes']+=s['nodes'];counts['probes']+=s['probes']
        E,_=hub(n,F)
        for z in product((0,1),repeat=n):
            if valid(F,z,pins):
                for i,j,b in E:assert z[i]^z[j]==b;counts['hub_certificate_relations_checked']+=1
    for k in [3,5,9,17,33,65,129]:
        F,mask=parity_wheel(k);n=k+2;initial=[0]*k;start=score(n,F,initial);assert start==1
        local=[]
        for i in range(k):
            for t in (1,2):
                S=initial.copy();S[i]=t;local.append(score(n,F,S))
        assert min(local)>=1 and score(n,F,[1]*k)==0
        E,o=hub(n,F);assert o>=1
        # Same source and same empty guard: independent hub graph vs summed parity + exact occupancy closure.
        d,U=close(n,F,E);assert d is not None and not U
        d2,U2=close(n,F,[(0,1,0)]);assert d2 is not None and not U2
        sat,ss=solver(n,F,use_hub=True,probe=False);assert sat is not None and valid(F,sat)
        noF=F+[(0,2,3,4)];no,sn=solver(n,noF,use_hub=True,probe=False);assert no is None
        assert close(n,noF,[(0,1,0)])[0] is None
        # Run initial/stagnation failed-polarity closure explicitly on small common residuals (no cap bypass).
        if k<=9:
            a,sa=solver(n,F,use_hub=False,probe=True);b,sb=solver(n,noF,use_hub=False,probe=True)
            assert a is not None and b is None
        # Exhaustive topology test for smallest wheels only.
        exhaustive=0
        if k<=5:
            for S in product(range(3),repeat=k):
                assert (score(n,F,S)==0)==all(t!=0 for t in S);exhaustive+=1
        rings.append({'rim':k,'source_variables':n,'initial_score':start,'one_rotations':len(local),'min_one_rotation_score':min(local),'max_one_rotation_score':max(local),'full_rotation_score':0,'exact_required_rotations':k,'SAT_verified':True,'UNSAT_neighbor_verified':True,'hub_nodes':ss['nodes']+sn['nodes'],'exhaustive_topologies':exhaustive})
    # Even ring: every source solution obeys same-side equality; both phase cases remain.
    even=[]
    for k in [4,6,8]:
        F,mask=parity_wheel(k);E,o=hub(k+2,F);assert o==0;solutions=[x for x in product((0,1),repeat=k+2) if valid(F,x)]
        assert len(solutions)==6 and all(all(x[i]^x[j]==b for i,j,b in E) for x in solutions)
        even.append({'rim':k,'solutions':len(solutions),'deduced_equalities':len(E)})
    print(json.dumps({'seed':20261126,'random_controls':counts,'odd_wheels':rings,'even_controls':even},indent=2))
if __name__=='__main__':main()
