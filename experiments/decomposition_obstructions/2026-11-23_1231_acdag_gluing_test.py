from itertools import product
from random import Random
from collections import Counter

def rank(rows):
    piv={}
    for v in rows:
        while v:
            j=v.bit_length()-1
            if j in piv: v^=piv[j]
            else: piv[j]=v; break
    return len(piv)

def span(rows):
    s={0}
    for v in rows: s |= {x^v for x in s}
    return s

def dot(a,b): return (a&b).bit_count()%2
def cut(a,b): return rank(a)+rank(b)-rank(a+b)

def basis(rows):
    out=[]
    for v in rows:
        if rank(out+[v])>len(out): out.append(v)
    return out

def test():
    rng=Random(481); stats=Counter(); parity=Counter()
    # Small oracle: explicit dependency/span enumeration, not a fast solver.
    for n in range(2,8):
        for _ in range(80):
            blocks=[basis([rng.randrange(1,1<<n) for _ in range(rng.randint(1,3))]) for j in range(rng.randint(2,4))]
            rows=sum(blocks,[]); r=rank(rows); h=len(rows)-r
            deps=basis([a for a in range(1,1<<len(rows)) if not xor_selected(rows,a)])
            assert len(deps)==h
            dp={0:1}; off=0; predicates=[]; messages=[]
            syndrome_cols=[sum(((q>>j)&1)<<i for i,q in enumerate(deps)) for j in range(len(rows))]
            offsets=[0]
            for block in blocks:
                k=len(block); allowed={a for a in range(1<<k) if rng.randrange(3)}; predicates.append(allowed)
                msg=Counter()
                for a in allowed:
                    s=sum(dot(a<<off,q)<<j for j,q in enumerate(deps)); msg[s]+=1
                nxt=Counter()
                for a,c in dp.items():
                    for b,d in msg.items(): nxt[a^b]+=c*d
                dp=nxt; off+=k; messages.append(msg); offsets.append(off)
            z=dp.get(0,0)<<(n-r)
            oracle=sum(all(sum(dot(x,v)<<j for j,v in enumerate(b)) in p for b,p in zip(blocks,predicates)) for x in range(1<<n))
            assert z==oracle
            def tree(lo,hi):
                l,u=offsets[lo],offsets[hi]; inside=syndrome_cols[l:u]; outside=syndrome_cols[:l]+syndrome_cols[u:]
                inter=span(inside)&span(outside)
                assert len(inter)==1<<cut(rows[l:u],rows[:l]+rows[u:])
                if hi-lo==1:return Counter({a:c for a,c in messages[lo].items() if a in inter})
                mid=(lo+hi)//2; left,right=tree(lo,mid),tree(mid,hi); out=Counter()
                for a,c in left.items():
                    for b,d in right.items():
                        if a^b in inter:out[a^b]+=c*d
                return out
            assert tree(0,len(blocks)).get(0,0)<<(n-r)==oracle; stats['tree']+=1
            stats['syndrome']+=1; stats['sat' if z else 'unsat']+=1; parity[(r%2,h%2,(n-r)%2)]+=1
            a,b=blocks[0],sum(blocks[1:],[])
            H=basis([rng.randrange(1<<n) for _ in range(rng.randrange(n+1))]); A,B,HH=span(a),span(b),span(H); AB=span(a+b)
            qp=lambda v:min(v^h for h in HH)
            s2=(len({qp(v) for v in A}&{qp(v) for v in B})).bit_length()-1
            dim=lambda s:len(s).bit_length()-1
            gamma=dim(HH&AB)-dim(HH&A)-dim(HH&B)+dim(HH&A&B)
            assert s2==cut(a,b)-dim(HH&A&B)+gamma
            stats['quotient']+=1; stats['cut_up' if s2>cut(a,b) else 'cut_down' if s2<cut(a,b) else 'cut_same']+=1
            Hlocal=basis([v for v in list(A|B) if rng.randrange(5)==0]); HH=span(Hlocal)
            assert dim({min(v^h for h in HH) for v in A}&{min(v^h for h in HH) for v in B})==cut(a,b)-dim(HH&A&B)
            stats['local_quotient']+=1
    for k in range(3,13):
        rows=[1<<i for i in range(k-1)]+[(1<<(k-1))-1]
        assert rank(rows)==k-1 and all(cut([a],[b])==0 for i,a in enumerate(rows) for b in rows[i+1:])
        assert all(cut(rows[:j],rows[j:])==1 for j in range(1,k))
        for c in [0,1]:
            charges=[0]*(k-1)+[c]
            assert sum(all(dot(x,v)==q for v,q in zip(rows,charges)) for x in range(1<<(k-1)))==1-c
            stats['circuit_controls']+=1
    print(dict(stats)); print('rank,excess,nullity parity:',dict(sorted(parity.items())))

def xor_selected(rows,a):
    x=0
    for j,v in enumerate(rows):
        if a>>j&1:x^=v
    return x

if __name__=='__main__':test()
