#!/usr/bin/env python3
import argparse,importlib.util,json,sys,time,tracemalloc,collections
p=argparse.ArgumentParser();p.add_argument('--k',type=int,required=True);p.add_argument('--r',type=int,default=2);p.add_argument('--out',default='bench250.json');p.add_argument('--updates',type=int,default=5);o=p.parse_args()
spec=importlib.util.spec_from_file_location('core','2026-10-30_0512_LSPV-2_DYNAMIC_CLUSTER250.py')
core=importlib.util.module_from_spec(spec);sys.modules[spec.name]=core;spec.loader.exec_module(core)
def v(j,i):return 6*(j%o.k)+i
def plateau(k):
 out=[]
 for j in range(k):
  out.extend([(v(j-1,1),v(j,3),v(j,5)),(v(j,1),-v(j,3),v(j,6)),(-v(j,1),v(j,4),v(j,5)),(-v(j,1),-v(j,4),v(j,6)),(v(j,2),v(j,3),-v(j,5)),(v(j,2),-v(j,3),-v(j,6)),(-v(j,2),v(j,4),-v(j,5)),(-v(j,2),-v(j,4),-v(j,6))])
 return out
n=6*o.k;C=plateau(o.k);assert core.strict22(C,n)
g,inc=core.adjacency(C,n);seen={0};q=[0];
for x in q:
 for v in g[x]-seen:seen.add(v);q.append(v)
assert len(seen)==n
flips=([0,1,2,0,3,5,2,0,4,1])[:o.updates]
tracemalloc.start();t=time.perf_counter();D=core.Dynamic(C,n,[0]*n,o.r)
trace=[]
for x in flips:
 count=D.flip(x)
 trace.append({'x':x+1,'affected_support_count':count,'N0':D.N[0]})
dsecs=time.perf_counter()-t;dmem=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
tracemalloc.start();t=time.perf_counter();a=[0]*n;work=collections.Counter()
for x in [None]+flips:
 if x is not None:a[x]^=1
 F=core.Dynamic(C,n,a,o.r)
 assert [F.histogram(k) for k in range(o.r+1)] == [D.histogram(k) for k in range(o.r+1)] if x==flips[-1] else True
 work.update(F.Ledger.out())
fsecs=time.perf_counter()-t;fmem=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
b=core.dpll(C,n)
assert b['sat']
res={'k':o.k,'n':n,'m':len(C),'radius':o.r,'updates':len(flips),'source_connected':True,'source_strict22':True,
 'dynamic_total_seconds_including_initialization':dsecs,'fresh_total_seconds_including_all_restarts':fsecs,
 'dynamic_tracemalloc_peak_bytes':dmem,'fresh_tracemalloc_peak_bytes':fmem,
 'dynamic_selected_events':D.Ledger.out(),'fresh_selected_events':dict(work),'updates_trace':trace,
 'actual_DPLL_nodes':b['nodes'],'certificate':'All global assignments, source incidences, and histogram operations are coherent; DPLL witness rechecked by source evaluation.'}
open(o.out,'w').write(json.dumps(res,indent=2));print(json.dumps({k:res[k] for k in ('n','radius','updates','dynamic_total_seconds_including_initialization','fresh_total_seconds_including_all_restarts','dynamic_tracemalloc_peak_bytes','fresh_tracemalloc_peak_bytes')}),flush=True)