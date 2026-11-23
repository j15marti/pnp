#!/usr/bin/env python3
"""Independent direct 3-color DPLL, never invoking diamond contraction.

Usage: python3 research/agents/meta-solver-theorem/2026-11-23_1157_distributed_wheel_dpll.py
"""
from pathlib import Path
import runpy

base=Path(__file__).with_name("2026-11-23_1157_distributed_wheel_check.py")
a=runpy.run_path(str(base))

def direct_solver(G,cap=2000000):
    adj=[set() for _ in range(G["V"])]
    for i,j in G["E"]:
        adj[i].add(j);adj[j].add(i)
    nodes=0
    def recurse(dom):
        nonlocal nodes
        nodes+=1
        if nodes>cap:raise RuntimeError("DPLL cap exceeded")
        todo=[i for i,x in enumerate(dom) if x.bit_count()==1]
        seen=set()
        while todo:
            i=todo.pop()
            if i in seen:continue
            seen.add(i)
            for j in adj[i]:
                new=dom[j]&~dom[i]
                if not new:return None
                if new!=dom[j]:
                    dom[j]=new
                    if new.bit_count()==1:todo.append(j)
        if all(x.bit_count()==1 for x in dom):
            return [x.bit_length()-1 for x in dom]
        i=min((j for j,x in enumerate(dom) if x.bit_count()>1),
              key=lambda j:(dom[j].bit_count(),-len(adj[j])))
        for color in (1,2,4):
            if dom[i]&color:
                d=dom.copy();d[i]=color
                w=recurse(d)
                if w is not None:return w
        return None
    d=[7]*G["V"]
    d[0]=1  # break global three-color permutation symmetry
    result=recurse(d)
    if result is not None:
        assert len(result)==G["V"]
        assert all(result[i]!=result[j] for i,j in G["E"])
    return result,nodes

def main():
    for k in (3,4,5):
        H=a["prism"](k)
        root=a["make"](H)
        neighbor=a["make"](H,deleted_rim_edge=H[0]-2)
        rw,rn=direct_solver(root)
        nw,nn=direct_solver(neighbor)
        assert rw is None and nw is not None
        print("prism",k,"root UNSAT nodes",rn,"neighbor SAT nodes",nn)
    print("PASS: independent uncontracted graph-color DPLL")

if __name__=="__main__":main()
