from itertools import product, combinations
from functools import lru_cache
import random

def gf_rank(rows):
    p={}
    for x in rows:
        while x:
            i=x.bit_length()-1
            if i in p:x^=p[i]
            else:p[i]=x;break
    return len(p)

def lift(R):return {x|((x.bit_count()%2)<<3) for x in R}
def matchable(R):
    S=lift(R)
    return all(any(j!=i and ((a^b)>>j)&1 and a^(1<<i)^(1<<j) in S for j in range(4)) for a in S for b in S for i in range(4) if (a^b)>>i&1)

def family(h,perm=None):
    # edge t_i i->i+1, b_i h+i->h+i+1, rung r_i=2h+i
    perm=list(range(h)) if perm is None else perm
    inv=[perm.index(i) for i in range(h)]
    P=[]; R=[]
    for rail in range(2):
        for i in range(h):
            P.append([rail*h+(i-1)%h,rail*h+i,2*h+(i if rail==0 else inv[i])])
            def ok(a,b,c):
                if i==0:return (c if rail==0 else 1-c)==(b & (1-a))
                return a==(b&c) if rail==0 else b==(a|c)
            R.append({a+2*b+4*c for a,b,c in product(range(2),repeat=3) if ok(a,b,c)})
    return P,R,3*h

def satisfied(P,R,x):return all(sum(((x>>j)&1)<<i for i,j in enumerate(ps)) in S for ps,S in zip(P,R))
def brute(P,R,e):return next((x for x in range(1<<e) if satisfied(P,R,x)),None)
def clauses(P,R,compact=False):
    out=set()
    for ps,S in zip(P,R):
        for k in range(1,4):
            if not compact and k!=3:continue
            for I in combinations(range(3),k):
                for bits in product(range(2),repeat=k):
                    if all(any((s>>i&1)!=b for i,b in zip(I,bits)) for s in S):
                        c=frozenset((ps[i]+1)*(1 if b==0 else -1) for i,b in zip(I,bits))
                        if not compact or not any(d<c for d in out):out.add(c)
    return out

def bin_relax(P,R):
    C=clauses(P,R,True);return {c for c in C if len(c)<=2}
def binary_unsat(C,e):
    if frozenset() in C:return True
    g={i:set() for i in range(-e,e+1) if i}
    for c in C:
        assert 1<=len(c)<=2
        a,b=(list(c)*2)[:2];g[-a].add(b);g[-b].add(a)
    def reach(i):
        seen={i};todo=[i]
        while todo:
            for j in g[todo.pop()]-seen:seen.add(j);todo.append(j)
        return seen
    return any(-i in reach(i) and i in reach(-i) for i in range(1,e+1))

def exact(C,e):
    terms=[]
    for c in C:
        m=sum(1<<(abs(i)-1) for i in c);w=sum(1<<(abs(i)-1) for i in c if i<0);terms.append((m,w))
    @lru_cache(None)
    def dp(m,w):
        if any(m&a==a and w&a==b for a,b in terms):return 1,0
        best=10**9;depth=10**9
        for i in range(e):
            b=1<<i
            if m&b:continue
            x,y=dp(m|b,w),dp(m|b,w|b)
            best=min(best,x[0]+y[0]);depth=min(depth,1+max(x[1],y[1]))
        return best,depth
    ans=dp(0,0);rev=[dp(((1<<e)-1)^((1<<i)-1),0) for i in range(e+1)]
    return ans,rev,dp.cache_info().currsize

def witness(h,removed,perm=None):
    # top removed => x=1 and bottom all 1; bottom removed => x=0 and top all 0.
    perm=list(range(h)) if perm is None else perm
    rail,i=divmod(removed,h);x=1-rail
    top=[1]*h if rail==0 else [0]*h
    bot=[1]*h if rail==0 else [0]*h
    if i:
        if rail==0:top=[int(j<i) for j in range(h)]
        else:bot=[int(j<i) for j in range(h)]
    # if special vertex removed, all rails x; rungs free within constraints
    r=[x]+([0]*(h-1) if rail==0 else [0]*(h-1))
    for j in range(1,h):
        if rail==0:r[j]=top[j-1] # split a=AND(b,c) except deleted; if a=b=1 need c=1
        else:r[j]=bot[perm[j]] # merge b=OR(a,c) except deleted; if a=b=0 need c=0
    return sum(b<<i for i,b in enumerate(top+bot+r))

def core(h):
    x=2*h+1; C={frozenset((-x,1)),frozenset((-x,-h)),frozenset((x,h+1)),frozenset((x,-2*h))}
    for rail in range(2):
        for i in range(1,h):C.add(frozenset((-(rail*h+i),rail*h+i+1)))
    return C

