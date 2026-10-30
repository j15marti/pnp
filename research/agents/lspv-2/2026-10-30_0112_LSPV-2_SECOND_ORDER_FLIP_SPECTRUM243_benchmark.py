#!/usr/bin/env python3
"""Same-run peak memory and wall-clock comparison of enumerated and compressed Hamming-2 distributions."""
from __future__ import annotations
import collections,importlib.util,itertools,json,os,sys,time,tracemalloc
src=os.path.join(os.path.dirname(__file__),'2026-10-30_0112_LSPV-2_SECOND_ORDER_FLIP_SPECTRUM243.py')
spec=importlib.util.spec_from_file_location('spectrum',src);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)

def naive(F,n):
    hist=collections.Counter();source_literal_reads=0;source_clause_evals=0
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            a={x:int(x==i or x==j) for x in range(1,n+1)}
            z=[0,0,0,0]
            for c in F:
                t=sum(a[abs(l)]==int(l>0) for l in c)
                z[t]+=1;source_clause_evals+=1;source_literal_reads+=len(c)
            hist[tuple(z)]+=1
    return {'hist':dict(hist),'source_literal_reads':source_literal_reads,'source_clause_evals':source_clause_evals}

def run(fn,*args):
    tracemalloc.start();start=time.perf_counter();r=fn(*args);sec=time.perf_counter()-start
    current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return r,{'wall_seconds':sec,'peak_traced_Python_bytes':peak}

def main():
    all=[]
    for blockcount in [1,2,4,8,16]:
        F=m.plateau(blockcount);n=6*blockcount
        a={i:0 for i in range(1,n+1)}
        sparse,sm=run(m.four_class_spectrum,F,a,False)
        exhaustive,em=run(naive,F,n)
        assert exhaustive['hist']=={tuple(q['N']):q['count'] for q in sparse['hamming2_histogram']}
        all.append({'blocks':blockcount,'n':n,'m':len(F),'state_pairs':n*(n-1)//2,
                    'sparse_histogram_states':len(sparse['hamming2_histogram']),
                    'sparse_charged_selected_events':sparse['charged_work']['charged_selected_events'],
                    'naive_input_literal_reads':exhaustive['source_literal_reads'],
                    'naive_clause_evals':exhaustive['source_clause_evals'],
                    'sparse':sm,'naive':em,
                    'same_formula_both_have_identical_exact_four_category_histograms':True})
    print(json.dumps({'seed':m.SEED,'benchmarks':all},indent=2))
if __name__=='__main__':main()
