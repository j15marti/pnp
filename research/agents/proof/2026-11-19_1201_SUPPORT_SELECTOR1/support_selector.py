"""Bounded shared-support selector; independent exhaustive finite audit."""
import itertools, random, json

def sccsolve(clauses,d):
    if any(not c for c in clauses): return None
    assert all(len(c)<=2 for c in clauses)
    g=[[] for _ in range(2*d)]; h=[[] for _ in g]
    def node(l): return 2*(abs(l)-1)+(l<0)
    for c in clauses:
        a=node(c[0]); b=node(c[-1])
        for u,v in ((a^1,b),(b^1,a)):
            g[u].append(v); h[v].append(u)
    seen=set(); order=[]
    def visit(u):
        if u in seen:return
        seen.add(u)
        for v in g[u]:visit(v)
        order.append(u)
    for u in range(2*d):visit(u)
    comp={}
    def assign(u,k):
        if u in comp:return
        comp[u]=k
        for v in h[u]:assign(v,k)
    for u in reversed(order):
        if u not in comp:assign(u,len(comp))
    if any(comp[2*i]==comp[2*i+1] for i in range(d)):return None
    x=[comp[2*i]>comp[2*i+1] for i in range(d)]
    assert all(any(x[abs(l)-1]==(l>0) for l in c) for c in clauses)
    return x

def residual(block,z):
    out=[]
    for guards,private in block:
        if any(z[abs(l)-1]==(l>0) for l in guards):continue
        out.append(private)
    return out

def solve(blocks,h,d):
    rows=list(itertools.product((False,True),repeat=h))
    selector=[None]*len(rows); calls=0; marks=0
    for i,block in enumerate(blocks):
        support=sorted({abs(l)-1 for g,p in block for l in g})
        for a in itertools.product((False,True),repeat=len(support)):
            z=[False]*h
            for j,v in zip(support,a):z[j]=v
            calls+=1
            if sccsolve(residual(block,z),d) is not None:continue
            free=[j for j in range(h) if j not in support]
            for f in itertools.product((False,True),repeat=len(free)):
                for j,v in zip(free,f):z[j]=v
                index=sum(int(v)<<(h-1-j) for j,v in enumerate(z))
                marks+=1
                if selector[index] is None:selector[index]=i
    for row,i in zip(rows,selector):
        if i is None:
            for block in blocks:
                x=sccsolve(residual(block,row),d)
                assert x is not None
                # A production stream emits this block's private colors here.
                assert all(any(x[abs(l)-1]==(l>0) for l in c)
                           for c in residual(block,row))
            return True,row,calls,marks
    return False,selector,calls,marks

def run():
    rng=random.Random(202611191201); stats={'cases':0,'sat':0,'unsat':0,'local_calls':0,'row_marks':0}
    for trial in range(240):
        h=3; d=2; blocks=[]
        for i in range(3):
            support=rng.sample(range(1,h+1),rng.randrange(3))
            block=[]
            for _ in range(rng.randrange(1,9)):
                guards=tuple(v*rng.choice((-1,1)) for v in rng.sample(support,rng.randrange(len(support)+1)))
                private=tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,d+1),rng.randrange(3)))
                block.append((guards,private))
            blocks.append(block)
        answer,payload,calls,marks=solve(blocks,h,d)
        brute=False
        for bits in itertools.product((False,True),repeat=h+3*d):
            if all(all(any(bits[abs(l)-1]==(l>0) for l in g) or
                       any(bits[h+i*d+abs(l)-1]==(l>0) for l in p)
                       for g,p in block) for i,block in enumerate(blocks)):
                brute=True;break
        assert answer==brute
        if not answer:
            for row,i in zip(itertools.product((False,True),repeat=h),payload):
                assert not any(all(any(x[abs(l)-1]==(l>0) for l in c) for c in residual(blocks[i],row))
                               for x in itertools.product((False,True),repeat=d))
        stats['cases']+=1;stats['sat' if answer else 'unsat']+=1
        stats['local_calls']+=calls;stats['row_marks']+=marks
    # Changing bad-block index is essential even with no private variables.
    blocks=[[((1,),())],[((-1,),())]]
    ans,sel,_,_=solve(blocks,1,0)
    assert not ans and sel==[0,1]
    # T5 local path endpoint support, checked from original arc relation.
    words=0
    for length in range(1,5):
        for word in itertools.product((1,-1),repeat=length):
            actual=set()
            for c in itertools.product(range(5),repeat=length):
                colors=(0,)+c
                if all((sign*(colors[i+1]-colors[i]))%5 in (1,3) for i,sign in enumerate(word)):
                    actual.add(c[-1])
            expected={(length+word.count(-1)+2*j)%5 for j in range(length+1)}
            assert actual==expected;words+=1
    stats['t5_path_words']=words;stats['rotating_selector_control']=sel
    stats['seed']=202611191201
    return stats

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
