"""Streaming signed-twin candidate. Finite checks do not prove SAT coverage."""
import hashlib
import itertools as it
import json
from pathlib import Path
import random
import signal
import tempfile
import time

def alarm(*args):
    raise TimeoutError('25 second budget exceeded')

def tokens(path, limit):
    # Fixed-size I/O buffering and a bounded token, never read the whole source.
    with open(path, 'rb') as f:
        buf = bytearray()
        while True:
            c = f.read(1)
            if not c:
                if buf: yield bytes(buf)
                return
            if c.isspace():
                if buf:
                    yield bytes(buf)
                    buf.clear()
            else:
                buf.extend(c)
                if len(buf)>limit: raise ValueError('oversized token')

def header(path, size):
    z=tokens(path, len(str(max(1,size)))+3)
    if next(z)!=b'p' or next(z)!=b'cnf': raise ValueError('header')
    n,m=int(next(z)),int(next(z))
    if n<1 or m<0 or n>8*size or m>8*size: raise ValueError('bounds')
    return n,m,z

def clauses(path,size):
    n,m,z=header(path,size)
    c=[]; count=0
    for raw in z:
        x=int(raw)
        if abs(x)>n: raise ValueError('literal')
        if x:
            c.append(x)
            if len(c)>n: raise ValueError('clause too long')
        else:
            yield c
            c=[]; count+=1
    if c or count!=m: raise ValueError('clause count')

class Partition:
    def __init__(self,n):
        self.n=n; self.blocks=1; self.moves=0; self.touches=0
        self.owner=[0]*n
        self.prev=[v-1 for v in range(n)]
        self.nxt=[v+1 for v in range(n)]; self.nxt[-1]=-1
        self.head=[-1]*n; self.head[0]=0
        self.size=[0]*n; self.size[0]=n
        self.bhead=[-1]*n; self.count=[0]*n; self.link=[-1]*n
    def refine(self,subset):
        touched=[]
        for v in subset:
            b=self.owner[v]
            if self.count[b]==0: touched.append(b)
            self.link[v]=self.bhead[b]; self.bhead[b]=v
            self.count[b]+=1
        for b in touched:
            self.touches+=1
            if self.count[b]<self.size[b]:
                nb=self.blocks; self.blocks+=1
                v=self.bhead[b]
                while v!=-1:
                    follow=self.link[v]
                    a,c=self.prev[v],self.nxt[v]
                    if a!=-1: self.nxt[a]=c
                    else: self.head[b]=c
                    if c!=-1: self.prev[c]=a
                    first=self.head[nb]
                    self.prev[v]=-1; self.nxt[v]=first
                    if first!=-1: self.prev[first]=v
                    self.head[nb]=v; self.owner[v]=nb
                    self.size[b]-=1; self.size[nb]+=1; self.moves+=1
                    v=follow
            self.count[b]=0; self.bhead[b]=-1
    def groups(self):
        out=[]
        for b in range(self.blocks):
            row=[]; v=self.head[b]
            while v!=-1:
                row.append(v+1); v=self.nxt[v]
            out.append(tuple(sorted(row)))
        return sorted(out)

def _inspect(path):
    size=0
    with open(path,'rb') as f:
        while True:
            chunk=f.read(4096)
            if not chunk: break
            size+=len(chunk)
    n,m,_=header(path,size)
    if n**3>(8*size)**2: return {'status':'FAIL_DENSITY','source_bits':8*size}
    part=Partition(n); seen=[0]*n; stamp=0; literals=0
    for c in clauses(path,size):
        stamp+=1; pos=[]; neg=[]
        for lit in c:
            v=abs(lit)-1
            if seen[v]==stamp: raise ValueError('duplicate or tautology')
            seen[v]=stamp
            (pos if lit>0 else neg).append(v)
        literals+=len(c); part.refine(pos); part.refine(neg)
    # Test-facing group list is O(n); the production choice needs only one list.
    groups=part.groups()
    chosen=max(groups,key=lambda g:(len(g),g))
    if len(chosen)<2: return {'status':'FAIL_SINGLETON','groups':groups}
    values=[[None]*(n+1) for _ in range(3)]
    for v in chosen:
        values[0][v]=False; values[1][v]=True
        values[2][v]=(v==chosen[1])
    # Exact output-size measurement uses original IDs and exact DIMACS headers.
    sizes=[]; child_counts=[]
    for a in values:
        count=0; body=0
        for c in clauses(path,size):
            if any(a[abs(x)] is not None and a[abs(x)]==(x>0) for x in c): continue
            r=[x for x in c if a[abs(x)] is None]
            count+=1; body+=len((' '.join(map(str,r))+' 0\n').encode())
        sizes.append(8*(len(f'p cnf {n} {count}\n'.encode())+body))
        child_counts.append(count)
    return {'status':'REDUCE' if all(s**3<=(8*size)**2 for s in sizes) else 'FAIL_SIZE',
            'groups':groups,'chosen':chosen,'values':values,'source_bits':8*size,
            'child_bits':sizes,'child_counts':child_counts,'literal_occurrences':literals,'moves':part.moves,
            'touched_blocks':part.touches,'splits':part.blocks-1,
            'scan_contract':'size scan, refinement scan, three size scans; up to three emission scans'}

