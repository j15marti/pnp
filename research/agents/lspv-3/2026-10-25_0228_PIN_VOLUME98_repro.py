#!/usr/bin/env python3
"""PIN-VOLUME98. Exact finite structural audit, not unrestricted SAT resource bound."""
import itertools,json,math,random,hashlib,sys

def prism(r):
    return sorted({tuple(sorted(e)) for e in ([(i,(i+1)%r) for i in range(r)] +[(r+i,r+(i+1)%r) for i in range(r)] +[(i,r+i) for i in range(r)])})

def tcnf(v,edges,charge_vertex=None):
    inc=[[] for _ in range(v)]
    for i,(a,b) in enumerate(edges,1): inc[a].append(i);inc[b].append(i)
    assert all(len(t)==3 for t in inc)
    out=[]
    for u in range(v):
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2 != (u==charge_vertex):
                out.append(tuple(-x if bit else x for x,bit in zip(sorted(inc[u]),bits)))
    return out

def blen(n,m):
    h=(64*(n+m+1)-1).bit_length()
    return (2+4*m)*h

def frontier(clauses,k):
    before={abs(z) for c in clauses[:k] for z in c}
    after={abs(z) for c in clauses[k:] for z in c}
    return before & after

def pin_child(clauses,left,right):
    # Fully serialized, proper-three-clause eager child with source name mapping.
    names=sorted({abs(z) for c in clauses for z in c}|set(left)|set(right))
    mp={v:j+1 for j,v in enumerate(names)}
    out=[tuple((1 if lit>0 else -1)*mp[abs(lit)] for lit in c) for c in clauses]
    fresh=len(names)+1
    for v in list(sorted(left))+list(sorted(right)):
        a,b=fresh,fresh+1;fresh+=2
        for s,t in itertools.product((1,-1),repeat=2):
            # pin source variable to 0
            out.append((-mp[v],s*a,t*b))
    assert all(len(set(abs(z) for z in c))==3 for c in out)
    return fresh-1,out

def count_models_zero_witness(clauses,n):
    # On even-charge Tseitin, setting every ORIGINAL var=0 satisfies source.
    # Auxiliary pins to zero are immaterial because every pinned (-v) is true.
    return all(any(z<0 for z in c) for c in clauses)

def brute_models(clauses,n):
    count=0
    for assignment in range(1<<n):
        if all(any(((assignment>>(abs(lit)-1))&1)==int(lit>0) for lit in clause)
               for clause in clauses):
            count+=1
    return count

def full_audit():
    rng=random.Random(202610250228)
    results=[]
    checks=0
    for r in (3,4,5,6,8,10,14):
        v=2*r; ed=prism(r);ne=len(ed)
        yes=tcnf(v,ed,None);no=tcnf(v,ed,0)
        assert len(yes)==len(no)==4*v
        assert count_models_zero_witness(yes,ne)
        assert not count_models_zero_witness(no,ne)
        assert sorted(tuple(sorted(abs(z) for z in c)) for c in yes)==sorted(tuple(sorted(abs(z) for z in c)) for c in no)
        checks+=3
        if r<=5:
            assert brute_models(yes,ne)==(1 << (ne-v+1))
            assert brute_models(no,ne)==0
            checks+=2
        N=blen(ne,len(yes)); b=math.ceil(math.sqrt(len(yes)))
        data=[]
        for trial in range(32):
            perm=list(range(len(yes))); rng.shuffle(perm)
            cls=[yes[i] for i in perm]
            cuts=list(range(0,len(cls),b)) + [len(cls)]
            cuts=sorted(set(cuts))
            fronts=[frontier(cls,j) for j in cuts]
            j=max(range(len(cuts)),key=lambda i:len(fronts[i]))
            assert j not in (0,len(cuts)-1)
            # choose preceding block to ensure highest frontier is a right boundary
            lo,hi=cuts[j-1],cuts[j]
            nchild,child=pin_child(cls[lo:hi],fronts[j-1],fronts[j])
            nchildbits=blen(nchild,len(child))
            assert len(child)==hi-lo+4*(len(fronts[j-1])+len(fronts[j]))
            assert nchildbits>=blen(nchild,4*len(fronts[j]))
            assert count_models_zero_witness(child,nchild)
            data.append({'max_frontier':len(fronts[j]),'child_bits':nchildbits,'parent_bits':N,'clause_block':hi-lo,'cut':hi,
                'pinned_names':len(fronts[j-1])+len(fronts[j]),'clauses_child':len(child),'aux_variables':nchild-len(set(abs(z) for c in cls[lo:hi] for z in c)|fronts[j-1]|fronts[j])})
            checks+=4
        results.append({'vertices':v,'edges':ne,'clauses':len(yes),'parent_bits':N,'block_clause_budget':b,
            'trials':len(data),'min_block_frontier':min(x['max_frontier'] for x in data),
            'min_child_bits':min(x['child_bits'] for x in data),'min_child_parent_ratio':min(round(x['child_bits']/N,4) for x in data),
            'max_child_bits':max(x['child_bits'] for x in data),'sample':data[:2]})
    summary={'run':'PIN-VOLUME98','claim':'finite eager source-named four-proper-clause pin volume only; not all-algorithm lower bound',
        'seed':202610250228,'assertion_groups':checks,'failures':0,'source':'proper 3CNF Tseitin prism both charges','samples':results}
    return summary

if __name__=='__main__':
    raw=full_audit()
    s=json.dumps(raw,sort_keys=True,indent=2)+'\n'
    print(s)
