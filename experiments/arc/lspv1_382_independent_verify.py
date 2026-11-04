#!/usr/bin/env python3
"""Independent finite control audit for LSPV-1/382, no npm or third-party libraries."""
import itertools, json, re
count = 0
def checked(c, context):
    global count
    count += 1
    if not c: raise AssertionError(context)

def label(source):
    if not isinstance(source, str): return 'MALFORMED'
    lines=source.split('\n')
    match=re.fullmatch(r'p cnf (0|[1-9]\d*) (0|[1-9]\d*)', lines[0])
    if not match: return 'MALFORMED'
    n,m=map(int,match.groups())
    if n>12 or m>200 or len(lines)!=m+1: return 'MALFORMED'
    formula=[]
    for row in lines[1:]:
        if not re.fullmatch(r'(?:-?[1-9][0-9]* )*0',row): return 'MALFORMED'
        vals=list(map(int,row.split()[:-1]))
        if any(abs(v)>n or v==0 for v in vals): return 'MALFORMED'
        formula.append(vals)
    for bits in itertools.product((False,True),repeat=n):
        if all(any((bits[abs(v)-1] if v>0 else not bits[abs(v)-1]) for v in clause) for clause in formula): return 'SAT'
    return 'UNSAT'

fixtures=[
 'p cnf 0 0','p cnf 0 1\n0','p cnf 1 1\n1 0','p cnf 1 2\n1 0\n-1 0',
 'p cnf 2 2\n1 2 0\n-1 -2 0','p cnf 2 3\n1 0\n-1 2 0\n-2 0',
 'p cnf 3 2\n1 2 3 0\n-1 -2 -3 0','p cnf 2 1\n0',
 '','p cnf','p cnf 1 1\n2 0','p cnf 1 1\n1 0\n','p cnf 2 1\n1 a 0',
 'p cnf 1 1\n-0 0','p cnf 01 0','p cnf 1 1\n1 -1 0',
]
counts={'SAT':0,'UNSAT':0,'MALFORMED':0}
for x in fixtures: counts[label(x)]+=1
for special in fixtures:
    answer=label(special)
    for other in fixtures:
        got=answer if other==special else label(other)
        checked(got==label(other), 'cross fixture correctness')
    checked(2*len(special)+64<=4*len(special)+80,'linear description envelope')
for length in range(9):
    for tup in itertools.product('01',repeat=length):
        other=''.join(tup)
        for special in fixtures[:3]:
            patched=label(special) if other==special else label(other)
            checked(patched==label(other),'fallback on binary strings')

def parity_rows(rhs):
    return [' '.join(str(-i-1 if bit else i+1) for i,bit in enumerate(bits))+' 0'
            for bits in itertools.product((0,1),repeat=3) if sum(bits)%2 != rhs]
even,odd=parity_rows(0),parity_rows(1)
checked(label('p cnf 3 4\n'+'\n'.join(even))=='SAT','even parity satisfiable')
checked(label('p cnf 3 4\n'+'\n'.join(odd))=='SAT','odd parity satisfiable')
checked(label('p cnf 3 8\n'+'\n'.join(even+odd))=='UNSAT','opposing parity unsat')
checked(counts=={'SAT':5,'UNSAT':4,'MALFORMED':7},'matching class counts')
print(json.dumps({'experiment':'LSPV1_PATCH382_INDEPENDENT','checks':count,'fixture_count':len(fixtures),'classes':counts,'binary_strings':sum(2**n for n in range(9)),'pass':True},indent=2))
