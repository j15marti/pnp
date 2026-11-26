import audit as a
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
import json
s=a.Solver(1,1);fs=s.fs[1];co=s.fs[0];vs=sorted({v for f in fs for v in f});ix={v:i for i,v in enumerate(vs)}
e,(p,q)=next(iter(s.ed[0].items())); groups=[]
for p0 in (p,q):
    i=a.edges(co[p0]).index(e)
    groups.append([s.maps[1][p0][j] for j,t in enumerate(a.T) if any(v.count(0)==1 and v[i]==0 for v in t)])
mat=lil_matrix((len(vs)+2,len(fs)),dtype=float)
for j,f in enumerate(fs):
    for v in f:mat[ix[v],j]=1
for i,gg in enumerate(groups):mat[len(vs)+i,gg]=1
lower=np.ones(len(vs)+2);upper=lower.copy();upper[-2:]=np.inf
z=milp(np.zeros(len(fs)),integrality=np.ones(len(fs)),bounds=Bounds(0,1),constraints=LinearConstraint(mat.tocsr(),lower,upper),options={'time_limit':20})
print('milp status',z.status,z.message,flush=True)
if z.x is not None:
    w={j for j,v in enumerate(z.x) if v>.5};g=tuple((min(w&set(gg)),1) for gg in groups);a.verify(fs,w,g);assert a.closure(fs,g) is not None;assert s.solve(1,g) is None
    d={'guards':g,'native_witness':sorted(w),'patches':[p,q],'edge':e,'cone':s.cone(g),'stats':s.stats(),'milp_status':int(z.status)}
    print({k:v for k,v in d.items() if k!='native_witness'});path='/mnt/data/C02_03/results.json';R=json.load(open(path));R['native_sat_template_no']=d;json.dump(R,open(path,'w'),indent=2)
