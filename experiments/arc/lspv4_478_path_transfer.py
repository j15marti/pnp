#!/usr/bin/env python3
"""Independent finite resource test for tree-centroid recomputation on *original signed* cubic-prism 3-CNF.
No native FLMV interpreter. Deterministic seed, all exceptional packets four proper signed ternary clauses.
"""
import json, itertools, random, hashlib, math
from functools import lru_cache
from collections import defaultdict
R=random.Random(47820261107)

class Tester:
    def __init__(self,m,D,odd,forced=False):
        self.m=m; self.V=2*m;self.E=3*m; self.D=set(D)
        self.edges={}
        for i in range(m):
            self.edges[i]= (i,(i+1)%m)
            self.edges[m+i]=(m+i,m+(i+1)%m)
            self.edges[2*m+i]=(i,m+i)
        self.inc=defaultdict(list)
        for e,(a,b) in self.edges.items(): self.inc[a].append(e);self.inc[b].append(e)
        self.inc={v:tuple(sorted(es)) for v,es in self.inc.items()}
        self.gD={v:sorted([w for e in self.inc[v] for w in self.edges[e] if w!=v and w in self.D]) for v in self.D}
        assert all(len(v)==3 for v in self.inc.values())
        assert len(self.D)<m  # inner cycle intact and connected
        # source packet: 4 strict 3 clauses, each forbidding a concrete local triple
        self.forbidden={}
        for v in range(self.V):
            if v in self.D:
                forbidden=sorted(R.sample(list(range(8)),4))
            else:
                b=R.randrange(2)
                forbidden=[x for x in range(8) if (x.bit_count()%2)!=b]
            self.forbidden[v]=tuple(forbidden)
        if forced:
            # two consecutive exceptional vertices: force their shared edge to conflicting values
            a,b=sorted([0,1]); edge=next(e for e in self.inc[a] if b in self.edges[e])
            self.forbidden[a]=tuple(x for x in range(8) if (x>>self.inc[a].index(edge))&1)
            self.forbidden[b]=tuple(x for x in range(8) if not ((x>>self.inc[b].index(edge))&1))
        self.charge={v:(next(x for x in range(8) if x not in self.forbidden[v]).bit_count()%2) for v in range(self.V) if v not in self.D}
        self.q=0
        for v,b in self.charge.items():self.q^=b
        self.clauses=[(v,tuple((e, bool((mask>>i)&1)) for i,e in enumerate(self.inc[v]))) for v in range(self.V) for mask in self.forbidden[v]]
        assert len(self.clauses)==4*self.V
        for v,c in self.clauses:
            assert all(e in self.inc[v] for e,_ in c) and len({e for e,_ in c})==3
        self.rec_calls=0;self.max_depth=0;self.max_boundary=0;self.max_size=0
    def allowed(self,v,assignment):
        return assignment not in self.forbidden[v]
    def exhaustive(self):
        sats=0
        for bits in range(1<<self.E):
            for v,c in self.clauses:
                if not any(((bits>>e)&1)!=forbidden_bit for e,forbidden_bit in c):break
            else:sats+=1
        return sats
    def components(self,U):
        U=set(U);ret=[]
        while U:
            start=min(U);q=[start];s={start};U.remove(start)
            for v in q:
                for w in self.gD[v]:
                    if w in U:U.remove(w);s.add(w);q.append(w)
            ret.append(frozenset(s))
        return ret
    def center(self,U):
        # Exact centroid, materialized ONLY in host finite test, not the proposed low-space machine.
        best=None
        for v in sorted(U):
            comps=self.components(set(U)-{v})
            mx=max(map(len,comps),default=0)
            if best is None or (mx,v)<best:best=(mx,v)
        assert best[0]*2<=len(U)
        return best[1]
    def centroid(self,U,bound,depth=1):
        U=frozenset(U)
        self.rec_calls+=1;self.max_depth=max(self.max_depth,depth)
        self.max_boundary=max(self.max_boundary,len(bound));self.max_size=max(self.max_size,len(U))
        if not U:return {0}
        v=self.center(U)
        children=self.components(set(U)-{v})
        out=set()
        for x in range(8):
            if not self.allowed(v,x):continue
            ev={e:(x>>i)&1 for i,e in enumerate(self.inc[v])}
            if any(ev[e]!=b for e,b in bound.items() if e in self.inc[v]): continue
            syndrome=0
            for e,b in ev.items():
                a,z=self.edges[e]
                if (a if z==v else z) not in self.D:syndrome^=b
            totals={syndrome};good=True
            for child in children:
                newbound={e:b for e,b in bound.items() if any(u in self.edges[e] for u in child)}
                cedges=[e for e,b in ev.items() if any(u in self.edges[e] for u in child)]
                assert len(cedges)==1
                newbound[cedges[0]]=ev[cedges[0]]
                sub=self.centroid(child,newbound,depth+1)
                if not sub:good=False;break
                totals={a^b for a in totals for b in sub}
            if good:out|=totals
        return out
    def direct_dp(self,U,parent=None,edgeval=None):
        # INDEPENDENT baseline, rooted child memo via one-edge interface and small syndrome.
        v=min(U)
        seen={v};stack=[v];pairs=[]
        for p in stack:
            for w in self.gD[p]:
                if w in U and w not in seen: seen.add(w);stack.append(w);pairs.append((p,w))
        children=defaultdict(list)
        for p,w in pairs:children[p].append(w)
        @lru_cache(None)
        def f(v,par):
            ans=set()
            for x in range(8):
                if not self.allowed(v,x):continue
                ev={e:(x>>i)&1 for i,e in enumerate(self.inc[v])}
                if par is not None and ev[par[0]]!=par[1]:continue
                syndrome=0
                for e,b in ev.items():
                    if any(w not in self.D for w in self.edges[e]):syndrome^=b
                cur={syndrome}
                for w in children[v]:
                    e=next(e for e in self.inc[v] if w in self.edges[e]);vals=f(w,(e,ev[e]))
                    cur={a^b for a in cur for b in vals}
                ans|=cur
            return ans
        return f(v,None)
    def solve(self):
        comps=self.components(self.D)
        result={0}; ref={0}
        for c in comps:
            sub=self.centroid(c,{});check=self.direct_dp(c)
            assert sub==check,(self.m,self.D,sub,check)
            result={a^b for a in result for b in sub}
            ref={a^b for a in ref for b in check}
        assert result==ref
        return self.q in result


    def path_syndrome(self):
        """Constant-state source-driven transfer, no retained per-vertex syndrome table."""
        # Source is cubic prism, all defects on outer ring, at least one intact outer vertex.
        assert all(v<self.m for v in self.D) and len(self.D)<self.m
        starts=[v for v in range(self.m) if v in self.D and ((v-1)%self.m) not in self.D]
        global_set={0}
        traversed=[]
        for start in starts:
            # left e_(start-1) carries initial boundary syndrome
            states={(left,left) for left in (0,1)} # (left outer edge bit, syndrome)
            i=start
            while i in self.D:
                traversed.append(i)
                nxt=set()
                eleft=(i-1)%self.m
                eright=i
                espoke=2*self.m+i
                ev=self.inc[i]
                for left,p in states:
                    for tri in range(8):
                        if tri in self.forbidden[i]: continue
                        vals={e:(tri>>j)&1 for j,e in enumerate(ev)}
                        if vals[eleft]!=left:continue
                        nxt.add((vals[eright],p^vals[espoke]))
                states=nxt
                i=(i+1)%self.m
            spectrum={p^right for right,p in states}
            global_set={a^b for a in global_set for b in spectrum}
        assert set(traversed)==self.D, (traversed,self.D)
        return global_set

