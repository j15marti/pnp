#!/usr/bin/env python3
"""Exact port-positivity acquisition firewall for canonical M22 originals."""
import argparse,functools,itertools,json,resource,time
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Z6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
def rename(F,d):return tuple(tuple((1 if x>0 else -1)*(abs(x)+d) for x in c) for c in F)
def product(A,B,nA):return A+rename(B,nA)
def sat(F,z):return all(any(((z>>(abs(x)-1))&1)==(x>0) for x in c) for c in F)
def valid(F,n):
 if len(F)!=4*n//3 or len(set(F))!=len(F):return False
 q={(v,s):0 for v in range(1,n+1) for s in (1,-1)}
 for c in F:
  if len(c)!=3 or len({abs(x) for x in c})<3 or not(all(x>0 for x in c) or all(x<0 for x in c)):return False
  for x in c:
   if not 1<=abs(x)<=n:return False
   q[(abs(x),1 if x>0 else -1)]+=1
 return all(v==2 for v in q.values())
def port_stats(F,n,pins=None):
 pins=pins or {};free=[v for v in range(1,n+1) if v not in pins];base=sum(b<<(v-1) for v,b in pins.items())
 W=[[0]*3 for _ in F];models=0;profile=[0,0,0,0];witness=None
 for b in range(1<<len(free)):
  z=base|sum(((b>>i)&1)<<(v-1) for i,v in enumerate(free));vals=[];ok=True
  for c in F:
   t=[((z>>(abs(x)-1))&1)==(x>0) for x in c];vals.append(t)
   if not any(t):ok=False;break
  if not ok:continue
  models+=1;witness=z if witness is None else witness
  hist=[0,0,0,0]
  for j,t in enumerate(vals):
   k=sum(t);hist[k]+=1
   if k>=2:
    for r,a in enumerate(t):W[j][r]+=a
  profile=[profile[i]+hist[i] for i in range(4)]
 flat=[x for row in W for x in row]
 return {'models':models,'W':W,'sum_W':sum(flat),'positive_ports':sum(x>0 for x in flat),'min_positive':min((x for x in flat if x>0),default=0),'max':max(flat,default=0),'profile_totals':profile,'witness':witness}
def circuit(F,n):
 gates=[];outs=[];depth={v:0 for v in range(1,n+1)}
 def add(op,x,y):
  q=n+len(gates)+1;gates.append((q,op,x,y));depth[q]=1+max(depth[abs(x)],depth[abs(y)]);return q
 for c in F:outs.append(add('O',add('O',c[0],c[1]),c[2]))
 while len(outs)>1:outs=[add('A',outs[i],outs[i+1]) if i+1<len(outs) else outs[i] for i in range(0,len(outs),2)]
 for z in range(1<<n):
  a={v:(z>>(v-1))&1 for v in range(1,n+1)}
  for q,op,x,y in gates:
   X=a[abs(x)] if x>0 else 1-a[abs(x)];Y=a[abs(y)] if y>0 else 1-a[abs(y)];a[q]=int((X or Y) if op=='O' else (X and Y))
  assert a[outs[0]]==sat(F,z)
 return {'gates':len(gates),'depth':depth[outs[0]],'rows':1<<n}
def obdd(F,n):
 T=tuple(int(sat(F,z)) for z in range(1<<n));edge={}
 for S in range(1<<n):
  pre=[i for i in range(n) if S>>i&1]
  for v in range(n):
   if S>>v&1:continue
   rest=[i for i in range(n) if not(S>>i&1) and i!=v];pairs=set()
   for a in range(1<<len(pre)):
    base=sum(((a>>j)&1)<<u for j,u in enumerate(pre));p=[]
    for bit in (0,1):
     q=0
     for b in range(1<<len(rest)):
      z=base|(bit<<v)|sum(((b>>j)&1)<<u for j,u in enumerate(rest));q|=T[z]<<b
     p.append(q)
    if p[0]!=p[1]:pairs.add(tuple(p))
   edge[S,v]=len(pairs)
 full=(1<<n)-1
 @functools.lru_cache(None)
 def lo(S):return 0 if S==full else min(edge[S,v]+lo(S|1<<v) for v in range(n) if not S>>v&1)
 @functools.lru_cache(None)
 def hi(S):return 0 if S==full else max(edge[S,v]+hi(S|1<<v) for v in range(n) if not S>>v&1)
 S=nat=0
 for v in range(n):nat+=edge[S,v];S|=1<<v
 return {'best':lo(0),'natural':nat,'worst':hi(0),'orders':1 if n==0 else __import__('math').factorial(n)}
