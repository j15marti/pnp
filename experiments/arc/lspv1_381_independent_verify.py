#!/usr/bin/env python3
"""Independent Python verifier of LSPV-1/381 public-output affine bank.
Read JSON producer fixture evidence, reject malformed records, and re-evaluate
both implementations across every full boundary input. No external packages.
"""
import json,sys
src=sys.argv[1] if len(sys.argv)>1 else 'fixtures.json'
data=json.load(open(src,encoding='utf-8'))
checks=0

def check(x):
    global checks
    assert x
    checks+=1

def op(name,a,b):
    ab=a&b; o=a|b; z=a^b
    return {'AND':ab,'OR':o,'XOR':z,'NAND':1-ab,'NOR':1-o,'XNOR':1-z}[name]

def validate(spec,bank):
    B,k=spec['B'],spec['k']
    assert 1<=k<=B
    assert len(spec['rows'])==k
    for row in spec['rows']:
        assert len(row['bits'])==B
        assert all(b in [0,1] for b in row['bits'])
        assert row['c'] in [0,1]
    for j,gate in enumerate(spec['gates']):
        assert gate['op'] in ('AND','OR','XOR','NAND','NOR','XNOR')
        assert 0<=gate['a']<k+j and 0<=gate['b']<k+j
    assert all(0<=idx<k+len(spec['gates']) for idx in spec['outputs'])
    for j,gate in enumerate(bank['ands']):
        assert gate['sa'] in (-1,1) and gate['sb'] in (-1,1)
        assert 0<=gate['a']<B+j and 0<=gate['b']<B+j
    assert all(0<=a['id']<B+len(bank['ands']) and a['s'] in (-1,1) for a in bank['outputs'])
    assert len(bank['outputs'])==len(spec['outputs'])

def reference(spec,mask):
    B=spec['B']
    vec=[(mask>>j)&1 for j in range(B)]
    bits=[]
    for row in spec['rows']:
        bits.append((row['c']+sum(a*b for a,b in zip(vec,row['bits'])))%2)
    for gate in spec['gates']:
        bits.append(op(gate['op'],bits[gate['a']],bits[gate['b']]))
    return tuple(bits[j] for j in spec['outputs'])

def witness(bank,mask):
    values=[(mask>>j)&1 for j in range(bank['B'])]
    def lit(i,sign):
        return values[i] if sign==1 else 1-values[i]
    for gate in bank['ands']:
        values.append(lit(gate['a'],gate['sa']) & lit(gate['b'],gate['sb']))
    return tuple(lit(a['id'],a['s']) for a in bank['outputs'])

for fx in data['fixtures']:
    spec,bank=fx['spec'],fx['bank'];validate(spec,bank)
    B,k,r=spec['B'],spec['k'],len(spec['outputs'])
    check(len(bank['ands'])<=3*k*B+r*k*(2**k)+1)
    for mask in range(2**B):
        check(reference(spec,mask)==witness(bank,mask))
    mutant=json.loads(json.dumps(bank));mutant['outputs'][0]['s']=0
    try:validate(spec,mutant)
    except AssertionError:checks+=1
    else:raise AssertionError('Corrupt alias accepted')
    bad=json.loads(json.dumps(spec));bad['rows'][0]['bits'].pop()
    try:validate(bad,bank)
    except AssertionError:checks+=1
    else:raise AssertionError('Malformed row accepted')

def k4models(charges):
    edge=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    return sum(all(sum(((mask>>j)&1) for j,(a,b) in enumerate(edge) if v in (a,b))%2==charges[v] for v in range(4)) for mask in range(64))
# A three-variable OR does not factor through any single nonzero affine row.
for row in range(1,8):
    groups = {0:set(),1:set()}
    for word in range(8):
        inner = (word&row).bit_count()%2
        groups[inner].add(int(word!=0))
    check(any(len(v)>1 for v in groups.values()))
check(k4models((0,0,0,0))==8)
check(k4models((1,0,0,0))==0)
print(json.dumps({'run':'AFFINE_SKETCH_BANK381_INDEPENDENT','assertions':checks,'fixtures':len(data['fixtures']),'k4_even':8,'k4_odd':0,'status':'PASS','scope':'finite exact fixture replay; no Rmix341 soundness claim'},indent=2))
