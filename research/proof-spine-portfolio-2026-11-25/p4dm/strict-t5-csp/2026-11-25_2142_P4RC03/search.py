from ring import *
if __name__=='__main__':
 rng=random.Random(803);out=[];unknown=[];T,_,_=ring(5);accepted=0
 for i in range(10000):
  j,k=rng.sample(range(len(T)),2);S=swap(T,j,k,rng.randrange(4))
  if S==T or len(set(S))!=len(S) or not nx.check_planarity(graph(S))[0]:continue
  T=S;accepted+=1
  if accepted%2:continue
  result,stats,witness=solve(T,weighted=False,cap=0);truth=ref(T,{}) is not None;assert result=='UNKNOWN' or (result=='YES')==truth
  if result=='UNKNOWN':
   entry=dict(iteration=i,source=T,truth=truth,**stats);unknown.append(entry);print('UNKNOWN',entry,flush=True);break
  out.append(dict(iteration=i,truth=truth,result=result,**stats))
 print('accepted',accepted,'samples',len(out),'unknown',len(unknown),flush=True)
 json.dump(dict(accepted=accepted,trial=i,results=out,unknown=unknown),open('search_results.json','w'),indent=2)
