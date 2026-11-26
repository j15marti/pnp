function audit(){
 let checks=0; const ck=(v)=>{checks++;if(!v)throw Error("assertion "+checks)};
 const pc=x=>{let k=0;for(;x;x&=x-1)k++;return k};
 const high=x=>31-Math.clz32(x);
 function piv(vs){let p=[];for(let v of vs){while(v){let i=high(v);if(p[i])v^=p[i];else{p[i]=v;break}}}return p}
 const rank=vs=>piv(vs).filter(Boolean).length;
 function kernel(rows,n){const p=piv(rows), out=[];for(let j=0;j<n;j++)if(!p[j]){let x=1<<j;for(let i=0;i<p.length;i++)if(p[i]&&pc(p[i]&x)%2)x^=1<<i;out.push(x)}return out}
 const syndrome=(cols,x)=>cols.reduce((s,c,i)=>s^((x>>i&1)?c:0),0);
 const rowcols=(rows,n)=>Array.from({length:n},(_,i)=>rows.reduce((s,r,j)=>s|((r>>i&1)<<j),0));
 const all=(n)=>Array.from({length:n},(_,i)=>i);
 function minBrute(cols,b,weights,allowed=()=>true){let best=Infinity,mask=0;for(let x=0;x<2**cols.length;x++)if(allowed(x)&&syndrome(cols,x)===b){let w=weights.reduce((z,c,i)=>z+((x>>i&1)?c:0),0);if(w<best){best=w;mask=x}}return {cost:best,mask}}
 // This bounded audit uses exact recursive pairing, NOT a polynomial blossom implementation.
 function join(edges,V,target,weights){
  let dist=Array.from({length:V},(_,i)=>Array.from({length:V},(_,j)=>i===j?0:Infinity)),path=Array.from({length:V},()=>Array(V).fill(0));
  edges.forEach(([a,b],i)=>{if(a!==b&&weights[i]<dist[a][b]){dist[a][b]=dist[b][a]=weights[i];path[a][b]=path[b][a]=1<<i}});
  for(let k=0;k<V;k++)for(let i=0;i<V;i++)for(let j=0;j<V;j++)if(dist[i][k]+dist[k][j]<dist[i][j]){dist[i][j]=dist[i][k]+dist[k][j];path[i][j]=path[i][k]^path[k][j]}
  const memo=new Map([[0,{cost:0,mask:0}]]);
  function go(t){if(memo.has(t))return memo.get(t);let i=high(t),rest=t^(1<<i),best={cost:Infinity,mask:0};for(let j=0;j<V;j++)if(rest>>j&1){let z=go(rest^(1<<j)),cost=z.cost+dist[i][j];if(cost<best.cost)best={cost,mask:z.mask^path[i][j]}}memo.set(t,best);return best}
  let a=go(target);if(Number.isFinite(a.cost)){ck(syndrome(edges.map(([u,v])=>(1<<u)^(1<<v)),a.mask)===target);ck(weights.reduce((z,w,i)=>z+((a.mask>>i&1)?w:0),0)===a.cost)}return a
 }
 function trans(cols,edges){let p=[],q=[];for(let j=0;j<cols.length;j++){let a=cols[j],b=(1<<edges[j][0])^(1<<edges[j][1]);while(a){let i=high(a);if(p[i]){a^=p[i];b^=q[i]}else{p[i]=a;q[i]=b;break}}if(!a)ck(!b)}ck(rank(cols)===rank(edges.map(([u,v])=>(1<<u)^(1<<v))));return s=>{let t=0;while(s){let i=high(s);if(!p[i])return null;s^=p[i];t^=q[i]}return t}}
 function solve(cols,b,weights,R,E,edges,V,allowedException=()=>true){
  let map=trans(R.map(i=>cols[i]),edges), dp=new Map([[0,{cost:0,mask:0}]]);
  // If pins on exceptions exist, handle via restriction of the permitted bit at each transition.
  for(let j of E){let nd=new Map();for(let [s,v] of dp)for(let bit of [0,1])if(allowedException(j,bit)){let t=s^(bit?cols[j]:0),cost=v.cost+bit*weights[j];if(!nd.has(t)||nd.get(t).cost>cost)nd.set(t,{cost,mask:v.mask|(bit<<j)})}dp=nd}
  ck(dp.size<=2**rank(E.map(i=>cols[i])));
  let best={cost:Infinity,mask:0,states:dp.size};
  for(let [s,v] of dp){let t=map(b^s);if(t===null)continue;let w=join(edges,V,t,R.map(i=>weights[i]));if(v.cost+w.cost<best.cost){let mask=v.mask;R.forEach((j,i)=>{if(w.mask>>i&1)mask|=1<<j});best={cost:v.cost+w.cost,mask,states:dp.size}}}
  if(Number.isFinite(best.cost)){ck(syndrome(cols,best.mask)===b);ck(weights.reduce((z,w,i)=>z+((best.mask>>i&1)?w:0),0)===best.cost)}return best
 }
 let seed=6112604;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 let cases=0, infeasible=0,maxStates=0;
 for(let k=0;k<180;k++){
  let V=3+rnd(5),m=3+rnd(6),e=1+rnd(5),edges=all(m).map(()=>[rnd(V),rnd(V)]),R=all(m),E=all(e).map(j=>j+m),weights=all(m+e).map(()=>rnd(6)),gcols=edges.map(([u,v])=>(1<<u)^(1<<v)),ex=all(e).map(()=>rnd(1<<V)),cols=gcols.concat(ex),b=rnd(1<<V);
  let ans=solve(cols,b,weights,R,E,edges,V),ref=minBrute(cols,b,weights);ck(ans.cost===ref.cost);cases++;infeasible+=!Number.isFinite(ans.cost);maxStates=Math.max(maxStates,ans.states)
 }
 const F=[[3,8,13],[1,5,17],[0,16,17],[6,8,13],[1,5,9],[2,11,13],[3,8,10],[0,7,12],[2,7,12],[5,9,16],[4,6,11],[2,3,7],[4,11,12],[10,14,15],[10,14,16],[9,14,15],[4,6,15],[0,1,17]];
 const rot=[[25,20,35],[19,22,35],[23,29,26],[18,24,29],[30,34,28],[22,19,27],[34,21,28],[26,29,25],[24,18,21],[33,22,27],[32,24,31],[28,23,30],[30,26,25],[21,18,23],[31,33,32],[33,31,34],[27,20,32],[20,19,35],[3,13,8],[17,5,1],[0,16,17],[8,13,6],[1,5,9],[13,2,11],[3,8,10],[7,0,12],[2,7,12],[5,16,9],[6,11,4],[7,2,3],[11,12,4],[10,15,14],[16,10,14],[14,15,9],[15,6,4],[1,0,17]];
 let seen=new Set(),faces=0;for(let i=0;i<36;i++){ck(rot[i].length===3);for(let j of rot[i]){ck(rot[j].includes(i));ck(i<18?F[j-18].includes(i):F[i-18].includes(j));if(!seen.has(i+","+j)){faces++;let a=i,b=j;do{ck(!seen.has(a+","+b));seen.add(a+","+b);let c=rot[b][(rot[b].indexOf(a)+1)%3];a=b;b=c}while(a!==i||b!==j)}}}
 let connected=new Set([0]),todo=[0];while(todo.length){for(let v of rot[todo.pop()])if(!connected.has(v)){connected.add(v);todo.push(v)}}ck(connected.size===36);ck(36-54+faces===2);ck(seen.size===108);
 let rows=F.map(r=>r.reduce((s,j)=>s|(1<<j),0)),K=kernel(rows,18),C=rowcols(rows,18);ck(K.length===3);for(let z of K)ck(syndrome(C,z)===0);
 let dc=rowcols(K,18);ck(new Set(dc).size===7&&dc.every(Boolean));
 let labels=[];for(let z=0;z<8;z++){let x=((1<<18)-1)^syndrome(K,z),bad=F.filter(r=>r.every(i=>x>>i&1)).length;ck(syndrome(C,x)===(1<<18)-1);ck(3*pc(x)===18+2*bad);labels.push({phase:z,weight:pc(x),defects:bad,mask:x})}
 let E=[12],R=all(18).filter(i=>i!==12),small=kernel(rows.concat([1<<12]),18);ck(small.length===2);let groups=[[],[],[],[]];R.forEach(i=>groups[small.reduce((s,v,j)=>s|((v>>i&1)<<j),0)].push(i));ck(groups.slice(1).every(g=>g.length>0));
 let mapedge=new Map(),V=2;for(let type of [1,2,3]){let prev=0;groups[type].forEach((j,i)=>{let next=i===groups[type].length-1?1:V++;mapedge.set(j,[prev,next]);prev=next})}for(let j of groups[0])mapedge.set(j,[0,V++]);
 let ed=R.map(j=>mapedge.get(j)),native=[];
 for(let pin of [null,0,1]){let allowed=(j,b)=>pin===null||b===pin;let ans=solve(C,(1<<18)-1,Array(18).fill(1),R,E,ed,V,allowed),ref=minBrute(C,(1<<18)-1,Array(18).fill(1),x=>pin===null||(x>>12&1)===pin);ck(ans.cost===ref.cost);ck(ans.cost>=6);if(ans.cost===6)ck(F.every(r=>r.reduce((s,j)=>s+(ans.mask>>j&1),0)===1));native.push({pin,cost:ans.cost,mask:ans.mask,satisfiable:ans.cost===6,states:ans.states})}
 // Repeated exceptions: count 10, rank 1, two DP states.
 let many=solve([3,6,3,3,3,3,3,3,3,3,3,3],5,Array(12).fill(1),[0,1],all(10).map(j=>j+2),[[0,1],[1,2]],3);ck(many.states===2&&many.cost===2);
 return {assertions:checks,random_cases:cases,infeasible,maxStates,native:{rows:F,rotation:rot,faces,kernel:K,dualColumns:dc,labels,exception:E,remaining:R,graph:ed,vertices:V,decisions:native},manyExceptions:many};
}
console.log(JSON.stringify(audit(),null,2));
