#!/usr/bin/env python3
"""ARC-PADDED-GUEST-GATE157: real two-level ordinary DIMACS SAT calls.
Padding step counts are symbolic and are NOT measured FLMV machine time.
"""
import itertools,json

def pack(cs,n):
    return ('p cnf %d %d\n'%(n,len(cs))+''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode()
def unpack(buf):
    ls=buf.decode().splitlines();p=ls[0].split();assert p[:2]==['p','cnf']
    n,m=map(int,p[2:]);cs=[]
    for row in ls[1:]:
        q=list(map(int,row.split()));assert q and q[-1]==0
        c=tuple(q[:-1]);assert all(0<abs(z)<=n for z in c);cs.append(c)
    assert len(cs)==m
    return tuple(cs),n
def sat(cs,n):
    return any(all(any((bs[abs(z)-1]==(z>0)) for z in c) for c in cs)
               for bs in itertools.product((False,True),repeat=n))
def pin(cs,v,b):
    return tuple(tuple(z for z in c if abs(z)!=v) for c in cs
                 if not any((z>0)==b for z in c if abs(z)==v))
class Base:
    def call(self,b):
        c,n=unpack(b);return sat(c,n),0
class Pad:
    def __init__(self,d,inner):self.d,self.inner=d,inner
    def call(self,b):
        answer,cost=self.inner.call(b)
        return answer,cost+len(b)**self.d
    def peel(self):return self.inner

U=tuple(tuple(s[i]*(i+1) for i in range(3))
        for s in itertools.product((-1,1),repeat=3))
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
cases={'SAT3':(((1,2,3),),3),'UNSAT8':(U,3),
       'Y6':(Y,6),'2SAT_UNSAT':(((1,2),(-1,2),(1,-2),(-1,-2)),2),
       'Horn_SAT':(((1,),(-1,2),(2,3)),3),
       'empty_UNSAT':(((),),2)}
rows=[]
for name,(f,n) in cases.items():
    src=pack(f,n);direct=sat(f,n);q=Pad(2,Pad(1,Base()))
    assert q.call(src)[0]==q.peel().call(src)[0]==q.peel().peel().call(src)[0]==direct
    calls=[]
    for a,b in itertools.product((False,True),repeat=2):
        c1=pack(pin(f,1,a),n);c2=pack(pin(pin(f,1,a),2,b),n)
        assert unpack(c2)[1]==n
        answer,cost=q.call(c2)
        calls.append((len(c1),len(c2),answer,cost))
    assert any(z[2] for z in calls)==direct
    rows.append({'name':name,'sat':direct,'N':len(src),
                 'leaf_calls':len(calls),'max_leaf_length':max(z[1] for z in calls),
                 'charged_pad_cost':sum(z[3] for z in calls)})
print(json.dumps({'status':'PASS','note':'padding costs symbolic; not FLMV steps',
                  'cases':rows,'calls':sum(x['leaf_calls'] for x in rows)},indent=2))
