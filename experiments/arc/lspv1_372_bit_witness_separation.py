#!/usr/bin/env python3
"""Finite controls for the BIT-WITNESS-SEPARATION372 toy calculus.
A binary AND node carries an explicit truth table on all n source variables.
Not a legal added operation of Rmix341. No SAT/equivalence oracle.
"""
import hashlib, json, itertools, sys
from pathlib import Path

def php(h):
    assert isinstance(h,int) and h>=1
    v=lambda p,j:p*h+j+1
    C=[tuple(v(p,j) for j in range(h)) for p in range(h+1)]
    for j in range(h):
        for p in range(h+1):
            for q in range(p+1,h+1):C.append((-v(p,j),-v(q,j)))
    return h*(h+1),C

def valid(n,C):
    return isinstance(n,int) and n>=1 and isinstance(C,list) and all(
        isinstance(c,tuple) and 1<=len(c)<=n
        and all(type(x)==int and 0<abs(x)<=n for x in c)
        and len({abs(x) for x in c})==len(c) for c in C)

def clause(c,a):
    return any(bool(((a>>(abs(x)-1))&1) if x>0 else not ((a>>(abs(x)-1))&1)) for x in c)

def witness(n,C):
    return next((a for a in range(1<<n) if all(clause(c,a) for c in C)),None)

def vector(n,c):
    return bytes(int(clause(c,a)) for a in range(1<<n))

def build(n,C):
    if not valid(n,C) or len(C)<2:raise ValueError('source')
    m=len(C);prev=vector(n,C[0]);nodes=[]
    for j in range(1,m):
        out=bytes(x&y for x,y in zip(prev,vector(n,C[j])))
        nodes.append((0 if j==1 else m+j-2,j,out));prev=out
    return nodes

def verify(n,C,nodes,require_unsat=True):
    if not valid(n,C) or len(C)<2 or not isinstance(nodes,list) or not nodes:raise ValueError('formula or proof')
    m=len(C);mem={i:vector(n,c) for i,c in enumerate(C)}
    for j,rec in enumerate(nodes):
        if not isinstance(rec,tuple) or len(rec)!=3:raise ValueError('record')
        l,r,tab=rec
        if any(type(i)!=int or i<0 or i>=m+j for i in (l,r)):raise ValueError('parent')
        if not isinstance(tab,bytes) or len(tab)!=(1<<n):raise ValueError('payload')
        if tab!=bytes(x&y for x,y in zip(mem[l],mem[r])):raise ValueError('corrupt')
        mem[m+j]=tab
    if require_unsat and any(mem[m+len(nodes)-1]):raise ValueError('not UNSAT')
    return True

def k4(odd):
    edges=list(itertools.combinations(range(4),2));C=[]
    for v in range(4):
        inc=[edges.index(e)+1 for e in edges if v in e]
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2 != (int(bool(odd)) if v==0 else 0):
                C.append(tuple(-x if b else x for x,b in zip(inc,bits)))
    return 6,C

def res_ok(n,P,Q,pivot,conclusion):
    if not isinstance(pivot,int) or not 0<abs(pivot)<=n:return False
    if pivot not in P or -pivot not in Q:return False
    r=(set(P)-{pivot}) | (set(Q)-{-pivot})
    return not any(-x in r for x in r) and set(conclusion)==r

def main():
    out={'run':'BIT_WITNESS_SEPARATION372','model':'binary-full-table toy, distinct paid nodes=one per AND, vector over all 2^n assignments',
         'proof_status':'COMPUTATIONAL for finite cases; symbolic lemma separate','PHP':[],'controls':{},'test_assertions':0}
    def ck(test,why):
        out['test_assertions']+=1
        if not test:raise AssertionError(why)
    for h in (1,2,3):
        n,C=php(h);m=len(C)
        ck(valid(n,C),'source')
        ck(witness(n,C) is None,'UNSAT')
        deletions=[]
        for i in range(m):
            w=witness(n,C[:i]+C[i+1:]);ck(w is not None,'deletion SAT');deletions.append(w)
        signs=0
        for i,c in enumerate(C):
            for j,x in enumerate(c):
                altered=list(C);cc=list(c);cc[j]=-x;altered[i]=tuple(cc)
                ck(witness(n,altered) is not None,'sign-repair SAT');signs+=1
        proof=build(n,C)
        ck(len(proof)==m-1,'cost')
        ck(verify(n,C,proof),'proof')
        ck(not any(proof[-1][2]),'root')
        ck(len(proof)*(1<<n)==(m-1)*(1<<n),'bits')
        tampered=list(proof);a,b,t=tampered[-1];tt=bytearray(t);tt[0]^=1;tampered[-1]=(a,b,bytes(tt))
        try:verify(n,C,tampered);ck(False,'corrupt accepted')
        except ValueError:ck(True,'corrupt rejected')
        tampered=list(proof);a,b,t=tampered[0];tampered[0]=(m,a,t)
        try:verify(n,C,tampered);ck(False,'future parent accepted')
        except ValueError:ck(True,'future parent rejected')
        dimacs=f'p cnf {n} {m}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in C)
        out['PHP'].append({'holes':h,'pigeons':h+1,'variables':n,'source_clauses':m,
             'source_DIMACS_bytes':len(dimacs.encode()),'min_binary_fanin_nodes':m-1,
             'actual_binary_table_nodes':len(proof),'one_node_table_bits':1<<n,
             'full_table_bits':(m-1)*(1<<n),'source_deletion_sat_witness_count':m,
             'sign_flip_sat_witness_count':signs,
             'source_deletion_witness_sha256':hashlib.sha256(json.dumps(deletions).encode()).hexdigest(),
             'proof_tables_sha256':hashlib.sha256(b''.join(r[2] for r in proof)).hexdigest()})
    labels={}
    for odd in (False,True):
        n,C=k4(odd);k=sum(all(clause(c,a) for c in C) for a in range(1<<n))
        ck(k==(0 if odd else 8),'K4 label')
        proof=build(n,C)
        try:
            verify(n,C,proof);ck(bool(odd),'SAT accepted as UNSAT')
        except ValueError:ck(not odd,'odd rejected')
        labels['odd' if odd else 'even']={'satisfying_assignments':k,'clauses':len(C)}
    out['controls']['K4']=labels
    sat=[(1,2),(-1,2)];unsat=[(1,),(-1,)]
    ck(witness(2,sat) is not None,'2SAT witness')
    ck(witness(2,unsat) is None,'2SAT UNSAT')
    try:verify(2,sat,build(2,sat));ck(False,'2SAT SAT admitted')
    except ValueError:ck(True,'2SAT SAT rejected')
    ck(verify(2,unsat,build(2,unsat)),'2SAT UNSAT')
    for malformed in [[(0,)],[(-3,)],[('1',)],[(1,-1)]]:
        ck(not valid(2,malformed),'malformed accepted')
    ck(res_ok(2,(1,2),(-1,),1,(2,)),'RES positive')
    ck(not res_ok(2,(1,2),(-1,),2,(2,)),'pivot accepted')
    ck(not res_ok(2,(1,2),(-1,),1,(1,)),'resolvent accepted')
    out['controls']['2SAT']={'SAT':True,'UNSAT':True,'malformed_rejections':4,
                               'resolution_bad_pivot_and_clause_rejections':2}
    payload=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)==3 and sys.argv[1]=='--out':Path(sys.argv[2]).write_text(payload)
    print(payload,end='')

if __name__=='__main__':main()
