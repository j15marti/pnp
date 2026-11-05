#!/usr/bin/env python3
"""Independent source-hash and essential-boundary-port replay for LSPV-4/418."""
import json,itertools,hashlib,sys
j=json.load(open(sys.argv[1] if len(sys.argv)>1 else '2026-11-05_1036_LSPV4_418_RAW_summary.json'))
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def graph(name):
 if name=='K4':return 4,[(i,k) for i in range(4) for k in range(i+1,4)],set(range(2))
 if name=='cube':return 8,[(i,i^p) for i in range(8) for p in (1,2,4) if i<i^p],set(range(4))
 if name=='Petersen':return 10,[(i,(i+1)%5) for i in range(5)]+[(i,5+i) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)],set(range(5))
 if name=='Heawood':return 14,[(i,7+k) for k in range(7) for i in (k,(k+1)%7,(k+3)%7)],set(range(7))
 raise ValueError(name)
def comps(es,S):
 unseen=set(S);cs=[]
 while unseen:
  todo=[unseen.pop()];c=set()
  while todo:
   v=todo.pop();c.add(v)
   for a,b in es:
    w=b if a==v else a if b==v else None
    if w in unseen:unseen.remove(w);todo.append(w)
  cs.append(c)
 return cs
def relation(es,cs,bound,odd,mask):
 xs={e:(mask>>i)&1 for i,e in enumerate(bound)}
 return all(sum(xs[i] for i,(a,b) in enumerate(es) if (a in c)!=(b in c))%2==int(odd and 0 in c) for c in cs)
ck(j['schema']=='LSPV4_418_PUBLIC_RAW_SUMMARY')
for row in j['fixtures']:
 H,es,S=graph(row['graph']);es=sorted(tuple(sorted(e)) for e in es)
 B=[i for i,(a,b) in enumerate(es) if (a in S)!=(b in S)]
 C=comps(es,S);odd=row['charge']=='odd'
 ck(len(B)==row['boundary_b']);ck(len(C)==row['components'])
 lines=[]
 for v in range(H):
  ids=[i+1 for i,(a,b) in enumerate(es) if v in (a,b)]
  ck(len(ids)==3)
  for bits in itertools.product((0,1),repeat=3):
   if (sum(bits)&1)!=int(odd and v==0):
    lines.append(' '.join(str(-z if x else z) for z,x in zip(ids,bits))+' 0\n')
 source=('p cnf %d %d\n'%(len(es),len(lines))+''.join(lines)).encode()
 ck(len(source)*8==row['source_bits'])
 ck(hashlib.sha256(source).hexdigest()==row['sha256_source'])
 ck(sum(i.bit_length() for i in range(1,len(B)+1))<=row['child_bits'])
 witness=0
 for c in C:
  if odd and 0 in c:
   edge=next(i for i,(a,b) in enumerate(es) if (a in c)!=(b in c))
   witness^=1<<B.index(edge)
 ck(relation(es,C,B,odd,witness))
 for i in range(len(B)):ck(not relation(es,C,B,odd,witness^(1<<i)))
print('PASS',checks,'independent compact checks')
