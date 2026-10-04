from functools import lru_cache
from collections import Counter

# READ2-RECOMP5: Q4 edge-cover exact linear-width / read-2 calibration.
# Computes:
#   * exact linear-width(Q4)=7 by closed-set DP;
#   * one width-7 edge layout;
#   * reduced OBDD size/width for edge-cover under that layout;
#   * the 64-node syntactic read-2 upper bound (2|E|).
#
# P versus NP is not addressed by this finite calibration.

D=4
V=list(range(1<<D))
E=[]
for u in V:
    for d in range(D):
        v=u^(1<<d)
        if u<v:
            E.append((u,v,d))
M=len(E)
ALL=(1<<M)-1
INC=[0]*len(V)
for i,(u,v,d) in enumerate(E):
    INC[u]|=1<<i
    INC[v]|=1<<i

@lru_cache(None)
def closure(S):
    F=0
    for i,(u,v,d) in enumerate(E):
        if ((S>>u)&1) and ((S>>v)&1):
            F|=1<<i
    return F

def mid_size(F):
    R=ALL^F
    return sum(bool(INC[v]&F) and bool(INC[v]&R) for v in V)

def has_layout(k):
    choice={}
    @lru_cache(None)
    def rec(S):
        F=closure(S)
        if F==ALL:
            return True
        for i,(u,v,d) in enumerate(E):
            if (F>>i)&1:
                continue
            if mid_size(F|(1<<i))>k:
                continue
            S2=S|(1<<u)|(1<<v)
            if rec(S2):
                choice[S]=i
                return True
        return False
    return rec(0),choice,rec.cache_info().currsize

ok6,_,states6=has_layout(6)
ok7,choice,states7=has_layout(7)
assert not ok6 and ok7

# Reconstruct one layout.  When closure adds induced edges, appending those
# edges cannot increase the current middle set.
S=0;F=0;order=[]
while F!=ALL:
    i=choice[S]
    order.append(i)
    u,v,_=E[i]
    S2=S|(1<<u)|(1<<v)
    Fc=closure(S2)
    base=F|(1<<i)
    order += [j for j in range(M)
              if ((Fc>>j)&1) and not ((base>>j)&1)]
    S,F=S2,Fc
assert len(order)==M and len(set(order))==M

F=0; frontier_profile=[]
frontiers=[]
for k in range(M+1):
    R=ALL^F
    fm=0
    for v in V:
        if (INC[v]&F) and (INC[v]&R):
            fm|=1<<v
    frontiers.append(fm)
    if k<M:
        F|=1<<order[k]
        frontier_profile.append(mid_size(F))
assert max(frontier_profile)==7

# Reduced OBDD for EC_Q4 = AND_v OR_{e incident v} x_e.
FALSE,TRUE=0,1
node_ids={}
nodes=[]

@lru_cache(None)
def bdd(k,cov):
    if k==M:
        return TRUE
    ei=order[k];u,v,_=E[ei]
    curf,nxt=frontiers[k],frontiers[k+1]
    kids=[]
    for bit in (0,1):
        c=cov
        if bit:
            c|=(1<<u)|(1<<v)
        departed=(curf|(1<<u)|(1<<v)) & ~nxt
        if departed & ~c:
            kids.append(FALSE)
        else:
            kids.append(bdd(k+1,c&nxt))
    lo,hi=kids
    if lo==hi:
        return lo
    key=(k,cov,lo,hi)
    if key not in node_ids:
        node_ids[key]=len(nodes)+2
        nodes.append(key)
    return node_ids[key]

root=bdd(0,0)
layers=Counter(k for k,c,lo,hi in nodes)

# Read-2 construction: check each vertex clause sequentially.
# Each edge variable occurs in exactly the two endpoint clauses.
read2_nodes=sum(sum(bool(INC[v]&(1<<e)) for e in range(M)) for v in V)
assert read2_nodes==2*M==64

print("Q4 vertices",len(V),"edges",M)
print("linearwidth<=6",ok6,"linearwidth<=7",ok7)
print("exact linearwidth",7)
print("layout",order)
print("frontier profile",frontier_profile)
print("reduced OBDD query nodes",len(nodes))
print("reduced OBDD peak width",max(layers.values()))
print("read-2 sequential-clause query nodes",read2_nodes)
print("read-2 reduction vs this OBDD",1-read2_nodes/len(nodes))
print("NOTE: the same 64-node program with terminals swapped computes D(4,8) SAT on the exact-weight-8 promise, because an 8-edge set covers all 16 Q4 vertices iff it is a perfect matching.")
