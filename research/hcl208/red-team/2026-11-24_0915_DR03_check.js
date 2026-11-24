"use strict";
function main(){
 const out={seed:3270915,abstractTests:0,abstractAligned:0,abstractOracleNodes:0,graphCases:0,rootSAT:0,rootUNSAT:0,guardCases:0,consistentGuards:0,closureRejected:0,guardSAT:0,guardUNSAT:0,aligned:0,alignedSAT:0,alignedUNSAT:0,sourceAssignments:0,closureScans:0,rankReductions:0,removed:0,fvsCertificates:0,parityEquations:0,discrepancies:0,benchmarks:[]};
 let seed=out.seed; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
 const fail=(s)=>{throw Error(s)};
 function parity(x){let p=0;while(x){p^=1;x&=x-1}return p;}
 function reduce(rows,v,b=0){out.rankReductions++;for(const [a,c] of rows){const k=31-Math.clz32(a);if(v&(1<<k)){v^=a;b^=c}}return [v,b]}
 function add(rows,v,b=0){[v,b]=reduce(rows,v,b);if(!v)return !b;rows.push([v,b]);rows.sort((a,b)=>b[0]-a[0]);return true}
 function rank(v){const b=[];for(const x of v)add(b,x);return b.length}
 function plane(a,b){return [a,b,a^b].sort((x,y)=>x-y)}
 function alignment(ps){
  const uniq=[...new Map(ps.map(p=>[p.join(","),p])).values()];const cnt=new Map();
  for(const p of uniq)for(const v of p)cnt.set(v,(cnt.get(v)||0)+1);
  const B=new Set();
  for(const p of uniq){const f=p.filter(v=>cnt.get(v)>1);if(f.length>2)return null;for(const v of p)if(f.length<2&&!f.includes(v))f.push(v);for(const v of f)B.add(v)}
  return rank(B)===B.size?[...B]:null;
 }
 function bruteAlign(ps,i=0,B=new Set()){
  out.abstractOracleNodes++;
  if(i===ps.length)return true;
  for(let j=0;j<3;j++){const next=new Set(B);for(let k=0;k<3;k++)if(k!==j)next.add(ps[i][k]);if(rank(next)===next.size&&bruteAlign(ps,i+1,next))return true}
  return false
 }
 for(let i=0;i<800;i++){
  const d=2+rnd(5),m=1+rnd(7),ps=[];for(let j=0;j<m;j++){let a=1+rnd((1<<d)-1),b;do{b=1+rnd((1<<d)-1)}while(a===b);ps.push(plane(a,b))}
  const a=!!alignment(ps),b=bruteAlign(ps);out.abstractTests++;out.abstractAligned+=+a;if(a!==b)fail("recognizer");
 }
 function forest(n,edges){const p=Array.from({length:n},(_,i)=>i);function root(a){while(p[a]!==a)a=p[a];return a}const T=[];for(const e of edges){let u=root(e[0]),v=root(e[1]);if(u!==v){p[u]=v;T.push(e)}}return {T,root}}
 function coverRemoved(n,edges){const {root}=forest(n,edges),S=[];for(let i=0;i<n;i++)if(root(i)!==i)S.push(i);return S}
 function norm(n,edges,G){
  let L=[];for(const [a,b] of G)if(!add(L,a,b))return null;
  const r=L.length;let E=edges.slice(),D=[];let changed=true;
  while(changed){changed=false;out.closureScans++;for(let i=0;i<E.length;i++){
    const [u,v,q]=E[i],a=(1<<u)^(1<<v),b=a<<n,pa=reduce(L,a)[0],pb=reduce(L,b)[0];
    if(pa&&pb&&pa!==pb)continue;
    let good=[];for(let z=0;z<4;z++){if(z===q)continue;const H=L.slice();if(add(H,a,z&1)&&add(H,b,z>>1))good.push(z)}
    if(!good.length)return {reject:true,r};
    if(good.length===1){const before=L.length;if(!add(L,a,good[0]&1)||!add(L,b,good[0]>>1))fail("closure");out.parityEquations+=L.length-before}
    D.push(E[i]);E.splice(i,1);out.removed++;changed=true;break;
  }}
  return {r,L,E,D,reject:false}
 }
 function allowed(n,edges,x){return edges.every(([u,v,q])=>{const a=(1<<u)^(1<<v);return (parity(a&x)+2*parity((a<<n)&x))!==q})}
 function fvsCheck(n,edges,res,B){
  const {L,E,D,r}=res,T=forest(n,E).T;
  const coords=e=>{const a=(1<<e[0])^(1<<e[1]),p=plane(reduce(L,a)[0],reduce(L,a<<n)[0]);return B.filter(x=>p.includes(x))};
  const uses=new Map();for(const e of T){const z=coords(e);if(z.length!==2)fail("tree coords");for(const v of z)uses.set(v,(uses.get(v)||0)+1)}
  const s=2*T.length-uses.size,bad=T.filter(e=>coords(e).some(v=>uses.get(v)>1));
  if(bad.length>2*s||s>L.length)fail("bad forest budget");
  const X=coverRemoved(n,bad),Y=coverRemoved(n,D),S=new Set([...X,...Y]);
  const R=edges.filter(e=>!S.has(e[0])&&!S.has(e[1]));
  if(forest(n,R).T.length!==R.length||S.size>5*r||Y.length>r||L.length>2*r)fail("fvs bound");
  out.fvsCertificates++;
 }
 function runGraph(n,edges,name){
   out.graphCases++;let rootModels=0;
   const root=norm(n,edges,[]);if(!root||root.reject)fail("unexpected root closure");
   const rootPlanes=edges.map(([u,v])=>{let a=(1<<u)^(1<<v);return plane(a,a<<n)});
   if(!!alignment(rootPlanes)!==(forest(n,edges).T.length===edges.length))fail("raw forest equivalence");
   const guards=[[]];for(let j=0;j<12;j++){const G=[],m=1+rnd(4);for(let k=0;k<m;k++)G.push([1+rnd((1<<(2*n))-1),rnd(2)]);guards.push(G)}
   for(let j=0;j<guards.length;j++){const G=guards[j],res=norm(n,edges,G);out.guardCases++;if(res)out.consistentGuards++;if(res?.reject)out.closureRejected++;
    let models=0;
    for(let x=0;x<(1<<(2*n));x++){out.sourceAssignments++;const a=G.every(([v,b])=>parity(v&x)===b)&&allowed(n,edges,x);if(a)models++;
      const b=!!res&&!res.reject&&res.L.every(([v,c])=>parity(v&x)===c)&&allowed(n,res.E,x);if(a!==b)fail("model preservation");
    }
    if(models)out.guardSAT++;else out.guardUNSAT++;
    if(j===0){rootModels=models;out[models?"rootSAT":"rootUNSAT"]++}
    if(res&&!res.reject){const {L,E,D,r}=res;if(coverRemoved(n,D).length>r||L.length>2*r)fail("DA03 budget");const ps=E.map(([u,v])=>{const a=(1<<u)^(1<<v);return plane(reduce(L,a)[0],reduce(L,a<<n)[0])});const B=alignment(ps);if(B){out.aligned++;out[models?"alignedSAT":"alignedUNSAT"]++;fvsCheck(n,edges,res,B)}}
   }
   if(name)out.benchmarks.push({name,models:rootModels});
 }
 const K5=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)K5.push([u,v,0]);runGraph(5,K5,"K5");
 for(let i=0;i<K5.length;i++)runGraph(5,K5.filter((_,j)=>i!==j),"K5-e"+i);
 for(let i=0;i<120;i++){const n=3+rnd(4),E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(100)<55)E.push([u,v,rnd(4)]);runGraph(n,E,null)}
 return out
}
console.log(JSON.stringify(main(),null,2));
