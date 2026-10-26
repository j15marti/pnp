#!/usr/bin/env python3
"""Independent audit for GLOBAL-BACKDOOR-PRODUCT162.

Checks the mixed-sign W1 product completely, and checks the syntax and
connectivity of the clause-monotone cyclic U product.  UNSAT(U) is imported
from Döcker (arXiv:1912.08032, Appendix C), not recomputed here.
"""
from collections import Counter, deque
from itertools import combinations, product
import json, math

W1 = tuple(tuple(map(int, row.split())) for row in '''
-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;
4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;
-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;
-5 -12 15;-1 13 14'''.replace('\n','').split(';'))

# Exact source records from repository blob
# f9dda41a810ad8e02bd553f2711a26a4050861f9 (Döcker Appendix C).
U = (
(-193,-196,-198),(194,196,197),(1,2,197),(-2,-3,-194),(-2,-4,-194),(-3,-5,-6),(-4,-5,-6),(5,7,8),(6,7,8),(-7,-18,-19),(-7,-20,-21),(-8,-18,-19),(-8,-20,-21),(3,9,10),(3,11,12),(4,13,14),(4,15,16),(9,12,15),(10,13,17),(11,16,17),(-9,-13,-16),(-9,-14,-17),(-10,-11,-14),(-10,-12,-16),(-11,-13,-15),(-12,-15,-17),(2,24,32),(18,23,25),(18,28,29),(19,23,25),(19,28,29),(20,22,26),(20,30,31),(21,22,31),(21,26,27),(24,27,30),(-1,-22,-23),(-1,-24,-25),(-22,-25,-32),(-23,-24,-26),(-26,-28,-30),(-27,-28,-31),(-27,-29,-31),(-29,-30,-32),(33,34,196),(-34,-35,-195),(-34,-36,-198),(-35,-37,-38),(-36,-37,-38),(37,39,40),(38,39,40),(-39,-50,-51),(-39,-52,-53),(-40,-50,-51),(-40,-52,-53),(35,41,42),(35,43,44),(36,45,46),(36,47,48),(41,44,47),(42,45,49),(43,48,49),(-41,-45,-48),(-41,-46,-49),(-42,-43,-46),(-42,-44,-48),(-43,-45,-47),(-44,-47,-49),(34,56,64),(50,55,57),(50,60,61),(51,55,57),(51,60,61),(52,54,58),(52,62,63),(53,54,63),(53,58,59),(56,59,62),(-33,-54,-55),(-33,-56,-57),(-54,-57,-64),(-55,-56,-58),(-58,-60,-62),(-59,-60,-63),(-59,-61,-63),(-61,-62,-64),(65,66,193),(-66,-67,-195),(-66,-68,-197),(-67,-69,-70),(-68,-69,-70),(69,71,72),(70,71,72),(-71,-82,-83),(-71,-84,-85),(-72,-82,-83),(-72,-84,-85),(67,73,74),(67,75,76),(68,77,78),(68,79,80),(73,76,79),(74,77,81),(75,80,81),(-73,-77,-80),(-73,-78,-81),(-74,-75,-78),(-74,-76,-80),(-75,-77,-79),(-76,-79,-81),(66,88,96),(82,87,89),(82,92,93),(83,87,89),(83,92,93),(84,86,90),(84,94,95),(85,86,95),(85,90,91),(88,91,94),(-65,-86,-87),(-65,-88,-89),(-86,-89,-96),(-87,-88,-90),(-90,-92,-94),(-91,-92,-95),(-91,-93,-95),(-93,-94,-96),(-97,-98,-197),(98,99,195),(98,100,195),(99,101,102),(100,101,102),(-101,-103,-104),(-102,-103,-104),(103,114,115),(103,116,117),(104,114,115),(104,116,117),(-99,-105,-106),(-99,-107,-108),(-100,-109,-110),(-100,-111,-112),(-105,-108,-111),(-106,-109,-113),(-107,-112,-113),(105,109,112),(105,110,113),(106,107,110),(106,108,112),(107,109,111),(108,111,113),(-98,-120,-128),(-114,-119,-121),(-114,-124,-125),(-115,-119,-121),(-115,-124,-125),(-116,-118,-122),(-116,-126,-127),(-117,-118,-127),(-117,-122,-123),(-120,-123,-126),(97,118,119),(97,120,121),(118,121,128),(119,120,122),(122,124,126),(123,124,127),(123,125,127),(125,126,128),(-129,-130,-196),(130,131,193),(130,132,194),(131,133,134),(132,133,134),(-133,-135,-136),(-134,-135,-136),(135,146,147),(135,148,149),(136,146,147),(136,148,149),(-131,-137,-138),(-131,-139,-140),(-132,-141,-142),(-132,-143,-144),(-137,-140,-143),(-138,-141,-145),(-139,-144,-145),(137,141,144),(137,142,145),(138,139,142),(138,140,144),(139,141,143),(140,143,145),(-130,-152,-160),(-146,-151,-153),(-146,-156,-157),(-147,-151,-153),(-147,-156,-157),(-148,-150,-154),(-148,-158,-159),(-149,-150,-159),(-149,-154,-155),(-152,-155,-158),(129,150,151),(129,152,153),(150,153,160),(151,152,154),(154,156,158),(155,156,159),(155,157,159),(157,158,160),(-161,-162,-193),(162,163,198),(162,164,198),(163,165,166),(164,165,166),(-165,-167,-168),(-166,-167,-168),(167,178,179),(167,180,181),(168,178,179),(168,180,181),(-163,-169,-170),(-163,-171,-172),(-164,-173,-174),(-164,-175,-176),(-169,-172,-175),(-170,-173,-177),(-171,-176,-177),(169,173,176),(169,174,177),(170,171,174),(170,172,176),(171,173,175),(172,175,177),(-162,-184,-192),(-178,-183,-185),(-178,-188,-189),(-179,-183,-185),(-179,-188,-189),(-180,-182,-186),(-180,-190,-191),(-181,-182,-191),(-181,-186,-187),(-184,-187,-190),(161,182,183),(161,184,185),(182,185,192),(183,184,186),(186,188,190),(187,188,191),(187,189,191),(189,190,192),(1,33,65),(-97,-129,-161),(5,37,69),(-101,-133,-165),(6,38,70),(-102,-134,-166),(14,46,78),(-110,-142,-174),(32,64,96),(-128,-160,-192)
)

