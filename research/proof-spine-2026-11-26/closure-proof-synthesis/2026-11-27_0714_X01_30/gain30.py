from lazy30 import *
from syndrome26 import owners

def main():
 a=auth();r=ref();base=[local((i,)) for i in range(len(owners))]; C=[]; calls=0; baseB=[basis(sorted(b['S'])) for b in base]; n=len(base); intersections={}
 for i in range(n):
  for j in range(n):intersections[i,j]=basis(sorted(set(base[i]['S'])&set(base[j]['S'])))
 for i,j in it.combinations(range(n),2):
  U=baseB[i]+baseB[j];d=rank(U);o=len(baseB[i])+len(baseB[j])-d
  if d>8 or o<=0:continue
  gains=[]
  for k in range(n):
   g=d+len(baseB[k])-rank(U+baseB[k])-rank(intersections[i,k]+intersections[j,k]);calls+=2;assert g>=0;gains.append(g)
  C.append((-sum(gains),-o,d,i,j))
 C.sort();out=dict(auth=a,reference=r,rank_calls=calls,order=C,lanes={})
 for lane in ['gain_join','gain_hybrid']:
  B=list(base);ticks=0;pos=0;rows=[]
  for target in (0,20,40,60,80,100,140,180,220):
   for _,_,d,i,j in C[pos:target]:
    b,num=make_pair(base[i],base[j]);ticks+=len(base[i]['P'])+len(base[j]['P'])+num;B.append(b)
   pos=target; P=[b['P'] for b in B];ar=arc(B) if lane.endswith('hybrid') else None
   if ar and ar['status']=='NO':rows.append(dict(target=target,status='NO_ARC',ticks=ticks,arc=ar));break
   Q=ar['supports'] if ar else P; E,_,g=graph(B); M,b,tags=matrix(B,Q,E);res=solve(M,b);rec=dict(target=target,ticks=ticks,states=sum(map(len,P)),remaining=sum(map(len,Q)),graph=g,arc_ticks=ar['ticks'] if ar else 0,result=res);rows.append(rec);print(lane,target,res['status'],res['cols'],res['nnz'],ticks,flush=True)
   if res['status']=='NO':break
  out['lanes'][lane]=rows;json.dump(out,open('gain30.json','w'))
if __name__=='__main__':main()
