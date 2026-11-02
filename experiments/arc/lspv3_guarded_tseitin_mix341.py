#!/usr/bin/env python3
"""LSPV-3/341 guarded Tseitin mixed refutation producer, stdlib only.
Usage: python3 lspv3_guarded_tseitin_mix341.py [output.json]
"""
import json, sys
from fractions import Fraction

def edges_for(name):
    if name == 'K4': return [(i,j) for i in range(4) for j in range(i+1,4)],4
    if name == 'Q3':
        return sorted({tuple(sorted((i,i^(1<<k)))) for i in range(8) for k in range(3)}),8
    if name == 'Petersen':
        es={(min(i,(i+1)%5),max(i,(i+1)%5)) for i in range(5)}
        es|={(i,i+5) for i in range(5)}
        es|={tuple(sorted((i+5,((i+2)%5)+5))) for i in range(5)}
        return sorted(es),10
    raise ValueError(name)

def connected(vertices,edges):
    s=set(vertices)
    if not s: return False
    seen={next(iter(s))};stack=list(seen)
    while stack:
        u=stack.pop()
        for a,b in edges:
            v=b if a==u else a if b==u else None
            if v in s and v not in seen:seen.add(v);stack.append(v)
    return seen==s

def cut(mask,edges):
    return sum(bool(mask&(1<<u))!=bool(mask&(1<<v)) for u,v in edges)

