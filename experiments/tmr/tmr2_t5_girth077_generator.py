#!/usr/bin/env python3
"""Generate canonical original T5 sources from the incidence graph W(3,4).
Run: python tmr2_t5_girth077_generator.py [yes|sample].
Sample is a deterministic orientation, NOT a certified NO instance.
"""
import itertools,random,sys
SEED=202611172330

def mul(a,b):
 z=0
 if b&1:z^=a
 if b&2:z^=a<<1
 if z&8:z^=14
 if z&4:z^=7
 return z

def scale(a,v):return tuple(mul(a,x) for x in v)
def norm(v):
 for x in v:
  if x:return scale(next(z for z in (1,2,3) if mul(x,z)==1),v)
 raise ValueError('zero')
def symp(p,q):
 return mul(p[0],q[2])^mul(p[2],q[0])^mul(p[1],q[3])^mul(p[3],q[1])
def generate():
 P=sorted({norm(v) for v in itertools.product(range(4),repeat=4) if any(v)})
 assert len(P)==85
 index={p:i for i,p in enumerate(P)}
 lines=set()
 for i,p in enumerate(P):
  for q in P[i+1:]:
   if symp(p,q):continue
   line=tuple(sorted({index[norm(tuple(mul(a,x)^mul(b,y) for x,y in zip(p,q)))] for a in range(4) for b in range(4) if a or b}))
   assert len(line)==5
   lines.add(line)
 L=sorted(lines)
 assert len(L)==85
 E=sorted((p,85+j) for j,line in enumerate(L) for p in line)
 assert len(E)==425
 return E

def source(mode):
 E=generate()
 if mode=='sample':
  rng=random.Random(SEED)
  E=sorted((u,v) if rng.getrandbits(1) else (v,u) for u,v in E)
 assert mode in ('yes','sample')
 n=170
 return f'p t5 {n} {len(E)}\n'+''.join(f'v {i}\n' for i in range(n))+''.join(f'a {u} {v}\n' for u,v in E)

if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'yes'
 if mode not in ('yes','sample') or len(sys.argv)>2:raise SystemExit('usage: generator.py yes|sample')
 sys.stdout.write(source(mode))
