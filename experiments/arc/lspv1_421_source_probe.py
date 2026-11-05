#!/usr/bin/env python3
"""LSPV-1/421 source-block proof of concept; native Rmix checker is not invoked."""
import json,hashlib
from pathlib import Path
def k4(): return [(a,b) for a in range(4) for b in range(a+1,4)]
def prism(k):
 e=set()
 for t in range(2):
  for i in range(k):
   a=t*k+i;b=t*k+(i+1)%k;e.add((min(a,b),max(a,b)))
 for i in range(k):e.add((i,i+k))
 return sorted(e)
def bad_patterns(c):
 return [tuple((a>>j)&1 for j in range(3)) for a in range(8) if sum((a>>j)&1 for j in range(3))%2!=c]
def gauss(rows,n):
 a=[[m,b] for m,b in rows];r=0;p=[]
 for c in range(n):
  j=next((j for j in range(r,len(a)) if a[j][0]>>c&1),None)
  if j is None:continue
  a[r],a[j]=a[j],a[r]
  for i in range(len(a)):
   if i!=r and a[i][0]>>c&1:a[i][0]^=a[r][0];a[i][1]^=a[r][1]
  p.append(c);r+=1
 assert not any(m==0 and b for m,b in a)
 z=[0]*n
 for i in range(r-1,-1,-1):
  c=p[i];z[c]=a[i][1]^(sum(z[j] for j in range(c+1,n) if a[i][0]>>j&1)%2)
 assert all((sum(z[j] for j in range(n) if mask>>j&1)%2)==b for mask,b in rows)
 return z
def sat(c,z):return any(z[abs(v)-1]==(v>0) for v in c)
def parse(t):
 try:
  assert t.isascii() and t.endswith('\n')
  ls=t.splitlines();h=ls[0].split()
  assert len(h)==4 and h[:2]==['p','cnf']
  n,m=map(int,h[2:]);assert n>0 and m>0 and len(ls)==m+1
  cs=[]
  for line in ls[1:]:
   vals=[int(x) for x in line.split()]
   assert len(vals)>1 and vals[-1]==0
   v=vals[:-1];assert all(0<abs(x)<=n for x in v)
   assert len(set(abs(x) for x in v))==len(v);cs.append(v)
  return n,cs
 except Exception as e:raise ValueError('malformed DIMACS') from e
def test(name,h,edges):
 edges=sorted(edges);assert len(edges)==3*h//2
 inc=[[] for _ in range(h)]
 for j,(a,b) in enumerate(edges):inc[a].append(j);inc[b].append(j)
 assert all(len(z)==3 for z in inc)
 ch=[1]+[0]*(h-1);meta=[]
 for v in range(h):
  ids=sorted(inc[v])
  for j,z in enumerate(bad_patterns(ch[v])):
   c=[(1-2*bit)*(idx+1) for idx,bit in zip(ids,z)]
   meta.append((v,j,z,ids,c))
 cs=[z[4] for z in meta]
 raw=[' '.join(map(str,c))+' 0' for c in cs]
 width=max(map(len,raw))+3
 lines=[s.ljust(width)+'\n' for s in raw]
 head=f'p cnf {len(edges)} {len(cs)}\n'
 orig=head+''.join(lines);assert parse(orig)[1]==cs
 probes=[]
 for i,(v,j,z,ids,c) in enumerate(meta):
  alt=cs[4*v+(j+1)%4]
  replacement=(' '.join(map(str,alt))+' 0').ljust(width)+'\n'
  assert len(replacement)==len(lines[i])
  changed=head+''.join(lines[:i])+replacement+''.join(lines[i+1:])
  assert len(changed)==len(orig)
  offset=len(head)+i*(width+1)
  assert orig[:offset]==changed[:offset] and orig[offset+width+1:]==changed[offset+width+1:]
  assert parse(changed)[1][i]==alt
  eq=[]
  for u in range(h):
   if u!=v:eq.append((sum(1<<e for e in inc[u]),ch[u]))
  eq.extend((1<<t,b) for t,b in zip(ids,z))
  witness=gauss(eq,len(edges))
  assert not sat(c,witness)
  assert sum(not sat(p,witness) for p in cs)==1
  assert all(sat(p,witness) for p in parse(changed)[1])
  probes.append({'index':i,'vertex':v,'replacement_line':replacement.strip('\n'),
       'witness':''.join(map(str,witness)),'offset':offset})
 if len(edges)<=12:
  for mask in range(1<<len(edges)):
   z=[mask>>j&1 for j in range(len(edges))]
   assert not all(sat(p,z) for p in cs)
 return {'name':name,'h':h,'edge_count':len(edges),'m':len(cs),
         'N_bytes':len(orig),'W_mix341_prior':4*h-1,'source_sha256':hashlib.sha256(orig.encode()).hexdigest(),
         'source_dimacs':orig,'neighbors':probes}
def main():
 fs=[test('K4',4,k4())]
 fs.extend(test('prism'+str(k),2*k,prism(k)) for k in [3,4,5,6,8,12])
 malformed=['p cnf 2 2\n1 0\n','p cnf 2 1\n3 0\n',
 'p cnf 2 1\n1 1 0\n','p cnf a 1\n1 0\n',
 'p cnf 2 1\n1 -1 0\n','p cnf 2 1\n1 0','p cnf 2 1\n1 x 0\n']
 for x in malformed:
  try:parse(x);raise AssertionError('bad accepted')
  except ValueError:pass
 assert sum(f['m'] for f in fs)==320
 for f in fs:
  a=list(map(int,f['neighbors'][0]['witness']))
  assert not all(sat(p,a) for p in parse(f['source_dimacs'])[1])
 result={'schema':'LSPV1_421_compact','sources':fs,'malformed_rejected':len(malformed)}
 dest=Path('lspv1_421_compact_raw.json')
 dest.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':'PASS','sources':len(fs),'sat_neighbors':320,
                   'malformed':len(malformed),'native_checker':'NOT RUN',
                   'raw':str(dest)},indent=2))
if __name__=='__main__':main()