def dense_dp(h,edges):
    cuts=[cut(mask,edges) for mask in range(1<<h)]
    con=[False]*(1<<h)
    for mask in range(1,1<<h):
        con[mask]=connected([u for u in range(h) if mask&(1<<u)],edges)
    dp={}
    for mask in sorted((k for k in range(1,1<<h) if con[k]),key=int.bit_count):
        if mask.bit_count()==1:dp[mask]=cuts[mask];continue
        best=10**9;a=(mask-1)&mask
        while a:
            b=mask^a
            if a&(mask&-mask) and con[a] and con[b]:
                best=min(best,max(cuts[mask],dp[a],dp[b]))
            a=(a-1)&mask
        assert best<10**9
        dp[mask]=best
    alpha=min((Fraction(cuts[m],m.bit_count()) for m in range(1,1<<h)
               if m.bit_count()<=h//2))
    return dp[(1<<h)-1],alpha

def gf2(rows,cols):
    basis={}
    for mask,rhs in rows:
        while mask:
            pivot=(mask&-mask).bit_length()-1
            if pivot not in basis:basis[pivot]=(mask,rhs);break
            old,val=basis[pivot];mask^=old;rhs^=val
        else:
            if rhs:return None
    sol=0
    for pivot in sorted(basis,reverse=True):
        mask,rhs=basis[pivot]
        if rhs^((mask&sol).bit_count()&1):sol|=1<<pivot
    return sol

def solve_edges(h,edges,charge,v=None,pat=None):
    rows=[]
    for u in range(h):
        if u==v:continue
        rows.append((sum(1<<i for i,(a,b) in enumerate(edges) if u in (a,b)),charge[u]))
    if v is not None:
        around=[i for i,(a,b) in enumerate(edges) if v in (a,b)]
        rows.extend((1<<i,(pat>>k)&1) for k,i in enumerate(around))
    return gf2(rows,len(edges))

def sat(clauses,a):
    return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in clauses)

def build(name,t):
    edges,h=edges_for(name);e=len(edges)
    assert 2*e==3*h and connected(range(h),edges)
    assert all(connected((u for u in range(h) if u!=v),edges) for v in range(h))
    width,alpha=dense_dp(h,edges)
    charge=[1]+[0]*(h-1);n=t*(e+1)
    clauses=[[j+1 for j in range(t)]]
    witnesses=[None];blocks=[]
    for j in range(t):
        block=[]
        for v in range(h):
            around=[i for i,(a,b) in enumerate(edges) if v in (a,b)]
            indices=[]
            for pat in range(8):
                if pat.bit_count()%2==charge[v]:continue
                c=[-(j+1)]+[(t+j*e+ei+1)*(-1 if (pat>>k)&1 else 1)
                            for k,ei in enumerate(around)]
                idx=len(clauses);clauses.append(c);indices.append(idx)
                assignment=solve_edges(h,edges,charge,v,pat)
                assert assignment is not None
                a=[0]*n;a[j]=1
                for ei in range(e):a[t+j*e+ei]=(assignment>>ei)&1
                assert all(sat([c2],a) for ci,c2 in enumerate(clauses) if ci!=idx)
                witnesses.append(a)
            assert len(indices)==4
            block.append(indices)
        blocks.append(block)
    witnesses[0]=[0]*n
    assert len(clauses)==1+4*h*t
    for i,c in enumerate(clauses):
        a=witnesses[i]
        for k in range(len(c)):
            mutated=[list(x) for x in clauses]
            mutated[i][k]*=-1
            assert sat(mutated,a)
    # Same graph, one even-charge block and all other blocks odd.
    zero=solve_edges(h,edges,[0]*h)
    assert zero is not None
    even=[0]*n;even[0]=1
    for ei in range(e):even[t+ei]=(zero>>ei)&1
    satc=[list(c) for c in clauses]
    for v in range(h):
        around=[i for i,(a,b) in enumerate(edges) if v in (a,b)]
        for k,pat in enumerate(p for p in range(8) if p.bit_count()%2==1):
            satc[blocks[0][v][k]]=[-1]+[(t+ei+1)*(-1 if (pat>>pos)&1 else 1)
                                     for pos,ei in enumerate(around)]
    assert sat(satc,even)
    proof=[];prior={}
    def add(node):
        node['id']='p'+str(len(proof));proof.append(node);prior[node['id']]=node
        return node['id']
    neg_guards=[]
    for j in range(t):
        accum=None
        for v in range(h):
            variables=sorted(t+j*e+i+1 for i,(a,b) in enumerate(edges) if v in (a,b))
            term=add({'rule':'guarded_xor3','parents':['s'+str(i) for i in blocks[j][v]],
                      'guard':-(j+1),'vars':variables,'rhs':charge[v]})
            if accum is None:accum=term
            else:
                old=prior[accum]
                accum=add({'rule':'xor_add','parents':[accum,term],
                           'guard':-(j+1),
                           'vars':sorted(set(old['vars'])^set(variables)),
                           'rhs':old['rhs']^charge[v]})
        assert prior[accum]['vars']==[] and prior[accum]['rhs']==1
        neg_guards.append(add({'rule':'guard_contradiction',
                               'parents':[accum],'clause':[-(j+1)]}))
    parent='s0';remaining=list(clauses[0])
    for j,ng in enumerate(neg_guards):
        remaining.remove(j+1)
        parent=add({'rule':'resolution','parents':[parent,ng],
                    'pivot':j+1,'clause':list(remaining)})
    assert remaining==[] and len(proof)==t*(2*h+1)
    dimacs='p cnf '+str(n)+' '+str(len(clauses))+'\n'+''.join(
      ' '.join(map(str,c))+' 0\n' for c in clauses)
    return dict(graph=name,vertices=h,edges=edges,selectors=t,nvars=n,
                nclauses=len(clauses),nsource_signs=sum(map(len,clauses)),
                encoded_bits=8*len(dimacs.encode()),charges=charge,
                clauses=clauses,blocks=blocks,certificate=proof,proof_nodes=len(proof),
                source_fanin_lower=(len(clauses)-1+2)//3,
                sign_flip_witnesses=witnesses,
                sat_control=dict(clauses=satc,assignment=even),
                graph_alpha=[alpha.numerator,alpha.denominator],
                dense_minimax_cut_width=width,
                dense_minimax_peak_entries=1<<(width-1),
                asserted_status='UNSAT odd charge, SAT even control')

def main():
    cases=[build(g,t) for g,t in [('K4',1),('K4',2),('Q3',1),('Q3',2),('Petersen',1)]]
    raw=dict(run='GUARDED-TSEITIN-MIX341',model='Rmix-v1, unit nodes',
             finite_status='COMPUTATIONAL',cases=cases,
             input_encoding='literal-signed decimal DIMACS ASCII',
             no_randomness=True)
    output=sys.argv[1] if len(sys.argv)>1 else 'lspv3_341_raw.json'
    with open(output,'w',encoding='utf8') as f:json.dump(raw,f,indent=2);f.write('\n')
    for x in cases:
        print(x['graph'],x['selectors'],x['nclauses'],x['encoded_bits'],
              x['proof_nodes'],x['dense_minimax_cut_width'])
    print('PASS: all finite SAT/UNSAT, sign, parity, connected-cut and DAG construction tests')

if __name__=='__main__': main()