def indispensable_witnesses(h,perm=None):
    perm=list(range(h)) if perm is None else perm
    P,R,e=family(h,perm); out={}
    def record(v,w):
        ps=P[v];word=sum(((w>>j)&1)<<i for i,j in enumerate(ps));assert word not in R[v]
        c=frozenset((j+1)*(1 if (w>>j&1)==0 else -1) for j in ps)
        assert all(i==v or sum(((w>>j)&1)<<k for k,j in enumerate(q)) in R[i] for i,q in enumerate(P))
        out[c]=w
    for rail in range(2):
        for i in range(1,h):
            v=rail*h+i;w=witness(h,v,perm);j=P[v][2]
            record(v,w&~(1<<j));record(v,w|(1<<j))
        for a,b in [(0,0),(0,1),(1,1)]:
            # first and last rail edges, monotonically extended
            top=[1-rail]*h;bot=[1-rail]*h
            bits=[a]*(h-1)+[b]
            if rail==0:top=bits
            else:bot=bits
            r=[1-rail]+[top[j-1] if rail==0 else bot[perm[j]] for j in range(1,h)]
            w=sum(bit<<i for i,bit in enumerate(top+bot+r));record(rail*h,w)
    assert len(out)==4*h+2
    return out

def resolution_certificate(P,R,h):
    full=clauses(P,R);C=core(h);steps=[];seen=set(full)
    def add(a,b,p):
        assert a in seen and b in seen and p in a and -p in b
        c=(a-{p})|(b-{-p});assert not any(-i in c for i in c);seen.add(c);steps.append(c);return c
    def derive(c):
        z=next(z for z in range(1,3*h+1) if c|{z} in seen and c|{-z} in seen and z not in c and -z not in c)
        assert add(c|{z},c|{-z},z)==c;return c
    x=2*h+1;units=[]
    for rail in range(2):
        s=-x if rail==0 else x;first=rail*h+1;last=(rail+1)*h
        chain=derive(frozenset((-first,first+1)))
        for i in range(first+1,last):chain=add(chain,derive(frozenset((-i,i+1))),i)
        pos=add(frozenset((s,first,last)),frozenset((s,first,-last)),last)
        neg=add(chain,frozenset((s,-first,-last)),last)
        units.append(add(pos,neg,first))
    assert add(units[1],units[0],x)==frozenset()
    return len(steps)

def min_cut(P):
    v=len(P);best=10**9
    for m in range(1<<v):
        if not 2<=m.bit_count()<=v-2:continue
        counts={}
        for i,ps in enumerate(P):
            if m>>i&1:
                for e in ps:counts[e]=counts.get(e,0)+1
        best=min(best,sum(c==1 for c in counts.values()))
    return best

def recognize(P,R,e):
    # Return (recognized, SAT, witness). Ordered ports are part of source.
    v=len(P)
    if v<6 or v%2 or e!=3*v//2:return False,None,None
    h=v//2;inc={}
    for i,ps in enumerate(P):
        if len(set(ps))!=3:return False,None,None
        for j,k in enumerate(ps):inc.setdefault(k,[]).append((i,j))
    if set(inc)!=set(range(e)) or any(len(a)!=2 for a in inc.values()):return False,None,None
    nxt={};mate={}
    for i,ps in enumerate(P):
        a=next(x for x in inc[ps[1]] if x!=(i,1));b=next(x for x in inc[ps[2]] if x!=(i,2))
        if a[1]!=0 or b[1]!=2:return False,None,None
        nxt[i]=a[0];mate[i]=b[0]
    def cycle(i):
        seen=[]
        while i not in seen:seen.append(i);i=nxt[i]
        return seen if i==seen[0] and len(seen)==h else []
    for i in range(v):
        top=cycle(i);bot=cycle(mate[i])
        if not top or not bot or set(top)&set(bot) or any(mate[j] not in bot for j in top):continue
        order=top+bot;perm=[bot.index(mate[j]) for j in top];Q,S,_=family(h,perm)
        mapping={};flips={};deleted=[];good=True
        for k,j in enumerate(order):
            for a,b in zip(Q[k],P[j]):
                if a in mapping and mapping[a]!=b:good=False
                mapping[a]=b
            if R[j]==set(range(8)):deleted.append(k);continue
            masks=[m for m in range(8) if {x^m for x in S[k]}==R[j]]
            if len(masks)!=1:good=False;break
            for a,b in zip(P[j],range(3)):
                f=masks[0]>>b&1
                if a in flips and flips[a]!=f:good=False
                flips[a]=f
        if not good or len(deleted)>1 or len(set(mapping.values()))!=e:continue
        if not deleted:return True,False,None
        z=witness(h,deleted[0],perm);w=sum((((z>>a)&1)^flips.get(b,0))<<b for a,b in mapping.items())
        assert satisfied(P,R,w)
        return True,True,w
    return False,None,None

