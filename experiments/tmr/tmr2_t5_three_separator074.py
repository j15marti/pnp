#!/usr/bin/env python3
"""TMR-2/074: source-authenticated three-terminal K(h,h) T5 counting.
Canonical input: p t5 n m, n 'v i' lines, m sorted 'a u v' lines.
Run with --audit or source-file path; CPython standard library only.
"""
import json, random, sys
from collections import defaultdict

REV = 'tmr2-t5-3sep074-py.v1'
SEED = 202611171912

def beat(a,b): return (b-a)%5 in (1,3)
def encode(n,edges):
    e=sorted(edges)
    return f'p t5 {n} {len(e)}\n' + ''.join(f'v {i}\n' for i in range(n)) + ''.join(f'a {u} {v}\n' for u,v in e)
def parse(source):
    if not source.endswith('\n') or '\r' in source or not source.isascii(): raise ValueError('ASCII/newline')
    lines=source[:-1].split('\n'); head=lines[0].split(' ')
    if len(head)!=4 or head[:2]!=['p','t5']: raise ValueError('header')
    def integer(s): return bool(s) and (s=='0' or (s[0] in '123456789' and s.isdigit()))
    if not integer(head[2]) or not integer(head[3]): raise ValueError('integer')
    n,m=map(int,head[2:]); L=len(source)
    if n>L or m>L or len(lines)!=1+n+m: raise ValueError('count')
    if any(lines[1+i]!=f'v {i}' for i in range(n)): raise ValueError('declarations')
    edges=[]
    for s in lines[1+n:]:
        f=s.split(' ')
        if len(f)!=3 or f[0]!='a' or not integer(f[1]) or not integer(f[2]): raise ValueError('arc')
        u,v=map(int,f[1:])
        if u>=n or v>=n: raise ValueError('range')
        edges.append((u,v))
    if len(set(edges))!=m or edges!=sorted(edges) or source!=encode(n,edges): raise ValueError('canonical')
    return n,edges

def family(h,b,kind='base'):
    assert h>=4 and b>=2
    terminals=[0,1,2]; edges=[]; idx=3
    for _ in range(b):
        priv=list(range(idx,idx+h-3));idx+=h-3
        sinks=list(range(idx,idx+h));idx+=h
        edges.extend((u,w) for u in terminals+priv for w in sinks)
    extras={'base':[], 'one':[(0,1)], 'yes':[(0,1),(0,2)], 'no':[(0,1),(1,2)], 'opposite':[(0,1),(1,0)]}
    edges.extend(extras[kind]);return idx,sorted(edges)

def recognize(n,edges):
    if n<13 or any(u==v for u,v in edges): return None
    outs=[set() for _ in range(n)];ins=[set() for _ in range(n)]
    for u,v in edges: outs[u].add(v);ins[v].add(u)
    sinks={v for v in range(n) if not outs[v]}
    if not sinks:return None
    h=len(ins[next(iter(sinks))]);q=len(sinks)
    if h<4 or q%h or q//h<2 or any(len(ins[w])!=h for w in sinks):return None
    b=q//h
    if n!=3+b*(2*h-3):return None
    tosink=[len(outs[v]&sinks) for v in range(n)]
    terminals={v for v in range(n) if tosink[v]==q}
    if len(terminals)!=3:return None
    priv=set(range(n))-sinks-terminals
    if len(priv)!=b*(h-3) or any(tosink[v]!=h for v in priv):return None
    groups=defaultdict(list)
    for v in priv:
        groups[frozenset(outs[v]&sinks)].append(v)
    if len(groups)!=b or any(len(key)!=h or len(xs)!=h-3 for key,xs in groups.items()):return None
    if set().union(*groups.keys())!=sinks or sum(len(k) for k in groups)!=q:return None
    expected=set()
    for group,vertices in groups.items():
        for u in terminals.union(vertices):
            for w in group:expected.add((u,w))
    given=set(edges)
    if not expected<=given:return None
    extras=given-expected
    if any(u not in terminals or v not in terminals for u,v in extras):return None
    return h,b,tuple(sorted(terminals)),tuple(sorted(extras)),tuple((tuple(sorted(k)),tuple(sorted(v))) for k,v in groups.items())

def fblock(labels,h):
    common=set(range(5))
    for a in labels: common&={(a+1)%5,(a+3)%5}
    r=h-3
    if len(common)==2:return 2**h+2*(2**r-1)
    if len(common)==1:return 2**r
    return 0

def fast(n,edges):
    cert=recognize(n,edges)
    if cert is None:return None
    h,b,terminals,extra,_=cert
    total=0; witness=None
    for a in range(5):
        for d in range(5):
            for e in range(5):
                labels=dict(zip(terminals,(a,(a+d)%5,(a+e)%5)))
                if any(not beat(labels[u],labels[v]) for u,v in extra):continue
                f=fblock(list(labels.values()),h)
                total+=f**b
                if f and witness is None:
                    x=[None]*n
                    for u,v in labels.items():x[u]=v
                    for sinks,priv in cert[4]:
                        for u in priv:x[u]=a
                        options=set.intersection(*({(labels[t]+1)%5,(labels[t]+3)%5} for t in terminals))
                        target=min(options)
                        for w in sinks:x[w]=target
                    if all(x[v] is not None for v in range(n)) and all(beat(x[u],x[v]) for u,v in edges):witness=x
    assert (witness is not None)==(total>0)
    return total,witness,cert

