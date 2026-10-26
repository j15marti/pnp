#!/usr/bin/env python3
"""CIRCUIT_QPORT_SWAP162. Independent stdlib check for a historical
15-variable forcing port, regularizer, two actual levels, and bit locality.
No 348-variable source, full Cook verifier compiler or mixed M_j is claimed.
Run: python 2026-10-26_0540_CIRCUIT_QPORT_SWAP162_repro.py
"""
from collections import Counter
from itertools import product
import json
W_TEXT = """
 -1 3 -14 2 -8 9 10 -13 14 3 7 -13
 -4 -9 -11 5 8 -14 4 -8 -11 1 7 13
 1 -7 10 -5 -6 -15 -2 -6 12 -4 9 -10
 -2 5 -12 -3 6 -15 6 -7 11 2 -9 11
 4 8 -10 -3 12 15 -5 -12 15 -1 13 14
"""
WI=[int(x) for x in W_TEXT.split()]
W=[tuple(WI[i:i+3]) for i in range(0,len(WI),3)]
Q=[c for c in W if c!=(1,7,13)]
J=((-1,-2,-3),(2,4,-5),(2,5,-6),(3,6,-4),
   (3,-5,-6),(-2,4,5),(-3,-4,6))
H_BASE=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
H=H_BASE+tuple(tuple(-x for x in c) for c in H_BASE)

def sat(C,a):
    return all(any(a[abs(z)]==int(z>0) for z in clause) for clause in C)

def balance(C,n,ports=()):
    plus=Counter();minus=Counter()
    assert len(set(C))==len(C)
    for c in C:
        assert len(c)==3 and len({abs(x) for x in c})==3
        for x in c:
            if x>0:plus[x]+=1
            else:minus[-x]+=1
    for x in range(1,n+1):
        assert (plus[x],minus[x])==((1,2) if x in ports else (2,2))
    assert 3*len(C)==4*n-len(ports)

def check_q_and_j():
    assert len(W)==20 and len(Q)==19
    balance(W,15);balance(Q,15,(1,7,13))
    qcount=0
    for b in product((0,1),repeat=15):
        a=(None,)+b
        assert not sat(W,a)
        if sat(Q,a):
            qcount+=1
            assert not (a[1] or a[7] or a[13])
    assert qcount==244 and sat(Q,(None,)+(0,)*15)
    for omit in range(20):
        assert any(sat(W[:omit]+W[omit+1:],(None,)+b)
                   for b in product((0,1),repeat=15))
    # J port is the negative of local symbol 1.
    p,n=Counter(),Counter()
    for c in J:
        for z in c:
            if z>0:p[z]+=1
            else:n[-z]+=1
    assert all((p[x],n[x])==(2,2) for x in range(2,7))
    jc={}
    for bit in (0,1):
        jc[str(bit)]=sum(sat(J,(None,bit)+b)
                         for b in product((0,1),repeat=5))
    assert jc=={'0':9,'1':5}
    balance(H,6)
    assert sat(H,(None,1,1,0,0,1,0))
    hcount=sum(sat(H,(None,)+b) for b in product((0,1),repeat=6))
    assert hcount==18
    # The paper's monotone-case arm: 3 clauses, 16 fresh H copies.
    monotone=[(1,2,3),(4,5,6),(7,8,9)]
    for k in range(16):
        off=9+6*k
        monotone.extend(tuple((1 if x>0 else -1)*(off+abs(x))
                              for x in row) for row in H)
    assert len(monotone)==131
    for bits in product((0,1),repeat=9):
        a=(None,)+bits+((1,1,0,0,1,0)*16)
        assert sat(monotone,a)==all(any(bits[3*j+i] for i in range(3))
                                    for j in range(3))
    return {'Q_models':qcount,'J_port_truth_counts':jc,
            'H_models':hcount,'monotone_port_vectors':512}

