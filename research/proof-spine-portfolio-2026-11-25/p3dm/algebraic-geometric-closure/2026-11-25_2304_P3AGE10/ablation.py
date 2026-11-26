import json
from hybrid import *
a=json.load(open('medial96.json'));M=list(map(tuple,a['T']));h,hn=honey(2,2);out=[]
for sat in (False,True):
    T,n=splice([(V if sat else U,3),(h,hn),(M,a['n'])]);P=acquire_groups(T,n);index={frozenset(S):j for j,S in enumerate(P)};row={'m':len(T),'sat':sat,'modes':{}}
    for name,mode in [('mixed',lambda S:['geometry','boolean','algebra'][index[frozenset(S)]]),('only_geometry','geometry'),('only_algebra','algebra'),('only_boolean','boolean'),('no_geometry',('algebra','boolean')),('no_algebra',('geometry','boolean')),('no_boolean',('geometry','algebra'))]:
        r=seam_solver(T,n,P,mode=mode);row['modes'][name]={k:v for k,v in r.items() if k!='witness'};assert r['status'] in ('UNKNOWN','YES' if sat else 'NO');print(len(T),name,r['status'],flush=True)
    out.append(row)
json.dump(out,open('ablation_results.json','w'),indent=2)
