#!/usr/bin/env python3
"""LSPV-3/412: readable-DEF-facet / strict-RES context replay.
Run: python experiments/arc/lspv3_412_contextual_gate_replay.py
Optional output: LSPV3_412_OUT=/path/to/record.json
No claim of full native R_mix341 exported DEF facet grammar or B3.
"""
import itertools, json, os, random
R = random.Random(412)
checks = 0
def ck(test, msg):
    global checks
    checks += 1
    if not test: raise AssertionError(msg)
def gate(m, a, b): return (m >> (2*a+b)) & 1
def lit(v, b): return v if b else -v
def canon(c):
    s = set(c)
    if any(-v in s for v in s): return None
    return tuple(sorted(s, key=lambda v:(abs(v),v<0)))
def facets(g):
    rows=[]
    for a,b in itertools.product((0,1),repeat=2):
        c=canon((-lit(g['u'],a),-lit(g['v'],b),lit(g['out'],gate(g['mask'],a,b))))
        if c is not None and c not in rows: rows.append(c)
    return rows
def values(gs,a):
    d={1:a[0],2:a[1],3:a[2]}
    for g in gs:
        ck(g['u'] in d and g['v'] in d and g['out'] not in d, 'nonfresh gate')
        d[g['out']]=gate(g['mask'],d[g['u']],d[g['v']])
    return d
class DAG:
    def __init__(self,new):
        self.lines={};self.parents={};self.info={};self.r=0;self.row={}
        for i,g in enumerate(new):
            for j,c in enumerate(facets(g)):
                k=f'G{i}.{j}'
                self.lines[k]=c;self.parents[k]=[];self.info[k]=['facet',g['out'],j]
                self.row[(i,c)]=k
    def res(self,a,b,p):
        c,d=self.lines[a],self.lines[b]
        ck((p in c and -p in d) or (-p in c and p in d),'wrong pivot')
        out=canon([v for v in c if abs(v)!=p]+[v for v in d if abs(v)!=p])
        ck(out is not None,'tautological resolvent')
        self.r+=1;k=f'R{self.r}'
        self.lines[k]=out;self.parents[k]=[a,b];self.info[k]=['RES',p]
        return k
def build(old):
    t=len(old)
    tables={}
    for g in old:
        f=[]
        for a in itertools.product((0,1),repeat=3):f.append(values(old,a)[g['out']])
        tables[g['out']]=f
    new=[];nxt=4+t
    for g in old:
        f=tables[g['out']]
        def co(k):
            return sum(f[(k<<2)|(a<<1)|b]<<(2*a+b) for a,b in itertools.product((0,1),repeat=2))
        a,b,d,e=nxt,nxt+1,nxt+2,nxt+3;nxt+=4
        new.extend([dict(out=a,u=2,v=3,mask=co(0)),
                    dict(out=b,u=2,v=3,mask=co(1)),
                    dict(out=d,u=a,v=b,mask=6),
                    dict(out=e,u=1,v=d,mask=8),
                    dict(out=g['out'],u=a,v=e,mask=6)])
    dag=DAG(new);contexts={}
    for x in itertools.product((0,1),repeat=3):
        ov=values(old,x);v=values(new,x)
        for g in old:ck(ov[g['out']]==v[g['out']],'output mismatch')
        blockers=set(-lit(i,x[i-1]) for i in (1,2,3))
        cond={}
        for j,g in enumerate(new):
            a,b=v[g['u']],v[g['v']]
            row=canon((-lit(g['u'],a),-lit(g['v'],b),lit(g['out'],v[g['out']])))
            ck(row is not None,'impossible actual row')
            k=dag.row[(j,row)]
            for u in (g['u'],g['v']):
                if u>3 and -lit(u,v[u]) in dag.lines[k]:
                    ck(lit(u,v[u]) in dag.lines[cond[u]],'missing input port')
                    k=dag.res(k,cond[u],u)
            c=dag.lines[k]
            ck(set(c)<=blockers|{lit(g['out'],v[g['out']])},'bad context clause')
            ck(lit(g['out'],v[g['out']]) in c,'lost conditional output')
            cond[g['out']]=k
        contexts[x]=(v,cond)
    roots=[]
    for g in old:
        for C in facets(g):
            fixed={abs(l):(0 if l>0 else 1) for l in C if abs(l)<=3}
            free=[i for i in (1,2,3) if i not in fixed];leaves={}
            for tail in itertools.product((0,1),repeat=len(free)):
                x=dict(fixed);x.update(zip(free,tail));aa=tuple(x[i] for i in (1,2,3))
                v,cond=contexts[aa]
                hits=[l for l in C if abs(l)>3 and v[abs(l)]==(l>0)]
                ck(bool(hits),'old facet not entailed')
                k=cond[abs(hits[0])]
                ck(set(dag.lines[k])<=set(-lit(i,aa[i-1]) for i in (1,2,3))|set(C),'bad leaf')
                leaves[tuple(x[i] for i in free)]=k
            for j in range(len(free)-1,-1,-1):
                i=free[j];merged={}
                for key in sorted({v[:j] for v in leaves}):
                    l,h=leaves[key+(0,)],leaves[key+(1,)]
                    if i in dag.lines[l] and -i in dag.lines[h]: k=dag.res(l,h,i)
                    elif i not in dag.lines[l]: k=l
                    elif -i not in dag.lines[h]: k=h
                    else: raise AssertionError('bad join')
                    merged[key]=k
                leaves=merged
            k=leaves[()]
            ck(set(dag.lines[k])<=set(C),'wrong final subclause')
            roots.append(dict(old_facet=C,derived=dag.lines[k],node=k))
    for x in itertools.product((0,1),repeat=3):
        v=values(new,x)
        for C in dag.lines.values():
            ck(any(v[abs(l)]==(l>0) for l in C),'invalid proof line')
    ck(len(new)+dag.r <= 113*t,'bound exceeded')
    return dict(t=t,defs=len(new),facet_count=len(roots),res=dag.r,
        paid=len(new)+dag.r,bound=113*t,old=old,new=new,
        roots=roots, proof=dict(clauses=dag.lines,parents=dag.parents,info=dag.info))
def main():
    samples=[]
    for t in (1,2,3,5,8,12,16):
        for trial in range(9):
            old=[]
            for i in range(t):
                name=4+i
                old.append(dict(out=name,u=R.randrange(1,name),v=R.randrange(1,name),mask=R.randrange(16)))
            proof=build(old)
            samples.append({k:proof[k] for k in ('t','defs','facet_count','res','paid','bound')})
    special=[dict(out=4,u=1,v=2,mask=6),dict(out=5,u=4,v=3,mask=6),
             dict(out=6,u=5,v=5,mask=6),dict(out=7,u=4,v=5,mask=8),
             dict(out=8,u=6,v=7,mask=15)]
    sp=build(special);samples.append({**{k:sp[k] for k in ('t','defs','facet_count','res','paid','bound')},'fixture':'XOR-cancel-reconverge'})
    result=dict(run='LSPV3_412',status='PASS',seed=412,checks=checks,
        trials=len(samples),max_ratio=max(x['paid']/x['t'] for x in samples),
        samples=samples,structured_witness=sp,
        caveat='conditional readable DEF facets and strict RES consumers only; full native/B3 OPEN')
    with open(os.getenv('LSPV3_412_OUT','lspv3_412_raw.json'),'w') as f: json.dump(result,f,indent=2)
    print(json.dumps({k:result[k] for k in ('run','status','seed','checks','trials','max_ratio')},indent=2))
if __name__=='__main__':main()
