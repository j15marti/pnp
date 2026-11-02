#!/usr/bin/env python3
"""Two explicit forward DAGs for F9, with independent exhaustive gate verification.
Conventional basis AND2/OR2/NOT1: 41 gates. AND2/OR2/NAND2: 35 gates.
Neither is claimed globally minimum across unrestricted circuits.
"""
import json
from collections import Counter
from pathlib import Path

P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))


def direct_eval(x):
    pos=all(any((x>>(v-1))&1 for v in c) for c in P)
    neg=all(not all((x>>(v-1))&1 for v in c) for c in N)
    return pos and neg

class DAG:
    def __init__(self):
        self.gates=[];self.depth={i:0 for i in range(9)}
    def gate(self,op,*ins):
        n=9+len(self.gates)
        self.gates.append((op,ins))
        self.depth[n]=1+max(self.depth[i] for i in ins)
        return n
    def build(self,use_nand=False):
        cl=[]
        for a,b,c in P:
            cl.append(self.gate('OR',self.gate('OR',a-1,b-1),c-1))
        for a,b,c in N:
            z=self.gate('AND',a-1,b-1)
            if use_nand:
                cl.append(self.gate('NAND',z,c-1))
            else:
                cl.append(self.gate('NOT',self.gate('AND',z,c-1)))
        while len(cl)>1:
            next_cl=[]
            for i in range(0,len(cl),2):
                next_cl.append(self.gate('AND',cl[i],cl[i+1]) if i+1<len(cl) else cl[i])
            cl=next_cl
        self.output=cl[0]
    def evaluate(self,mask):
        state={i:(mask>>i)&1 for i in range(9)}
        for j,(op,ins) in enumerate(self.gates):
            v=[state[a] for a in ins]
            state[9+j] = (int(not v[0]) if op=='NOT' else v[0] & v[1] if op=='AND' else v[0] | v[1] if op=='OR' else int(not(v[0] & v[1])))
        return state[self.output]


def main():
    result={}
    for use_nand,expected in [(False,41),(True,35)]:
        c=DAG();c.build(use_nand)
        assert len(c.gates)==expected
        assert all(bool(c.evaluate(x))==direct_eval(x) for x in range(512))
        counts=dict(Counter(g[0] for g in c.gates))
        tclauses=sum(2 if g[0]=='NOT' else 3 for g in c.gates)+1
        result['AND_OR_NAND' if use_nand else 'AND_OR_NOT']={
            'gate_count':len(c.gates), 'gate_types':counts,
            'forward_depth':c.depth[c.output],
            'tseitin_clause_count':tclauses,'tseitin_variables':9+len(c.gates),
            'all_inputs_tested':512,'models':sum(c.evaluate(x) for x in range(512))
        }
    out=Path(__file__).with_name('optimized_results.json')
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
