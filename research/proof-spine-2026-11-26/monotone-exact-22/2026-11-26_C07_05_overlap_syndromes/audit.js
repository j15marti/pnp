console.log(JSON.stringify((function audit(){
 const assert=(v,msg="assertion")=>{if(!v)throw Error(msg)};
 const bit=i=>1n<<BigInt(i),par=x=>{let s=0;while(x){x&=x-1n;s^=1}return s};
 const high=x=>x.toString(2).length-1;
 class Basis{
  constructor(){this.b=new Map()}
  reduce(v,t=0n){for(const p of [...this.b.keys()].sort((a,b)=>b-a)){if(v&bit(p)){let [w,z]=this.b.get(p);v^=w;t^=z}}return [v,t]}
  add(v,t=0n){let [w,z]=this.reduce(v,t);if(w===0n)return [false,z];this.b.set(high(w),[w,z]);return [true,0n]}
  solve(){let x=0n;for(const p of [...this.b.keys()].sort((a,b)=>a-b)){let [w,z]=this.b.get(p);if(par(w&x)!==Number(z))x|=bit(p)}return x}
 }
 const valid=(F,x,pins)=>F.every(C=>C.reduce((s,i)=>s+Number((x>>BigInt(i))&1n),0)===2)&&pins.every(([i,v])=>Number((x>>BigInt(i))&1n)===v);
 function chart(n,F,pins=[]){
  const A=new Basis(); for(const C of F)A.add(C.reduce((v,i)=>v^bit(i),0n));
  for(const [i,b] of pins){const [ok,z]=A.add(bit(i),BigInt(b));if(!ok&&z)return null}
  let P,forced=0;
  for(;;){P=[];let again=false;
   for(const C of F){let [u,a]=A.reduce(bit(C[0])^bit(C[1])),[v,b]=A.reduce(bit(C[0])^bit(C[2]));let r=u||v; const ev=(w,s,t)=>Number(s)^(w===0n?0:t);
    if(!u||!v||u===v){if(!r){if(!(a||b))return null;continue}
     let allow=[0,1].filter(t=>ev(u,a,t)||ev(v,b,t));if(!allow.length)return null;
     if(allow.length===1){assert(A.add(r,BigInt(allow[0]))[0]);forced++;again=true;break}continue}
    P.push({u,v,allowed:[0,1,2,3].filter(s=>((s&1)^Number(a))||(((s>>1)&1)^Number(b)))});
   }
   if(!again)return {A,P,forced}
  }
 }
 function forestSolve(n,F,pins=[],cap=12){
  let C=chart(n,F,pins);if(!C)return {status:"NO",closure:true,delta:0};
  const {A,P,forced}=C,m=P.length;
  let B=new Basis(),all=[];for(let i=0;i<m;i++)for(let j=0;j<2;j++){let [ok,z]=B.add(j?P[i].v:P[i].u,bit(2*i+j));if(!ok)all.push(z)}
  let rank=B.b.size,dep=all.length,edges=[];
  const dirs=P.map(({u,v})=>new Map([[u,1],[v,2],[u^v,3]]));
  for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){let common=[];for(const [v,a] of dirs[i])if(dirs[j].has(v))common.push([a,dirs[j].get(v)]);if(common.length)edges.push({i,j,pairs:common.slice(0,Math.min(2,common.length)),w:Math.min(2,common.length)})}
  edges.sort((a,b)=>b.w-a.w||a.i-b.i||a.j-b.j);
  let parent=Array.from({length:m},(_,i)=>i),find=i=>{while(parent[i]!==i)i=parent[i];return i};
  let K=new Basis(),adj=P.map(()=>[]),weight=0;
  for(const e of edges){let a=find(e.i),b=find(e.j);if(a===b)continue;parent[a]=b;weight+=e.w;
   adj[e.i].push([e.j,e.pairs]);adj[e.j].push([e.i,e.pairs.map(([a,b])=>[b,a])]);
   for(const [a,b] of e.pairs){let z=(BigInt(a)<<BigInt(2*e.i))^(BigInt(b)<<BigInt(2*e.j));assert(K.add(z)[0],"forest relations dependent")}
  }
  const E=[];for(const z of all)if(K.add(z)[0])E.push(z);
  const delta=E.length;assert(delta===dep-weight&&delta>=0);
  if(delta>cap)return {status:"UNKNOWN",m,rank,dep,weight,delta,forced};
  const contrib=P.map((_,i)=>[0,1,2,3].map(s=>E.reduce((a,z,j)=>a+(par(z&(BigInt(s)<<BigInt(2*i)))?2**j:0),0)));
  const lp=(a,s)=>par(BigInt(a&s));let merges=0;
  function combine(L,R){let Z=new Map();for(const [a,x] of L)for(const [b,y] of R){merges++;if(!Z.has(a^b))Z.set(a^b,x.concat(y))}return Z}
  let visited=new Set();
  function dfs(i,p){visited.add(i);let D=new Map(P[i].allowed.map(s=>[s,new Map([[contrib[i][s],[[i,s]]]])]));
   for(const [j,pairs] of adj[i]){if(j===p)continue;let child=dfs(j,i);
    for(const [s,M] of D){let R=new Map();for(const [t,L] of child)if(pairs.every(([a,b])=>lp(a,s)===lp(b,t)))for(const [h,w] of L)if(!R.has(h))R.set(h,w);D.set(s,combine(M,R))}
   }return D}
  let total=new Map([[0,[]]]);
  for(let i=0;i<m;i++)if(!visited.has(i)){let D=dfs(i,-1),R=new Map();for(const M of D.values())for(const [s,w] of M)if(!R.has(s))R.set(s,w);total=combine(total,R)}
  let info={m,rank,dep,weight,delta,forced,merges};
  if(!total.has(0))return {status:"NO",...info};
  for(const [i,s] of total.get(0)){for(const [v,b] of [[P[i].u,s&1],[P[i].v,s>>1]]){let [ok,z]=A.add(v,BigInt(b));assert(ok||!z,"lift conflict")}}
  let x=A.solve();assert(valid(F,x,pins),"invalid lift");return {status:"YES",...info,witness:x.toString(16)}
 }
 // Independent reference on full original variables and guards.
 function brute(n,F,pins=[]){for(let x=0;x<2**n;x++)if(valid(F,BigInt(x),pins))return true;return false}
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const counts={random:0,yes:0,no:0,unknown:0,closureNO:0,forestWeightPositive:0};for(let t=0;t<180;t++){let n=4+rnd(7),F=[],pins=[];for(let j=0,k=1+rnd(8);j<k;j++){let a=[];while(a.length<4){let x=rnd(n);if(!a.includes(x))a.push(x)}F.push(a)}for(let i=0;i<n;i++)if(rnd(5)===0)pins.push([i,rnd(2)]);let w=brute(n,F,pins),r=forestSolve(n,F,pins);assert(r.status==="UNKNOWN"||(r.status==="YES")===w);counts.random++;counts[r.status.toLowerCase()]++;if(r.closure)counts.closureNO++;if(r.weight>0)counts.forestWeightPositive++}
 // Fano plane, known NO. Independently enumerate all 128 original NAE words.
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const nae=(G,x)=>G.every(C=>{let k=C.reduce((s,i)=>s+Number((x>>BigInt(i))&1n),0);return k>0&&k<3});
 assert(!Array.from({length:128},(_,i)=>i).some(x=>nae(fano,BigInt(x))));
 assert(Array.from({length:128},(_,i)=>i).some(x=>nae(fano.slice(1),BigInt(x))));
 function compile(G,n){return [n+G.length,G.map((C,i)=>C.concat(n+i))]}
 let chain=[];for(const t of [0,8,32,128,256]){
  for(const isNO of [false,true]){
   let G=(isNO?fano:fano.slice(1)).map(C=>C.slice()),a=0,n=7;
   for(let i=0;i<t;i++){G.push([a,n,n+1]);a=n;n+=2}
   let [N,F]=compile(G,n),r=forestSolve(N,F);assert(r.status===(isNO?"NO":"YES"));assert(r.delta===(isNO?8:6));delete r.witness;chain.push({tail:t,variables:N,clauses:F.length,...r})
  }
 }
 // High-rank native grid anchor: shared directions absorb a large fraction but not all dependencies.
 // A star of clauses with one common pair has tree-exact overlap and arbitrary local rank.
 let star=[];for(const m of [8,32,128,256]){
  const F=Array.from({length:m},(_,i)=>[0,1,2+2*i,3+2*i]),r=forestSolve(2+2*m,F);assert(r.status==="YES"&&r.delta===0&&r.weight===m-1);delete r.witness;star.push({variables:2+2*m,clauses:m,...r})
 }
 // Single-cycle linear triples, no pairwise plane overlap but only one dependency.
 let cycles=[];for(const m of [5,17,65,129]){
  let [n,F]=compile(Array.from({length:m},(_,i)=>[i,(i+1)%m,m+i]),2*m),r=forestSolve(n,F);assert(r.status==="YES"&&r.delta===1&&r.weight===0);delete r.witness;cycles.push({variables:n,clauses:m,...r})
 }
 // Matching degree<=2 native controls, no calls to external matching.
 let matching=[];for(const m of [4,16,64]){
  let F=Array.from({length:m},(_,i)=>[i,(i+1)%m,m+2*i,m+2*i+1]);let r=forestSolve(3*m,F);assert(r.status==="YES");delete r.witness;matching.push({variables:3*m,clauses:m,...r})
 }
 return {seed:20261126,counts,chain,star,cycles,matching}
})(),null,2));
