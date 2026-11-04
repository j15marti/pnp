#!/usr/bin/env python3
"""Independent finite replay of LSPV3/379 gate/RES data, not a full Rmix341 checker."""
import itertools, json, sys
r=json.load(open(sys.argv[1],encoding='utf-8'))
checks=0
def must(b,s):
    global checks
    if not b: raise AssertionError(s)
    checks+=1
def literal(l,a): return a[abs(l)] == (l>0)
def clause(c,a): return any(literal(l,a) for l in c)
gates=r['gates']
must([g['out'] for g in gates]==[7,8,9],'gate ids')
must([g['input'] for g in gates]==[[1,2],[7,3],[8,4]],'gate input ids')
for bits in itertools.product([False,True],repeat=9):
    a={i+1:b for i,b in enumerate(bits)}
    for g in gates:
        u,v=g['input']
        must(all(clause(c,a) for c in g['slots']) == (a[g['out']] == (a[u] and a[v])),'gate clauses iff AND')
for bits in itertools.product([False,True],repeat=6):
    a={i+1:b for i,b in enumerate(bits)}
    for g in gates:
        u,v=g['input'];a[g['out']]=a[u] and a[v]
    p,q=r['premises'];out=r['resolvent']
    must(not(clause(p,a) and clause(q,a)) or clause(out,a),'RES sound')
    must((clause(p,a) and clause(q,a))==clause(out,a),'non-tautological factor')
    must(all(clause(c,a) for g in gates for c in g['slots']),'conservative definition')
p,q=r['premises'];pivot=r['pivot']
must(pivot in p and -pivot in q,'signed pivot present')
res=sorted(set(p).difference({pivot}).union(set(q).difference({-pivot})))
must(res==r['resolvent'],'resolution exact')
support={i:{i} for i in range(1,7)}
for g in gates:support[g['out']]=support[g['input'][0]]|support[g['input'][1]]
lexical={abs(v) for c in r['premises'] for v in c}
base=set().union(*(support[v] for v in lexical))
must(sorted(lexical)==r['lexicalSupport'],'lexical support')
must(sorted(base)==r['baseSupport'],'base support')
must(len(lexical)==3 and len(base)==6,'retyping mismatch')
must(clause(p,{9:True,5:False,6:False}) and not clause(r['resolvent'],{9:True,5:False,6:False}),'missing premise falsifier')
edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
for charge,expect in [([1,0,0,0],0),([0,0,0,0],8)]:
    models=0
    for mask in itertools.product([0,1],repeat=6):
        if all(sum(mask[i] for i,e in enumerate(edges) if v in e)%2 == charge[v] for v in range(4)):
            models+=1
    must(models==expect,'opposite parity labels')
must(r['corrupted_or_malformed_rejected']==9,'negative fixtures logged')
print(json.dumps({'assertions':checks,'status':'PASS','scope':'local signed gates, strict RES and K4'}))
