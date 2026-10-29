"""Independent MILP full-CNF SAT/UNSAT controls for a signed-token permutation family."""
import importlib.util,json, numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
path='/mnt/data/pnp_run_20261029_0656/2026-10-29_0656_LSPV-3_PORT_QUANTIFIER_CLOSURE161_repro.py'
spec=importlib.util.spec_from_file_location('lib161',path);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
controls=[('SAT',[(1,0),(0,0),(0,1),(0,1), (0,0),(1,0),(1,1),(1,1)]),
          ('UNSAT',[(0,1),(0,0),(1,1),(1,1), (0,0),(0,1),(1,0),(1,0)])]
results=[]
for label,tokens in controls:
    cnf=p.full_permutation_formula(p.base(),tokens,2)
    n=30;mat=lil_matrix((len(cnf),n));low=np.zeros(len(cnf))
    for j,cl in enumerate(cnf):
        neg=0
        for lit in cl:
            mat[j,abs(lit)-1]+=1 if lit>0 else -1
            neg+=(lit<0)
        low[j]=1-neg
    res=milp(c=np.zeros(n),integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.ones(n)),constraints=LinearConstraint(mat.tocsr(),low,np.inf))
    is_sat=res.status==0
    assert is_sat==(label=='SAT'),res.message
    if is_sat:
        x=np.rint(res.x).astype(int)
        assert all(any(x[abs(lit)-1]==(lit>0) for lit in c) for c in cnf)
    results.append({'label':label,'sat':is_sat,'status':int(res.status),'message':res.message})
print(json.dumps({'independent_full_cnf_milp':results},sort_keys=True,indent=2))
