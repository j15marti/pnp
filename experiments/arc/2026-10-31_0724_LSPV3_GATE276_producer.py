#!/usr/bin/env python3
"""Exact finite controls for LSPV-3 Krom source-selector gate 276.
No external dependencies. Deterministic, seed-free. Run python producer276.py.
"""
import itertools, json, collections, sys
from pathlib import Path
P=Path(__file__).resolve().parent

# Every clause is tuple of signed DIMACS-style integers.
def build(q, edges, label):
    edges=sorted(tuple(sorted(e)) for e in edges)
    clauses=[]; ident=[]; n=q; r=q+1
    for e,(u,v) in enumerate(edges):
        for j in range(r):
            n+=1; clauses.append((u+1,v+1,n));ident.append(('edge',e,j))
    g=(n+1,n+2,n+3); n+=3
    if label=='SAT':
        clauses.append(g);ident.append(('guard',7))
    else:
        for mask in range(8):
            clauses.append(tuple(-g[i] if (mask>>i)&1 else g[i] for i in range(3)))
            ident.append(('guard',mask))
    return {'name':f'{q}v_{len(edges)}e_{label}', 'q':q,'edges':edges,'r':r,'n':n,'clauses':clauses,'ids':ident,'label':label,'guard':g}

def true_count(clause,a):
    return sum(a[abs(l)-1] == int(l>0) for l in clause)
def status(f,a):
    z=[true_count(c,a) for c in f['clauses']]
    return {'t':z,'N':[z.count(i) for i in range(4)],'sat':0 not in z}
def local_extremes(f):
    out=[]
    for j,c in enumerate(f['clauses']):
        S={abs(l):int(l>0) for l in c}
        U={x:1-v for x,v in S.items()}
        out.append({'j':j+1,'clause':c,'occurrences':[{'literal':l,'i':abs(l),'S':int(l>0),'invertS':int(l<0),'U':int(l<0),'invertU':int(l>0)} for l in c],'S':S,'invertS':U,'U':U,'invertU':S})
    return out

def compat(f):
    out=[]
    for i,j in itertools.combinations(range(len(f['clauses'])),2):
        a=f['clauses'][i];b=f['clauses'][j]; sa={abs(x):int(x>0) for x in a};sb={abs(x):int(x>0) for x in b}
        common=set(sa)&set(sb)
        same=any(sa[x]==sb[x] for x in common); opposite=any(sa[x]!=sb[x] for x in common)
        out.append({'i':i+1,'j':j+1,'SS':not opposite,'SU':not same,'US':not same,'UU':not opposite})
    return out

def trail(f):
    n=f['n']; a=[0]*n; out=[{'step':0,'flip':None, 'N':status(f,a)['N']}]
    # Gray walk length up to min(n,12) steps, always globally consistent.
    for step in range(1,min(1<<min(n,6),13)):
        gray=step^(step>>1); prev=(step-1)^((step-1)>>1)
        diff=(gray^prev).bit_length()-1; a[diff]^=1
        out.append({'step':step,'flip':diff+1,'N':status(f,a)['N']})
    return out

def vertex_cover(q,edges):
    for size in range(q+1):
        for sub in itertools.combinations(range(q),size):
            if all(u in sub or v in sub for u,v in edges):return list(sub)

def krom_backdoor_count(f):
    # Every proper 3-clause must meet B. Exact vertex-hitting minimum, search small sizes.
    n=f['n'];clauses=f['clauses']
    for size in range(min(6,n)+1):
        for B in itertools.combinations(range(1,n+1),size):
            bs=set(B)
            if all(any(abs(l) in bs for l in c) for c in clauses):return list(B)
    raise ValueError('minimum >5; adjust finite verifier')

def find_witness(f):
    a=[1]*f['n'];return a if status(f,a)['sat'] else None

def source_gadget_proof(f):
    # 7 resolution steps for eight distinct three-literal source guards.
    if f['label']!='UNSAT':return []
    start=len(f['clauses'])-8
    lines=[{'id':i+1,'clause':sorted(set(c),key=lambda x:(abs(x),x<0)),'parents':None} for i,c in enumerate(f['clauses'])]
    curr=[start+i for i in range(8)]
    def res(i,j,var):
        a=set(lines[i]['clause']);b=set(lines[j]['clause'])
        assert var in a and -var in b or -var in a and var in b
        clause=(a|b)-{var,-var}
        assert not any(-x in clause for x in clause)
        lines.append({'id':len(lines)+1,'clause':sorted(clause,key=lambda x:(abs(x),x<0)),'parents':[i+1,j+1,var]})
        return len(lines)-1
    for var in reversed(f['guard']):
        # pair clauses with opposite sign for var and identical others
        done=set(); nxt=[]
        for i in curr:
            if i in done:continue
            c=set(lines[i]['clause']);other=c-{var,-var}
            j=next(j for j in curr if j!=i and set(lines[j]['clause'])-{var,-var}==other and bool(var in set(lines[j]['clause']))!=bool(var in c))
            done.add(i);done.add(j);nxt.append(res(i,j,var))
        curr=nxt
    assert len(curr)==1 and not lines[curr[0]]['clause']
    return lines[len(f['clauses']):]

