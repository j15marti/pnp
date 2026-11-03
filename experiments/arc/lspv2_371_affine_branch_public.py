#!/usr/bin/env python3
"""LSPV-2 371 compact public affine-first branch reproducer.
Checks circuit semantics and at-most-4^g partition for selected chains; full
independent Res(XOR) certificate verifier and 24 fixtures are in the archive.
"""
import json

TABLE={'xor':(0,1,1,0),'xnor':(1,0,0,1),'and':(0,0,0,1),'or':(0,1,1,1),
       'nota':(1,1,0,0)}

def coefficients(t):
    c,p,q=t[0],t[0]^t[2],t[0]^t[1]
    return (c,p,q,t[0]^t[1]^t[2]^t[3])

def combine(a,b):return (a[0]^b[0],a[1]^b[1])
def value(expr,x):return (expr[0]&x).bit_count()%2 ^ expr[1]
def valid(cs,n):
    return any(all(((m&x).bit_count()%2)==v for m,v in cs) for x in range(1<<n))

def branch(gates,n):
    def arg(ref,env):return (1<<(ref-1),0) if isinstance(ref,int) else env[ref]
    def rec(i,env,cs):
        if i==len(gates):return [dict(constraints=cs,forms=env)]
        name,tt,left,right=gates[i]
        l,r=arg(left,env),arg(right,env)
        c,p,q,t=coefficients(tt)
        if not t:
            out=(0,c)
            if p:out=combine(out,l)
            if q:out=combine(out,r)
            return rec(i+1,{**env,name:out},cs)
        ans=[]
        for a in (0,1):
            ca=cs+[(l[0],a^l[1])]
            if not valid(ca,n):continue
            for b in (0,1):
                cb=ca+[(r[0],b^r[1])]
                if valid(cb,n):ans+=rec(i+1,{**env,name:(0,tt[2*a+b])},cb)
        return ans
    leaves=rec(0,{},[])
    nonlinear=sum(coefficients(g[1])[3] for g in gates)
    assert len(leaves)<=4**nonlinear
    for x in range(1<<n):
        chosen=[L for L in leaves if all((m&x).bit_count()%2==v for m,v in L['constraints'])]
        assert len(chosen)==1,(n,x)
        real={}
        for name,tt,left,right in gates:
            a=((x>>(left-1))&1) if isinstance(left,int) else real[left]
            b=((x>>(right-1))&1) if isinstance(right,int) else real[right]
            real[name]=tt[2*a+b]
            assert value(chosen[0]['forms'][name],x)==real[name],(name,x)
    return {'affine':len(gates)-nonlinear,'nonlinear':nonlinear,'leaves':len(leaves)}

def main():
    assert sum(coefficients(tuple((code>>(2*a+b))&1 for a,b in ((0,0),(0,1),(1,0),(1,1))))[3]==0 for code in range(16))==8
    out={}
    out['no_gates']=branch([],2)
    for depth in (1,8,48):
        gs=[('u0',TABLE['xor'],1,2)]
        for j in range(1,depth):gs.append((f'u{j}',TABLE['xnor'] if j%2 else TABLE['nota'],f'u{j-1}',1))
        out[f'affine_{depth}']=branch(gs,2)
        out[f'affine_{depth}_and']=branch(gs+[('z',TABLE['and'],f'u{depth-1}',1)],2)
    gs=[('u',TABLE['xor'],1,2),('v',TABLE['xnor'],3,4),
        ('z0',TABLE['and'],'u',1),('z1',TABLE['or'],'v',3)]
    out['two_nonlinear']=branch(gs,4)
    assert out['affine_48']['leaves']==1
    assert out['affine_48_and']['leaves']==4
    assert out['two_nonlinear']['leaves']==16
    print(json.dumps({'status':'PASS','data':out},sort_keys=True,indent=2))
if __name__=='__main__':main()
