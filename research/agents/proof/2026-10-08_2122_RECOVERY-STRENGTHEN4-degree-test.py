"""Exhaustive odd-field affine degree audit. Standalone, deterministic, <=25s."""
import hashlib, itertools, json, signal, time
from pathlib import Path
signal.alarm(25)
start = time.monotonic()
P = 3

def add(a, b):
    c = a.copy()
    for e, v in b.items():
        c[e] = (c.get(e, 0) + v) % P
    return {e: v for e, v in c.items() if v}

def mul(a, b):
    c = {}
    for e, v in a.items():
        for f, w in b.items():
            g = tuple(x+y for x, y in zip(e,f))
            c[g] = (c.get(g,0)+v*w) % P
    return {e: v for e, v in c.items() if v}

def compose(f, A, b):
    forms = [{(0,0):b[i],(1,0):A[2*i],(0,1):A[2*i+1]} for i in range(2)]
    out = {}
    for e,v in f.items():
        term = {(0,0):v}
        for i,n in enumerate(e):
            for _ in range(n):
                term = mul(term,forms[i])
        out = add(out,term)
    return out

def mm(a,b):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%P for i in range(2) for j in range(2))

def order(a):
    c=(1,0,0,1)
    for k in range(1,49):
        c=mm(c,a)
        if c==(1,0,0,1): return k
    raise AssertionError('order exceeds GL2 size')

matrices=[a for a in itertools.product(range(P),repeat=4) if (a[0]*a[3]-a[1]*a[2])%P]
exps=list(itertools.product(range(2),repeat=2))
counts={'affine_polynomial_pairs':0,'translation_degree_budget_checks':0}
classified=[]
for a in matrices:
    mono=all(sum(a[2*i+j]!=0 for i in range(2))==1 for j in range(2))
    preserves=True
    for b in itertools.product(range(P),repeat=2):
        for coeffs in itertools.product(range(P),repeat=4):
            f={e:c for e,c in zip(exps,coeffs) if c}
            g=compose(f,a,b)
            counts['affine_polynomial_pairs']+=1
            if any(max(e)>1 for e in g): preserves=False
            delta=[max((e[i] for e in f),default=0) for i in range(2)]
            budget=[sum(delta[i] for i in range(2) if a[2*i+j]) for j in range(2)]
            assert all(e[j]<=budget[j] for e in g for j in range(2))
            assert all(sum(e)<=max((sum(x) for x in f),default=0) for e in g)
            counts['translation_degree_budget_checks']+=1
    assert preserves==mono
    classified.append({'matrix':a,'order':order(a),'monomial':mono,'preserves_all_multilinear':preserves})

# Exact smallest odd-field, two-variable counterexample, including function values.
shear=(1,1,0,1)
g=compose({(1,1):1},shear,(0,0))
assert g=={(1,1):1,(0,2):1}
target=[(u*v+v*v)%P for u,v in itertools.product(range(P),repeat=2)]
for cs in itertools.product(range(P),repeat=4):
    vals=[sum(c*u**e[0]*v**e[1] for e,c in zip(exps,cs))%P for u,v in itertools.product(range(P),repeat=2)]
    assert vals!=target

# Repeated shears cancel at depth 3: exact fused budget recovers degree 1,1.
a=(1,0,0,1)
for _ in range(3): a=mm(a,shear)
assert a==(1,0,0,1)
assert compose({(1,1):1},a,(0,0))=={(1,1):1}
out={'status':'COMPUTATIONAL','base_commit':'5dc4147396c3969887b231a8d372c00ace23d58f','field':P,'seed':None,'exhaustive':True,'counts':counts,'GL2_matrices':len(matrices),'monomial_matrices':sum(x['monomial'] for x in classified),'full_order_matrices':sum(x['order']==8 for x in classified),'max_monomial_order':max(x['order'] for x in classified if x['monomial']),'classification':classified,'counterexample':{'F':'xy','A':shear,'composite':'uv+v^2','not_functionally_multilinear':True},'three_shear_fusion':'identity','seconds':time.monotonic()-start,'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':'Exhaustive tiny-field algebra, not extractor entropy or all-input SAT resource test.'}
print(json.dumps(out,indent=2))