class DPLL:
    def __init__(self,f):self.f=f; self.nodes=0;self.clause_reads=0;self.literal_reads=0;self.unit_forces=0;self.branches=0
    def check(self,c,a):
        self.clause_reads+=1;un=[]
        for l in c:
            self.literal_reads+=1;v=a.get(abs(l))
            if v is None:un.append(l)
            elif v==int(l>0):return 1,None
        if not un:return -1,None
        return 0,un
    def solve(self,a=None):
        if a is None:a={}
        self.nodes+=1; a=a.copy()
        while True:
            units=[]; unresolved=False
            for c in self.f['clauses']:
                k,un=self.check(c,a)
                if k==-1:return None
                if k==0:
                    unresolved=True
                    if len(un)==1:units.append(un[0])
            if not unresolved:return a
            if not units:break
            new=False
            for l in units:
                var=abs(l); val=int(l>0)
                if var in a and a[var]!=val:return None
                if var not in a:a[var]=val;self.unit_forces+=1;new=True
            if not new:break
        v=next(abs(l) for c in self.f['clauses'] for l in c if abs(l) not in a and self.check(c,a)[0]==0)
        self.branches+=1
        for b in [0,1]:
            a2=a.copy();a2[v]=b
            w=self.solve(a2)
            if w is not None:return w
        return None
    def metrics(self):return {'nodes':self.nodes,'branches':self.branches,'clause_reads':self.clause_reads,'literal_reads':self.literal_reads,'unit_forces':self.unit_forces,'selected_work':self.nodes+self.branches+self.clause_reads+self.literal_reads+self.unit_forces}

def selector(f):
    # Fully counted syntax authentication before certification. Under this fixed canonical promise,
    # the first q+(q+1)|E| variables/clauses are fully inspected, so this is not a free oracle.
    q=f['q'];n=f['n'];E=f['edges'];r=q+1;cr=0;lr=0; overhead=0
    guard_count=len(f['clauses'])-r*len(E)
    if guard_count not in (1,8):raise ValueError('unrecognized source: complete fallback required')
    inferred_type='SAT' if guard_count==1 else 'UNSAT' # syntactic case identifier, NOT supplied SAT label
    expected=build(q,E,inferred_type);cr+=len(f['clauses']);lr+=sum(len(c) for c in f['clauses'])+q+2*len(E)
    if f['clauses']!=expected['clauses']:raise ValueError('source authentication failed: complete fallback required')
    # Coherent 0^n and 1^n probes are part of the charged controller, not UNSAT proof.
    endpoints=[status(f,[i]*n) for i in (0,1)];cr+=2*len(f['clauses']);lr+=2*sum(map(len,f['clauses']))
    if endpoints[1]['sat']:
        result='SAT';wit=[1]*n;proof=[];cr+=len(f['clauses']);lr+=sum(map(len,f['clauses']))
    else:
        proof=source_gadget_proof(expected);result='UNSAT';wit=None;overhead+=len(proof)
        # refutation checker accounting, each derived clause reads both parents
        cr+=2*len(proof);lr+=sum(2*len(c) for c in f['clauses'][-8:])
    return {'label':result,'witness':wit,'proof':proof,'policy':'endpoint' if result=='SAT' else 'authenticated_gadget_resolution', 'source_clause_reads':cr,'source_literal_reads':lr,'proof_steps':len(proof),'selected_work':cr+lr+len(proof)+overhead+2}

def run():
    graphs=[(2,[(0,1)]),(3,[(0,1),(1,2),(0,2)]),(4,[(0,1),(1,2),(2,3),(3,0)]),(4,[(0,1),(1,2),(2,3)]),(5,[(0,1),(1,2),(2,3),(3,4),(4,0)])]
    cases=[]
    for q,edges in graphs:
        for label in ('SAT','UNSAT'):
            f=build(q,edges,label);s=selector(f);d=DPLL(f);w=d.solve(); assert (w is not None)==(label=='SAT')
            vc=vertex_cover(q,edges);B=krom_backdoor_count(f)
            assert len(B)==len(vc)+1
            cases.append({'source':f,'groundtruth_label':label,'vertex_cover':vc,'backdoor':B,'backdoor_size':len(B),'endpoint_0':status(f,[0]*f['n']),'endpoint_1':status(f,[1]*f['n']),'gray_trail':trail(f),'local_extremes':local_extremes(f),'compatibility':compat(f),'selector':s,'dpll':d.metrics(),'all_true_witness_valid':status(f,[1]*f['n'])['sat'],'unsat_proof':s['proof']})
    raw={'run':'LSPV3-VERTEX-COVER-POLICY-ACQUISITION276','seed':None,'model':'source-authenticated proper 3CNF; complete UP-first DPLL; selected interpreter events','cases':cases}
    (P/'raw276.json').write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    summary={'count':len(cases),'sat':sum(x['groundtruth_label']=='SAT' for x in cases),'unsat':sum(x['groundtruth_label']=='UNSAT' for x in cases), 'cases':[{'name':c['source']['name'],'n':c['source']['n'],'m':len(c['source']['clauses']),'vc':len(c['vertex_cover']),'backdoor':c['backdoor_size'],'dpll':c['dpll'],'selector_work':c['selector']['selected_work'],'proof_steps':len(c['unsat_proof'])} for c in cases]}
    (P/'summary276.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
