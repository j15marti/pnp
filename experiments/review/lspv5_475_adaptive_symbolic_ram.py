#!/usr/bin/env python3
"""Finite executable control of exact symbolic read-over-write for adaptive RAM.

Scope: fixed M-cell Boolean table with adaptive addresses; symbolic DAG is an
analysis representation, not a physical low-space runtime simulator or a SAT
lower bound. Uses standard theory-of-arrays select/store semantics.
"""
import json
from functools import lru_cache

class SymbolicRAM:
    def __init__(self, m):
        self.m=m
        self.nodes=[]
        self.cache={}
        self.writes=[]
        self.probe_cost=0
        self.C0=self.mk('const',0)
        self.C1=self.mk('const',1)
        self.A=self.mk('addr')
    def mk(self,op,*args):
        key=(op,)+tuple(args)
        if key not in self.cache:
            self.cache[key]=len(self.nodes)
            self.nodes.append(key)
        return self.cache[key]
    def add(self,*args):return self.mk('addmod',*args)
    def xor(self,x,y):return self.mk('xor',x,y)
    def guard(self,x,y):return self.mk('and',x,y)
    def eq(self,x,y):return self.mk('eq',x,y)
    def ite(self,g,y,n):return self.mk('ite',g,y,n)
    def read(self, addr):
        val=self.mk('base',addr)
        for a,v,en in self.writes:
            self.probe_cost+=1
            g=self.guard(self.eq(addr,a),en)
            val=self.ite(g,v,val)
        return val
    def write(self,a,v,en):self.writes.append((a,v,en))
    def evaluate(self,expr,table,address):
        @lru_cache(None)
        def f(i):
            op,*args=self.nodes[i]
            if op=='const':return args[0]
            if op=='addr':return address
            if op=='addmod':return sum(f(a) for a in args)%self.m
            if op=='xor':return f(args[0])^f(args[1])
            if op=='and':return f(args[0])&f(args[1])
            if op=='eq':return int(f(args[0])==f(args[1]))
            if op=='ite':return f(args[1]) if f(args[0]) else f(args[2])
            if op=='base':return table[f(args[0])]
            raise ValueError(op)
        return f(expr)

def symbolic_program(m,depth):
    b=SymbolicRAM(m)
    prev=b.C0
    for i in range(depth):
        ra=b.add(b.A,prev,b.mk('const',i))
        r=b.read(ra)
        wa=b.add(b.A,r,b.mk('const',i+1))
        v=b.xor(r,b.mk('const',i%2))
        en=b.C1 if i%2==0 else r
        b.write(wa,v,en)
        prev=r
    lastaddr=b.add(b.A,prev,b.mk('const',depth+1))
    return b,b.read(lastaddr)

def concrete_program(m,depth,table,address):
    mem=list(table);prev=0
    for i in range(depth):
        r=mem[(address+prev+i)%m]
        wa=(address+r+i+1)%m
        if i%2==0 or r==1:
            mem[wa]=r^(i%2)
        prev=r
    return mem[(address+prev+depth+1)%m]

def main():
    result={'model':'fixed-size adaptive Boolean RAM; source table read-only initial, stores symbolic', 'status':'PROVED/RESTRICTED algebra + COMPUTATIONAL finite controls','cases':[], 'checks':0, 'failures':0}
    for m in (2,4,8):
        for depth in range(1,9):
            ram,output=symbolic_program(m,depth)
            nc=0
            for mask in range(1<<m):
                table=tuple((mask>>i)&1 for i in range(m))
                for address in range(m):
                    got=ram.evaluate(output,table,address)
                    exp=concrete_program(m,depth,table,address)
                    result['checks']+=1;nc+=1
                    if got!=exp:
                        result['failures']+=1
                        raise AssertionError((m,depth,mask,address,got,exp))
            expected=depth*(depth+1)//2
            assert ram.probe_cost==expected,(ram.probe_cost,expected)
            result['checks']+=1
            result['cases'].append({'memory_cells':m,'rounds':depth,'source_assignment_checks':nc,'symbolic_dag_nodes':len(ram.nodes),'read_write_alias_candidates':ram.probe_cost,'alias_bound':expected,'base_read_muxes_not_paid_for':depth+1})
    result['total_cases']=sum(row['source_assignment_checks'] for row in result['cases'])
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
