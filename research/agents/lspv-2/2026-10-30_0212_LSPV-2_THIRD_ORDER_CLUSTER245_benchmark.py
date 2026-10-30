#!/usr/bin/env python3
"""Same-input indexed Python triple histogram benchmark; run separately per size."""
import argparse,collections,importlib.util,itertools,json,math,time,tracemalloc
from pathlib import Path
p=Path(__file__).with_name('2026-10-30_0212_LSPV-2_THIRD_ORDER_CLUSTER245.py')
spec=importlib.util.spec_from_file_location('triple245',p);lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)

def naive_incremental(F,base):
    n=len(base);inc=collections.defaultdict(list);counts=[0]*4;T=[];operations=0
    for j,c in enumerate(F):
        for z in c:inc[abs(z)].append(j);operations+=1
        t=sum(base[abs(z)]==int(z>0) for z in c);T.append(t);counts[t]+=1;operations+=len(c)
    H=collections.Counter()
    for triple in itertools.combinations(range(1,n+1),3):
        changed=set(inc[triple[0]]+inc[triple[1]]+inc[triple[2]])
        v=counts[:]
        for j in changed:
            c=F[j];t=T[j]
            for z in c:
                if abs(z) in triple:t+=1 if base[abs(z)]!=int(z>0) else -1
                operations+=1
            v[T[j]]-=1;v[t]+=1
        H[tuple(v)]+=1;operations+=1
    return {k:v for k,v in H.items() if v},operations

def measure(fn):
    tracemalloc.start();t=time.perf_counter();x=fn();elapsed=time.perf_counter()-t;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return x,{'seconds':elapsed,'traced_peak_bytes':peak}

def run(r):
    F=lib.plateau(r);n=6*r;a={i:0 for i in range(1,n+1)}
    compressed,p1=measure(lambda:lib.three_flip_spectrum(F,a,False))
    naive,p2=measure(lambda:naive_incremental(F,a))
    encoded={tuple(z['N0_N1_N2_N3']):z['count'] for z in compressed['three_flip_histogram']}
    assert encoded==naive[0]
    return {'n':n,'m':len(F),'original_clause_degree_bound':4,
            'triple_states_avoided_by_compressed':math.comb(n,3),
            'compressed_distinct_vectors':len(encoded),
            'compressed':{**p1,'selected_operations':compressed['counted_selected_operations']},
            'enumeration':{**p2,'selected_operations':naive[1]},
            'histograms_equal':True}
if __name__=='__main__':
    args=argparse.ArgumentParser();args.add_argument('r',type=int);x=args.parse_args()
    v=run(x.r)
    print(json.dumps(v,indent=2))
    out=Path(__file__).with_name(f'benchmark_r{x.r:02}.json');out.write_text(json.dumps(v,indent=2))