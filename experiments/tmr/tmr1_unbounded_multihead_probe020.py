#!/usr/bin/env python3
"""TMR-1/020 finite input-head locality/collision verifier, not a TM compiler."""
import json
from itertools import product


def cell(x,u):
    return '<' if u==0 else '>' if u==len(x)+1 else x[u-1] if 1<=u<=len(x) else '_'


def classify(u,L,t):
    return 'far-left' if u < -t else 'far-right' if u > L+1+t else u


def park(x,h,mode):
    L=len(x); n=int(x,2)
    if mode=='spread': return tuple(1+(2*j+1)*L//(2*h) for j in range(h))
    if mode=='far-encoded': return tuple(-2*L-10-n-3*j for j in range(h))
    if mode=='mixed': return tuple(-2*L-10-n if j%2==0 else (n+j)%(L+2) for j in range(h))
    return tuple(0 if j%2==0 else L+1 for j in range(h))


def sketch(x,s,mode):
    if s==0: return ''
    if mode=='prefix': return x[:s]
    a=[0]*s
    for j,v in enumerate(x): a[(j*j+3*j+1)%s]^=int(v)
    return ''.join(map(str,a))


def window(x,heads,t):
    indices=sorted({j for u in heads for j in range(max(1,u-t),min(len(x),u+t)+1)})
    return ''.join(x[j-1] for j in indices),indices


def probe(x,heads,st,p,t):
    heads=list(heads);q=int(st or '0',2);seen=[]
    for step in range(t+1):
        symbols=tuple(cell(x,u) for u in heads)
        if step==t: seen.append((q,symbols,'stop')); break
        i=(q+p+step)%len(heads)
        delta=-1 if symbols[i] in ('1','>') or (q+p+step)%2 else 1
        seen.append((q,symbols,(i,delta)))
        q=(q*3+p+step+int(symbols[i] in ('1','>')))%17
        heads[i]+=delta
    return seen


def run():
    counts=dict(cases=0,guaranteed=0,collisions=0,physical_probe_agreements=0,
                far_encoded_collisions=0,geometry_controls=0,failures=0)
    examples=[]
    for L in range(1,11):
        inputs=[format(i,f'0{L}b') for i in range(1<<L)]
        for h,s,mode,sm,t in product((1,2,3),(0,1,2),('spread','far-encoded','mixed','edges'),('prefix','xor'),(0,1,2,3)):
            counts['cases']+=1
            known={};pair=None
            for x in inputs:
                heads=park(x,h,mode); st=sketch(x,s,sm)
                obs,indices=window(x,heads,t)
                key=(st,tuple(classify(u,L,t) for u in heads),obs)
                if key in known:
                    pair=(known[key],(x,heads,st,indices))
                    break
                known[key]=(x,heads,st,indices)
            B=(L+2*t+4)**h*(2**s)*(2**(h*(2*t+1)))
            if 2**L>B:
                counts['guaranteed']+=1
                assert pair is not None,(L,h,s,mode,sm,t)
            if pair is None: continue
            counts['collisions']+=1
            (x,a,st,indices),(y,b,ss,other)=pair
            assert x!=y and st==ss and indices==other
            assert all(classify(u,L,t)==classify(v,L,t) for u,v in zip(a,b))
            p=next(i+1 for i,(u,v) in enumerate(zip(x,y)) if u!=v)
            assert p not in indices and probe(x,a,st,p,t)==probe(y,b,ss,p,t)
            counts['physical_probe_agreements']+=1
            if mode=='far-encoded': counts['far_encoded_collisions']+=1
            if len(examples)<4 and mode=='far-encoded':
                examples.append(dict(L=L,h=h,s=s,radius=t,x=x,y=y,parked_a=a,parked_b=b,index=p))
        for h in (1,2,3):
            centers=park('0'*L,h,'spread')
            maximum=max(min(abs(p-u) for u in centers) for p in range(1,L+1))
            assert maximum<= (L+h-1)//(2*h)+1
            counts['geometry_controls']+=1
    return {'status':'COMPUTATIONAL','run':'TMR-1/020','lengths':[1,10],
      'input_head_counts':[1,2,3],'retained_sketch_bits':[0,1,2],
      'radius':[0,3],'source_policies':['spread','far-encoded','mixed','edges'],
      'counts':counts,'witness_examples':examples,
      'limitations':'Synthetic head parking and sketches are over-permissive controls. Adaptive probe uses only physical current-cell symbols; Python is not a charged general TM compiler. Asymptotic theorem is symbolic.'}


if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
