#!/usr/bin/env python3
"""Standalone compact ARC-EPOCH-INDEX-LIFT265 cross-check.
This is a companion, not the expanded archived producer or independent
source-proof checker. It needs only Python 3 standard library.
"""
import json
import random
from fractions import Fraction

SEED = 202610302336
W1 = [
 [-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
 [5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
 [-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],
 [2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]]
S15 = [
 [-1,-3,14],[2,8,-9],[-10,13,14],[3,-7,-13],[-4,9,-11],
 [-5,-8,-14],[4,-8,11],[1,7,-13],[1,-7,10],[-5,-6,15],
 [-2,6,-12],[4,9,-10],[-2,5,-12],[3,6,-15],[-6,7,11],
 [2,-9,-11],[-4,8,10],[-3,12,15],[5,12,-15],[-1,13,-14]]
COUNT = 0

def test(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise AssertionError(message)

def counts(formula, a):
    return [sum(((a >> (abs(l)-1)) & 1) == int(l>0) for l in c)
            for c in formula]

def compatible(c, d, side1, side2):
    desired = {}
    for clause, side in ((c,side1),(d,side2)):
        for literal in clause:
            k = abs(literal)
            want = int(literal>0) if side == 'S' else int(literal<0)
            if k in desired and desired[k] != want:
                return False
            desired[k] = want
    return True

def exhaustive_formula(label, formula):
    n = max(abs(l) for c in formula for l in c)
    models = 0
    for a in range(1 << n):
        t = counts(formula,a)
        tc = counts(formula, a ^ ((1 << n)-1))
        test(all(u+v == 3 for u,v in zip(t,tc)),
             "complement identity")
        models += (0 not in t)
    expected = 0 if label == "W1_UNSAT" else 861
    test(models == expected, "wrong exact SAT/UNSAT label")
    for j,c in enumerate(formula):
        S = {abs(l):int(l>0) for l in c}
        U = {abs(l):int(l<0) for l in c}
        test(all(S[k] == 1-U[k] for k in S), "local S/U")
        for k,d in enumerate(formula):
            if j>=k:continue
            for x in 'SU':
                for y in 'SU':
                    got = compatible(c,d,x,y)
                    same = any(abs(u)==abs(v) and (u>0)==(v>0)
                               for u in c for v in d)
                    opp = any(abs(u)==abs(v) and (u>0)!=(v>0)
                              for u in c for v in d)
                    expect = not (opp if x==y else same)
                    test(got==expect, "SS/SU/US/UU mode error")
    return {"models":models,"clauses":len(formula),"variables":n}

def exact_flmv(c):
    best = None
    winner = None
    checked = {}
    for k in range(1,4):
        f = c**k / (2+sum((c**i for i in range(1,k)),Fraction(0)))
        d = min((1/f-c)/k,c**(-k))
        checked[str(k)] = str(d)
        if best is None or d>best: best,winner=d,k
    test(winner==2 and c**(-4)<best, "uncertified FLMV tail")
    return {"c":str(c),"dstar":str(best),"winner_k":winner,
            "k1_k2_k3":checked,"tail_upper":str(c**(-4))}

class EpochIndex:
    def __init__(self,m,T):
        self.m,self.T=m,T
        self.r=(m+T+1).bit_length()
        self.epoch=0
        self.cells={}
        self.v=0
        self.h=0
        self.index_head=0
        self.input_head=0
    def get(self,i):
        tag,bit=self.cells.get(i,(-1,0))
        return bit if tag==self.epoch else 0
    def write(self,i,b):
        old=self.get(i)
        self.cells[i]=(self.epoch,b)
        if i<self.r:
            self.v+=(b-old)*(1<<i)
        else:
            self.h+=b-old
    def jump(self):
        self.input_head=(self.v if self.h==0 and self.v<=self.m+self.T
                         else None)
        self.epoch+=1
        self.v,self.h=0,0
        # Crucial: do not reset index_head.
    def input_move(self,step):
        if self.input_head is not None:
            self.input_head=max(0,self.input_head+step)
            if self.input_head>self.m+self.T:self.input_head=None
    def input_read(self,text):
        return text[self.input_head] if self.input_head is not None and (
            0<=self.input_head<len(text)) else None

def epoch_stress():
    g=random.Random(SEED)
    idx=EpochIndex(300,10000)
    reference={}
    epochs=0
    actual_head=0
    queries=0
    for t in range(5000):
        k=g.choice((0,1,2,3,4,17,19,24,128,8192))
        if t%11==0:
            idx.jump()
            reference={}
            epochs+=1
            test(idx.index_head==actual_head,"index-head reset")
            if k>=24: test(idx.input_head is None or
                            idx.input_head<=idx.m+idx.T,"FAR")
        else:
            b=g.randrange(2)
            idx.write(k,b)
            reference[k]=b
            test(idx.get(k)==b,"write mismatch")
        for i in (0,1,2,3,4,17,19,24,128,8192):
            test(idx.get(i)==reference.get(i,0),"stale epoch bit")
        actual_head=k
        idx.index_head=k
        queries+=1
    idx.write(128,1)
    idx.jump()
    test(idx.input_head is None,"high index must imply FAR")
    for _ in range(1000):
        idx.input_move(-1)
        test(idx.input_read('0'*300) is None,"FAR false hit")
    return {"operations":queries,"reset_events":epochs,
            "far_left_moves":1000,"checks":COUNT}

def main():
    sources={
        "W1_UNSAT":exhaustive_formula("W1_UNSAT",W1),
        "S15_SAT":exhaustive_formula("S15_SAT",S15)}
    test([sorted(abs(t) for t in c) for c in W1] ==
         [sorted(abs(t) for t in c) for c in S15],
         "unsigned-support twin violated")
    f1=exact_flmv(Fraction(6,5))
    f2=exact_flmv(Fraction(241,200))
    test(f1["dstar"]=="23/45","FLMV 6/5")
    test(f2["dstar"]=="11642479/23232400","FLMV 241/200")
    stress=epoch_stress()
    print(json.dumps({"run":"ARC-EPOCH-INDEX-LIFT265_compact",
                      "status":"finite controls only, not native FLMV TM",
                      "seed":SEED,"sources":sources,"flmv":[f1,f2],
                      "epoch":stress,"total_assertions":COUNT,
                      "universal_ARC":"OPEN","P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":
    main()
