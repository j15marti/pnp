#!/usr/bin/env python3
"""Deterministic typed ER2 local macro producer. Python 3 stdlib only.
python lspv3_357_er2_macros.py --cert > summary.json
Then node lspv3_357_independent_verify.js lspv3_357_macro_certs.json
"""
import json, itertools, sys

def canon(items):
    a=frozenset(items)
    return None if any(-v in a for v in a) else tuple(sorted(a,key=lambda z:(abs(z),z<0)))

class Macro:
    def __init__(self):
        self.names={};self.defs=[];self.source=[];self.source_tags=[]
    def v(self,name):
        if name not in self.names:self.names[name]=len(self.names)+1
        return self.names[name]
    def add(self,lits,tag='hyp'):
        c=canon(lits)
        if c is None:return
        self.source.append(c);self.source_tags.append(tag)
    def signed_and(self,o,a,b):
        assert o>0 and abs(a)!=abs(b)
        for j,cl in enumerate([[-o,a],[-o,b],[o,-a,-b]]):
            self.add(cl,tag='gate:'+str(len(self.defs))+':'+str(j))
        self.defs.append((o,a,b))
    def xor(self,name,x,y):
        assert abs(x)!=abs(y),'ER2 forbids repeated absolute input IDs'
        f=self.v(name+'$f');d=self.v(name+'$d');e=self.v(name+'$e')
        self.signed_and(d,x,-y)
        self.signed_and(e,-x,y)
        self.signed_and(f,-d,-e)
        return -f

    def eq(self,a,b):
        self.add([-a,b]);self.add([a,-b])
    def parity(self,xs,s):
        for bits in itertools.product((0,1),repeat=len(xs)):
            if sum(bits)%2 != s:
                self.add([(-v if bit else v) for v,bit in zip(xs,bits)])

def run(m,keep,target,verbose=False):
    C={c:('SRC',i) for i,c in enumerate(m.source)}
    derived=[];peak=len(C)
    for p in sorted(set(m.names.values())-set(keep)):
        pos=[c for c in C if p in c];neg=[c for c in C if -p in c]
        new={}
        for a in pos:
            for b in neg:
                cl=canon([x for x in a if x!=p]+[x for x in b if x!=-p])
                if cl is None or cl in C or cl in new:continue
                new[cl]=(a,b,p)
        derived.extend(new.items())
        C={c:r for c,r in C.items() if p not in c and -p not in c}
        C.update({c:('RES',t) for c,t in new.items()})
        peak=max(peak,len(C))
    assert target in C,('missing output clause',target)
    auth=set(m.source)
    for c,(a,b,p) in derived:
        assert a in auth and b in auth and p in a and -p in b
        assert canon([x for x in a if x!=p]+[x for x in b if x!=-p])==c
        auth.add(c)
    return dict(vars=len(m.names),source_clauses=len(m.source),
       paid_DEF=len(m.defs),paid_RES=len(derived),
       peak_active_clauses=peak,projected_clauses=len(C),
       target=list(target),projected=[list(c) for c in C],
       cert_derived=[(list(c),list(a),list(b),p) for c,(a,b,p) in derived] if verbose else None)

def make_case(case):
    m=Macro()
    if case in ('vertex_0','vertex_1'):
        a,b,c=[m.v(z) for z in 'abc'];t=m.xor('t',a,b);r=m.xor('r',t,c)
        m.parity([a,b,c],int(case[-1]))
        return m,{abs(r)},canon([r if case[-1]=='1' else -r])
    if case in ('vertex_copy_0','vertex_copy_1'):
        a,b,c=[m.v(z) for z in 'abc'];d,e,f=[m.v(z) for z in 'def']
        for x,y in ((a,d),(b,e),(c,f)):m.eq(x,y)
        t=m.xor('t',d,e);r=m.xor('r',t,f)
        m.parity([a,b,c],int(case[-1]))
        return m,{abs(r)},canon([r if case[-1]=='1' else -r])
    if case=='assoc':
        a,b,c=[m.v(z) for z in 'abc']
        ab=m.xor('ab',a,b);left=m.xor('left',ab,c)
        bc=m.xor('bc',b,c);right=m.xor('right',a,bc)
        return m,{abs(left),abs(right)},canon([-left,right])
    if case=='commute':
        a,b=[m.v(z) for z in 'ab'];t=m.xor('t',a,b);u=m.xor('u',b,a)
        return m,{abs(t),abs(u)},canon([-t,u])
    if case=='congruence':
        a,b,c=[m.v(z) for z in 'abc'];m.eq(a,b)
        t=m.xor('t',a,c);u=m.xor('u',b,c)
        return m,{abs(t),abs(u)},canon([-t,u])
    if case=='cancel':
        a=m.v('a');s=m.v('s');u=m.xor('u',a,s);t=m.xor('t',a,u)
        return m,{abs(t),abs(s)},canon([-t,s])
    if case=='cancel_equiv':
        a,b,s=[m.v(z) for z in 'abs'];m.eq(a,b)
        u=m.xor('u',b,s);t=m.xor('t',a,u)
        return m,{abs(t),abs(s)},canon([-t,s])
    if case=='clone':
        one=m.v('one');z=m.v('z');q=m.v('q');m.add([one])
        m.signed_and(q,one,z)
        return m,{z,q},canon([q,-z])
    if case=='neutral':
        a=m.v('a');zero=m.v('zero');m.add([-zero]);t=m.xor('t',a,zero)
        return m,{abs(a),abs(t)},canon([-a,t])
    if case=='value':
        a=m.v('a');b=m.v('b');m.add([a]);m.add([-b]);t=m.xor('t',a,b)
        return m,{abs(t)},canon([t])
    raise ValueError(case)

def main():
    names=('vertex_0','vertex_1','vertex_copy_0','vertex_copy_1','assoc',
       'commute','congruence','cancel','cancel_equiv','clone','neutral','value')
    results={};certs={}
    for name in names:
        m,keep,target=make_case(name);r=run(m,keep,target,True)
        results[name]={k:v for k,v in r.items() if k!='cert_derived'}
        certs[name]=dict(vars=m.names,defs=m.defs,
           source=[dict(clause=list(c),tag=t) for c,t in zip(m.source,m.source_tags)],
           steps=r['cert_derived'],target=list(target),keep=sorted(keep))
    if '--cert' in sys.argv:
        with open('lspv3_357_macro_certs.json','w') as f:
            json.dump(certs,f,separators=(',',':'))
    print(json.dumps(dict(status='COMPUTATIONAL',results=results),indent=2))

if __name__=='__main__':main()
