#!/usr/bin/env python3
"""LSPV-2 268 compact reproducibility checker (standard library only).
The complete original-source producer, independent verifier and raw data
are included in the user-facing ZIP; this standalone copy replays the
canonical indexed-DIMACS accessor and both-label parity claims on small b.
This is a restricted finite test, not an all-input ARC compiler.
"""
import itertools
import json
from math import isqrt
from collections import Counter

def clauses_xor(a, b, z):
    return [tuple(-v if bit else v for v, bit in zip((a,b,z), (p,q,r)))
            for p,q,r in itertools.product((0,1),repeat=3) if r != (p^q)]

def clauses_pin(z, p, q, bit):
    return [tuple(-v if t else v for v,t in zip((z,p,q),(1-bit,a,c)))
            for a,c in itertools.product((0,1),repeat=2)]

def canonical_chain(b, req, offset):
    clauses=[]
    for j in range(2,b+1):
        clauses+=clauses_xor(1 if j==2 else offset+j-2,j,offset+j-1)
    clauses+=clauses_pin(offset+b-1,offset+b,offset+b+1,req)
    return clauses

def source(b, reqs):
    F=[]
    for i,r in enumerate(reqs):
        F+=canonical_chain(b,r,b+i*(b+1))
    return F

def row_str(C):
    return " ".join(map(str,C))+" 0\n"

def digit_count(t): return len(str(t))
def digit_prefix(t):
    if t<=0:return 0
    total=0;low=1;k=1
    while low<=t:
        high=min(t,10*low-1)
        total+=(high-low+1)*k
        low*=10;k+=1
    return total

def gate_prefix(b,offset,t):
    if t<2:return 0
    digits=digit_count(1)+digit_count(2)+digit_count(offset+1)
    if t>=3:
        digits+=(digit_prefix(offset+t-2)-digit_prefix(offset)
                 +digit_prefix(t)-digit_prefix(2)
                 +digit_prefix(offset+t-1)-digit_prefix(offset+1))
    return 26*(t-1)+4*digits

class CharacterAccessor:
    def __init__(self,b,reqs):
        self.b=b
        self.reqs=tuple(sorted(set(reqs)))
        n=b+len(self.reqs)*(b+1)
        m=4*b*len(self.reqs)
        self.header=f"p cnf {n} {m}\n"
        self.blocks=[]
        end=len(self.header)
        for i,r in enumerate(self.reqs):
            offset=b+i*(b+1)
            pin_len=4*sum(map(digit_count,(offset+b-1,offset+b,offset+b+1)))+(28 if r==0 else 24)
            length=gate_prefix(b,offset,b)+pin_len
            self.blocks.append((end,end+length,offset,r))
            end+=length
        self.length=end

    def read(self,pos):
        if pos<0 or pos>=self.length:return None
        if pos<len(self.header):return self.header[pos]
        for begin,end,offset,r in self.blocks:
            if not begin<=pos<end:continue
            relative=pos-begin
            gate_end=gate_prefix(self.b,offset,self.b)
            if relative<gate_end:
                left,right=2,self.b
                while left<right:
                    mid=(left+right)//2
                    if gate_prefix(self.b,offset,mid)>relative:right=mid
                    else:left=mid+1
                j=left
                relative-=gate_prefix(self.b,offset,j-1)
                rows=clauses_xor(1 if j==2 else offset+j-2,j,offset+j-1)
            else:
                relative-=gate_end
                rows=clauses_pin(offset+self.b-1,offset+self.b,offset+self.b+1,r)
            for C in rows:
                item=row_str(C)
                if relative<len(item):return item[relative]
                relative-=len(item)
            raise AssertionError("Incorrect character offset")
        raise AssertionError("Missing character block")

    def materialize(self):
        out=self.header
        for _,_,offset,r in self.blocks:
            out+="".join(map(row_str,canonical_chain(self.b,r,offset)))
        return out

def source_witness(b,values,reqs):
    a={i+1:values[i] for i in range(b)}
    for k,r in enumerate(reqs):
        offset=b+k*(b+1)
        running=0
        for j in range(1,b+1):
            running^=a[j]
            if j>=2:a[offset+j-1]=running
        a[offset+b]=0
        a[offset+b+1]=0
    return a

def sat_clauses(clauses,assignment):
    return all(any(assignment[abs(l)]==(l>0) for l in C) for C in clauses)

def ext_mode(C,D,s,t):
    assign={}
    for c,mode in ((C,s),(D,t)):
        for lit in c:
            x=abs(l)
            val=(lit>0) if mode=="S" else (lit<0)
            if x in assign and assign[x]!=val:return False
            assign[x]=val
    return True

def test():
    assertions=0
    checks=[]
    for b in range(2,8):
        for reqs in ((0,),(1,),(0,0),(0,1),(1,1,0)):
            F=source(b,reqs)
            child=CharacterAccessor(b,reqs)
            word=child.materialize()
            assert len(word)==child.length
            for i in range(-1,len(word)+1):
                assert child.read(i)==(word[i] if 0<=i<len(word) else None)
                assertions+=1
            assert len(F)==4*b*len(reqs)
            for values in itertools.product((0,1),repeat=b):
                a=source_witness(b,values,reqs)
                correct=all((sum(values)%2)==r for r in reqs)
                assert sat_clauses(F,a)==correct
                child_assignment=source_witness(b,values,sorted(set(reqs)))
                G=[]
                for i,r in enumerate(sorted(set(reqs))):
                    G+=canonical_chain(b,r,b+i*(b+1))
                assert sat_clauses(G,child_assignment)==correct
                assertions+=2
            # Independent consistency check on all local S/U extremes.
            for i,C in enumerate(F):
                for D in F[i+1:]:
                    for s,t in itertools.product(("S","U"),repeat=2):
                        witness=ext_mode(C,D,s,t)
                        same=any(l in D for l in C)
                        opposite=any(-l in D for l in C)
                        predicted=(not opposite) if s==t else (not same)
                        assert witness==predicted
                        assertions+=1
            checks.append({"b":b,"requirements":list(reqs),"clauses":len(F),
                "length":len(word),"sat":len(set(reqs))==1})
    # Completeness of an auxiliary-free CNF rejecting all odd parity rows.
    for b in range(2,9):
        guards=[tuple((i+1 if v==0 else -(i+1))
                       for i,v in enumerate(bits))
                for bits in itertools.product((0,1),repeat=b)
                if sum(bits)%2==1]
        assert len(guards)==2**(b-1)
        for bits in itertools.product((0,1),repeat=b):
            assert sat_clauses(guards,{i+1:bool(bits[i]) for i in range(b)})==(sum(bits)%2==0)
            assertions+=1
    return {"status":"COMPUTATIONAL, restricted; universal ARC OPEN",
            "cases":len(checks),"assertions":assertions,"sat":sum(x["sat"] for x in checks),
            "unsat":sum(not x["sat"] for x in checks),
            "note":"A supplied canonical grouping was checked, not freely discovered."}

if __name__=="__main__":
    print(json.dumps(test(),sort_keys=True))
