#!/usr/bin/env python3
"""Q4-VIRTUAL-INDEX290, compact GitHub reproducer; full tape-event ledger in separate downloadable archive.
Execute from j15marti/pnp repository root with Python 3.10+.
No dependency outside standard library and existing REF258 project artifacts.
The compiler uses only parent encoded bits and a fixed source-independent U198 critical template.
"""
import ast, importlib.util, json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
src=R/"experiments/arc/lspv3_283/DOECKER61_original_source.txt"
U=ast.literal_eval("".join(s for s in src.read_text().splitlines() if not s.startswith("#")))
D=U[:1]+U[2:]
V=[c[:] for c in U]
V[2][2],V[44][2]=V[44][2],V[2][2]
Y=[list(x) for x in [(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]]
report=json.loads((R/"results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.json").read_text())
D_WITNESS=report["actual_controls"]["D"]["witness"]
spec=importlib.util.spec_from_file_location("ref258",R/"experiments/arc/lspv5_258/nonminimum_branch_reentry_referee258.py")
ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
def gamma(x):
    z=format(x,"b")
    return "0"*(len(z)-1)+z
def encode(F):
    n=max(abs(v) for c in F for v in c);w=n.bit_length()
    return gamma(n)+gamma(len(F))+"".join(("1" if c[0]>0 else "0")+"".join(format(abs(v),f"0{w}b") for v in c) for c in F)
class Source:
    def __init__(self,bits):
        self.bits=bits;self.queries=0
        p=0;heads=[]
        for k in range(2):
            z=0
            while p<len(bits) and self.bit(p)=="0":z+=1;p+=1
            if p+z>=len(bits):raise ValueError("bad gamma header")
            heads.append(int("".join(self.bit(j) for j in range(p,p+z+1)),2));p+=z+1
        self.n,self.m=heads;self.h=p;self.w=self.n.bit_length();self.r=1+3*self.w
        if len(bits)!=p+self.m*self.r:raise ValueError("bad length")
    def bit(self,q):
        self.queries+=1
        return self.bits[q]
    def row(self,j):
        k=self.h+j*self.r
        sign=1 if self.bit(k)=="1" else -1
        return [sign*int("".join(self.bit(k+1+t*self.w+s) for s in range(self.w)),2) for t in range(3)]
class Q4:
    def __init__(self,src,pivot,b):
        self.src=src;self.pivot=pivot;self.sign=1 if b else -1
        self.other=-self.sign;self.n=src.n;self.m=src.m
        self.h=gamma(src.n+201)+gamma(src.m+268)
        self.w=(src.n+201).bit_length();self.r=1+3*self.w
        self.rem=[];self.binary=[];self.slots=[]
        for j in range(self.m):
            c=src.row(j)
            if self.sign*pivot in c:
                self.rem.append(j)
                self.slots += [self.sign*(abs(v)-(abs(v)>pivot)) for v in c if abs(v)!=pivot]
            elif self.other*pivot in c:self.binary.append(j)
        assert len(self.rem)==len(self.binary)==2 and len(self.slots)==4
        for match in (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))):
            if all(abs(self.slots[i])!=abs(self.slots[j]) for i,j in match):
                self.pairs=[(self.slots[i],self.slots[j]) for i,j in match];break
        self.setup_reads=src.queries
    def row(self,j):
        if j<self.m-2:
            idx=j
            for removed in self.rem:
                if idx>=removed:idx+=1
            c=self.src.row(idx)
            c=[(1 if v>0 else -1)*(abs(v)-(abs(v)>self.pivot)) for v in c if abs(v)!=self.pivot]
            if len(c)==2:c.append(self.other*(self.n-1+(194,196)[self.binary.index(idx)]))
            return c
        if j<self.m+261:
            return [self.other*(1 if v>0 else -1)*(self.n-1+abs(v)) for v in D[j-self.m+2]]
        z=[self.n-1+198+k for k in (1,2,3,4)]
        p=[self.sign*v for v in z];n=[self.other*v for v in z]
        rows=[[*self.pairs[0],p[0]],[*self.pairs[1],p[2]],[p[0],p[1],p[3]],[p[1],p[2],p[3]],[n[0],n[1],self.other*(self.n-1+197)],[n[0],n[2],n[3]],[n[1],n[2],n[3]]]
        return rows[j-self.m-261]
    def __len__(self):
        return len(self.h)+(self.m+268)*self.r
    def bit(self,q):
        if q<len(self.h):return self.h[q]
        j,t=divmod(q-len(self.h),self.r)
        c=self.row(j)
        if t==0:return "1" if c[0]>0 else "0"
        k,u=divmod(t-1,self.w)
        return format(abs(c[k]),f"0{self.w}b")[u]
def trial(name,F,pivot,b):
    assert ref.valid_target(F)
    bits=encode(F);s=Source(bits);v=Q4(s,pivot,b)
    child=ref.build_child(F,pivot,b,D,D_WITNESS)["child"]
    reference=encode(child)
    assert len(v)==len(reference) and len(v)>len(bits)
    assert all(v.bit(q)==reference[q] for q in range(len(v)))
    return {"case":name,"parent_bits":len(bits),"child_bits":len(v),"setup_reads":v.setup_reads,"source_reads":s.queries-v.setup_reads,"bit_checks":len(v),"status":"PASS"}
if __name__=="__main__":
    cases=[("Y6 SAT 1",Y,1,True),("Y6 SAT 0",Y,1,False),("U198 UNSAT",U,3,True),("V198 SAT",V,3,True)]
    print(json.dumps([trial(*c) for c in cases],indent=2))
    print("PASS, q4 bit interface; ARC/FLMV and P versus NP OPEN")
