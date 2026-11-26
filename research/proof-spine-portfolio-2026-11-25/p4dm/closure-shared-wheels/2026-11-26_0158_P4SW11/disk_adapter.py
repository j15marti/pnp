"""P4SW11: exact native-to-slot face map for ordered zero-flux disk substitutions.
Uses actual native embedding and original IDs; no target is needed to acquire the map.
"""
import networkx as nx,collections as co,itertools as it,random,json,sys,time
from audit import incidence,faces,construct,table
from height import recover

def face_index(emb):
    F=list(faces(emb));return F,{(a,b):i for i,c in enumerate(F) for a,b in zip(c,c[1:]+c[:1])}

def acquire(T):
    R,G=incidence(T);ok,emb=nx.check_planarity(G);assert ok
    result=recover(T,R,G,co.Counter())
    if result in (None,False):return None
    parts,priv,ports,raw,E,equal,sides,n,ref=result
    F,f=face_index(emb);rot=emb.get_data();mr={};disk_orders=[]
    for i,S in enumerate(parts):
        P=set(ports[i]);priv_e={('e',*e) for e,r in priv[i]};nodes={('t',j) for j in S}|priv_e;D={}
        for v in nodes:
            D[v]=[]
            for w in rot[v]:
                if w in nodes:D[v].append(w)
                else:
                    assert v[0]=='t' and v[1] in P and w[0]=='e' and w[1]==0
                    p=('p',v[1]);D[v].append(p);D[p]=[v]
        ee=nx.PlanarEmbedding();ee.set_data(D);ee.check_structure();FF,ff=face_index(ee)
        boundary=[tuple(v[1] for v in c if v[0]=='p') for c in FF if any(v[0]=='p' for v in c)]
        if len(boundary)!=1 or set(boundary[0])!=P or len(boundary[0])!=len(P):return None
        order=list(boundary[0]);disk_orders.append(order)
        slot=[E[j][0] for j in order]
        # Each slot is a contiguous cyclic block, and each actual mode uses exactly one port in each block.
        if any(sum(slot[a]==v and slot[a-1]!=v for a in range(len(slot)))>1 for v in set(slot)):return None
        for v in set(slot):
            ids=[j for j in order if E[j][0]==v]
            assert len(ids)==3 and all(sum(j in mask for j in ids)==1 for mask in raw[i])
            mr[v]=[E[j][1] for j in reversed(ids)]
    for v in {w for u,w in E.values()}:
        mr[v]=[E[t[1]][0] for t in rot['e',0,v[1]]]
    me=nx.PlanarEmbedding();me.set_data(mr);me.check_structure();MF,mf=face_index(me)
    assert len(mr)-len(E)+len(MF)==2
    mapping={}
    for j,(v,w) in E.items():
        a,b=('t',j),('e',0,w[1])
        for nf,mm in [(f[a,b],mf[v,w]),(f[b,a],mf[w,v])]:
            if nf in mapping:assert mapping[nf]==mm,'face splitting in disk replacement'
            mapping[nf]=mm
    assert set(mapping.values())==set(range(len(MF)))
    X=nx.Graph();X.add_nodes_from(mapping)
    for j,(v,w) in E.items():
        a,b=('t',j),('e',0,w[1]);X.add_edge(f[a,b],f[b,a])
    assert nx.is_connected(X), 'exposed native dual disconnected'
    root=min(mapping);mroot=mapping[root]
    # native y=3x-1 orientation plus rows->tuples; boundary color0 is plus.
    nsides={}
    for j,t in enumerate(T):
        for c,e in enumerate(t):
            u,v=('t',j),('e',c,e)
            if c in (0,1):u,v=v,u
            nsides[j,c]=(f[u,v],f[v,u])
    msides={j:(mf[w,v],mf[v,w]) for j,(v,w) in E.items()}
    def integrate(sides,n,root,val,mod=None):
        adj=co.defaultdict(list)
        for j,(l,r) in sides.items():
            d=val(j);adj[r].append((l,d));adj[l].append((r,-d))
        h={root:0};Q=[root]
        for u in Q:
            for v,d in adj[u]:
                z=h[u]+d
                if mod:z%=mod
                if v not in h:h[v]=z;Q.append(v)
                else:assert h[v]==z
        assert len(h)==n
        return h
    nr=integrate(nsides,len(F),root,lambda j:-1,3);rr=integrate(msides,len(MF),mroot,lambda j:-1,3)
    assert all(nr[f]==rr[g] for f,g in mapping.items())
    def compare(W):
        W=set(W);assert all(sum(j in W for j in row)==1 for row in R.values())
        H=integrate(nsides,len(F),root,lambda jc:3*int(jc[0] in W)-1);K=integrate(msides,len(MF),mroot,lambda j:3*int(j in W)-1)
        assert all(H[f]==K[g] for f,g in mapping.items())
        assert all((H[f]-nr[f])//3==(K[g]-rr[g])//3 for f,g in mapping.items())
        return H,K
    counts=co.Counter(mapping.values())
    stats=dict(tuples=len(T),native_faces=len(F),macro_faces=len(MF),mapped_native_faces=len(mapping),retired_internal_faces=len(F)-len(mapping),merged_exterior_faces=len(mapping)-len(MF),max_merged_fiber=max(counts.values()),regions=len(parts),ports=len(E),disk_orders=disk_orders,face_map=mapping)
    return result,stats,compare

def run(k,mode):
    T,meta=construct(k,mode);R,G=incidence(T);A,stats,compare=acquire(T);parts,priv,ports,raw,E,equal,sides,n,ref=A
    rng=random.Random(261126110+k);words=[];checks=[]
    if k==2 and mode=='coupled':
        for masks in it.product(*[list(B) for B in raw]):
            occ=co.Counter(E[j][1] for mask in masks for j in mask)
            if all(occ[r]==1 for u,r in E.values()):words.append(set(it.chain.from_iterable(B[m] for B,m in zip(raw,masks))))
    # Three full canonical phase controls and independent vertex modes, from generator metadata only.
    byid={min(s):i for i,s in enumerate(parts)}
    for trial in range(11):
        phase={v:rng.randrange(2)*2 for v in {s['grid_vertex'] for s in meta['spec'].values()}}
        W=set()
        for S in meta['spec'].values():
            i=byid[min(S['ids'])];j=trial if trial<3 else phase[S['grid_vertex']];mask=tuple(S['mode_ports'][j]);W.update(raw[i][mask])
        words.append(W)
    for W in words:
        H,K=compare(W);checks.append(dict(witness=sorted(W),native_height_range=[min(H.values()),max(H.values())],macro_height_range=[min(K.values()),max(K.values())]))
    stats['witness_checks']=checks
    print(mode,k,{z:v for z,v in stats.items() if z not in ('face_map','disk_orders','witness_checks')},'witnesses',len(checks),flush=True)
    json.dump(stats,open(f'disk_{mode}{k}.json','w'),indent=2)

if __name__=='__main__':run(int(sys.argv[1]),sys.argv[2])
