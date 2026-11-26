import json
import networkx as nx
import sympy as sp

U = [(0,0,0),(0,1,2),(0,1,0),(1,1,0),(1,1,1),(1,2,1),
     (1,2,3),(2,2,1),(2,3,2),(3,3,3),(3,3,2),(3,0,2)]
V = U + [(0,0,2)]
W = [(0,0,2),(0,0,0),(0,1,1),(0,1,0),(1,1,0),(1,2,3),
     (2,2,3),(2,2,1),(2,3,1),(3,3,2),(3,3,3),(3,0,0)]

def incidence(n, triples):
    g = nx.Graph()
    g.add_nodes_from((c, i) for c in range(3) for i in range(n))
    for j, t in enumerate(triples):
        for c, v in enumerate(t):
            g.add_edge(('t', j), (c, v))
    return g

def ring(n, bad=False):
    t = []
    for i in range(n):
        if i % 2 == 0:
            t.extend([(i,i,i),(i,i,i+1),(i,(i+1)%n,i+1),
                      (i,(i+1)%n,(i+2)%n)])
        else:
            t.extend([(i,i,(i if bad and i==1 else i+1)%n),
                      (i,(i+1)%n,(i+2 if bad and i==1 else i+1)%n)])
    return t

def pole(k):
    t = []
    for i in range(k):
        x, z = 2*i, i+2
        d = 0 if i==0 else 1 if i==1 else k+i
        t.extend([(x,x,0),(x,x,z),(x,x+1,1),(x,x+1,z),
                  (x+1,x,d),(x+1,x+1,d)])
    return t

counts = {'fixtures': 0, 'rings': 0, 'pole_sources': 0,
          'cofacial_gadgets': 0, 'exact_lp_identity_checks': 0}
for t in [U, V, W]:
    g = incidence(4,t)
    assert nx.check_planarity(g)[0] and nx.is_connected(g)
    counts['fixtures'] += 1
for n in [4,8,16,32,64,128,256]:
    for bad in [False,True]:
        g = incidence(n,ring(n,bad))
        assert nx.check_planarity(g)[0] and nx.is_connected(g)
        counts['rings'] += 1
for k in [3,5,8,16,32,64,128]:
    g = incidence(2*k,pole(k))
    assert nx.check_planarity(g)[0] and nx.is_connected(g)
    counts['pole_sources'] += 1
for d in [0,1,3]:
    t = [(0,0,0),(0,0,2),(0,1,1),(0,1,2),(1,0,d),(1,1,d)]
    g = incidence(4,t)
    g.add_edge((2,0),(2,1))
    assert nx.check_planarity(g)[0]
    counts['cofacial_gadgets'] += 1

# Exact LP diagnostic: U is already rejected by a single LP pin check.
a,b = sp.symbols('a b')
A = sp.Matrix([[int(t[c]==v) for t in U] for c in range(3) for v in range(4)])
x = sp.Matrix([1-b,1-a-2*b,a+3*b-1,1-a-2*b,a+b,-a,
               a+b,1-b,b,1-a-b,a,b])
assert A*x == sp.ones(12,1)
counts['exact_lp_identity_checks'] += 1
assert len(A.nullspace()) == 2
counts['exact_lp_identity_checks'] += 1
assert x[5] == -a and x[10] == a and x[8] == b
counts['exact_lp_identity_checks'] += 1
# Nonnegativity gives a=0, 1/3 <= b <= 1/2, so x[8] cannot be 0 or 1.
print(json.dumps({'counts':counts,'lp_pin_U':'infeasible at either Boolean value of triple index 8',
                  'networkx':nx.__version__,'sympy':sp.__version__}, indent=2))