checks = 0
def ck(x):
    global checks
    checks += 1
    assert x

def sat(F, bits):
    return all(any(bits[abs(x)-1] == (x > 0) for x in c) for c in F)

def syntax(F, n, monotone=False):
    ck(len(F) == len(set(F)))
    cnt = Counter()
    for c in F:
        ck(len(c) == 3 and len({abs(x) for x in c}) == 3)
        ck(all(1 <= abs(x) <= n for x in c))
        if monotone: ck(all(x > 0 for x in c) or all(x < 0 for x in c))
        cnt.update(c)
    for v in range(1, n+1):
        ck(cnt[v] == 2 and cnt[-v] == 2)
    return cnt

def hits(F, B):
    B = set(B)
    return all(any(abs(x) in B for x in c) for c in F)

def shift(F, off):
    return tuple(tuple((1 if x > 0 else -1)*(abs(x)+off) for x in c) for c in F)

def product_formula(F, n, p):
    return tuple(c for i in range(p) for c in shift(F, i*n))

def dimacs_bytes(F, n):
    return len((f'p cnf {n} {len(F)}\n' + ''.join(' '.join(map(str,c))+' 0\n' for c in F)).encode())

def dense_bits(n,m):
    return (2+4*n+4*m)*math.ceil(math.log2(64*(n+m+1)))

def incidence_connected(F, n):
    adj = {('v',v): set() for v in range(1,n+1)}
    for i,c in enumerate(F):
        q=('c',i); adj[q]=set()
        for x in c:
            v=('v',abs(x)); adj[q].add(v); adj[v].add(q)
    seen=set(); todo=deque([next(iter(adj))])
    while todo:
        z=todo.popleft()
        if z in seen: continue
        seen.add(z); todo.extend(adj[z]-seen)
    return len(seen)==len(adj)

def cyclic_U(p):
    F=[]
    for i in range(p):
        for j,c in enumerate(U):
            d=list((1 if x>0 else -1)*(abs(x)+198*i) for x in c)
            if j==1:
                ck(d == [194+198*i,196+198*i,197+198*i])
                d[0]=194+198*((i+1)%p)
            F.append(tuple(d))
    return tuple(F)

out={'run':'GLOBAL-BACKDOOR-PRODUCT162','status':'COMPUTATIONAL','cases':[]}

# W1: complete truth table and exact transversal number.
syntax(W1,15,False)
models=sum(sat(W1,b) for b in product((False,True), repeat=15))
ck(models==0)
mins=[]
for r in range(6):
    for B in combinations(range(1,16),r):
        if hits(W1,B): mins.append(B)
    if mins: break
ck(r==5 and mins==[(2,4,7,14,15)])
for p in (1,2,4,8,16,32,64):
    F=product_formula(W1,15,p)
    syntax(F,15*p,False)
    N=dense_bits(15*p,20*p)
    out['cases'].append({'family':'W1_disjoint','p':p,'n':15*p,'m':20*p,
        'dense_bits':N,'dimacs_bytes':dimacs_bytes(F,15*p),
        'tau_exact':5*p,'tau_over_log2N':5*p/math.log2(N)})

# U source syntax. Its UNSAT bit is a cited theorem dependency.
ck(len(U)==264)
syntax(U,198,True)
ck(incidence_connected(U,198))
ck(U[1]==(194,196,197))

# Connected, clause-monotone exact-(2,2) cyclic controls.
for p in (2,3,4,8,16,32):
    F=cyclic_U(p); n=198*p; m=264*p
    syntax(F,n,True)
    ck(incidence_connected(F,n))
    # Fully unpaired: no literalwise-complement clause is present.
    S=set(F)
    ck(all(tuple(-x for x in c) not in S for c in F))
    N=dense_bits(n,m)
    out['cases'].append({'family':'U_cyclic_monotone','p':p,'n':n,'m':m,
        'dense_bits':N,'connected':True,'global_hitting_lower_bound':m//4,
        'unsat_status':'PROVED from imported UNSAT(U) plus port-permutation lemma'})

# Ordinary connected bridge control keeps intact W1 cores but violates (2,2).
for p in (2,3,5,8):
    F=list(product_formula(W1,15,p))
    F += [(15*i+1,15*(i+1)+1,15*p+i+1) for i in range(p-1)]
    ck(incidence_connected(tuple(F),15*p+p-1))
    counts=Counter(x for c in F for x in c)
    ck(any(counts[v]!=2 or counts[-v]!=2 for v in range(1,15*p+p)))
    out['cases'].append({'family':'W1_connected_bridge_ordinary','p':p,
        'connected':True,'proper':all(len({abs(x) for x in c})==3 for c in F),
        'signed_exact22':False,'unsat_reason':'contains intact W1 copy'})

out['assertion_groups']=checks
out['limitations']=[
  'UNSAT(U) imported from Döcker; not recomputed',
  'finite execution checks syntax/arithmetic, not FLMV machine costs',
  'families refute global hitting-backdoor coverage only, not adaptive certificates or SAT runtime'
]
print(json.dumps(out,indent=2,sort_keys=True))
