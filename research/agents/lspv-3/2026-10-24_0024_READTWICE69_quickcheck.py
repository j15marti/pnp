#!/usr/bin/env python3
"""READTWICE69 independent stdlib quickcheck. Deterministic, no dependencies."""
import itertools, json, random, hashlib

SEED=202610240024

def hwb(bits):
    w=sum(bits)
    return int(w>0 and bits[w-1]==1)

def two_pass_graph(h):
    g={}
    for i in range(h):
        for count in range(i+1):
            nxt={}
            for bit in (0,1):
                c=count+bit
                nxt[bit]=('A',i+1,c) if i<h-1 else (('B',0,c) if c else 0)
            g[('A',i,count)]=(i,nxt)
    for c in range(1,h+1):
        for i in range(c):
            g[('B',i,c)]=(i,{bit:(bit if i==c-1 else ('B',i+1,c)) for bit in (0,1)})
    assert len(g)==h*(h+1)
    return g

def run_graph(graph,h,b):
    node=('A',0,0)
    addresses=[]
    while isinstance(node,tuple):
        pos,nxt=graph[node]
        addresses.append(pos)
        node=nxt[b[pos]]
    return node,addresses

def matching_size(clauses,n):
    links=[set(abs(l)-1 for l in clause) for clause in clauses]
    owner=[-1]*n
    def augment(j,seen):
        for x in links[j]:
            if x in seen:
                continue
            seen.add(x)
            if owner[x]<0 or augment(owner[x],seen):
                owner[x]=j
                return True
        return False
    return sum(augment(j,set()) for j in range(len(links)))

def horn_lift(clauses,n):
    out=[]
    for j,cl in enumerate(clauses):
        selectors=[n+3*j+a+1 for a in range(3)]
        out.append(tuple(selectors))
        out.extend((-selectors[a],cl[a]) for a in range(3))
    return out,n+3*len(clauses)

def sat_brute(formula,n):
    return any(all(any(x[abs(l)-1]==(l>0) for l in clause) for clause in formula)
               for x in itertools.product((0,1),repeat=n))

def audit():
    statistics={'seed':SEED,'program':[],'hall_cases':0,'hall_matches':0,'controls':{}}
    for h in range(1,13):
        graph=two_pass_graph(h)
        yes=no=0
        for b in itertools.product((0,1),repeat=h):
            answer,reads=run_graph(graph,h,b)
            assert answer==hwb(b)
            assert reads[:h]==list(range(h))
            assert reads[h:]==list(range(sum(b)))
            yes+=answer
            no+=1-answer
        statistics['program'].append({'h':h,'nodes':len(graph)+2,'edges':2*len(graph),
                                      'yes':yes,'no':no,'inputs':2**h})
    rng=random.Random(SEED)
    for n in range(3,8):
        for m in range(1,9):
            for _ in range(30):
                formula=[tuple(x*(-1 if rng.getrandbits(1) else 1)
                            for x in rng.sample(range(1,n+1),3)) for j in range(m)]
                lifted,n2=horn_lift(formula,n)
                assert (m-matching_size(formula,n)==
                        4*m-matching_size(lifted,n2))
                statistics['hall_cases']+=1
                statistics['hall_matches']+=1
    cube=list(itertools.product((-1,1),repeat=3))
    all8=[tuple(sign[j]*(j+1) for j in range(3)) for sign in cube]
    for label,formula,expected in [
        ('unsat_all8',all8,False),
        ('sat_first4',all8[:4],True)]:
        assert sat_brute(formula,3)==expected
        lifted,n2=horn_lift(formula,3)
        assert len(formula)-matching_size(formula,3)==len(lifted)-matching_size(lifted,n2)
        statistics['controls'][label]=expected
    assert sat_brute([(1,2),(-1,2)],2)
    assert not sat_brute([(1,),(-1,)],1)
    print(json.dumps(statistics,sort_keys=True,indent=2))

if __name__=="__main__":
    audit()
