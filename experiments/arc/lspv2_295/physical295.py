#!/usr/bin/env python3
"""LSPV-2 fixed-location index/output tape event tracer (offline macro simulator).
No claim of native FLMV resource accounting. Outputs every actual declared write.
"""
from pathlib import Path
import gzip, json
import k5_scc295 as S
R=Path(__file__).resolve().parent

def append(F,Y):
 n=max(abs(l) for c in F for l in c)
 return tuple(F)+tuple(tuple((1 if l>0 else -1)*(n+abs(l)) for l in c) for c in Y)

def trace(H,name):
 P=append(H,S.Y6)
 assert S.valid(P) and S.valid(H)
 source=S.encode(P);child=S.encode(H)
 assert S.decode(source)==P and S.decode(child)==H
 np=max(abs(l) for c in P for l in c);nc=np-6
 wp=np.bit_length();wc=nc.bit_length();mp=len(P);mc=len(H)
 hp=len(S.gamma(np))+len(S.gamma(mp));hc=len(S.gamma(nc))+len(S.gamma(mc))
 rp=1+3*wp;rc=1+3*wc
 ilen=max(1,(len(source)-1).bit_length());index=[0]*ilen
 output=[0]*len(child)
 counters={'source_validation_bit_reads':len(source),'source_bit_reads':0,'index_writes':0,'output_writes':0,'unchanged_writes':0,'dphys_sum':0,'dphys_endpoint':None,'dlogic_endpoint':None,'changed_original_clause_ids':[]}
 visited=set();tape_events=0
 eventfile=R/(name+'_physical_events295.jsonl.gz')
 with gzip.open(eventfile,'wt',encoding='utf-8') as gz:
  def emit(tape,at,new):
   nonlocal tape_events
   ar=index if tape=='index' else output
   old=ar[at];ar[at]=new;delta=old!=new
   counters[tape+'_writes']+=1
   counters['dphys_sum']+=int(delta)
   counters['unchanged_writes']+=int(not delta)
   gz.write(json.dumps([tape,at,old,new,int(delta)],separators=(',',':'))+'\n')
   tape_events+=1
  for q,target in enumerate(child):
   if q<hc:bit=int(target)
   else:
    rel=q-hc;clause=rel//rc;off=rel%rc
    if off==0:src=hp+clause*rp
    else:
     k=(off-1)//wc;b=(off-1)%wc
     src=hp+clause*rp+1+k*wp+(wp-wc)+b
    if clause>=mc or src>=len(source):raise AssertionError('source address')
    visited.add(clause)
    for z in range(ilen):emit('index',z,(src>>z)&1)
    bit=int(source[src]);counters['source_bit_reads']+=1
   if bit!=int(target):raise AssertionError('incorrect indexed child bit')
   emit('output',q,bit)
 counters['physical_events']=tape_events
 counters['dphys_endpoint']=sum(index)+sum(output)
 counters['dlogic_endpoint']=sum(int(a!=b) for a,b in zip(source,child))+abs(len(source)-len(child)) # separate aligned-bit diagnostic
 counters['changed_original_clause_ids']=sorted(visited)
 counters['parent_bits']=len(source);counters['child_bits']=len(child)
 counters['source_bits']=source;counters['child_bits_string']=child
 return counters

def main():
 U,V=S.source198()
 result={name:trace(H,name) for name,H in [('Y6plusY6_SAT',S.Y6),('U198plusY6_UNSAT',U),('V198plusY6_SAT',V)]}
 (R/'physical295.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:{p:v for p,v in stats.items() if p not in ('source_bits','child_bits_string','changed_original_clause_ids')} for k,stats in result.items()},indent=2))
if __name__=='__main__':main()
