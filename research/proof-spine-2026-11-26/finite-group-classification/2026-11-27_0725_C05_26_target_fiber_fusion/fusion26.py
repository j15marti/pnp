"""C05-26 target-conditioned nonexpansive joins; original source unchanged.
Every block stores attained syndrome -> (one original-ID witness, union of original IDs).
No inference from absence of a representative alone. Sequential variants.
"""
from owner25 import *
from time import perf_counter

def rows(T,n,c):
 F,t=factors_owner(T,n,c)
 return [((i,),{v:((e,),1<<e) for e,v in A.items()}) for i,A in enumerate(F)],t

def hull(F):
 a=0;D={}
 for I,A in F:
  b=min(A);a^=b
  for v in A:add_basis(D,v^b)
 return a,D

def width(F):
 return max((len(hull(F[:i])[1])+len(hull(F[i:])[1])-len(hull(F)[1]) for i in range(len(F)+1)),default=0)

def insert(A,v,w,ids):
 if v in A:A[v]=(A[v][0],A[v][1]|ids)
 else:A[v]=(w,ids)

def prune(F,t,M):
 # Explicit unary target-fiber closure, recomputed until fixed point.
 while True:
  changed=False
  for i,(I,A) in enumerate(F):
   b,D=hull(F[:i]+F[i+1:]);B={}
   for v,z in A.items():
    M['unary']+=1
    if not reduce(D,t^b^v):B[v]=z
   if not B:return None
   if len(B)<len(A):changed=True;F[i]=(I,B)
  if not changed:return F

def fuse(F,t,adjacent,M,keyed=False):
 while True:
  F=prune(F,t,M)
  if F is None:return None
  best=None
  for i,j in itertools.combinations(range(len(F)),2):
   if adjacent and j!=i+1:continue
   I,A=F[i];J,B=F[j];b,D=hull([R for k,R in enumerate(F) if k not in (i,j)])
   C={};M['pair_tests']+=1
   if keyed:
    L=defaultdict(list);R=defaultdict(list);goal=reduce(D,t^b)
    for v,z in A.items():L[reduce(D,v)].append((v,z));M['key_tests']=M.get('key_tests',0)+1
    for u,z in B.items():R[goal^reduce(D,u)].append((u,z));M['key_tests']=M.get('key_tests',0)+1
    for k in L.keys()&R.keys():
     for v,(w,ids) in L[k]:
      for u,(q,js) in R[k]:
       M['pair_products']+=1;insert(C,v^u,w+q,ids|js)
   else:
    for v,(w,ids) in A.items():
     for u,(q,js) in B.items():
      M['pair_products']+=1
      if not reduce(D,t^b^v^u):insert(C,v^u,w+q,ids|js)
   if not C:return None
   if len(C)>len(A)+len(B)-1:continue
   # preserve inherited order for adjacent lane; arbitrary lane explicitly charges reorder
   R=F[:i]+[(tuple(sorted(I+J)),C)]+F[i+1:j]+F[j+1:]
   score=(len(A)+len(B)-len(C),-width(R),-len(C),-i,-j)
   if best is None or score>best[0]:best=(score,R,I,J,C)
  if best is None:return F
  _,F,I,J,C=best
  M['trace'].append(dict(left=I,right=J,rows=len(C),total=sum(len(A) for _,A in F),width=width(F)))

def run(T,n,c,mode):
 F,t=rows(T,n,c);M=dict(unary=0,pair_tests=0,pair_products=0,trace=[],removed_ids=[],initial_width=width(F),initial_rows=sum(len(A) for _,A in F));original=0
 for _,A in F:
  for _,ids in A.values():original|=ids
 if mode in ('adjacent','all','hybrid','adj_hybrid','keyed_hybrid'):
  F=fuse(F,t,mode in ('adjacent','adj_hybrid'),M,keyed=mode=='keyed_hybrid')
 if F is None:return dict(M,status='NO',reason='empty target fiber',events=0,peak=0)
 live=0
 for _,A in F:
  for _,ids in A.values():live|=ids
 M['removed_ids']=[i for i in T if not live>>i&1];M['final_width']=width(F);M['final_rows']=sum(len(A) for _,A in F);M['blocks']=len(F)
 # Reclosure on original IDs; no native decisions based on lost representatives.
 if M['removed_ids']:
  C=close({i:v for i,v in T.items() if live>>i&1},n)
  if C is None:return dict(M,status='NO',reason='native reclosure',events=0,peak=0)
  M['reclosed_live']=len(C)
  # If native closure makes extra deductions, do not silently apply to compiled rows.
  # Rebuild is needed to use them; proceeding on weaker exact decision chart is sound.
 G,z=norm([{i:v for i,v in enumerate(A)} for _,A in F],t)
 if mode in ('hybrid','adj_hybrid','saturation','keyed_hybrid'):
  G,z,cert,tests,h=contract(G,z);M.update(saturation_rank=h,saturation_tests=tests)
 # Standalone fusion uses unfiltered trellis; baseline uses suffix.
 out=trellis(G,z,mode not in ('adjacent','all'),cap=20000,statecap=4096)
 return dict(M,**out)

def main():
 j=json.load(open('peer_source.json'));src={i:tuple(t) for i,t in enumerate(j['T'])};n=j['q'];fp=hashlib.sha256(json.dumps({k:j[k] for k in ('q','T','guard')},separators=(',',':')).encode()).hexdigest();assert fp=='f2f17606f508eb8644f36634a32291fbdc84a121043eb4b0f44c76b4c5d19aeb';assert nx.check_planarity(graph(src,n))[0] and len(set(src.values()))==len(src)
 T=close({i:t for i,t in src.items() if i not in j['guard']},n);assert sorted(T)==j['live_ids'];assert close(T,n)==T;assert ref(T,n)[0]==0
 out=[]
 for c in range(3):
  for mode in ('baseline','saturation','adjacent','all','adj_hybrid','hybrid','keyed_hybrid'):
   r=run(T,n,c,mode);assert r['status']!='POSSIBLE';out.append(dict(shore=c,mode=mode,**r));print(c,mode,r['status'],r['events'],r['peak'],r.get('final_rows'),r.get('final_width'),r['pair_products'],len(r['trace']),len(r['removed_ids']),flush=True)
 json.dump(dict(source_sha=fp,results=out),open('fusion26_results.json','w'),indent=2)
if __name__=='__main__':main()
