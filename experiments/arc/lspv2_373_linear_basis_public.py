#!/usr/bin/env python3
"""LSPV-2 373: compact, independent-of-third-party-libraries both-label test."""
import json

def graph(name):
    if name == 'K4': return 4, [(i,j) for i in range(4) for j in range(i+1,4)]
    if name == 'K33': return 6, [(i,j) for i in range(3) for j in range(3,6)]
    if name == 'cube': return 8, [(i,i^(1<<b)) for i in range(8) for b in range(3) if i<(i^(1<<b))]
    if name == 'Petersen':
        return 10, [(i,(i+1)%5) for i in range(5)] + [(i,5+i) for i in range(5)] + [(5+i,5+(i+2)%5) for i in range(5)]
    raise ValueError('unknown')

def sat(h, edges, c):
    # Actual GF(2) elimination, not a presumed parity answer.
    pivots={}
    for v in range(h):
        mask=sum(1<<j for j,(a,b) in enumerate(edges) if a==v or b==v)
        rhs=c[v]
        while mask:
            k=mask.bit_length()-1
            if k in pivots:
                mask^=pivots[k][0]; rhs^=pivots[k][1]
            else:
                pivots[k]=(mask,rhs); break
        if not mask and rhs:return False
    return True

def run():
    checks=0; cases=[]
    def check(b):
        nonlocal checks
        checks+=1
        if not b:raise AssertionError('failed case '+str(checks))
    for name in ('K4','K33','cube','Petersen'):
        h,edges=graph(name)
        check(len(edges)*2==3*h)
        yes=0
        for z in range(1<<h):
            c=[(z>>i)&1 for i in range(h)]
            y=[sum(c)&1]+c[1:]
            inv=[sum(y)&1]+y[1:]
            check(inv==c)
            original=sat(h,edges,c)
            check(original==(y[0]==0))
            yes+=int(original)
            for j in range(h):
                cc=c[:];cc[j]^=1
                check(sat(h,edges,cc)!=original)
                yy=y[:];yy[j]^=1
                ci=[sum(yy)&1]+yy[1:]
                check((sat(h,edges,ci)!=original)==(j==0))
            if name in ('K4','K33'):
                models=0
                for assignment in range(1<<len(edges)):
                    good=True
                    for v in range(h):
                        parity=0
                        for k,(u,w) in enumerate(edges):
                            if u==v or w==v:parity^=(assignment>>k)&1
                        if parity!=c[v]:good=False;break
                    models+=int(good)
                check(models==(2**(len(edges)-h+1) if original else 0))
        check(yes==(1<<(h-1)))
        cases.append({'graph':name,'h':h,'all_charge_vectors':1<<h,'SAT':yes,'UNSAT':(1<<h)-yes,
                      'raw_depth':h,'recoded_depth':1})
    return {'status':'PASS','checks':checks,'charge_cases':sum(i['all_charge_vectors'] for i in cases),
            'scope':'promised charge-bit queries; not all-CNF input-bit queries','cases':cases}

if __name__=='__main__':print(json.dumps(run(),indent=2))
