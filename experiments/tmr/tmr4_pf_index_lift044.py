#!/usr/bin/env python3
"""TMR-4 PF-lift exact finite checks. No claimed P versus NP proof.
Usage: python3 tmr4_pf_index_lift044.py [output.json]
Deterministic tests, Python 3.11+, no external dependencies.
"""
import itertools
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

SEED = 4044
rng = random.Random(SEED)
checks = 0

def ck(pred, msg):
    global checks
    checks += 1
    if not pred:
        raise AssertionError(msg)

class Gates:
    def __init__(self, n):
        self.n=n
        self.ops=[]
    def AND(self, a,b):
        self.ops.append(('and',a,b)); return self.n+len(self.ops)-1
    def OR(self, a,b):
        self.ops.append(('or',a,b)); return self.n+len(self.ops)-1
    def NOT(self,a):
        self.ops.append(('not',a)); return self.n+len(self.ops)-1
    def XOR(self,a,b):
        # (a AND ~b) OR (~a AND b), no XOR primitive
        return self.OR(self.AND(a,self.NOT(b)),self.AND(self.NOT(a),b))
    def eval(self, bits):
        wires=list(bits)
        for op in self.ops:
            if op[0]=='and': wires.append(wires[op[1]] & wires[op[2]])
            elif op[0]=='or': wires.append(wires[op[1]] | wires[op[2]])
            elif op[0]=='not': wires.append(1-wires[op[1]])
            else: raise AssertionError('unknown op')
        return wires

def direct_formula(clauses, x):
    return int(all(any((x[abs(l)-1] if l>0 else 1-x[-l-1]) for l in cl) for cl in clauses))

def syntax_tag(clauses):
    return sum((abs(z)*3+int(z<0)+len(cl)*11) for cl in clauses for z in cl)%2

def direct_indexed(clauses,v,idx):
    val=direct_formula(clauses,idx[:v])
    parity=sum(idx)%2
    return val ^ (parity & syntax_tag(clauses))

def compile_indexed(clauses, v, n):
    g=Gates(n)
    terms=[]
    for cl in clauses:
        lits=[(l-1 if l>0 else g.NOT(-l-1)) for l in cl]
        terms.append(g.OR(g.OR(lits[0],lits[1]),lits[2]))
    out=terms[0]
    for t in terms[1:]: out=g.AND(out,t)
    if syntax_tag(clauses):
        parity=0
        for j in range(1,n): parity=g.XOR(parity,j)
        out=g.XOR(out,parity)
    return g,out

formula_count=0
bit_count=0
max_gates=0
classes={'sat':0,'unsat':0,'unique':0,'horn':0,'all_positive':0,'all_negative':0}
for v in (3,4,5,6):
    possible = list(itertools.combinations(range(1,v+1),3))
    cases=[]
    for _ in range(90 if v <= 5 else 15):
        m=rng.randint(1,6)
        clauses=[]
        for j in range(m):
            support=rng.choice(possible)
            clauses.append(tuple(z if rng.randrange(2) else -z for z in support))
        cases.append(clauses)
    # 3-var contradictory complete clause family and a unique-witness forcing 7/8 clauses
    if v==3:
        all8=[]
        for signs in itertools.product((-1,1),repeat=3):
            all8.append(tuple(signs[j]*(j+1) for j in range(3)))
        cases += [all8,all8[:-1],[(1,2,3)],[(-1,-2,-3)],
                  [all8[j] for j in (0,3,5,6)]]  # affine-parity 3-CNF
    if v==6:
        cases += [[(1,2,3),(4,5,6)],
                  [(1,2,3),(-1,-2,-3),(4,5,6),(-4,-5,-6)]]
    for clauses in cases:
        satisfying=sum(direct_formula(clauses,x) for x in itertools.product((0,1),repeat=v))
        classes['sat' if satisfying else 'unsat']+=1
        classes['unique']+=int(satisfying==1)
        classes['horn']+=int(all(sum(l>0 for l in cl)<=1 for cl in clauses))
        classes['all_positive']+=int(all(all(l>0 for l in cl) for cl in clauses))
        classes['all_negative']+=int(all(all(l<0 for l in cl) for cl in clauses))
        n=v+2
        g,out=compile_indexed(clauses,v,n)
        for idx in itertools.product((0,1),repeat=n):
            bit0=direct_indexed(clauses,v,idx)
            bit1=g.eval(idx)[out]
            ck(bit0==bit1,'compiled indexed mismatch')
            bit_count+=1
        max_gates=max(max_gates,len(g.ops))
        formula_count+=1

# Exact integer exponent/audit of a known linear-logarithmic circuit upper bound.
# Bounds below are PROXIES with K=128, not Pippenger-Fischer's implicit constant.
K=128
frontier=[]
win_count=0
for a,mu_num,mu_den,d in [(10,3,10,2),(6,1,2,2),(12,1,4,2),(2,1,2,1),(1,1,2,1),(8,1,4,1),(5,2,5,1),(4,3,4,2)]:
    threshold_exp=Fraction(a*mu_num,mu_den)
    predicted=threshold_exp>max(1,d)
    oldpred=threshold_exp>2*max(1,d)
    rec={'a':a,'mu':f'{mu_num}/{mu_den}','d':d,'a_mu':str(threshold_exp),'pf_strict':predicted,'quadratic_strict':oldpred,'samples':[]}
    for h in (8,12,16,20,24):
        if a*h*mu_num % mu_den: continue
        L=1<<h
        n=a*h
        t=1<<(h*d)
        H=L+n+t+2
        s=1<<(a*h*mu_num//mu_den)
        logH=H.bit_length()+1
        linear_log=K*H*logH
        quadratic=K*H*H
        ck((linear_log < s)==(s>linear_log),'pf comparison mismatch')
        ck(quadratic>linear_log,'quadratic must dominate')
        ck(logH>=math.ceil(math.log2(H+1)),'log bound too small')
        rec['samples'].append({'h':h,'log2_H_ceil':H.bit_length(),'s_bits':s.bit_length(), 'pf_lts':linear_log<s,'quadratic_lts':quadratic<s})
        win_count+=int(linear_log<s and quadratic>=s)
    frontier.append(rec)
ck(any(x['pf_strict'] and not x['quadratic_strict'] for x in frontier),'no strict improvement case')
ck(win_count>0,'finite degree window not witnessed')

# Exact contrapositive using bound s < K*H*ceil(log_2(2H)) implies H > s/(K*ceil(log_2(2s)))
for h in range(2,60):
    for logL in range(0,10):
        s=1<<h
        H=1<<logL
        if H >= 1 and s < K*H*(H.bit_length()+1):
            bound=(s//(K*(s.bit_length()+1)))
            ck(H>=bound,'inverse linear/log implication failed')

out={
    'experiment':'TMR4-PF-LIFT044',
    'status':'COMPUTATIONAL finite regression checks; theorem uses Pippenger-Fischer 1979 Theorem 4',
    'seed':SEED,
    'assertions':checks,
    'failed':0,
    'formulas':formula_count,
    'indexed_bits_checked':bit_count,
    'max_index_circuit_gates':max_gates,
    'formula_controls':classes,
    'frontier_proxy_K':K,
    'strict_improvement_sample_count':win_count,
    'frontier':frontier,
    'no_exponential_truth_tables_allocated':True,
    'no_TM_to_circuit_compiler_executed':True,
}
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/mnt/data/tmr4_pf_index_lift044_raw.json')
path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf8')
print(json.dumps({'assertions':checks,'failed':0,'formulas':formula_count,'indexed_bits_checked':bit_count,'strict_window_samples':win_count,'output':str(path)},sort_keys=True))
