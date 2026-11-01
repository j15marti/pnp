#!/usr/bin/env python3
"""Event-sourced fixed-location writable/index tape simulation for a certified
canonical M22 disjoint-component child emitter. Input read-only; index and
output register/tape writes are explicit, including no-op writes. Not FLMV TM.
"""
import ast, gzip, json, pathlib, hashlib
P=pathlib.Path(__file__).resolve().parent
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
U=tuple(tuple(x) for x in ast.literal_eval(''.join(x for x in (P/'U198.txt').read_text().splitlines() if not x.startswith('#'))))
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))
def gamma(x):
 b=bin(x)[2:];return '0'*(len(b)-1)+b
def encode(F,n):
 w=n.bit_length()
 return gamma(n)+gamma(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)
def joined(F,n):
 m=n
 return tuple(F)+tuple(tuple((1 if x>0 else -1)*(abs(x)+m) for x in c) for c in Y)

def simulate(name,F,n):
 parent=joined(F,n);nP=n+6;nC=n;mP=len(parent);mC=len(F)
 Pbits=encode(parent,nP);Cbits=encode(F,nC)
 hP=len(gamma(nP))+len(gamma(mP));hC=len(gamma(nC))+len(gamma(mC))
 wP=nP.bit_length();wC=nC.bit_length();rP=1+3*wP;rC=1+3*wC
 idxwidth=max(len(Pbits),len(Cbits)).bit_length()
 si=[0]*idxwidth;oi=[0]*idxwidth;out=[0]*len(Cbits)
 counts={'index_tape_writes':0,'output_index_tape_writes':0,'output_tape_writes':0,'source_reads':0,'actual_one_cell_changes':0,'noop_writes':0,'event_records':0,'header_bits':0,'indexed_body_bits':0}
 path=P/f'{name}_physical_events295.jsonl.gz'
 with gzip.open(path,'wt') as dest:
  def write(tape,index,bit,rec):
   arr={'SI':si,'OI':oi,'OUT':out}[tape]
   old=arr[index];arr[index]=bit
   counts['event_records']+=1
   counts['actual_one_cell_changes']+=int(old!=bit)
   counts['noop_writes']+=int(old==bit)
   counts[{'SI':'index_tape_writes','OI':'output_index_tape_writes','OUT':'output_tape_writes'}[tape]]+=1
   dest.write(json.dumps({'t':tape,'i':index,'a':old,'b':bit,'clause':rec},separators=(',',':'))+'\n')
  def program(tape,integer,rec):
   for k in range(idxwidth):write(tape,k,(integer>>k)&1,rec)
  for i in range(len(Cbits)):
   j=None
   if i<hC:
    bit=int((gamma(nC)+gamma(mC))[i]);counts['header_bits']+=1
   else:
    q=i-hC;j,t=divmod(q,rC)
    if t==0:at=hP+j*rP
    else:
     k=t-1;at=hP+j*rP+1+(k//wC)*wP+(wP-wC)+(k%wC)
    assert 0<=at<len(Pbits)
    program('SI',at,j)
    bit=int(Pbits[at]);counts['source_reads']+=1;counts['indexed_body_bits']+=1
   program('OI',i,j)
   write('OUT',i,bit,j)
  # Index tapes reset to their physically fixed zero configuration.
  program('SI',0,None);program('OI',0,None)
 assert ''.join(map(str,out))==Cbits
 assert si==oi==[0]*idxwidth
 counts['physical_endpoint_xor']=sum(out)
 counts['parent_length']=len(Pbits);counts['child_length']=len(Cbits)
 counts['src_width']=wP;counts['child_width']=wC
 counts['changed_record_ids_removed']=list(range(mC,mP))
 counts['logical_removed_clause_records']=len(parent)-len(F)
 counts['read_only_source']='immutable parent bits';counts['writable_semantics']='fixed-cell 1 bit per write event, two index registers and output tape'
 counts['trace_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
 return counts

def main():
 result={'scope':'physical tape bit writes in declared simulator only; no native FLMV bound','cases':{}}
 for name,F,n in [('Y6+Y6_SAT',Y,6),('U198+Y6_UNSAT',U,198),('V198+Y6_SAT',V,198)]:
  result['cases'][name]=simulate(name,F,n)
 (P/'physical295.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({n:{k:v for k,v in d.items() if k not in ('changed_record_ids_removed','trace_sha256')} for n,d in result['cases'].items()},indent=2))
if __name__=='__main__':main()