def reference(n,edges):
    # Independently enumerate all source-side labels and integrate each sink's outgoing constraints.
    outs=[set() for _ in range(n)];ins=[set() for _ in range(n)]
    for u,v in edges:outs[u].add(v);ins[v].add(u)
    src=[v for v in range(n) if outs[v]]
    sinks=[v for v in range(n) if not outs[v]]
    x=[0]*n;count=0
    def go(i):
        nonlocal count
        if i==len(src):
            if any(not beat(x[u],x[v]) for u,v in edges if v in src):return
            p=1
            for w in sinks:
                p*=sum(all(beat(x[u],val) for u in ins[w]) for val in range(5))
                if not p:return
            count+=p;return
        u=src[i]
        for a in range(5):x[u]=a;go(i+1)
    go(0);return count

def brute(n,edges):
    # Complete iterative original-label backtracking, with no recursion-depth limit.
    x=[0]*n; total=0; i=0
    inbound=[[] for _ in range(n)]
    for u,v in edges:inbound[max(u,v)].append((u,v))
    while i>=0:
        if i==n:
            total+=1; i-=1
            if i>=0:x[i]+=1
        elif x[i]==5:
            x[i]=0; i-=1
            if i>=0:x[i]+=1
        elif all(beat(x[u],x[v]) for u,v in inbound[i]):i+=1
        else:x[i]+=1
    return total

def runaudit():
    rng=random.Random(SEED);checks=0;case_count=0;bad=0;records=[]
    def check(cond,label):
        nonlocal checks,bad
        checks+=1
        if not cond:bad+=1;raise AssertionError(label)
    for h in range(4,10):
        for d in range(5):
            for e in range(5):
                colors=(0,d,e);r=h-3
                # independent explicit private-source choices, sink choices counted with product.
                actual=0
                def go(k,chosen):
                    nonlocal actual
                    if k==r:
                        actual+=sum(all(beat(u,w) for u in colors+tuple(chosen)) for w in range(5))**h
                        return
                    for a in range(5):go(k+1,chosen+[a])
                if h<=7:go(0,[]);check(actual==fblock(colors,h),'block transfer')
                else:check(fblock(colors,h)>=0,'positive integer')
    for h,b in [(4,2),(4,3),(5,2),(5,3),(6,2),(8,6),(20,30)]:
        for kind in ['base','one','yes','no','opposite']:
            n,ed=family(h,b,kind);src=encode(n,ed)
            check(parse(src)==(n,ed),'parser');got=fast(n,ed)
            check(got is not None,'recognized')
            z,w,c=got
            expected={'base':5*((2**h+2*(2**(h-3)-1))**b+6*(2**(h-3))**b),
              'one':10*2**(b*(h-3)), 'yes':5*2**(b*(h-3)), 'no':0,'opposite':0}[kind]
            check(z==expected,'formula')
            check((w is not None)==(z>0),'witness')
            if (h<=5 and b<=2) or (h==4 and b==3):
                check(reference(n,ed)==z,'independent direct enumeration')
            if h==4 and b==2 and kind in ['base','yes','no']:
                # Full original-label brute may still prune quickly on this 13-vertex source.
                check(brute(n,ed)==z,'brute original five labels')
            perm=list(range(n));rng.shuffle(perm)
            ed2=sorted((perm[u],perm[v]) for u,v in ed)
            check(fast(*parse(encode(n,ed2)))[0]==z,'permutation')
            records.append({'h':h,'blocks':b,'kind':kind,'vertices':n,'arcs':len(ed),'count':str(z),'treewidth':h})
            case_count+=1
    n,ed=family(4,2)
    check(recognize(n,ed[:-1]) is None,'missing original arc')
    check(recognize(n,ed+[(4,3)]) is None,'unexpected original arc')
    for source in [encode(n,ed).rstrip('\n'),encode(n,ed).replace('v 1\n','v 01\n'),encode(n,ed).replace('p t5','p   t5')]:
        try:parse(source);check(False,'malformed accepted')
        except ValueError:check(True,'malformed rejected')
    return {'revision':REV,'seed':SEED,'assertions':checks,'failures':bad,'family_cases':case_count,
        'records':records,'status':'COMPUTATIONAL finite tests; symbolic family theorem independent of tests'}

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--audit':print(json.dumps(runaudit(),indent=2))
    else:
        with open(sys.argv[1] if len(sys.argv)>1 else '/dev/stdin',encoding='utf8') as f:source=f.read()
        n,ed=parse(source);result=fast(n,ed)
        if result is None: print(brute(n,ed))
        else:print(result[0])