def signed_regularize(F,n):
    assert all(len(c)==3 and len(set(abs(x) for x in c))==3 for c in F)
    serial=0
    def alloc(h):
        nonlocal serial
        v=tuple(range(serial+1,serial+h+1));serial+=h;return v
    clones=[];source=[];sign=[];rings={i:[] for i in range(1,n+1)}
    for row in F:
        for x in row:
            v=alloc(1)[0];clones.append(v);source.append(abs(x))
            sign.append(1 if x>0 else -1);rings[abs(x)].append(v)
    dummies={}
    for x in range(1,n+1):
        dummies[x]=alloc(3)
        rings[x].extend(dummies[x])
    clauses=[tuple(sign[3*i+j]*clones[3*i+j] for j in range(3))
             for i in range(len(F))]
    edges=[]
    for x in range(1,n+1):
        r=rings[x]
        for j in range(len(r)):
            edges.append((r[j],r[(j+1)%len(r)]))
    assert len(edges)%3==0
    q_blocks=0
    for i in range(0,len(edges),3):
        names=alloc(15)
        clauses.extend(tuple((1 if z>0 else -1)*names[abs(z)-1]
                              for z in row) for row in Q)
        for j,p in enumerate((1,7,13)):
            a,b=edges[i+j]
            clauses.append((-a,b,names[p-1]))
        q_blocks+=1
    j_blocks=0
    def make_j(port):
        nonlocal j_blocks
        aux=alloc(5);mp={2:aux[0],3:aux[1],4:aux[2],
                         5:aux[3],6:aux[4]}
        for c in J:
            clauses.append(tuple((port if z<0 else -port) if abs(z)==1
                else ((1 if z>0 else -1)*mp[abs(z)]) for z in c))
        j_blocks+=1
    for v,s in zip(clones,sign): make_j(-s*v)
    for ds in dummies.values():
        for v in ds:
            make_j(v);make_j(-v)
    m=len(F)
    assert q_blocks==m+n and j_blocks==3*m+6*n
    assert (serial,len(clauses))==(33*m+48*n,44*m+64*n)
    balance(clauses,serial)
    return clauses,serial,{'clones':clones,'source':source,
       'dummies':dummies,'vars':serial}

def extension(values,state):
    v=[0]*(state['vars']+1)
    for clone,src in zip(state['clones'],state['source']):
        v[clone]=values[src]
    for x,ds in state['dummies'].items():
        for z in ds:v[z]=values[x]
    return v

def bit_locality():
    levels={'one':[], 'two':[]}
    for a,b in product((0,1),repeat=2):
        F=(((-1 if a else 1),2,3),((-1 if b else 1),-2,-3))
        child,n,_=signed_regularize(F,3)
        child2,_,_=signed_regularize(child,n)
        levels['one'].append(child)
        levels['two'].append(child2)
    sigs={}
    legal={'0000','1111','0011','1100','0101','1010'}
    for tag,children in levels.items():
        counts=Counter()
        for rows in zip(*children):
            for ls in zip(*rows):
                assert len(set(map(abs,ls)))==1
                s=''.join('1' if x>0 else '0' for x in ls)
                assert s in legal
                counts[s]+=1
        sigs[tag]={'clauses':len(children[0]),'slots':sum(counts.values()),
                   'signatures':dict(sorted(counts.items()))}
    return sigs

def full_circuit_control():
    all8=[tuple((j+1 if b[j]==0 else -(j+1))
                for j in range(3))
          for b in product((0,1),repeat=3)]
    assert not any(sat(all8,(None,)+b) for b in product((0,1),repeat=3))
    neighbor=all8[:-1]+[all8[0]]
    assert any(sat(neighbor,(None,)+b) for b in product((0,1),repeat=3))
    assert len(neighbor)==len(all8)==8
    for bits in product((0,1),repeat=8):
        enabled=[all8[j] for j in range(8) if bits[j]]
        assert any(sat(enabled,(None,)+b) for b in product((0,1),repeat=3))!=(all(bits))
    return {'mask_function':'NAND8','opposite_label_same_length':True}

def run():
    gadgets=check_q_and_j()
    inputs={
        'SAT':[(1,2,3),(-1,-2,-3)],
        'UNSAT':[tuple(j+1 if b[j]==0 else -(j+1)
                       for j in range(3))
                 for b in product((0,1),repeat=3)],
        'SAT_unique':[tuple(j+1 if b[j]==0 else -(j+1)
                            for j in range(3))
                      for b in list(product((0,1),repeat=3))[:-1]]
    }
    records=[]
    for tag,F in inputs.items():
        n=3
        a=[b for b in product((0,1),repeat=3)
           if sat(F,(None,)+b)]
        c1,v1,state1=signed_regularize(F,n)
        for b in a:
            assert sat(c1,extension((None,)+b,state1))
        info={'case':tag,'source_models':len(a),
              'level1_vars':v1,'level1_clauses':len(c1)}
        if tag in ('SAT','UNSAT'):
            c2,v2,state2=signed_regularize(c1,v1)
            info.update(level2_vars=v2,level2_clauses=len(c2))
            if a:
                w1=extension((None,)+a[0],state1)
                assert sat(c2,extension(w1,state2))
                info['second_level_witness_checked']=True
            else:
                info['UNSAT_preservation']='projection theorem'
        records.append(info)
    return {'run':'CIRCUIT_QPORT_SWAP162','Q_and_monotone':gadgets,
        'two_level':records,'bit_locality':bit_locality(),
        'full_circuit':full_circuit_control(),
        'note':'348/463 raw source and mixed M_j templates unavailable',
        'P_vs_NP':'OPEN'}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
