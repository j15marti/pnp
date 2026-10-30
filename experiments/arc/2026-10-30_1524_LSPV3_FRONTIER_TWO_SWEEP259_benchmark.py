#!/usr/bin/env python3
"""Matched Python-runtime baseline vs adaptive two-sweep DP, with certificate replay."""
import json,time,tracemalloc,statistics,sys
sys.path.insert(0,'/mnt/data/pnp_arc259')
from experiment import prep,greedy_order,messages,dpll
from verify import independent_replay

CASES=['strict22_W1_UNSAT','strict22_SWAP6_SAT','chain_XOR_12_SAT','chain_XOR_12_UNSAT','dense_planted14_SAT','dense14_UNSAT','Krom_easy_UNSAT']

def dp_controller(F):
 reads=sum(len(c) for c in F)
 original=list(range(len(F)));w=prep(F,original)[2]
 if w>4:
  greedy,work=greedy_order(F);wg=prep(F,greedy)[2]
  order=greedy if wg<w else original
 else:order=original
 out=messages(F,order,cap=9)
 if out['status']=='done':
  independent_replay(F,out['order'],out)
  return out['SAT'],out['status'],reads
 other=dpll(F)
 return other['SAT'],'fallback',reads

def plain(F):
 reads=sum(len(c) for c in F)
 out=dpll(F)
 return out['SAT'],'DPLL',reads

def measure(F,fun,reps=5):
 times=[];spaces=[];out=None
 for i in range(reps):
  tracemalloc.start();t=time.perf_counter_ns();res=fun(F)
  secs=(time.perf_counter_ns()-t)/1e6;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
  times.append(secs);spaces.append(peak)
  if out is not None:assert res==out
  out=res
 return {'milliseconds_median':statistics.median(times),'milliseconds_range':[min(times),max(times)],
         'extra_Python_heap_bytes_peak_median':statistics.median(spaces),'response':out}

def main():
 cases=json.load(open('/mnt/data/pnp_arc259/raw.json'))['cases'];results={}
 for k in CASES:
  F=cases[k]['source'];a=measure(F,plain);b=measure(F,dp_controller)
  assert a['response'][0]==b['response'][0]==cases[k]['is_SAT']
  results[k]={'baseline':a,'adaptive':b}
 print(json.dumps({'scope':'Python 3.13, tracemalloc enabled for both, input clause scan charged, 5 repetitions, DP table verification included, no external CDCL','results':results},indent=2,sort_keys=True))
 with open('/mnt/data/pnp_arc259/benchmark.json','w') as f:json.dump({'results':results,'repetitions':5,'source':'benchmark.py'},f,indent=2,sort_keys=True)
if __name__=='__main__':main()
