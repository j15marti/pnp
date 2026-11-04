#!/usr/bin/env python3
"""LSPV-1/394 finite charge-vector test. Usage: python script.py OUTPUT.json."""
import json,itertools,sys
EDGES={'K4':(4,[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]),
       'PRISM6':(6,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])}
def encoded(b,g):
    if not 1<=g<=len(b):raise ValueError('bad group')
    out=[]
    for a in range(0,len(b),g):
        v=b[a:a+g]
        out.append(sum(v)%2)
        out.extend(v[1:])
    return out
def decoded(z,g):
    if not 1<=g<=len(z):raise ValueError('bad group')
    out=[]
    for a in range(0,len(z),g):
        v=z[a:a+g]
        out.append(v[0] ^ (sum(v[1:])%2))
        out.extend(v[1:])
    return out
def source_cnf(h,edges,b):
    inc=[[i for i,(a,c) in enumerate(edges) if a==v or c==v] for v in range(h)]
    assert all(len(t)==3 for t in inc)
    clauses=[]
    for v,nei in enumerate(inc):
        for val in itertools.product(range(2),repeat=3):
            if sum(val)%2!=b[v]:
                clauses.append(tuple((e+1)*(1 if x==0 else -1) for e,x in zip(nei,val)))
    return clauses
def satisfies(clauses,mask):
    return all(any(bool(mask & (1<<(abs(l)-1))) == (l>0) for l in C) for C in clauses)
def star(b,g):
    root=encoded(b,g)
    ds=[]
    for i in range(len(b)):
        v=list(b);v[i]^=1
        code=encoded(v,g)
        ds.append([j for j in range(len(b)) if root[j]!=code[j]])
    degree=[sum(j in d for d in ds) for j in range(len(b))]
    best=[]
    for size in range(len(b)+1):
        for cmb in itertools.combinations(range(len(b)),size):
            if all(any(j in cmb for j in d) for d in ds):
                best=list(cmb);break
        if best:break
    return {'neighbor_differences':ds,'coordinate_degrees':degree,
            'beta':max(degree),'minimum_star_hitting':len(best),
            'star_hitting_positions':best,'predicted_group_count':(len(b)+g-1)//g}
def strict_decode(s,g):
    if not isinstance(s,str) or not s.startswith('T1:'):raise ValueError('bad tag')
    dat=s[3:]
    if not dat or not all(c in '01' for c in dat):raise ValueError('bad payload')
    if len(dat) not in (4,6):raise ValueError('template length')
    return decoded([int(t) for t in dat],g)
def main():
    passes=0;records=[]
    def check(v):
        nonlocal passes
        if not v:raise AssertionError('check '+str(passes))
        passes+=1
    for name,(h,edges) in EDGES.items():
        counts=[]
        for t in range(1<<h):
            b=[(t>>j)&1 for j in range(h)]
            clauses=source_cnf(h,edges,b)
            models=sum(satisfies(clauses,x) for x in range(1<<len(edges)))
            check(len(clauses)==4*h)
            check((models>0)==(sum(b)%2==0))
            check(models==(1<<(len(edges)-h+1)) if sum(b)%2==0 else models==0)
            counts.append(models)
        center=[1]+[0]*(h-1)
        check(counts[1]==0)
        groups=[]
        for g in range(1,h+1):
            if h%g:continue
            for x in itertools.product(range(2),repeat=h):
                y=encoded(list(x),g)
                check(decoded(y,g)==list(x))
                check(sum(x)%2 == sum(y[k] for k in range(0,h,g))%2)
                check(strict_decode('T1:'+''.join(map(str,y)),g)==list(x))
            d=star(center,g)
            check(d['minimum_star_hitting']==h//g)
            check(d['beta']==g)
            check(all(0<len(v)<=2 for v in d['neighbor_differences']))
            check(d['star_hitting_positions']==list(range(0,h,g)))
            groups.append({'group_size':g,**d})
        records.append({'name':name,'variables':len(edges),'vertices':h,'edge_list':edges,
                        'unsat_charges':sum(v==0 for v in counts),
                        'sat_charges':sum(v>0 for v in counts),
                        'center_charge':center,'model_count_by_charge_int':counts,'groups':groups})
    bad=['','T1:','T1:000','T1:00000','T1:00a0','T2:0000','T1:0000extra',None,1]
    rejected=[]
    for s in bad:
        try:strict_decode(s,2)
        except (ValueError,TypeError):rejected.append(repr(s));check(True)
        else:raise AssertionError('malformed accepted')
    result={'result_id':'LSPV1_394_STAR_LOCALITY_QUERY_TRANSFER','status':'FINITE-COMPUTATIONAL',
            'random_seed':None,'assertions':passes,'graph_records':records,
            'malformed_rejections':rejected,
            'proof_scope':'Finite charge templates only; theorem concerns all adaptive encoded-bit readers.'}
    with open(sys.argv[1] if len(sys.argv)>1 else 'lspv1_394_star_locality_raw.json','w') as f:
        json.dump(result,f,indent=2)
    print(json.dumps({'passed':passes,'graphs':len(records),'malformed':len(rejected)}))
if __name__=='__main__':main()