def main():
    assert sum(matchable({i for i in range(8) if m>>i&1}) for m in range(256))==148
    print('local classification 148/256 independently checked')
    for h in (3,4,5,8,16,32,64):
        P,R,e=family(h);v=len(P);N=v+e+2+v*(3*e.bit_length()+8)
        assert all(gf_rank([x^min(S) for x in S])==3 and not matchable(S) for S in R)
        rank=gf_rank([sum(1<<j for j in ps) for ps in P]);assert rank==v-1
        C=core(h);B=bin_relax(P,R);assert C<=B and binary_unsat(B,e) and all(len(c)==2 for c in B)
        assert all(not binary_unsat(C-{c},e) for c in C)
        for i in range(v):
            RR=R[:];RR[i]=set(range(8));assert satisfied(P,RR,witness(h,i))
        cert=resolution_certificate(P,R,h);assert cert==4*h+1
        essential=indispensable_witnesses(h);assert set(essential)<=clauses(P,R)
        print('h,v,e,N,rank,fullCNF,core,proof',h,v,e,N,rank,len(clauses(P,R)),len(C),cert,'min_nontrivial_cut',min_cut(P) if h<=5 else 'not enumerated')
        if h<=4:
            assert brute(P,R,e) is None
            for i in range(v):
                RR=R[:];RR[i]=set(range(8));assert brute(P,RR,e) is not None
            print('full exact',exact(clauses(P,R),e));print('core exact',exact(C,e))
    rng=random.Random(20261127);stat={'SAT':0,'UNSAT':0,'binary_NO':0,'missed_NO':0}
    for _ in range(240):
        P,R,e=family(3)
        for i in range(len(R)):
            if rng.random()<.35:R[i]={j for j in range(8) if rng.random()<.5}
            if not R[i]:R[i]={rng.randrange(8)}
        # scramble edge numbering and globally complement selected edge variables
        perm=list(range(e));rng.shuffle(perm);mask=rng.randrange(1<<e)
        R=[{s^sum(((mask>>j)&1)<<i for i,j in enumerate(ps)) for s in S} for ps,S in zip(P,R)]
        P=[[perm[j] for j in ps] for ps in P]
        sat=brute(P,R,e) is not None;no=binary_unsat(bin_relax(P,R),e);assert not(sat and no)
        stat['SAT' if sat else 'UNSAT']+=1;stat['binary_NO']+=no;stat['missed_NO']+=not sat and not no
    print('mutated/renamed/signed',stat)
    for h in (4,5,8,16,32,64):
        for _ in range(12):
            tail=list(range(1,h));rng.shuffle(tail);perm=[0]+tail
            P,R,e=family(h,perm);assert binary_unsat(bin_relax(P,R),e)
            assert gf_rank([sum(1<<j for j in ps) for ps in P])==2*h-1
            assert resolution_certificate(P,R,h)==4*h+1
            assert set(indispensable_witnesses(h,perm))<=clauses(P,R)
            for i in range(2*h):
                RR=R[:];RR[i]=set(range(8));assert satisfied(P,RR,witness(h,i,perm))
            if h<=5:assert min_cut(P)>=4
            if h==4:assert brute(P,R,e) is None
    print('permuted rung networks 72, exact resolution certificates and all 4h+2 indispensable-clause witnesses checked')
    tests=0
    for h in (4,8,16,32):
        for _ in range(12):
            tail=list(range(1,h));rng.shuffle(tail);P,R,e=family(h,[0]+tail)
            for removed in (-1,rng.randrange(2*h)):
                RR=R[:]
                if removed>=0:RR[removed]=set(range(8))
                mask=rng.randrange(1<<e);perm=list(range(e));rng.shuffle(perm);order=list(range(2*h));rng.shuffle(order)
                S=[{s^sum(((mask>>j)&1)<<i for i,j in enumerate(P[k])) for s in RR[k]} for k in order]
                Q=[[perm[j] for j in P[k]] for k in order]
                known,sat,w=recognize(Q,S,e);assert known and sat==(removed>=0);tests+=1
                if sat:assert satisfied(Q,S,w)
                else:assert binary_unsat(bin_relax(Q,S),e)
    print('both-label recognition with hidden names and global signs',tests)
if __name__=='__main__':main()
