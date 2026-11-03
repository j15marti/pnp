#!/usr/bin/env python3
"""LSPV-1 360: finite source/Resolution controls for known oracle barrier.
No oracle is implemented. Standard library only, deterministic and reproducible.
"""
import hashlib
import itertools
import json

def php(pigeons, holes):
    assert pigeons > holes and holes >= 1
    v = {(p,h):1+p*holes+h for p in range(pigeons) for h in range(holes)}
    clauses = [tuple(v[p,h] for h in range(holes)) for p in range(pigeons)]
    for h in range(holes):
        for p in range(pigeons):
            for q in range(p+1,pigeons):
                clauses.append((-v[p,h],-v[q,h]))
    return pigeons*holes, clauses

def sat_witness(n,clauses):
    for bits in itertools.product((False,True), repeat=n):
        if all(any(bits[abs(lit)-1] == (lit>0) for lit in clause) for clause in clauses):
            return ''.join('1' if b else '0' for b in bits)
    return None

def canonical(clause):
    s=set(clause)
    if 0 in s or any(-x in s for x in s):
        raise ValueError('tautological or malformed clause')
    return tuple(sorted(s,key=lambda l:(abs(l),l<0)))

def parse_dimacs(src):
    lines=[l.strip() for l in src.splitlines()
           if l.strip() and not l.lstrip().startswith('c')]
    if not lines: raise ValueError('missing header')
    head=lines[0].split()
    if len(head)!=4 or head[:2]!=['p','cnf']: raise ValueError('bad header')
    try: n,m=map(int,head[2:])
    except ValueError: raise ValueError('bad counts')
    if n<0 or m<0 or len(lines)!=m+1: raise ValueError('wrong counts')
    clauses=[]
    for line in lines[1:]:
        try: row=list(map(int,line.split()))
        except ValueError: raise ValueError('nonnumeric literal')
        if not row or row[-1]!=0 or row.count(0)!=1:
            raise ValueError('bad terminator')
        if any(abs(l)>n for l in row[:-1]): raise ValueError('out of range')
        clauses.append(canonical(row[:-1]))
    return n,clauses

def resolution_certificate(n,clauses):
    lines=[canonical(c) for c in clauses]
    index=set(lines)
    proof=[]
    front=0
    while front<len(lines):
        a=lines[front]
        for i in range(front):
            b=lines[i]
            for lit in a:
                if -lit in b:
                    q=set(a);q.remove(lit)
                    r=set(b);r.remove(-lit)
                    z=q|r
                    if any(-u in z for u in z): continue
                    z=canonical(z)
                    if z not in index:
                        proof.append([front,i,abs(lit),list(z)])
                        index.add(z);lines.append(z)
                        if not z: return proof
        front+=1
    raise RuntimeError('no resolution refutation found')

def replay(clauses,proof):
    lines=[canonical(x) for x in clauses]
    for i,j,p,z in proof:
        if not(0<=i<len(lines) and 0<=j<len(lines) and p>0):
            raise ValueError('bad parent')
        a,b=set(lines[i]),set(lines[j])
        if p in a and -p in b: a.remove(p);b.remove(-p)
        elif -p in a and p in b: a.remove(-p);b.remove(p)
        else: raise ValueError('bad pivot')
        expected=canonical(a|b)
        if expected!=tuple(z): raise ValueError('wrong resolvent')
        lines.append(expected)
    if not proof or lines[-1]!=(): raise ValueError('no contradiction')
    return len(proof)

def parity_k4(charge):
    edges=list(itertools.combinations(range(4),2))
    out=[]
    for state in itertools.product((0,1),repeat=6):
        if all((sum(state[i] for i,e in enumerate(edges) if v in e)&1)==charge[v]
               for v in range(4)):
            out.append(''.join(map(str,state)))
    return out

