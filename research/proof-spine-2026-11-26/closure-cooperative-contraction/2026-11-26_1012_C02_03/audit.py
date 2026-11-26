import itertools as I, collections as C, functools as F, json, time
Q=13

def patch(q):
    V=[(a,b,q-a-b) for a in range(q+1) for b in range(q-a+1)]
    v=lambda a,b:(a,b,q-a-b)
    T=[]
    for a in range(q):
        for b in range(q-a):
            T.append(tuple(sorted((v(a,b),v(a+1,b),v(a,b+1)))))
            if a+b+2<=q:T.append(tuple(sorted((v(a+1,b),v(a,b+1),v(a+1,b+1)))))
    return V,T
V,T=patch(Q); IX={v:i for i,v in enumerate(V)}; MASK=[sum(1<<IX[v] for v in t) for t in T]
INC=[[j for j,b in enumerate(MASK) if b>>i&1] for i in range(len(V))]

def cover(VS,ts,zero=(),one=()):
    vs=sorted(VS); ix={v:i for i,v in enumerate(vs)}
    bs=[sum(1<<ix[v] for v in t) if set(t)<=VS else 0 for t in ts]; Z=set(zero); R=(1<<len(vs))-1
    for j in one:
        if j in Z or not bs[j] or R&bs[j]!=bs[j]:return None
        R^=bs[j]
    inc=[[] for v in vs]
    for j,b in enumerate(bs):
        if b and j not in Z:
            for v in ts[j]:inc[ix[v]].append(j)
    @F.lru_cache(None)
    def rec(r):
        if not r:return ()
        poss=None; t=r
        while t:
            u=t&-t;t^=u
            cand=[j for j in inc[u.bit_length()-1] if r&bs[j]==bs[j]]
            if not cand:return None
            if poss is None or len(cand)<len(poss):poss=cand
        for j in poss:
            a=rec(r^bs[j])
            if a is not None:return (j,)+a
        return None
    w=rec(R)
    return None if w is None else tuple(one)+w

def vertices(E,c):return {v for v in V if min(v)>0 or (v.count(0)==1 and E[v.index(0)]) or (v.count(0)==2 and c)}
@F.lru_cache(None)
def local(E,c,g=()):
    if c and E!=(1,1,1):return None
    return cover(vertices(E,c),T,[j for j,b in g if not b],[j for j,b in g if b])
def geom(k):
    _,P=patch(k)
    return sorted({tuple(sorted(tuple(s[i]*v[i] for i in range(3)) for v in t)) for s in I.product((-1,1),repeat=3) for t in P})

def lift(f,t):return tuple(sorted(tuple(sum(w*v[d] for w,v in zip(b,f)) for d in range(3)) for b in t))
def edges(f):return [tuple(v for j,v in enumerate(f) if j!=i) for i in range(3)]
def verify(fs,w,g=()):
    count=C.Counter(v for j in w for v in fs[j]); assert set(count)=={v for f in fs for v in f} and set(count.values())=={1}
    assert all((j in w)==b for j,b in g)

def closure(fs,g):
    # Exact-one fixed point on original IDs; no semantic oracle.
    pins=dict(g); inc=C.defaultdict(list)
    for j,f in enumerate(fs):
        for v in f:inc[v].append(j)
    while True:
        before=len(pins)
        for L in inc.values():
            yes=[j for j in L if pins.get(j)==1];live=[j for j in L if pins.get(j)!=0]
            if len(yes)>1 or not live:return None
            if yes:
                for j in L:
                    if j!=yes[0]:pins[j]=0
            elif len(live)==1:pins[live[0]]=1
        if len(pins)==before:return pins

class Solver:
    def __init__(self,b,r):
        self.fs=[geom(b*Q**i) for i in range(r+1)];self.r=r;self.cache={};self.calls=0;self.hits=0;self.words=0;self.loc=0
        self.ed=[];self.parent=[None];self.maps=[None]
        for fs in self.fs:
            ed=C.defaultdict(list)
            for j,f in enumerate(fs):
                for e in edges(f):ed[e].append(j)
            assert all(len(a)==2 for a in ed.values());self.ed.append(ed)
        for i in range(1,r+1):
            ids={f:j for j,f in enumerate(self.fs[i])};p=[None]*len(ids);maps=[]
            for j,f in enumerate(self.fs[i-1]):
                a=tuple(ids[lift(f,t)] for t in T);maps.append(a)
                for k,z in enumerate(a):assert p[z] is None;p[z]=(j,k)
            assert all(v is not None for v in p);self.parent.append(p);self.maps.append(maps)
    def solve(self,i,g):
        g=tuple(sorted(g));key=(i,g);self.calls+=1
        if key in self.cache:self.hits+=1;return self.cache[key]
        fs=self.fs[i];pins=closure(fs,g)
        if pins is None:self.cache[key]=None;return None
        if i==0:
            w=cover({v for f in fs for v in f},fs,[j for j,b in g if not b],[j for j,b in g if b]); ans=None if w is None else frozenset(w)
            self.cache[key]=ans;return ans
        # Only explicit input pins create recursive keys; sound closure pins redundant.
        ag=C.defaultdict(list)
        for j,b in g:
            a,k=self.parent[i][j];ag[a].append((k,b))
        A=sorted(ag);ed=self.ed[i-1];coarse=self.fs[i-1]
        E=sorted({e for a in A for e in edges(coarse[a])});B=sorted({j for e in E for j in ed[e]})
        options={}
        for a in A:
            for bits in I.product((0,1),repeat=3):
                for c in (0,1):
                    w=local(bits,c,tuple(sorted(ag[a])));self.loc+=1
                    if w is not None:options[a,bits,c]=w
        if any(not any(k[0]==a for k in options) for a in A):self.cache[key]=None;return None
        for z in I.product((0,1),repeat=len(B)):
            sig=dict(zip(B,z))
            if any(sig[u] and sig[v] for u,v in (ed[e] for e in E)):continue
            free=[e for e in E if not any(sig[j] for j in ed[e])]
            fixed={e:next(j for j in ed[e] if sig[j]) for e in E if any(sig[j] for j in ed[e])}
            feasible=None
            for o in I.product((0,1),repeat=len(free)):
                self.words+=1;own=fixed|{e:ed[e][b] for e,b in zip(free,o)}
                if all((a,tuple(int(own[e]==a) for e in edges(coarse[a])),sig[a]) in options for a in A):feasible=own;break
            if feasible is None:continue
            w=self.solve(i-1,tuple(zip(B,z)))
            if w is None:continue
            own=dict(feasible)
            for e,(a,b) in ed.items():
                if e not in own:own[e]=a if a in w else b if b in w else min(a,b)
            out=set()
            for a,f in enumerate(coarse):
                bits=tuple(int(own[e]==a) for e in edges(f)); c=int(a in w)
                v=options[a,bits,c] if a in ag else local(bits,c)
                assert v is not None;out.update(self.maps[i][a][j] for j in v)
            ans=frozenset(out);verify(fs,ans,g);self.cache[key]=ans;return ans
        self.cache[key]=None;return None
    def cone(self,g):
        S={j for j,b in g};out=[]
        for i in range(self.r,0,-1):
            A={self.parent[i][j][0] for j in S};B={j for a in A for e in edges(self.fs[i-1][a]) for j in self.ed[i-1][e]};out.append([len(S),len(A),len(B)]);S=B
        return out
    def stats(self):return dict(calls=self.calls,hits=self.hits,keys=len(self.cache),edge_words=self.words,local_queries=self.loc)