def inspect(path):
    try:
        return _inspect(path)
    except (ValueError, StopIteration):
        return {'status':'REJECT_ENCODING'}

def emit(path,result,index,out):
    size=result['source_bits']//8
    n,_,_=header(path,size); a=result['values'][index]
    with open(out,'wb') as dst:
        dst.write(f"p cnf {n} {result['child_counts'][index]}\n".encode())
        for c in clauses(path,size):
            if any(a[abs(x)] is not None and a[abs(x)]==(x>0) for x in c): continue
            r=[x for x in c if a[abs(x)] is None]
            dst.write((' '.join(map(str,r))+' 0\n').encode())

def residual(f,a):
    return [tuple(x for x in c if a[abs(x)] is None) for c in f
            if not any(a[abs(x)] is not None and a[abs(x)]==(x>0) for x in c)]

def sat(f):
    vs=sorted({abs(x) for c in f for x in c})
    return any(all(any(dict(zip(vs,b))[abs(x)]==(x>0) for x in c) for c in f)
               for b in it.product((False,True),repeat=len(vs)))

def main():
    signal.signal(signal.SIGALRM,alarm); signal.alarm(25)
    start=time.monotonic(); rng=random.Random(20261008); checks=0
    def write(path,n,f):
        path.write_text(f'p cnf {n} {len(f)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in f))
    def check(path,n,f):
        nonlocal checks
        write(path,n,f); r=inspect(path)
        if 'groups' in r:
            signatures={v:tuple((int(v in c),int(-v in c)) for c in f) for v in range(1,n+1)}
            for a in range(1,n+1):
                for b in range(1,n+1):
                    assert any(a in g and b in g for g in r['groups'])==(signatures[a]==signatures[b])
                    checks+=1
        if 'values' in r:
            assert sat(f)==any(sat(residual(f,a)) for a in r['values']); checks+=1
            for a,bits in zip(r['values'],r['child_bits']):
                out=path.with_suffix('.child'); write(out,n,residual(f,a))
                expected=out.read_bytes()
                emit(path,r,r['values'].index(a),out)
                assert out.read_bytes()==expected and len(expected)*8==bits; checks+=1
            assert r['moves']<=r['literal_occurrences']; checks+=1
        return r
    with tempfile.TemporaryDirectory() as folder:
        path=Path(folder)/'input.cnf'
        for _ in range(120):
            n=8; f=[]
            for __ in range(rng.randrange(1,18)):
                subset=rng.sample(range(1,7),rng.randrange(1,5))
                c=[]
                for v in subset:
                    sign=rng.choice((-1,1))
                    c.extend([sign*x for x in (7,8)] if v==1 else [sign*v])
                f.append(tuple(c))
            check(path,n,f)
        # A dense wide-clause family where the partial size gate genuinely passes.
        group=list(range(1,129)); tails=[129,130]
        f=[tuple([sign*v for v in group]+[t]) for sign in (-1,1) for t in tails+[-x for x in tails]]
        write(path,130,f); positive=inspect(path); assert positive['status']=='REDUCE'; checks+=1
        # Adding an independent outside component can make the gate fail.
        f2=f+[tuple((-v if v<141 and (j>>(v-131))&1 else v) for v in range(131,231)) for j in range(600)]
        write(path,230,f2); outside=inspect(path); assert outside['status']=='FAIL_SIZE'; checks+=1
        write(path,100,[(1,)])
        assert inspect(path)['status']=='FAIL_DENSITY'; checks+=1
        rejected=0
        for fbad in [[(1,1)],[(1,-1)]]:
            write(path,2,fbad)
            rejected+=int(inspect(path)['status']=='REJECT_ENCODING')
        assert rejected==2; checks+=2
    signal.alarm(0)
    def concise(r): return {k:v for k,v in r.items() if k not in ('groups','chosen','values')}
    print(json.dumps({'status':'COMPUTATIONAL','checks':checks,'seed':20261008,
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'positive':concise(positive),'independent_product':concise(outside),
         'seconds':time.monotonic()-start,
         'limitation':'Partial signed-twin macro only; no all-input coverage or P versus NP proof'},indent=2))

if __name__=='__main__': main()