def main():
    records=[];checks=0
    for holes in (1,2,3):
        p=holes+1;n,F=php(p,holes)
        assert sat_witness(n,F) is None;checks+=1
        repairs=[]
        for j in range(len(F)):
            w=sat_witness(n,F[:j]+F[j+1:])
            assert w is not None;checks+=1
            repairs.append(w)
        sign_repairs=0
        for j,row in enumerate(F):
            for h in range(len(row)):
                amended=[tuple(c) for c in F]
                changed=list(amended[j]);changed[h]=-changed[h]
                amended[j]=tuple(changed)
                assert sat_witness(n,amended) is not None;checks+=1
                sign_repairs+=1
        cert=None
        if holes<=2:
            cert=resolution_certificate(n,F)
            assert replay(F,cert)==len(cert);checks+=1
            attack=[list(row) for row in cert]
            attack[0]=list(attack[0]);attack[0][2]=n+10
            try:
                replay(F,attack)
                raise AssertionError('accepted forged pivot')
            except ValueError: checks+=1
        encoded='\n'.join(' '.join(map(str,c))+' 0' for c in F)+'\n'
        records.append({'pigeons':p,'holes':holes,'variables':n,'clauses':len(F),
                        'SAT':False,'all_deletions_SAT':len(repairs),
                        'all_single_literal_sign_flips_SAT':sign_repairs,
                        'sample_deletion_witness':repairs[0],
                        'resolution_upper_nodes':len(cert) if cert is not None else None,
                        'encoded_source_sha256':hashlib.sha256(encoded.encode()).hexdigest()})
    assert sat_witness(2,[(1,2)]) is not None;checks+=1
    assert sat_witness(1,[(1,),(-1,)]) is None;checks+=1
    assert len(parity_k4((1,0,0,0)))==0;checks+=1
    assert len(parity_k4((0,0,0,0)))==8;checks+=1
    for bad in [(0,), (1,-1), (999,-999)]:
        try:
            canonical(bad)
            raise AssertionError('accepted malformed clause')
        except ValueError: checks+=1
    valid='p cnf 1 2\n1 0\n-1 0\n'
    assert parse_dimacs(valid)==(1,[(1,),(-1,)]);checks+=1
    for malformed in ['p cnf 1 3\n1 0\n-1 0\n',
                      'p cnf 1 2\n2 0\n-1 0\n',
                      'p cnf 1 1\n1\n',
                      'p xnf 1 1\n1 0\n',
                      'p cnf 1 1\na 0\n',
                      'p cnf 1 1\n1 0 0\n']:
        try:
            parse_dimacs(malformed)
            raise AssertionError('accepted malformed DIMACS')
        except ValueError: checks+=1
    payload={
        'identifier':'LSPV1_360_QBF_ORACLE_RELATIVIZATION_FIREWALL',
        'status':{'oracle_collapse':'KNOWN THEOREM mathematical, not computationally simulated',
                  'resolution_asymptotics':'KNOWN THEOREM Haken 1985, not computationally simulated',
                  'finite_controls':'COMPUTATIONAL','full_Rmix341_B3':'OPEN'},
        'fixed_system':'Rmix341 remains unchanged; finite certificates use only strict RES with one unit per new derived node',
        'finite_php':records,
        'other_controls':{'SAT_unit_clauses':True,'UNSAT_contradictory_units':True,
                          'odd_K4_models':0,'even_K4_models':8,'malformed_clause_rejections':3,
                          'malformed_DIMACS_rejections':6,'corrupt_pivot_rejections':2},
        'assertions':checks,
        'oracle_queries_executed':0,
        'proof_discovery_work':'closure enumeration to obtain finite upper certificates; not charged to W_R',
        'source_ref':'Haken 1985 DOI 10.1016/0304-3975(85)90144-6',
        'oracle_ref':'Baker Gill Solovay 1975 DOI 10.1137/0204037',
        'note':'Finite n<=3 data do not establish the Haken lower bound or TQBF PSPACE theorem.'
    }
    print(json.dumps(payload,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
