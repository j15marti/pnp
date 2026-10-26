#!/usr/bin/env python3
"""ARC184: canonical first-violated-clause selector and exact validation identity.

This finite experiment is not a SAT lower bound.  It constructs a real,
bounded-fanin Boolean gate list J_F(y) for every given proper 3CNF F,
exhaustively tests J_F(y)=the first falsified clause (or 0 if F(y)=True),
and compares universal selector validity with UNSAT on several SAT/UNSAT
families, including the signed exact-(2,2) Q15/W20 source.

Invocation: python arc184_canonical_selector.py [optional results path]
All dependencies are Python standard library.
"""
from __future__ import annotations
import collections
import hashlib
import itertools
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path

SEED = 202610260313
Q_RAW = '''
 -1 3 -14      2 -8 9      10 -13 14      3 7 -13
 -4 -9 -11      5 8 -14       4 -8 -11     1 7 13
  1 -7 10     -5 -6 -15      -2 -6 12     -4 9 -10
 -2 5 -12     -3 6 -15       6 -7 11      2 -9 11
  4 8 -10     -3 12 15      -5 -12 15     -1 13 14
'''
W_VARS = list(map(int,Q_RAW.split()))
W = tuple(tuple(W_VARS[i:i+3]) for i in range(0,len(W_VARS),3))
Q = tuple(c for c in W if c != (1,7,13))
Y = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))


def formula_truth(clauses, mask):
    return all(any(((mask >> (abs(lit)-1)) & 1) == (lit>0) for lit in clause)
               for clause in clauses)


def first_falsified(clauses, mask):
    return next((j for j,clause in enumerate(clauses,1) if not any(
        ((mask >> (abs(lit)-1)) & 1) == (lit>0) for lit in clause)), 0)


def is_short_cnf(clauses,n):
    return all(0<=len(c)<=3 and len(set(abs(x) for x in c))==len(c) and
               all(1<=abs(x)<=n for x in c) for c in clauses)


def restrict_formula(clauses,pins):
    children=[]
    for clause in clauses:
        if any(abs(l) in pins and pins[abs(l)]==(l>0) for l in clause):
            continue
        children.append(tuple(l for l in clause if abs(l) not in pins))
    return tuple(children)


def is_proper(clauses, n):
    return all(len(c)==3 and len({abs(x) for x in c})==3 and
               all(1<=abs(x)<=n for x in c) for c in clauses)


def grammar(clauses, n):
    p=collections.Counter(abs(x) for clause in clauses for x in clause if x>0)
    m=collections.Counter(abs(x) for clause in clauses for x in clause if x<0)
    return dict(proper=is_proper(clauses,n),unique=len(set(clauses))==len(clauses),
                signed22=all(p[v]==m[v]==2 for v in range(1,n+1)),
                monotone=all(all(x>0 for x in c) or all(x<0 for x in c) for c in clauses))


@dataclass
class Gate:
    op: str
    a: int = -1
    b: int = -1


