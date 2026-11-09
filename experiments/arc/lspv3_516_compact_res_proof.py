#!/usr/bin/env python3
"""Standalone source-authenticated 7-RES tree builder for all Q4 matchings.
No historical mixed parser, no official XLRUP checker; Python >=3.9.
"""
from functools import lru_cache
from collections import Counter
import json

@lru_cache(None)
def matchings(mask):
    if not mask: return ((),)
    a=(mask & -mask).bit_length()-1
    out=[]
    for j in range(4):
        b=a^(1<<j)
        if mask>>b & 1:
            edge=(min(a,b),max(a,b))
            out.extend((edge,)+rest for rest in matchings(mask^(1<<a)^(1<<b)))
    return tuple(out)

def clause(edge):
    a,b=edge
    d=(a^b).bit_length()-1
    assert (a^b).bit_count()==1
    return tuple((i+1 if not (a>>i&1) else -i-1) for i in range(4) if i!=d)

def res(left,right,pivot):
    assert pivot in left and -pivot in right
    out=set(left)|set(right)
    out.remove(pivot);out.remove(-pivot)
    assert all(-x not in out for x in out)
    return tuple(sorted(out,key=abs))

def check(matching):
    cs=tuple(map(clause,matching))
    assert len(cs)==8 and len(set(cs))==8
    for a in range(16):
        bad=[i for i,c in enumerate(cs) if all(((a>>(abs(l)-1))&1)!=(l>0) for l in c)]
        assert len(bad)==1
    for i in range(8):
        assert sum(all(((a>>(abs(l)-1))&1)!=(l>0) for l in cs[i]) for a in range(16))==2
    for rhs in (0,1):
        for a in range(16):
            if a.bit_count()%2==rhs:continue
            full=[i+1 if not (a>>i&1) else -i-1 for i in range(4)]
            hints=[i for i,c in enumerate(cs) if set(c).issubset(full)]
            assert len(hints)==1
    counts=Counter((a^b).bit_length()-1 for a,b in matching)
    assert all(v%2==0 for v in counts.values())
    if len(counts)==4:
        assert sorted(counts.values())==[2]*4
        return False
    lookup={e:(i+1,cs[i]) for i,e in enumerate(matching)}
    nodes=[]
    def build(edges,free,fixed):
        if len(free)==1:
            assert len(edges)==1
            return lookup[edges[0]]
        dirs={(a^b).bit_length()-1 for a,b in edges}
        pivot=next(j for j in free if j not in dirs)
        left=tuple(e for e in edges if not (e[0]>>pivot&1))
        right=tuple(e for e in edges if (e[0]>>pivot&1))
        assert len(left)==len(right)==len(edges)//2
        la,lc=build(left,[j for j in free if j!=pivot],fixed+((pivot,0),))
        ra,rc=build(right,[j for j in free if j!=pivot],fixed+((pivot,1),))
        out=res(lc,rc,pivot+1)
        expected=tuple(j+1 if bit==0 else -(j+1) for j,bit in sorted(fixed))
        assert out==expected
        nodeid=9+len(nodes)
        nodes.append((nodeid,la,ra,pivot+1,out))
        return (nodeid,out)
    root=build(matching,list(range(4)),())
    assert root[1]==() and len(nodes)==7
    trace={i+1:c for i,c in enumerate(cs)}
    for ident,la,ra,p,out in nodes:
        assert ident not in trace and la in trace and ra in trace
        assert res(trace[la],trace[ra],p)==out
        trace[ident]=out
    ancestors=set()
    def walk(ident):
        if ident in ancestors:return
        ancestors.add(ident)
        if ident>8:
            _,left,right,_,_=next(t for t in nodes if t[0]==ident)
            walk(left);walk(right)
    walk(nodes[-1][0])
    assert len(ancestors)==15 and set(range(1,9)).issubset(ancestors)
    return True

if __name__=='__main__':
    match=matchings((1<<16)-1)
    assert len(match)==272 and len(set(match))==272
    ok=sum(check(m) for m in match)
    assert ok==232
    print(json.dumps({'matching_count':len(match),'exact_7_RES':ok,
      'four_direction_obstruction':len(match)-ok,'all_original_sources_verified':True,
      'all_7_RES_constructions_source_authenticated':True,
      'external_only_four_record_hint_coverages':len(match),
      'historical_Rmix341_checker_executed':False,'p_vs_np':'OPEN'},indent=2))
