#!/usr/bin/env python3
"""LSPV-3/459. Exact first width-4 and second width-5 legal RES controls.
Standalone source-indexed mathematical experiment, NOT historical
R_mix341 accepted-byte checker. Python stdlib only.
"""
import argparse, collections, hashlib, itertools, json, math, random, sys, time, resource

def source(n, seed):
    rng = random.Random(seed)
    out = []
    for _ in range(8*n):
        xs = sorted(rng.sample(range(1,n+1), 3))
        out.append(tuple(x if rng.getrandbits(1) else -x for x in xs))
    return out

def source_sha(src):
    return hashlib.sha256(('\n'.join(' '.join(map(str,c))+' 0' for c in src)+'\n').encode()).hexdigest()

def resolve(a,b,p):
    sa,sb=set(a),set(b)
    if not ((p in sa and -p in sb) or (-p in sa and p in sb)):
        return None
    rest_a={x for x in sa if abs(x)!=abs(p)}
    rest_b={x for x in sb if abs(x)!=abs(p)}
    new=rest_a|rest_b
    if any(-l in new for l in new):return None
    return tuple(sorted(new,key=lambda x:(abs(x),x)))

def exact_prob(n):
    m=8*n
    c=math.comb(n,3)
    p3=3*(n-3)/(2*c)
    p4=3*math.comb(n-3,2)/(2*c)
    p45=2*math.comb(n-4,2)/c if n>=6 else 0
    return {'p3':p3,'p4':p4,'p45':p45,'EZ3':math.comb(m,2)*p3,
            'EZ4':math.comb(m,2)*p4,'VarZ4':math.comb(m,2)*p4*(1-p4),
            'ET5':math.comb(m,2)*(m-2)*p4*p45}

def index(src):
    z=collections.defaultdict(list)
    for j,c in enumerate(src):
        for l in c:z[l].append(j)
    return z

def enumerate_counts(src, keep_sample=4):
    idx=index(src)
    z3=0;z4=0;t5=0
    s4=[];s5=[]
    for v in {abs(l) for c in src for l in c}:
        for i in idx[v]:
            for j in idx[-v]:
                if i==j:continue
                ci,cj=src[i],src[j]
                if len({abs(x) for x in ci}&{abs(x) for x in cj})!=1:continue
                r=resolve(ci,cj,v)
                if r is None or len(r)!=4:raise AssertionError('illegal source pair')
                z4+=1
                if len(s4)<keep_sample:s4.append([i,j,v,list(r)])
                supp={abs(x) for x in r}
                for l in r:
                    for k in idx[-l]:
                        if k==i or k==j:continue
                        ck=src[k]
                        if len(supp&{abs(x) for x in ck})!=1:continue
                        r2=resolve(r,ck,l)
                        if r2 is None or len(r2)!=5:raise AssertionError('illegal 2nd pivot')
                        t5+=1
                        if len(s5)<keep_sample:s5.append([i,j,k,v,l,list(r),list(r2)])
    for i,c in enumerate(src):
        for j in range(i+1,len(src)):
            d=src[j]
            if len({abs(x) for x in c}&{abs(x) for x in d})==2:
                found=[]
                for x in c:
                    if -x in d:
                        r=resolve(c,d,x)
                        if r is not None and len(r)==3:found.append(r)
                if len(found)==1:z3+=1
    return {'z3':z3,'z4':z4,'t5':t5,'samples4':s4,'samples5':s5}

def hostile(src, sample4, sample5):
    i,j,p,r=sample4
    assert resolve(src[i],src[j],p)==tuple(r)
    assert resolve(src[i],src[j],-p)==tuple(r)
    assert resolve(src[i],src[j],abs(p)+100000) is None
    assert resolve(src[i],src[i],p) is None
    a,b,k,x,y,inner,outer=sample5
    assert resolve(src[a],src[b],x)==tuple(inner)
    assert resolve(inner,src[k],y)==tuple(outer)
    assert resolve(inner,src[k],abs(y)+100000) is None
    assert source_sha(src)!=source_sha(src[:-1]+[tuple(-v for v in src[-1])])
    return 8

def run(ns,seeds):
    entries=[]
    t0=time.perf_counter()
    fixture=None
    for n in ns:
        for seed in seeds:
            src=source(n,seed)
            p=exact_prob(n)
            t1=time.perf_counter()
            res=enumerate_counts(src)
            sec=round(time.perf_counter()-t1,4)
            assertions=hostile(src,res['samples4'][0],res['samples5'][0])
            rec={'n':n,'m':len(src),'seed':seed,'sha256':source_sha(src),
                 'theory':p,'actual':res,'hostile_assertions':assertions,
                 'wall_seconds_experiment_only':sec}
            entries.append(rec)
            print('n',n,'seed',seed,'Z3',res['z3'],'Z4',res['z4'],'T5',res['t5'],
                  'EZ4',round(p['EZ4']),'ET5',round(p['ET5']),'sec',sec, flush=True)
            if fixture is None:fixture={'n':n,'seed':seed,'source':[list(c) for c in src],
                    'sha256':source_sha(src),'actual':res}
    return {'status':'COMPUTATIONAL; not native historical R_mix341',
            'family':'8n independently sampled proper signed 3-CNF clauses with replacement',
            'theorem':'pairwise-independent width-4 source-pair count; expected second width-5 paths',
            'entries':entries,'independent_fixture':fixture,
            'total_experiment_wall_seconds':round(time.perf_counter()-t0,4),
            'maxrss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--n',nargs='+',type=int,default=[64,128,256,512])
    ap.add_argument('--seeds',nargs='+',type=int,default=[11,23])
    ap.add_argument('--out',default='459_results.json')
    a=ap.parse_args()
    data=run(a.n,a.seeds)
    with open(a.out,'w') as f:json.dump(data,f,indent=2,sort_keys=True)
    print('WROTE',a.out)
if __name__=='__main__':main()