class CanonicalCircuit:
    """Explicit topologically ordered AND/OR/NOT fan-in-two circuit.

    Nodes 0 and 1 are Boolean constants, nodes [2..n+1] are input bits.
    Output is the binary, 1-based index of the first violated clause,
    with the all-zero word reserved for an assignment satisfying F.
    """
    def __init__(self, clauses, n):
        assert is_short_cnf(clauses,n)
        self.clauses=tuple(tuple(int(x) for x in c) for c in clauses)
        self.n=n
        self.gates=[Gate('C0'),Gate('C1')]+[Gate('IN',i) for i in range(n)]
        self.bitwidth=max(1,len(clauses).bit_length())
        self.not_inputs={}
        first=[]
        prefix=0
        for clause in self.clauses:
            falses=[self.false_literal(lit) for lit in clause]
            violation=1
            for bad in falses:
                violation=self.add('AND',violation,bad)
            is_first=self.add('AND',violation,self.add('NOT',prefix))
            first.append(is_first)
            prefix=self.add('OR',prefix,violation)
        self.any_violation=prefix
        self.output_nodes=[]
        for bit in range(self.bitwidth):
            acc=0
            for index,onehot in enumerate(first,1):
                if index & (1<<bit):
                    acc=self.add('OR',acc,onehot)
            self.output_nodes.append(acc)

    def add(self,op,a,b=-1):
        self.gates.append(Gate(op,a,b))
        return len(self.gates)-1

    def false_literal(self,lit):
        # If literal is positive x: it is false when x=0.
        # If literal is negative -x: it is false when x=1.
        v=abs(lit)-1
        inp=2+v
        if lit<0:return inp
        if v not in self.not_inputs:self.not_inputs[v]=self.add('NOT',inp)
        return self.not_inputs[v]

    def eval(self,mask):
        vals=[0]*len(self.gates)
        vals[1]=1
        for i,g in enumerate(self.gates[2:],start=2):
            if g.op=='IN': vals[i]=(mask>>g.a)&1
            elif g.op=='NOT': vals[i]=1-vals[g.a]
            elif g.op=='AND': vals[i]=vals[g.a]&vals[g.b]
            elif g.op=='OR': vals[i]=vals[g.a]|vals[g.b]
            else: raise ValueError(g.op)
        idx=sum(vals[node]<<bit for bit,node in enumerate(self.output_nodes))
        return idx, vals[self.any_violation]

    @property
    def size(self):return len(self.gates)-2-self.n


def eq_pin(lit,a,b):
    return [(lit,x*a,y*b) for x in (1,-1) for y in (1,-1)]


def odd_xor():
    # XOR(x,y,z)=1, its four forbidden even assignments are excluded.
    out=[]
    for values in itertools.product((0,1),repeat=3):
        if sum(values)%2==0:
            out.append(tuple((v if val==0 else -v) for v,val in zip((1,2,3),values)))
    return tuple(out)


def random_formulas(rng):
    for n in range(3,8):
        for j in range(10):
            m=3+j%5
            clauses=[]
            for _ in range(m):
                ids=rng.sample(range(1,n+1),3)
                clauses.append(tuple(v if rng.getrandbits(1) else -v for v in ids))
            yield f'RANDOM_{n}_{j}',n,tuple(clauses)