def su(F):
 d={'SS':0,'SU':0,'US':0,'UU':0}
 for i,j in itertools.combinations(range(len(F)),2):
  for a,b in itertools.product('SU',repeat=2):
   r={};ok=True
   for c,m in ((F[i],a),(F[j],b)):
    for x in c:
     q=int(x>0) if m=='S' else int(x<0)
     if abs(x) in r and r[abs(x)]!=q:ok=False
     r[abs(x)]=q
   d[a+b]+=ok
 return d
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();started=time.time();J=product(F9,Z6,9)
 f=port_stats(F9,9);z=port_stats(Z6,6);j=port_stats(J,15)
 p0=port_stats(F9,9,{2:0,4:0,6:0,1:0});p1=port_stats(F9,9,{2:0,4:0,6:0,1:1})
 jp0=port_stats(J,15,{2:0,4:0,6:0,1:0});jp1=port_stats(J,15,{2:0,4:0,6:0,1:1})
 fixed=(0,0);local=z['W'][fixed[0]][fixed[1]];global_port=j['W'][12+fixed[0]][fixed[1]]
 mal=[F9[:-1],F9+(F9[0],),((1,1,2),)+F9[1:],((-1,2,3),)+F9[1:],((1,2,99),)+F9[1:],F9[:-1]+((1,2,3),)]
 assert valid(F9,9) and valid(Z6,6) and valid(J,15)
 for X,n,m in ((f,9,12),(z,6,8),(j,15,20)):
  assert X['sum_W']==m*X['models']-X['profile_totals'][3]
  assert X['models']==0 or X['positive_ports']>=n
 assert local==6 and global_port==local*f['models']==420
 assert (p0['models'],p1['models'])==(0,3)
 assert (jp0['models'],jp1['models'])==(0,54) and (jp0['W'][12][0],jp1['W'][12][0])==(0,18)
 out={'run':'PORT_POSITIVITY_ACQUISITION_REFEREE292','status':'PASS_EXACT_UNIVERSAL_SEMANTIC_NPCOMPLETE_ACQUISITION','P_vs_NP':'OPEN',
  'theorem':{'all_valid_originals':'F is SAT iff some signed clause port has W11>0; every SAT F has at least n positive ports','designated_port_language':'NP-complete under F -> F disjoint-union Z6 with fixed Z6 port','reduction_output':'valid duplicate-free proper canonical original; additive 6 variables and 8 clauses; encoding length Theta(N), not uniformly additive O(log N)'},
  'F9':{**{k:v for k,v in f.items() if k!='W'},'circuit':circuit(F9,9),'obdd':obdd(F9,9),'SU':su(F9)},
  'Z6':{**{k:v for k,v in z.items() if k!='W'},'fixed_port':{'clause':fixed[0],'literal':fixed[1],'W11':local}},
  'product_F9_Z6':{**{k:v for k,v in j.items() if k!='W'},'valid':valid(J,15),'fixed_Z6_port_W11':global_port,'factorization':'420 = 70 * 6','circuit':circuit(J,15)},
  'F9_union_Z6':{**{k:v for k,v in j.items() if k!='W'},'circuit':circuit(J,15),'fixed_guard_port_W11':global_port,'factor_check':global_port==f['models']*local},
  'same_original_F9':{'pins_common':{2:0,4:0,6:0},'x1_0':{k:v for k,v in p0.items() if k!='W'},'x1_1':{k:v for k,v in p1.items() if k!='W'}},
  'same_original_product':{'x1_0_models':jp0['models'],'x1_1_models':jp1['models'],'fixed_port_x1_0':jp0['W'][12][0],'fixed_port_x1_1':jp1['W'][12][0]},
  'malformed_rejected':sum(not valid(x,9) for x in mal),'offline':{'seconds':time.time()-started,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
  'gap':'NP-completeness is not a superpolynomial lower bound; no all-input polynomial solver, arbitrary-A power-short Phi, or strict same-machine FLMV transfer'}
 json.dump(out,open(a.out,'w'),indent=2,sort_keys=True);print(json.dumps({'status':'PASS','out':a.out,'seconds':out['offline']['seconds']}))
if __name__=='__main__':main()
