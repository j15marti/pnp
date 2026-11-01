#!/usr/bin/env python3
"""Independent replay of event streams, including changed cells, idle writes,
source indexed reads, changed original clause records and endpoint XOR.
Does not import physical producer.
"""
from pathlib import Path
from collections import Counter
import json,gzip,ast,hashlib
P=Path(__file__).resolve().parent
D=json.loads((P/'physical295.json').read_text())
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
U=tuple(map(tuple,ast.literal_eval(''.join(s for s in (P/'U198.txt').read_text().splitlines() if not s.startswith('#')))))
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))
def gc(x):
 s=format(x,'b');return '0'*(len(s)-1)+s
def enc(F,n):
 w=n.bit_length()
 return gc(n)+gc(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)

def check(name,F,n):
 m=len(F); nP=n+6
 tail=tuple(tuple((1 if x>0 else -1)*(abs(x)+n) for x in c) for c in Y)
 parent=F+tail;Pbits=enc(parent,nP);Cbits=enc(F,n)
 W=max(len(Pbits),len(Cbits)).bit_length()
 tapes={'SI':[0]*W,'OI':[0]*W,'OUT':[0]*len(Cbits)}
 cnt=Counter();trace=P/f'{name}_physical_events295.jsonl.gz'
 srcidx=0;destidx=0;outwrites=0
 with gzip.open(trace,'rt') as z:
  for record in z:
   ev=json.loads(record);t=ev['t'];i=ev['i'];old=ev['a'];new=ev['b'];cl=ev['clause']
   assert t in tapes and 0<=i<len(tapes[t]);assert tapes[t][i]==old
   tapes[t][i]=new
   cnt['events']+=1;cnt['xor']+=(old!=new);cnt['noops']+=(old==new)
   cnt[t]+=1
   if t=='OUT':
    assert i==outwrites,'strict monotone materialization positions'
    assert new==int(Cbits[i]);outwrites+=1
   if t=='SI':srcidx=sum(q<<j for j,q in enumerate(tapes['SI']))
   if t=='OI':destidx=sum(q<<j for j,q in enumerate(tapes['OI']))
   if t=='OUT':assert destidx==i,'output head programmed'
 assert ''.join(map(str,tapes['OUT']))==Cbits
 assert tapes['SI']==tapes['OI']==[0]*W
 d=D['cases'][name]
 assert cnt['events']==d['event_records']
 assert cnt['xor']==d['actual_one_cell_changes']
 assert cnt['noops']==d['noop_writes']
 assert cnt['SI']==d['index_tape_writes']
 assert cnt['OI']==d['output_index_tape_writes']
 assert cnt['OUT']==d['output_tape_writes']
 assert sum(tapes['OUT'])==d['physical_endpoint_xor']
 assert d['changed_record_ids_removed']==list(range(m,m+8))
 assert hashlib.sha256(trace.read_bytes()).hexdigest()==d['trace_sha256']
 # Independent indexed child read mapping; not based on the producer output tape.
 hP=len(gc(nP))+len(gc(len(parent)));hC=len(gc(n))+len(gc(m))
 wP=nP.bit_length();wC=n.bit_length()
 for at in range(hC,len(Cbits)):
  j,t=divmod(at-hC,1+3*wC)
  src=hP+j*(1+3*wP)
  if t>0:
   k=t-1;src+=1+(k//wC)*wP+(wP-wC)+(k%wC)
  assert Pbits[src]==Cbits[at],(name,at,src)
 return {'status':'PASS','events':cnt['events'],'xor':cnt['xor'],'endpoint_xor':sum(tapes['OUT']),'indexed_bits':len(Cbits)-hC,'removed_source_records':8}

def main():
 summary={}
 for name,F,n in [('Y6+Y6_SAT',Y,6),('U198+Y6_UNSAT',U,198),('V198+Y6_SAT',V,198)]:summary[name]=check(name,F,n)
 (P/'physical_independent294.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()