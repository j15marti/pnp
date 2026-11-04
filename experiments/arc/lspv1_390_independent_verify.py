#!/usr/bin/env python3
"""Independent exhaustive signed Tseitin/duplicated-CNF checks for LSPV-1/390."""
import json
import sys
from itertools import product

check_count = 0

def require(p, message):
    global check_count
    check_count += 1
    if not p:
        raise AssertionError(message)

def edges(name):
    if name == 'k4':
        return [(a,b) for a in range(4) for b in range(a+1,4)]
    if name == 'prism6':
        return [(a,(a+1)%3) for a in range(3)] + [(a,3+(a-2)%3) for a in range(3,6)] + [(a,a+3) for a in range(3)]
    raise ValueError(name)

def signed_cnf(name, odd):
    ee = edges(name)
    h = 4 if name == 'k4' else 6
    clauses = []
    for vertex in range(h):
        incident = [i for i,(a,b) in enumerate(ee) if vertex == a or vertex == b]
        require(len(incident) == 3, 'cubic')
        for bits in product([0,1],repeat=3):
            if sum(bits)%2 != (int(odd) if vertex == 0 else 0):
                clauses.append(tuple((edge,bit) for edge,bit in zip(incident,bits)))
    require(len(clauses)==4*h, 'local parity clauses')
    return ee, clauses

def witness(clauses, n):
    for bits in product([0,1], repeat=n):
        if all(any(bits[i] != false_bit for i,false_bit in clause) for clause in clauses):
            return bits
    return None

def evaluate_one(clauses, values):
    return all(any(values[i] != false_bit for i,false_bit in c) for c in clauses)

def main(path):
    data = json.load(open(path,encoding='utf-8'))
    require(len(data['rows']) == 8,'eight cases')
    for row in data['rows']:
        ee, original = signed_cnf(row['graph'],True)
        r=row['r']; h=row['h']; L=sum(map(len,original));m=len(original)
        copies = [tuple(c) for c in original for _ in range(r)]
        require(witness(copies,len(ee)) is None, 'odd UNSAT')
        require(witness(signed_cnf(row['graph'],False)[1],len(ee)) is not None,'even SAT')
        require((m,L,4*h-1,r*L)==(row['classes'],row['literal_groups'],row['fixed_Rmix341_paid_node_minimum'],row['sign_positions']),'metadata')
        require(row['promised_integral_transversal']==L==row['promised_fractional_transversal'],'LP certificate')
        require(row['min_sat_sign_flips']==r,'radius formula')
        for j,c in enumerate(original):
            w=witness([v for i,v in enumerate(original) if i!=j], len(ee))
            require(w is not None and not any(w[i]!=false_bit for i,false_bit in c),'deletion witness')
            for k in range(3):
                modified=list(copies)
                for t in range(r):
                    cc=list(modified[j*r+t]);i,bit=cc[k];cc[k]=(i,1-bit);modified[j*r+t]=tuple(cc)
                require(evaluate_one(modified,w),'all r flips SAT with witness')
                if r>1:
                    cc=list(modified[j*r]);i,bit=cc[k];cc[k]=(i,1-bit); modified[j*r]=tuple(cc)
                    require(witness(modified,len(ee)) is None,'r-1 group flips UNSAT')
        # Pairwise disjoint SAT-neighbor r-bit groups, one per original source literal.
        seen=set()
        for j,c in enumerate(original):
            for k in range(len(c)):
                group={(j*r+t,k) for t in range(r)}
                require(not (group & seen),'disjoint groups')
                seen |= group
        require(len(seen)==r*L, 'cover all signed positions')
    for item in data['toyDist']:
        r = item['r']
        minimal = None
        count = 0
        for signs in product((0,1),repeat=2*r):
            clauses = [((0,signs[i]),) for i in range(r)] + [((0,1-signs[r+i]),) for i in range(r)]
            if witness(clauses, 1) is not None:
                count += 1
                distance = sum(signs)
                minimal = distance if minimal is None else min(minimal,distance)
        require(minimal==item['min']==r and count==item['countSat']==2,'exact toy radius')
    for bad in ['','0','1;','a','1;;-1','1;0']:
        import re
        valid = all(re.fullmatch(r'\s*-?[1-9]\d*(?:\s+-?[1-9]\d*)*\s*',clause) for clause in bad.split(';'))
        require(not valid,'malformed rejects')
    print(json.dumps({'independent_assertions':check_count,'status':'PASS','rows':len(data['rows']),'seed':'none'},sort_keys=True))
if __name__=='__main__':
    main(sys.argv[1])