def is_parity_packet(forbidden):
    return set(forbidden) in ({0,3,5,6},{1,2,4,7})

def encode_original(F):
    m=F.m;ell=m.bit_length();W=(3*m).bit_length()
    bits='1'*ell+'0'+format(m,f'0{ell}b')
    for v in range(F.V):
        for mask in F.forbidden[v]:
            for i,e in enumerate(F.inc[v]):
                bits+=str((mask>>i)&1)+format(e+1,f'0{W}b')
    return bits

def parse_signed_source(src):
    if not src or any(b not in '01' for b in src):return None
    ell=0
    while ell<len(src) and src[ell]=='1':ell+=1
    if ell==0 or ell>=len(src):return None
    if len(src)<2*ell+1:return None
    m=int(src[ell+1:2*ell+1],2)
    if m<6 or m.bit_length()!=ell:return None
    W=(3*m).bit_length();want=2*ell+1+24*m*(W+1)
    if len(src)!=want:return None
    pos=2*ell+1
    D=set();allf={}
    for v in range(2*m):
        if v<m:es=tuple(sorted(((v-1)%m,v,2*m+v)))
        else:
            j=v-m;es=tuple(sorted((m+(j-1)%m,m+j,2*m+j)))
        masks=[]
        for _ in range(4):
            mask=0
            for i,e in enumerate(es):
                sign=int(src[pos]);pos+=1
                varid=int(src[pos:pos+W],2);pos+=W
                if varid!=e+1:return None
                mask|=(sign<<i)
            masks.append(mask)
        allf[v]=tuple(masks)
        if v<m:
            if not is_parity_packet(masks):D.add(v)
        else:
            if not is_parity_packet(masks):return None
    if len(D)==m:return None
    return (m,D,allf)

