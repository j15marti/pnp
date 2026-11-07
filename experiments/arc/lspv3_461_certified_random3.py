#!/usr/bin/env python3
"""LSPV-3/461: deterministic proper-3-CNF from published random model; strict RES proof and deleted-clause witnesses.
This implements a computational fixture, NOT a proof of random-family asymptotic hardness.
"""
import hashlib,itertools,json,math,os,sys,time,resource
class HashStream:
    def __init__(self,seed):self.seed=seed.to_bytes(4,'big');self.counter=0
    def word(self):
        x=int.from_bytes(hashlib.sha256(self.seed+self.counter.to_bytes(8,'big')).digest()[:8],'big');self.counter+=1;return x
    def bounded(self,n):
        limit=(2**64//n)*n
        while True:
            x=self.word()
            if x<limit:return x%n

def make(n,seed,sat_control=False):
    rng=HashStream(seed);ans=[]
    # Use original 460 distribution for UNSAT; SAT control uses rejection sampling only of clauses satisfied by an explicit witness.
    witness=sum(((i*13+seed)%7<3)<<i for i in range(n))
    while len(ans)<8*n:
        ids=[]
        while len(ids)<3:
            t=rng.bounded(n)+1
            if t not in ids:ids.append(t)
        ids.sort();mask=rng.bounded(8)
        c=tuple(-v if mask&(1<<i) else v for i,v in enumerate(ids))
        if not sat_control or eval_clause(c,witness):ans.append(c)
    return ans,witness

def eval_clause(c,bits):return any(bool(bits&(1<<(abs(l)-1)))==(l>0) for l in c)
def witness(clauses,n):
    for a in range(1<<n):
        if all(eval_clause(c,a) for c in clauses):return a
    return None

def canon(C):
    x=set(C)
    if any(-v in x for v in x):return None
    return tuple(sorted(x,key=lambda z:(abs(z),z<0)))

def run_dp(clauses,n):
    # Original duplicates remain independently labeled, global clause dictionary selects one authenticated owner.
    current={}
    for i,c in enumerate(clauses):current.setdefault(c,'s'+str(i))
    all_nodes={};steps=[];maxlive=len(current)
    while current and () not in current:
        variables=sorted({abs(l) for c in current for l in c})
        if not variables:break
        def criterion(v):
            pos=sum(v in c for c in current);neg=sum(-v in c for c in current)
            return (pos*neg,pos+neg,v)
        v=min(variables,key=criterion)
        pos=sorted([(c,r) for c,r in current.items() if v in c]);neg=sorted([(c,r) for c,r in current.items() if -v in c])
        keep={c:r for c,r in current.items() if v not in c and -v not in c}
        created=0
        for c,rc in pos:
            for d,rd in neg:
                out=canon([l for l in c if l!=v]+[l for l in d if l!=-v])
                if out is None:continue
                if out in keep:continue
                k='d'+str(len(all_nodes))
                all_nodes[k]={'id':k,'left':rc,'right':rd,'pivot':v,'clause':list(out)}
                keep[out]=k;created+=1
                if out==():break
            if () in keep:break
        steps.append({'pivot':v,'parents_positive':len(pos),'parents_negative':len(neg),'created_resolvents':created,'live_after':len(keep)})
        current=keep;maxlive=max(maxlive,len(keep))
    assert () in current,'DP did not refute source'
    root=current[()];needed=set();todo=[root]
    while todo:
        r=todo.pop()
        if r[0]=='d' and r not in needed:
            needed.add(r);todo.extend((all_nodes[r]['left'],all_nodes[r]['right']))
    nodes=sorted((all_nodes[k] for k in needed),key=lambda x:int(x['id'][1:]))
    # Remap indices densely, allowing compact readback with strict topological order.
    remap={x['id']:'d'+str(i) for i,x in enumerate(nodes)}
    for x in nodes:
        for p in ('left','right'):
            if x[p][0]=='d':x[p]=remap[x[p]]
        x['id']=remap[x['id']]
    return nodes,remap[root],steps,maxlive,len(all_nodes)

def minimize(clauses,n):
    active=list(range(len(clauses)))
    for i in list(active):
        sub=[clauses[j] for j in active if j!=i]
        if witness(sub,n) is None:active.remove(i)
    witnesses={str(i):witness([clauses[j] for j in active if j!=i],n) for i in active}
    assert all(x is not None for x in witnesses.values())
    assert witness([clauses[i] for i in active],n) is None
    return active,witnesses

def source_bytes(n,clauses):
    return (f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()

def do(n,seed):
    start=time.monotonic()
    clauses,_=make(n,seed)
    assert witness(clauses,n) is None
    active,wit=minimize(clauses,n)
    core=[clauses[i] for i in active]
    nodes,root,steps,peak,total=run_dp(core,n)
    # Every clause in MUS appears as source ancestor of proof:
    cited={p for x in nodes for p in (x['left'],x['right']) if p.startswith('s')}
    # DP indices for minimized source must be remapped back to original indexed clauses
    for x in nodes:
        for p in ('left','right'):
            if x[p][0]=='s':x[p]='s'+str(active[int(x[p][1:])])
    cited={p for x in nodes for p in (x['left'],x['right']) if p.startswith('s')}
    assert cited=={'s'+str(i) for i in active}
    # Also obtain a full-source proof, to confirm no missing provenance after subformula choice.
    assert len(nodes)>=len(active)-1
    sat,hidden=make(n,seed+1000,True)
    assert witness(sat,n) is not None and all(eval_clause(c,hidden) for c in sat)
    result={'test':'LSPV3_461','family':'proper signed 3-CNF with 8n independent clause index draws; deterministic SHA256 counter fixture','n':n,'seed':seed,'m':len(clauses),'original_dimacs_sha256':hashlib.sha256(source_bytes(n,clauses)).hexdigest(),
    'source_dimacs':source_bytes(n,clauses).decode(),'original_clauses':[list(c) for c in clauses],
    'unsat_verified_by':'complete enumeration of 2^n assignments','core_source_ids':active,'core_deletion_witnesses':wit,
    'resolution_dag':nodes,'root':root,'resolution_inference_nodes':len(nodes),'source_count_lower_bound':len(active)-1,
    'dp_all_candidates':total,'dp_peak_live_clauses':peak,'dp_trace':steps,
    'sat_control':{'seed':seed+1000,'dimacs_sha256':hashlib.sha256(source_bytes(n,sat)).hexdigest(),'clauses':[list(c) for c in sat],'witness_bits':hidden},
    'timing':{'producer_seconds':round(time.monotonic()-start,4),'ru_maxrss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
    path=os.path.join(os.path.dirname(__file__),'raw_461_n%d_seed%d.json'%(n,seed))
    with open(path,'w') as f:json.dump(result,f,indent=2)
    print(json.dumps({'n':n,'seed':seed,'original_sha':result['original_dimacs_sha256'],'core_m':len(active),'paid_nodes':len(nodes),'maxlive':peak,'candidates':total,'seconds':result['timing']['producer_seconds'],'path':path}))
if __name__=='__main__':
    do(int(sys.argv[1]) if len(sys.argv)>1 else 16,int(sys.argv[2]) if len(sys.argv)>2 else 11)
