#!/usr/bin/env python3
"""ARC294: source-indexed virtual ordinary-CNF raw-cofactor emitter.
Exact output-bit and indexed-address accounting; NOT a canonical target child,
a SAT decider, an ARC contractor, or a native FLMV TM benchmark.
Run from any directory: python experiments/arc/lspv4_294/arc_virtual_cofactor294_compact.py
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
U=json.loads((HERE/"U_source.json").read_text())
Y=json.loads((HERE/"Y6_source.json").read_text())
V=[list(c) for c in U]
V[1][0],V[7][0]=V[7][0],V[1][0]

def gamma(x):
    assert x>0
    s=format(x,"b")
    return "0"*(len(s)-1)+s

def read_gamma(bits,start=0):
    zeros=0
    while bits[start+zeros]=="0":zeros+=1
    end=start+2*zeros+1
    return int(bits[start+zeros:end],2),end

def encode_source(F):
    n=max(abs(x) for c in F for x in c)
    w=n.bit_length()
    return gamma(n)+gamma(len(F))+"".join(
        ("1" if c[0]>0 else "0")+
        "".join(format(abs(x),f"0{w}b") for x in c) for c in F)

def direct(F,p):
    n=max(abs(x) for c in F for x in c)
    w=n.bit_length()
    rows=[]
    for C in F:
        if any(abs(x) in p and int(x>0)==p[abs(x)] for x in C):continue
        rows.append((C[0]>0,[x for x in C if abs(x) not in p]))
    assert rows,"A wholly satisfied residual is a SAT terminal"
    return gamma(n)+gamma(len(rows))+"".join(
        ("1" if sign else "0")+format(len(C),"02b")+
        "".join(format(abs(x),f"0{w}b") for x in C)+
        "0"*(w*(3-len(C))) for sign,C in rows)

class VirtualRaw:
    def __init__(self,source,p):
        self.src=source
        self.n,pos=read_gamma(source)
        self.m,pos=read_gamma(source,pos)
        self.h=pos
        self.w=self.n.bit_length()
        self.rl=1+3*self.w
        assert len(source)==self.h+self.m*self.rl
        self.p=dict(sorted(p.items()))
        self.affected=[]
        self.deleted=[]
        self.setup_reads=pos
        self.pin_comparisons=0
        for j in range(self.m):
            rec=source[self.h+j*self.rl:self.h+(j+1)*self.rl]
            self.setup_reads+=len(rec)
            sign=int(rec[0])
            names=[int(rec[1+i*self.w:1+(i+1)*self.w],2) for i in range(3)]
            mask=0
            touch=drop=False
            for i,name in enumerate(names):
                matched=False
                for x,b in self.p.items():
                    self.pin_comparisons+=1
                    if x==name:
                        matched=touch=True
                        if b==sign:drop=True
                        break
                if not matched:mask|=1<<i
            if touch:self.affected.append((j,mask,drop))
            if drop:self.deleted.append(j)
        self.mc=self.m-len(self.deleted)
        assert self.mc>0
        self.header=gamma(self.n)+gamma(self.mc)
        self.crl=3+3*self.w
        self.length=len(self.header)+self.mc*self.crl
        self.queries=self.source_reads=self.directory_checks=0
        self.index_one_writes=self.index_head_moves=self.index_jumps=0
        self.last_head=0

    def bit(self,q):
        assert 0<=q<self.length
        self.queries+=1
        if q<len(self.header):return self.header[q]
        j,t=divmod(q-len(self.header),self.crl)
        n_deleted=0
        for rank,d in enumerate(self.deleted):
            self.directory_checks+=1
            if d-rank<=j:n_deleted+=1
            else:break
        src_j=j+n_deleted
        mask=7
        for source_id,retained,deleted in self.affected:
            self.directory_checks+=1
            if source_id==src_j:
                assert not deleted
                mask=retained
                break
            if source_id>src_j:break
        offset=self.h+src_j*self.rl
        if t==0:address=offset
        elif t<3:return format(mask.bit_count(),"02b")[t-1]
        else:
            slot,bit=divmod(t-3,self.w)
            old_slots=[i for i in range(3) if mask&(1<<i)]
            if slot>=len(old_slots):return "0"
            address=offset+1+old_slots[slot]*self.w+bit
        self.source_reads+=1
        self.index_one_writes+=address.bit_count()
        extent=max(1,address.bit_length())
        self.index_head_moves+=self.last_head+extent-1
        self.last_head=extent-1
        self.index_jumps+=1
        return self.src[address]

def valid(F):
    from collections import Counter
    assert F
    ct=Counter(x for C in F for x in C)
    ids=set(abs(x) for x in ct)
    return (len(set(map(lambda c:tuple(sorted(c)),F)))==len(F) and
            all(len(C)==3 and len(set(abs(x) for x in C))==3 and
                (all(x>0 for x in C) or all(x<0 for x in C)) for C in F) and
            all(ct[v]==ct[-v]==2 for v in ids))

def cases():
    for name,F in (("Y6",Y),("U198",U),("V198",V)):
        n=max(abs(x) for C in F for x in C)
        for p in ({1:0},{1:1},{2:1},{1:0,2:1},{1:0,2:0},
                  {i:int(i%2==0) for i in range(1,min(8,n)+1)}):
            if any(not all(int(x>0)==p[abs(x)] for x in C if abs(x) in p)
                   for C in []):pass
            yield name,F,p
    for tern in itertools.product((None,0,1),repeat=6):
        p={i+1:b for i,b in enumerate(tern) if b is not None}
        if p and len(p)<=3:yield "Y6",Y,p

def run():
    rows=[]
    for name,F,p in cases():
        assert valid(F)
        source=encode_source(F)
        try:direct_bits=direct(F,p)
        except AssertionError:continue
        v=VirtualRaw(source,p)
        actual="".join(v.bit(i) for i in range(v.length))
        assert actual==direct_bits
        assert len(v.affected)<=4*len(p)
        assert len(v.deleted)<=2*len(p)
        rows.append({"source":name,"p":p,
                     "source_bits":len(source),"child_bits":v.length,
                     "affected_ids":[i for i,_,_ in v.affected],
                     "deleted_ids":v.deleted,
                     "output_source_reads":v.source_reads,
                     "index_one_writes":v.index_one_writes,
                     "index_head_moves":v.index_head_moves,
                     "index_jumps":v.index_jumps,
                     "setup_reads":v.setup_reads,
                     "directory_checks":v.directory_checks,
                     "child_sha256":hashlib.sha256(actual.encode()).hexdigest()})
    assert sum(all(any(bits[abs(x)-1]==int(x>0) for x in C) for C in Y)
               for bits in itertools.product((0,1),repeat=6))==20
    result={"run":"ARC294-COMPACT","cases":len(rows),
            "output_queries":sum(x["child_bits"] for x in rows),
            "output_source_reads":sum(x["output_source_reads"] for x in rows),
            "setup_reads":sum(x["setup_reads"] for x in rows),
            "index_one_writes":sum(x["index_one_writes"] for x in rows),
            "index_head_moves":sum(x["index_head_moves"] for x in rows),
            "directory_checks":sum(x["directory_checks"] for x in rows),
            "total_index_primitives":sum(x["index_one_writes"]+x["index_head_moves"]+
                                         x["index_jumps"] for x in rows),
            "native_FLMV_simulation":False,
            "canonical_child":False,
            "P_versus_NP":"OPEN"}
    print(json.dumps(result,indent=2))
    assert result["cases"]==249
    assert result["output_queries"]==96938
    assert result["output_source_reads"]==83642
    assert result["setup_reads"]==101388
    assert result["index_one_writes"]==502263
    assert result["index_head_moves"]==1743671
    assert result["directory_checks"]==1047042
    print("PASS ARC294 COMPACT")
if __name__=="__main__":run()