def main():
    rng=random.Random(SEED)
    controls=[('W20_UNSAT_signed22',15,W),('Q19_SAT_three_ports',15,Q),
        ('ODD_XOR_SAT_signed22',3,odd_xor()),
        ('Y8_SAT_monotone22',6,Y),
        ('U_LITERAL_SAT',3,tuple(eq_pin(1,2,3))),
        ('TWO_PIN_UNSAT',5,tuple(eq_pin(1,2,3)+eq_pin(-1,4,5))),
        ('SINGLE_SAT',3,((1,2,3),)),
        ('EMPTY_CONJ_SAT',3,tuple())]
    controls.extend(random_formulas(rng))
    total_checks=0
    total_assignments=0
    labelled={'SAT':0,'UNSAT':0}
    instances=[]
    max_circuit=0
    for name,n,clauses in controls:
        if not clauses:
            # Empty conjunction: constant selector zero.
            expected_models=1<<n
            labelled['SAT']+=1
            instances.append(dict(name=name,n=n,m=0,models=expected_models,gate_count=0,
                                  valid_selector=False,proper=True,skip_empty=True))
            total_checks+=1
            continue
        assert is_proper(clauses,n)
        circuit=CanonicalCircuit(clauses,n)
        max_circuit=max(max_circuit,circuit.size)
        models=0
        valids=0
        for assignment in range(1<<n):
            s=formula_truth(clauses,assignment)
            ref=first_falsified(clauses,assignment)
            idx,anybad=circuit.eval(assignment)
            assert idx==ref,(name,assignment,idx,ref)
            total_checks+=1
            assert (idx==0)==s,(name,assignment,'zero indicator wrong')
            total_checks+=1
            assert bool(anybad)==(not s),(name,assignment,'sum indicator wrong')
            total_checks+=1
            # Parent-validation failure iff assignment satisfies parent F.
            pred=(1<=idx<=len(clauses) and
                  not any(((assignment>>(abs(l)-1))&1)==(l>0) for l in clauses[idx-1])) if idx else False
            assert pred==(not s),(name,assignment,'semantic validation identity wrong')
            total_checks+=1
            models+=int(s)
            valids+=int(pred)
            total_assignments+=1
        assert ((valids==(1<<n))==(models==0))
        total_checks+=1
        g=grammar(clauses,n)
        instances.append(dict(name=name,n=n,m=len(clauses),models=models,
                 label='UNSAT' if models==0 else 'SAT',
                 gate_count=circuit.size,bitwidth=circuit.bitwidth,
                 universal_validity=(valids==(1<<n)),grammar=g))
        labelled['UNSAT' if models==0 else 'SAT']+=1
    Wgrammar=grammar(W,15)
    assert Wgrammar['signed22'] and Wgrammar['proper'] and Wgrammar['unique']
    assert sum(i['models'] for i in instances if i['name']=='W20_UNSAT_signed22')==0
    assert next(i for i in instances if i['name']=='Q19_SAT_three_ports')['models']==244
    assert next(i for i in instances if i['name']=='ODD_XOR_SAT_signed22')['models']==4
    assert next(i for i in instances if i['name']=='TWO_PIN_UNSAT')['models']==0
    assert next(i for i in instances if i['name']=='Y8_SAT_monotone22')['models']==20
    total_checks+=6
    # Two genuine levels of original-variable restriction with real residual
    # gate circuits. These are short-CNF children, NOT in exact-(2,2).
    two_level=[]
    for name,n,clauses in [('W20_UNSAT_signed22',15,W),('Y8_SAT_monotone22',6,Y)]:
        labels=[]
        for pins_tuple in itertools.product((0,1),repeat=2):
            pins={1:bool(pins_tuple[0]),2:bool(pins_tuple[1])}
            residual=restrict_formula(clauses,pins)
            circuit=CanonicalCircuit(residual,n)
            free=[v for v in range(1,n+1) if v not in pins]
            sat_count=0
            for fbits in range(1<<len(free)):
                assignment=sum((int(pins[v]) << (v-1)) for v in pins)
                assignment+=sum(((fbits>>i)&1) << (v-1) for i,v in enumerate(free))
                idx,anybad=circuit.eval(assignment)
                truth=formula_truth(clauses,assignment)
                assert (idx==0)==truth==(first_falsified(residual,assignment)==0)
                assert anybad==(not truth)
                total_checks+=2
                sat_count+=int(truth)
            labels.append(sat_count>0)
            two_level.append(dict(parent=name,pins=list(pins_tuple),mchild=len(residual),
                                  child_sat=bool(sat_count),models=sat_count,
                                  gate_count=circuit.size,exact22_child=False))
        assert any(labels)==(name=='Y8_SAT_monotone22')
        total_checks+=1
    script_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    output={'status':'COMPUTATIONAL; symbolic theorem needs independent review',
       'run_id':'ARC-CANONICAL-CONFLICT-SELECTOR184',
       'seed':SEED,'source_script_sha256':script_hash,
       'control_count':len(instances),'total_assignments':total_assignments,
       'checks':total_checks,'failures':0,'labels':labelled,
       'max_gate_count':max_circuit,'two_level_children':two_level,'model_scope':
       'all 2^n inputs per finite source, explicit bounded-fanin gate evaluation; not all-input SAT solver',
       'key_facts':{
          'canonical_selector_created_on_SAT_and_UNSAT':'YES',
          'universal_selector_validity_equals_UNSAT':'all enumerated controls',
          'canonical_invalidity_query_equivalent_to_parent_SAT':'every enumerated assignment',
          'short_selector_not_decision_circuit':True,
          'general_A_resource_transition_proved':False},
       'instances':instances}
    filepath=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('arc184_results.json')
    filepath.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='instances'},indent=2,sort_keys=True))

if __name__=='__main__':main()
