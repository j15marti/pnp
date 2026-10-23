#!/usr/bin/env python3
"""Reproduce a subset of TIMEOUT66 NAND2 all-input tape-scanner tests."""
from itertools import product

class Circuit:
    def __init__(self,n):
        self.n=n
        self.gates=[]
        self.depth=[0]*(n+2)
    def nand(self,a,b):
        z=len(self.depth)
        self.gates.append((a,b))
        self.depth.append(1+max(self.depth[a],self.depth[b]))
        return z
    def neg(self,a): return self.nand(a,a)
    def AND(self,a,b): return self.neg(self.nand(a,b))
    def OR(self,a,b): return self.nand(self.neg(a),self.neg(b))
    def or_all(self,items):
        items=list(items)
        if not items:return 0
        while len(items)>1:
            items=[self.OR(items[i],items[i+1]) if i+1<len(items) else items[i] for i in range(0,len(items),2)]
        return items[0]
    def eval(self,bits,outs):
        v=[0,1]+list(bits)
        for a,b in self.gates:v.append(1-(v[a]&v[b]))
        return tuple(v[o] for o in outs)

def compile_scanner(n,steps,mode):
    C=Circuit(n)
    cells=n+2
    ones=list(range(2,n+2))+[0,0]
    zeros=[C.neg(i) for i in range(2,n+2)]+[0,0]
    blanks=[0]*n+[1,1]
    E=[1]+[0]*(cells-1)
    O=A=R=[0]*cells
    tr=({('E',0):'E',('E',1):'O',('O',0):'O',('O',1):'E'}
        if mode=='parity' else
        {('E',0):'O',('E',1):'E',('O',0):'O',('O',1):'O'})
    accept='E' if mode=='parity' else 'O'
    for _ in range(steps):
        ee=[];oo=[];aa=[];rr=[]
        for j in range(cells):
            terms={'E':[],'O':[]}
            if j:
                for tag,heads in (('E',E),('O',O)):
                    for bit,flags in ((0,zeros),(1,ones)):
                        terms[tr[(tag,bit)]].append(C.AND(heads[j-1],flags[j-1]))
            ee.append(C.or_all(terms['E']))
            oo.append(C.or_all(terms['O']))
            aa.append(C.OR(A[j],C.AND(E[j] if accept=='E' else O[j],blanks[j])))
            rr.append(C.OR(R[j],C.AND(O[j] if accept=='E' else E[j],blanks[j])))
        E,O,A,R=ee,oo,aa,rr
    halt=C.or_all([C.OR(a,r) for a,r in zip(A,R)])
    return C,(halt,C.or_all(A))

if __name__=='__main__':
    cases=0
    for mode in ('parity','chain'):
        for n in range(1,8):
            for steps in (n,n+1,n+3):
                C,outputs=compile_scanner(n,steps,mode)
                for bits in product((0,1),repeat=n):
                    got=C.eval(bits,outputs)
                    halted=int(steps>=n+1)
                    label=(sum(bits)%2==0 if mode=='parity' else not all(bits))
                    expected=(halted,int(label) if halted else 0)
                    assert got==expected,(mode,n,steps,bits,got,expected)
                    cases+=1
    print('PASS',cases,'all-input NAND2 computations')
