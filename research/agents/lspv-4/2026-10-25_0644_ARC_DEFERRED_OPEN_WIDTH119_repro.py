"""LSPV-4 ARC-DEFERRED-OPEN-WIDTH119. Python 3 standard library, no randomness.
This is a finite ordinary proper-3CNF serialization and DPLL audit, NOT FLMV cycles.
"""
import json
from collections import Counter

C=Counter()
def check(z):
    C['assertions']+=1
    assert z

def gam(n):
    s=bin(n)[2:]; return '0'*(len(s)-1)+s

def ung(s,i):
    z=0
    while s[i+z]=='0': z+=1
    return int(s[i+z:i+2*z+1],2),i+2*z+1

def enc(f):
    v=max((abs(x) for c in f for x in c),default=0); w=max(1,v.bit_length())
    s=gam(v+1)+gam(len(f)+1)
    for c in f:
        check(len(c)==3 and len({abs(x) for x in c})==3)
        for x in c:s+=('1' if x<0 else '0')+format(abs(x),f'0{w}b')
    C['written_bits']+=len(s); C['written_zero_bits']+=s.count('0')
    return s

def dec(s):
    C['read_bits']+=len(s); v,p=ung(s,0); m,p=ung(s,p); w=max(1,(v-1).bit_length())
    a=[]
    for _ in range(m-1):
        c=[]
        for _ in range(3):
            x=int(s[p+1:p+1+w],2); check(1<=x<v)
            c.append(-x if s[p]=='1' else x);p+=1+w
        check(len(set(map(abs,c)))==3); a.append(tuple(c))
    check(p==len(s));return tuple(a)

def gadget(x,pos,a,b):
    return tuple(((x if pos else -x),i*a,j*b) for i in (-1,1) for j in (-1,1))

def flatten(g):return tuple(c for x,pos,a,b in g for c in gadget(x,pos,a,b))

def pin(g,b):
    z=max((k for x,_,a,c in g for k in (x,a,c)),default=1)+1
    return g+((1,b,z,z+1),)

def dpll(f):
    C['solver_calls']+=1
    def rec(d):
        while True:
            rest=[]
            for c in f:
                if any(abs(x) in d and d[abs(x)]==(x>0) for x in c):continue
                x=[z for z in c if abs(z) not in d]
                if not x:return False
                rest.append(x)
            if not rest:return True
            units=[c[0] for c in rest if len(c)==1]; change=False
            for x in units:
                k=abs(x);b=x>0
                if k in d and d[k]!=b:return False
                if k not in d:d[k]=b;change=True
            if change:continue
            counts=Counter(abs(x) for c in rest for x in c)
            k=counts.most_common(1)[0][0]
            return rec({**d,k:False}) or rec({**d,k:True})
    return rec({})

def stream(g):
    names=sorted({x for x,_,_,_ in g});last={x:max(i for i,z in enumerate(g) if z[0]==x) for x in names}
    e=[('O',x) for x in names]
    for i,(x,b,a,c) in enumerate(g):
        e.extend([('O',a),('O',c)]);e.extend(('C',z) for z in gadget(x,b,a,c))
        e.extend([('X',a),('X',c)])
        if last[x]==i:e.append(('X',x))
    return e+[('E',None)]

def valid(e):
    seen=set();live=set();f=[];w=0
    for k,z in e:
        C['events_checked']+=1
        if k=='O':check(z>0 and z not in seen);seen.add(z);live.add(z)
        elif k=='C':check(all(abs(x) in live for x in z));f.append(z)
        elif k=='X':check(z in live);live.remove(z)
        elif k=='E':check(not live)
        else:raise ValueError(k)
        w=max(w,len(live))
    check(e[-1]==('E',None))
    return tuple(f),w

def deferred(e):
    seen=set();o=[];high=0
    for k,z in e:
        if k=='O':pass
        elif k=='C':
            for x in sorted({abs(y) for y in z}):
                if x not in seen:o.append(('O',x));seen.add(x)
            o.append((k,z))
        elif k=='X':
            if z in seen:o.append((k,z));seen.remove(z)
        else:check(k=='E' and not seen);o.append((k,z))
        high=max(high,len(seen))
    C['deferred_events']+=len(o)
    return o,high

def audit(g):
    f=flatten(g);s=enc(f);check(dec(s)==f)
    e=stream(g);orig,raw=valid(e);check(orig==f)
    ee,high=deferred(e);norm,nw=valid(ee);check(norm==f and high==nw)
    check(nw<=4)
    return {'bytes_bits':len(s),'raw_width':raw,'deferred_width':nw,'sat':dpll(f),'raw_events':len(e),'deferred_events':len(ee)}

def case(q,sat):
    g=[];a=q+1
    for x in range(1,q+1):g.append((x,True,a,a+1));a+=2
    g.append((1,sat,a,a+1))
    root=audit(tuple(g));check(root['sat']==sat and root['raw_width']==q+2 and root['deferred_width']==4)
    cuts=(0,(q+1)//4,(q+1)//2,3*(q+1)//4,q+1)
    chunks=[tuple(g[cuts[i]:cuts[i+1]]) for i in range(4)]
    halves=[chunks[0]+chunks[1],chunks[2]+chunks[3]]
    first=[];leaves=[]
    for b in (False,True):
        H=[audit(pin(z,b)) for z in halves]
        L=[audit(pin(z,b)) for z in chunks]
        check(H[0]['sat']==all(x['sat'] for x in L[:2]))
        check(H[1]['sat']==all(x['sat'] for x in L[2:]))
        first.append(H);leaves.append(L)
    joined=any(all(x['sat'] for x in hh) for hh in first)
    check(joined==sat)
    naive=all(dpll(flatten(z)) for z in chunks)
    if not sat:check(naive)
    check(max(x['bytes_bits'] for hh in first for x in hh)<root['bytes_bits'])
    check(max(x['bytes_bits'] for ll in leaves for x in ll)<max(x['bytes_bits'] for hh in first for x in hh))
    return {'q':q,'sat':sat,'root':root,'half_max_bits':max(x['bytes_bits'] for hh in first for x in hh),
            'grandchild_max_bits':max(x['bytes_bits'] for ll in leaves for x in ll),
            'named_join':joined,'naive_status_only_AND':naive}

def main():
    cases=[case(q,b) for q in (8,12,16,24,32) for b in (False,True)]
    out={'run_id':'ARC-DEFERRED-OPEN-WIDTH119','method':'deterministic proper3CNF gamma-bit-serialization, independent generic DPLL, two actual levels, both pin values',
         'seed':None,'machine_note':'Python counts are not FLMV bit-time or physical flips',
         'metrics':dict(C),'cases':cases}
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
