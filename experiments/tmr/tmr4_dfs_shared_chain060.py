#!/usr/bin/env python3
"""TMR-4/060 source-authenticated shared-chain DFS vs depth layout; no dependencies."""
import json
from collections import Counter
REV='tmr4-dfs-shared-chain060.release1'

def encode(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode('ascii')
def family(m):
    gs=[];p='x0'
    for i in range(1,m+1):
        h=f'g{4*i-4}';a=f'g{4*i-3}';b=f'g{4*i-2}';z=f'g{4*i-1}'
        gs.extend([{'id':h,'a':f'x{2*i-1}','b':f'x{2*i}','op':6},
                   {'id':a,'a':p,'b':h,'op':8},{'id':b,'a':p,'b':h,'op':6},
                   {'id':z,'a':a,'b':b,'op':14}]);p=z
    return encode({'n':2*m+1,'gates':gs[::-1],'out':p})
def pairs(kv):
    d={}
    for k,v in kv:
        if k in d:raise ValueError('duplicate key')
        d[k]=v
    return d
def parse(raw):
    try:c=json.loads(raw.decode('ascii'),object_pairs_hook=pairs)
    except (ValueError,UnicodeError) as e:raise ValueError('invalid encoding') from e
    if encode(c)!=raw or type(c)!=dict or set(c)!={'n','gates','out'}:raise ValueError('not canonical')
    n=c['n'];rr=c['gates']
    if type(n)!=int or n<1 or type(rr)!=list or not rr:raise ValueError('bad sizes')
    if n>2*len(rr):raise ValueError('huge arity preallocation guard')
    g={}
    for r in rr:
        if type(r)!=dict or set(r)!={'id','a','b','op'}:raise ValueError('bad gate shape')
        if type(r['op'])!=int or not 0<=r['op']<=15 or type(r['id'])!=str:raise ValueError('bad gate')
        if r['id'] in g:raise ValueError('duplicate gate')
        g[r['id']]=r
    if set(g)!={f'g{i}' for i in range(len(rr))} or c['out'] not in g:raise ValueError('bad output or ids')
    use=Counter()
    for r in rr:
        for a in (r['a'],r['b']):
            if a not in g and a not in {f'x{i}' for i in range(n)}:raise ValueError('unknown operand')
            use[a]+=1
    if any(use[f'x{i}']==0 for i in range(n)):raise ValueError('unused input')
    depths={};vis={}
    def visit(v):
        if v.startswith('x'):return 0
        if vis.get(v)==1:raise ValueError('cycle')
        if vis.get(v)==2:return depths[v]
        vis[v]=1;r=g[v];depths[v]=1+max(visit(r['a']),visit(r['b']));vis[v]=2
        return depths[v]
    visit(c['out'])
    if len(vis)!=len(g):raise ValueError('dead gates')
    return n,g,c['out'],depths

def schedule(n,g,out,d,mode):
    if mode=='dfs':
        seen=set();seq=[]
        def go(v):
            if v in seen:return
            if v in g:
                for u in sorted({g[v]['a'],g[v]['b']},key=lambda z:(-d.get(z,0),z)):go(u)
            seen.add(v);seq.append(v)
        go(out);return seq
    first={f'x{i}':10**12 for i in range(n)}
    for v,r in g.items():
        for u in (r['a'],r['b']):
            if u.startswith('x'):first[u]=min(first[u],d[v])
    return [v for i in range(1,max(d.values())+1)
            for v in sorted((x for x in first if first[x]==i),key=lambda x:int(x[1:]))
                   +sorted((x for x in g if d[x]==i),key=lambda x:int(x[1:]))]

def prepare(n,g,out,seq):
    pos={v:i for i,v in enumerate(seq)};last={v:-1 for v in seq}
    if len(pos)!=n+len(g):raise AssertionError('missing vertex')
    for v,r in g.items():
        for u in (r['a'],r['b']):
            if pos[u]>=pos[v]:raise AssertionError('wrong topological order')
            last[u]=max(last[u],pos[v])
    last[out]=len(seq)
    live=set();peak=0
    for i,v in enumerate(seq):
        live.add(v)
        live={u for u in live if last[u]!=i}
        peak=max(peak,len(live))
    return last,peak

def run_stage(g,seq,last,state,x,bit):
    d=dict(state);d[x]=bit
    i=seq.index(x)
    while i<len(seq):
        v=seq[i]
        if i!=seq.index(x) and v.startswith('x'):break
        if v in g:
            r=g[v];d[v]=(r['op']>>(2*d[r['a']]+d[r['b']]))&1
        for u in list(d):
            if last[u]==i:del d[u]
        i+=1
    return tuple(sorted(d.items()))

def obdd(n,g,out,seq,last):
    xs=[v for v in seq if v.startswith('x')];states=[{():0}];edges=[]
    for j,x in enumerate(xs):
        follow={};es=[]
        for state,sid in states[-1].items():
            for bit in (0,1):
                target=run_stage(g,seq,last,state,x,bit)
                if j==n-1:
                    assert target[0][0]==out and len(target)==1
                    to=target[0][1]
                else:
                    if target not in follow:follow[target]=len(follow)
                    to=follow[target]
                es.append((sid,bit,to))
        edges.append(es)
        if j<n-1:states.append(follow)
    count={0:1}
    for es in edges:
        new={}
        for src,bit,dst in es:new[dst]=new.get(dst,0)+count[src]
        count=new
    return xs,edges,{'nodes':sum(len(s) for s in states),'arcs':sum(len(x) for x in edges),
                    'accepted':count.get(1,0),'rejected':count.get(0,0)}

def source(g,out,bits):
    memo={f'x{i}':v for i,v in enumerate(bits)}
    def val(v):
        if v not in memo:
            r=g[v];memo[v]=(r['op']>>(2*val(r['a'])+val(r['b'])))&1
        return memo[v]
    return val(out)
def walk(xs,edges,bits):
    node=0
    for i,x in enumerate(xs):
        e=next((e for e in edges[i] if e[0]==node and e[1]==bits[int(x[1:])]),None)
        if e is None:raise AssertionError('missing labelled arc')
        node=e[2]
    return node

def audit():
    o={'revision':REV,'mode':'deterministic exhaustive','seed':None,'cases':[],
       'checks':0,'failures':0,'assignments':0,'path_replays':0,'malformed_rejections':0}
    def ck(v):
        o['checks']+=1
        if not v:o['failures']+=1;raise AssertionError('audit failure')
    for m in range(1,6):
        raw=family(m);n,g,out,d=parse(raw);records=[]
        for mode in ('dfs','depth'):
            seq=schedule(n,g,out,d,mode);last,w=prepare(n,g,out,seq)
            xs,edges,res=obdd(n,g,out,seq,last)
            ck(res['nodes']<=n*(1<<w));ck(res['accepted']==(1<<n)-(1<<m))
            ck(res['accepted']+res['rejected']==(1<<n))
            for a in range(1<<n):
                bits=[a>>i&1 for i in range(n)]
                expected=bits[0] or any(bits[2*i-1]^bits[2*i] for i in range(1,m+1))
                ck(source(g,out,bits)==expected);ck(walk(xs,edges,bits)==expected)
                o['path_replays']+=1
            records.append({'mode':mode,'width':w,**res})
        ck(records[0]['width']<=3);ck(records[1]['width']>=2*m)
        o['assignments']+=1<<n
        o['cases'].append({'m':m,'n':n,'g':len(g),'source_bytes':len(raw),'results':records})
    valid=family(1)
    bad=[valid+b' ',valid.replace(b'"n":3',b'"n":3,"n":3',1),
         valid.replace(b'"op":6',b'"op":16',1),
         valid.replace(b'"out":"g3"',b'"out":"g99"',1),
         b'{"gates":[{"a":"x0","b":"x0","id":"g0","op":8}],"n":1000000000000,"out":"g0"}']
    for b in bad:
        try:parse(b)
        except ValueError:o['malformed_rejections']+=1
        else:raise AssertionError('accepted malformed source')
    return o
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,indent=2))
