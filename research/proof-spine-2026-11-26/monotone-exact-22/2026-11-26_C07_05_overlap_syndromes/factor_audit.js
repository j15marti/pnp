console.log(JSON.stringify((function factorAudit(){
 const bit=i=>1n<<BigInt(i),high=x=>x.toString(2).length-1,par=x=>{let r=0;while(x){x&=x-1n;r^=1}return r},assert=(x,m="assertion")=>{if(!x)throw Error(m)};
 class B{constructor(){this.M=new Map()} reduce(v,t=0n){for(let p of [...this.M.keys()].sort((a,b)=>b-a))if(v&bit(p)){let [w,z]=this.M.get(p);v^=w;t^=z}return[v,t]} add(v,t=0n){let[w,z]=this.reduce(v,t);if(w===0n)return[false,z];this.M.set(high(w),[w,z]);return[true,0n]} solve(){let x=0n;for(let p of [...this.M.keys()].sort((a,b)=>a-b)){let[w,t]=this.M.get(p);if(par(w&x)!==Number(t))x|=bit(p)}return x}}
 const valid=(F,x)=>F.every(C=>C.reduce((s,i)=>s+Number(Boolean(x&bit(i))),0)===2);
 function factor(n,F){
  let A=new B();F.forEach(C=>A.add(C.reduce((s,i)=>s^bit(i),0n)));
  let P=F.map(C=>[A.reduce(bit(C[0])^bit(C[1]))[0],A.reduce(bit(C[0])^bit(C[2]))[0]]);
  if(P.some(([u,v])=>!u||!v||u===v))return{status:"UNKNOWN",reason:"rank closure not implemented in this supplemental audit"};
  const m=P.length,flat=P.flat(),D=new B(),dep=[],parent=Array.from({length:2*m},(_,i)=>i);
  function find(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i]}return i}
  function union(i,j){parent[find(i)]=find(j)}
  for(let i=0;i<flat.length;i++){const[ok,z]=D.add(flat[i],bit(i));if(!ok){dep.push(z);for(let j=0;j<flat.length;j++)if(z&bit(j))union(i,j)}}
  for(let i=0;i<m;i++)union(2*i,2*i+1);
  const groups=new Map();for(let i=0;i<m;i++){let p=find(2*i);if(!groups.has(p))groups.set(p,[]);groups.get(p).push(i)}
  let sizes=[...groups.values()].map(G=>G.length),groupDelta=[];
  for(const G of groups.values()){let C=new B();G.forEach(i=>P[i].forEach(v=>C.add(v)));groupDelta.push(2*G.length-C.M.size)}
  assert(groupDelta.reduce((a,b)=>a+b,0)===dep.length,"non-direct sum");
  let info={variables:n,clauses:m,components:groups.size,maxComponent:Math.max(...sizes),globalDependency:dep.length,maxComponentDependency:Math.max(...groupDelta)};
  if(info.maxComponent>8)return{status:"UNKNOWN",...info};
  let tested=0;
  for(const G of groups.values()){
   let h=2*G.length,found=null;
   // Small local exact table search, independent of global source assignment.
   let localDeps=dep.filter(z=>G.some(i=>Boolean(z&(3n<<BigInt(2*i)))));
   for(let w=0;w<3**G.length;w++){
    tested++;let q=w,z=0n;
    for(const i of G){z|=BigInt(q%3+1)<<BigInt(2*i);q=Math.floor(q/3)}
    if(localDeps.every(d=>par(d&z)===0)){found=z;break}
   }
   if(found===null)return{status:"NO",...info,tested};
   for(const i of G)for(let j=0;j<2;j++){let [ok,z]=A.add(P[i][j],BigInt(Boolean(found&bit(2*i+j))));assert(ok||!z)}
  }
  let x=A.solve();assert(valid(F,x),"global witness");return{status:"YES",...info,tested}
 }
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function make(k,bad){let G=[],n=1;for(let q=0;q<k;q++){let U=q===k-1&&bad?fano:fano.slice(1);G.push(...U.map(C=>C.map(i=>i===0?0:n+i-1)));n+=6}return[n+G.length,G.map((C,i)=>C.concat(n+i))]}
 let data=[];for(const k of [1,2,4,8,16,32])for(const bad of [false,true]){let[n,F]=make(k,bad),r=factor(n,F);assert(r.status===(bad?"NO":"YES"));assert(r.components===k&&r.maxComponentDependency===(bad?8:6));data.push({modules:k,...r})}
 // Anchored grid: many raw dependencies, one inseparable component, but a common-coordinate chart.
 let grid=[];for(const k of [4,8,16]){let G=[],n=k*k+1;for(let i=0;i<k;i++)for(let j=0;j<k;j++){let u=1+i*k+j;if(i+1<k)G.push([0,u,u+k]);if(j+1<k)G.push([0,u,u+1])}let F=G.map((C,i)=>C.concat(n+i)),r=factor(n+G.length,F);assert(r.components===1);let x=0n;for(let i=1;i<n;i++)x|=bit(i);assert(valid(F,x));grid.push({side:k,...r,alignedWitnessVerified:true})}
 return{data,grid};
})(),null,2));
