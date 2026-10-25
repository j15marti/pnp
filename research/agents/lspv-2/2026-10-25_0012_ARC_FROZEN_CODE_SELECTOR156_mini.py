#!/usr/bin/env python3
"""Finite ARC frozen-code control, not a FLMV machine benchmark."""
import hashlib, json
from itertools import product

def gm(k):
    b=bin(k)[2:]
    return '0'*(len(b)-1)+b

def rg(s,i):
    z=0
    while i+z<len(s) and s[i+z]=='0':z+=1
    if i+2*z+1>len(s):raise ValueError('gamma truncated')
    return int(s[i+z:i+2*z+1],2),i+2*z+1

def enc(n,cs):
    return gm(n+1)+gm(len(cs)+1)+''.join(gm(len(c)+1)+''.join(gm(abs(v))+str(int(v<0)) for v in c) for c in cs)

def dec(s):
    if not s or set(s)-set('01'):raise ValueError('not bits')
    n,i=rg(s,0);m,i=rg(s,i);n-=1;m-=1;cs=[]
    for _ in range(m):
        z,i=rg(s,i);c=[]
        for _ in range(z-1):
            v,i=rg(s,i)
            if v<1 or v>n or i>=len(s):raise ValueError('bad literal')
            c.append(v if s[i]=='0' else -v);i+=1
        cs.append(tuple(c))
    if i!=len(s):raise ValueError('trailing bits')
    return n,tuple(cs)

def pin(cs,x,b):
    return tuple(tuple(v for v in c if abs(v)!=x) for c in cs if not any(abs(v)==x and (v>0)==b for v in c))

def sat(cs):
    if not cs:return True
    if any(not c for c in cs):return False
    u=next((c[0] for c in cs if len(c)==1),None)
    if u is not None:return sat(pin(cs,abs(u),u>0))
    x=abs(cs[0][0]);return sat(pin(cs,x,0)) or sat(pin(cs,x,1))

def calc(n,cs,tag=False,pad=0):
    tr=[];levels=[];writes=0
    def ask(f,kind):
        nonlocal writes
        z=enc(n,f);assert dec(z)==(n,f)
        writes+=len(z)
        for _ in range(pad):pass
        v=sat(f)
        tr.append((kind,hashlib.sha256(z.encode()).hexdigest(),v,len(z)))
        return v
    def walk(f,d):
        nonlocal writes
        z=enc(n,f);assert dec(z)==(n,f)
        writes+=len(z);levels.append((d,len(z)))
        if d==0:return ask(f,'leaf')
        xs=sorted({abs(x) for c in f for x in c})
        if not xs:return ask(f,'terminal')
        v=ask(f[:2],'steer');x=(xs[-1] if v else xs[0]) if tag else (xs[0] if v else xs[-1])
        a=walk(pin(f,x,0),d-1);b=walk(pin(f,x,1),d-1)
        return a or b
    outcome=walk(cs,2)
    return outcome,tr,levels,writes

def chain(k,b):
    clauses=[(1,)]+[(-i,i+1) for i in range(1,k)]+[((k,) if b else (-k,))]
    out=[];p=k+1
    for c in clauses:
        if len(c)==1:
            a,z=p,p+1;p+=2
            out.extend((c[0],s*a,t*z) for s,t in product((-1,1),repeat=2))
        else:
            z=p;p+=1;out.extend(((c[0],c[1],z),(c[0],c[1],-z)))
    return p-1,tuple(out)

def run():
    plus=['123','145','246','356'];minus=['124','136','235','456']
    y=tuple(tuple(map(int,s)) for s in plus)+tuple(tuple(-int(i) for i in s) for s in minus)
    cases=[('Y6',6,y),('xor_UNSAT',3,tuple(tuple(-i if b else i for i,b in enumerate(bits,1)) for bits in product((0,1),repeat=3))),
           ('horn_UNSAT',2,((1,),(-1,2),(-2,)))]
    for k in (4,8):
        for b in (False,True):
            n,cs=chain(k,b);cases.append((f'chain{k}_{int(b)}',n,cs))
    out=[];different=0
    for name,n,cs in cases:
        a,t1,l1,w1=calc(n,cs)
        b,t2,l2,w2=calc(n,cs,pad=250)
        c,t3,l3,w3=calc(n,cs,tag=True,pad=250)
        assert a==b==c==sat(cs) and t1==t2 and l1==l2
        different+=int(t1!=t3)
        out.append({'source':name,'sat':a,'root_bits':len(enc(n,cs)),'calls':len(t1),'leaf_calls':sum(q[0]=='leaf' for q in t1),
                    'same_implementation_blind_trace':t1==t2,'code_tag_changes_trace':t1!=t3,
                    'max_level2_leaf_bits':max((size for level,size in l1 if level==0),default=0),
                    'explicit_bit_writes':w1})
    return {'id':'ARC-FROZEN-CODE-SELECTOR156-MINI','seed':None,'cases':out,'case_count':len(out),
            'code_tag_different_cases':different,'failed_assertions':0,
            'scope':'Finite serialized Python logic, not bit-machine time or space'}
if __name__=='__main__':print(json.dumps(run(),indent=2))