def main():
    rows=[];checks=0;total_reads=0;total_centroid_calls=0;negative_checks=0
    for m in (6,9,12,24,96):
        for kind in range(4):
            D=({0,1,3} if kind==0 else set(range(0,m-1)) if kind==1 else {i for i in range(m) if i%3!=2} if kind==2 else {0,1})
            F=Tester(m,D,odd=kind%2==1,forced=(kind==3))
            source=encode_original(F)
            parsed=parse_signed_source(source)
            assert parsed is not None and parsed[0]==m and parsed[2]==F.forbidden
            # A random 4-clause packet may accidentally be a parity packet, reducing actual D.
            assert parsed[1].issubset(F.D)
            checks+=1
            # The fast-path D is syntactically inferred in actual source, not trusted externally.
            if parsed[1]!=F.D:
                F.D=parsed[1];F.gD={v:sorted([w for e in F.inc[v] for w in F.edges[e] if w!=v and w in F.D]) for v in F.D}
                F.charge={v:(next(x for x in range(8) if x not in F.forbidden[v]).bit_count()%2) for v in range(F.V) if v not in F.D}
                F.q=0
                for v,b in F.charge.items():F.q^=b
            spectrum=F.path_syndrome()
            sat=F.q in spectrum
            checks+=1
            if m<=12:
                independent=F.solve();assert sat==independent;checks+=1
                total_centroid_calls+=F.rec_calls
            else:
                independent_spectrum={0}
                for component in F.components(F.D):
                    sub=F.direct_dp(component)
                    independent_spectrum={a^b for a in independent_spectrum for b in sub}
                assert independent_spectrum==spectrum
                checks+=1
                independent=F.q in independent_spectrum
            if m==6:
                models=F.exhaustive();assert sat==(models>0);checks+=1
            else:models=None
            if kind==3:
                assert not sat
                # Each exceptional packet independently permits both parities, yet shared edge is inconsistent.
                for v in D:
                    allowed={tri.bit_count()%2 for tri in range(8) if tri not in F.forbidden[v]}
                    assert allowed=={0,1}
                checks+=1
            rows.append(dict(m=m,H=2*m,defects=len(F.D),kind=kind,sat=sat,syndrome_spectrum=sorted(spectrum),models=models,centroid_calls=F.rec_calls,max_centroid_depth=F.max_depth,connected_remainder=True,clauses=len(F.clauses)))
    # Structural parser must reject corrupted literal IDs, truncated, bad alphabet,
    # all-defect outer cycle, and non-parity inner packets.
    G=Tester(6,{0,1,3},odd=True)
    src=encode_original(G); assert parse_signed_source(src) is not None
    for bad in [src[:-1],src+'0',src.replace('0','x',1),src[:15]+('1' if src[15]=='0' else '0')+src[16:]]:
        assert parse_signed_source(bad) is None
        negative_checks+=1
    result=dict(algorithm='constant-state transfer for arbitrary proper subset of outer-cycle defective packets',status='COMPUTATIONAL finite; mathematical theorem requires independently checked proof',seed=47820261107,tested=len(rows),checks=checks,independent_centroid_cases=12,exhaustive_m6_cases=4,centroid_calls=total_centroid_calls,negative_controls=negative_checks,rows=rows)
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