def main():
    # Independently acquire all nine constant patch templates and verify exact coverage.
    sizes=[]
    for E in I.product((0,1),repeat=3):
        w=local(E,0);assert w is not None;verify_local(E,0,w);sizes.append(len(w))
    w=local((1,1,1),1);assert w is not None;verify_local((1,1,1),1,w);sizes.append(len(w))
    results={'patch_sizes':sizes,'tests':[]}
    for b,r in [(1,1),(4,1),(1,2)]:
        s=Solver(b,r);w=s.solve(r,());assert w is not None;verify(s.fs[r],w)
        # Pick one selected triangle in a nonselected macroface interior, delete it.
        g=((min(w),0),);v=s.solve(r,g);assert v is not None;verify(s.fs[r],v,g)
        # Genuine native UNSAT neighbor: require two triangles sharing a vertex.
        j=min(w);k=next(k for k,f in enumerate(s.fs[r]) if k!=j and set(f)&set(s.fs[r][j]));bad=((j,1),(k,1));good=((j,1),)
        assert s.solve(r,good) is not None and closure(s.fs[r],bad) is None
        results['tests'].append(dict(base=b,depth=r,triples=len(s.fs[r]),guard_delete=list(g),guard_positive=list(good),guard_negative=list(bad),cone=s.cone(g),stats=s.stats()));print(results['tests'][-1],flush=True)
    # Native SAT outside whole-edge template: split a shared edge between two unselected patches.
    s=Solver(1,1);w0=s.solve(0,());w=s.solve(1,());co=s.fs[0];ed=s.ed[0];found=None
    for e,(a,b) in ed.items():
        if a in w0 or b in w0:continue
        # Recover original chosen patch boundary masks from native witness.
        own={}
        for p in (a,b):
            ids=s.maps[1][p];used={v for j,t in enumerate(T) if ids[j] in w for v in t}
            E=tuple(int(any(v.count(0)==1 and v[i]==0 for v in used)) for i in range(3));own[p]=E
        ia=edges(co[a]).index(e);ib=edges(co[b]).index(e)
        if not own[a][ia]:a,b=b,a;ia,ib=ib,ia
        if not own[a][ia] or own[b][ib]:continue
        ea,eb=vertices(own[a],0),vertices(own[b],0)
        line=sorted(v for v in V if v.count(0)==1 and v[ia]==0)
        # Map actual shared boundary coordinates back to patch b.
        bm={lift(co[b],(v,))[0]:v for v in V if v.count(0)==1 and v[ib]==0}
        for lo in range(10):
            moved=set(line[lo:lo+3]);other={bm[lift(co[a],(v,))[0]] for v in moved}
            u=cover(ea-moved,T);v=cover(eb|other,T)
            if u is None or v is None:continue
            new=(set(w)-set(s.maps[1][a])-set(s.maps[1][b]))|{s.maps[1][a][j] for j in u}|{s.maps[1][b][j] for j in v}
            aa=next(j for j in u if any(x in set(line)-moved for x in T[j]));bb=next(j for j in v if any(x in other for x in T[j]));g=((s.maps[1][a][aa],1),(s.maps[1][b][bb],1));verify(s.fs[1],new,g)
            assert closure(s.fs[1],g) is not None;assert s.solve(1,g) is None
            found=dict(guards=g,native_witness=sorted(new),patches=[a,b],moved=sorted(moved),cone=s.cone(g),stats=s.stats());break
        if found:break
    results['native_sat_template_no']=found;print('split control',None if found is None else {k:v for k,v in found.items() if k!='native_witness'},flush=True)
    json.dump(results,open('/mnt/data/C02_03/results.json','w'),indent=2)

def verify_local(E,c,w):
    v=[x for j in w for x in T[j]];assert len(v)==len(set(v)) and set(v)==vertices(E,c)
if __name__=='__main__':main()
