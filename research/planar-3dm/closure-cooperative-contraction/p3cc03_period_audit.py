from p3cc03_audit import *

def reduce(v,H):
    for k,h in sorted(H.items(),reverse=True):
        if v>>k&1:v^=h
    return v

def periods(n,T,L):
    H={};log=[];calls=0
    while True:
        B={}
        for (x,y,z),l in zip(T,L):B.setdefault((x,y),set()).add(reduce(l,H))
        cand=sorted({a^b for S in B.values() for a in S for b in S if a!=b});found=False
        for p in cand:
            G=nx.Graph();left=[(0,i) for i in range(n)];G.add_nodes_from(left+[(1,i) for i in range(n)])
            G.add_edges_from(((0,x),(1,y)) for (x,y),S in B.items() if any(a^p not in S for a in S))
            calls+=1
            if len(nx.algorithms.bipartite.maximum_matching(G,top_nodes=left))<2*n:
                log.append((H.copy(),p));H[p.bit_length()-1]=p;found=True;break
        if not found:return H,log,calls

def signature(ids,L):
    s=0
    for i in ids:s^=L[i]
    return s

def restore(T,L,ids,target,log):
    ids=ids[:];switches=0
    for H,p in reversed(log):
        d=reduce(signature(ids,L)^target,H)
        assert d in (0,p)
        if d:
            found=False
            for j,i in enumerate(ids):
                for k,t in enumerate(T):
                    if t[:2]==T[i][:2] and reduce(L[k]^L[i],H)==p:
                        ids[j]=k;switches+=1;found=True;break
                if found:break
            assert found
    assert signature(ids,L)==target
    return ids,switches

def linear(n):
    T=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
    if n>=3:T += [(2,2,0),(2,1,2),(0,2,2)]
    for k in range(3,n):T += [(k,k,k-1),(k,k-1,k),(k-1,k,k)]
    return sorted(T)

def main():
    R={'dense':[],'obstruction':[],'small_guarded':0,'small_target_comparisons':0,'small_lifts':0,'switches':0};rng=random.Random(261125)
    for n in (4,8,16,32,64):
        T=octa(n);assert closure(n,T)==(T,[]);L=[1<<t[2] for t in T];H,log,calls=periods(n,T,L);assert len(H)==n-1
        O=Oracle(n,T,[reduce(l,H) for l in L]);S,B,I=acquire(O,n,1);assert S is not None and len(S)==1
        s=reduce((1<<n)-1,H);ids=lift(O,S,B,I,s);ids,k=restore(T,L,ids,(1<<n)-1,log)
        assert all(len({T[i][c] for i in ids})==n for c in range(3));R['switches']+=k
        R['dense'].append({'n':n,'triples':len(T),'period_rank':len(H),'remaining_support':len(S),'matching_tests':calls,'det_calls':O.calls,'restore_switches':k})
    for n in (4,8,12,16,32,64):
        T=linear(n);assert nx.check_planarity(source_graph(n,T))[0] and nx.is_connected(source_graph(n,T));assert closure(n,T)==(T,[])
        counts=[]
        for a,b,c in [(0,1,2),(0,2,1),(1,2,0)]:
            U=sorted((t[a],t[b],t[c]) for t in T);assert len({t[:2] for t in U})==len(U)
            L=[1<<t[2] for t in U];H,log,calls=periods(n,U,L);assert not H
            # Explicit disjoint tail swaps supply independent signature directions.
            g=nx.Graph();g.add_edges_from(((0,x),(1,y)) for x,y,z in U);assert nx.is_connected(g)
            diag=[U.index(next(t for t in U if t[:2]==(i,i))) for i in range(n)];base=signature(diag,L);deltas=[]
            for i in range(3,n-1,2):
                ids=[j for j in diag if U[j][0] not in (i,i+1)]
                ids.extend(U.index(next(t for t in U if t[:2]==p)) for p in ((i,i+1),(i+1,i)))
                assert len({U[j][0] for j in ids})==len({U[j][1] for j in ids})==n
                deltas.append(signature(ids,L)^base)
            assert rank([0]+deltas)==len(deltas)
            O=Oracle(n,U);S,B,I=acquire(O,n,32);counts.append(None if S is None else len(S))
        # Last three elements each occur in two of the three new triples; no exact cover.
        tail=[t for t in T if n-1 in t];assert len(tail)==3 and all(t.count(n-1)==2 for t in tail)
        if n<=16:assert (1<<n)-1 not in reference(n,T)
        R['obstruction'].append({'n':n,'triples':len(T),'lower_bound_each_lane':2**((n-3)//2),'supports_or_cap32':counts})
    for n in (2,3,4,5):
        for _ in range(25):
            T=[t for t in octa(n) if rng.random()<.9];L=[(1<<t[2])|(rng.randrange(4)<<n) for t in T]
            ref=reference(n,T,L)
            if not ref:continue
            H,log,calls=periods(n,T,L);quot=Counter()
            for s,k in ref.items():quot[reduce(s,H)]+=k
            O=Oracle(n,T,[reduce(l,H) for l in L]);S,B,I=acquire(O,n+2,1<<(n+2));assert S==dict(quot)
            for target in range(1<<(n+2)):
                yes=reduce(target,H) in S;assert yes==(target in ref);R['small_target_comparisons']+=1
                if yes:
                    ids=lift(O,S,B,I,reduce(target,H));ids,k=restore(T,L,ids,target,log);R['small_lifts']+=1;R['switches']+=k
            R['small_guarded']+=1
    print(json.dumps(R,indent=2))
if __name__=='__main__':main()
