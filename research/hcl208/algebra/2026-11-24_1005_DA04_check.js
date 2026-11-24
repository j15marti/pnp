'use strict';
function run(){
const C={nodes:0,branches:0,closureScans:0,pins:0,deletions:0,degreeCalls:0,nonGDP:0,slack:0,gdp:0,blockTests:0,cycleSteps:0,referenceNodes:0,lifts:0};
const assert=(x,m)=>{if(!x)throw Error(m)};
const colors=m=>[0,1,2,3].filter(x=>m&(1<<x)), pop=m=>colors(m).length;
function graph(n,E,L=Array(n).fill(15)){const A=Array.from({length:n},()=>[]);for(let i=0;i<E.length;i++){let [u,v,s]=E[i];A[u].push([v,s,i]);A[v].push([u,s,i]);}return {n,E,A,L};}
function close(G,L,X){while(true){C.closureScans++;if(L.includes(0))return false;let u=L.findIndex(m=>m>0&&pop(m)===1);if(u<0)return true;let c=colors(L[u])[0];X[u]=c;L[u]=-1;C.pins++;for(let [v,s] of G.A[u])if(L[v]>=0){let z=L[v]&~(1<<(c^s));if(z!==L[v])C.deletions++;L[v]=z;}else if((X[v]^c)===s)return false;}}
const deg=(G,L,u)=>G.A[u].filter(([v])=>L[v]>=0).length;
const deficit=(G,L)=>L.reduce((a,m,u)=>a+(m>=0&&pop(m)<deg(G,L,u)?1:0),0);
function degreeDec(G,L){
 C.degreeCalls++;if(L.includes(0))return false;
 const seen=new Set();for(let root=0;root<G.n;root++)if(L[root]>=0&&!seen.has(root)){
  const V=[root];seen.add(root);for(let j=0;j<V.length;j++)for(let [v]of G.A[V[j]])if(L[v]>=0&&!seen.has(v)){seen.add(v);V.push(v);}
  assert(V.every(u=>pop(L[u])>=deg(G,L,u)),"degree promise");
  if(V.some(u=>pop(L[u])>deg(G,L,u))){C.slack++;continue;}
  let timer=0,disc=new Map(),low=new Map(),stack=[],B=[];
  function dfs(u,pe){disc.set(u,++timer);low.set(u,timer);for(let [v,s,id]of G.A[u])if(L[v]>=0&&id!==pe){if(!disc.has(v)){stack.push(id);dfs(v,id);low.set(u,Math.min(low.get(u),low.get(v)));if(low.get(v)>=disc.get(u)){let ed=[],q;do{q=stack.pop();ed.push(q);}while(q!==id);B.push(ed);}}else if(disc.get(v)<disc.get(u)){stack.push(id);low.set(u,Math.min(low.get(u),disc.get(v)));}}}
  dfs(root,-1);
  const blocks=B.map(ed=>{let adj=new Map();for(let id of ed){let[u,v,s]=G.E[id];if(!adj.has(u))adj.set(u,[]);if(!adj.has(v))adj.set(v,[]);adj.get(u).push([v,s]);adj.get(v).push([u,s]);}let vs=[...adj.keys()];return {ed,adj,vs,clique:ed.length===vs.length*(vs.length-1)/2,cycle:vs.every(u=>adj.get(u).length===2)};});
  if(blocks.some(b=>!b.clique&&!b.cycle)){C.nonGDP++;continue;}
  C.gdp++;
  const memberships=new Map(V.map(u=>[u,[]]));blocks.forEach((b,i)=>b.vs.forEach(u=>memberships.get(u).push(i)));
  function vertex(u,parent){let m=L[u];for(let i of memberships.get(u))if(i!==parent)m&=block(i,u);return m;}
  function block(i,p){let b=blocks[i], masks=new Map(b.vs.filter(v=>v!==p).map(v=>[v,vertex(v,i)]));let answer=0;
   for(let c of colors(L[p])){
    C.blockTests++;let ok=false;
    if(b.clique){let ord=b.vs.filter(v=>v!==p),chosen=new Map([[p,c]]);function rec(j){if(j===ord.length)return true;let v=ord[j];for(let x of colors(masks.get(v)))if(b.adj.get(v).every(([w,s])=>!chosen.has(w)||(chosen.get(w)^x)!==s)){chosen.set(v,x);if(rec(j+1))return true;chosen.delete(v);}return false;}ok=rec(0);}
    else{let prev=p,cur=b.adj.get(p)[0][0],last=1<<c;while(cur!==p){let s=b.adj.get(cur).find(([v])=>v===prev)[1];let next=0;for(let x of colors(masks.get(cur)))for(let y of colors(last)){C.cycleSteps++;if((x^y)!==s)next|=1<<x;}last=next;let nxt=b.adj.get(cur).find(([v])=>v!==prev)[0];prev=cur;cur=nxt;}let s=b.adj.get(p).find(([v])=>v===prev)[1];ok=colors(last).some(x=>(x^c)!==s);}
    if(ok)answer|=1<<c;
   }return answer;
  }
  if(!vertex(root,-1))return false;
 }return true;
}
function valid(G,X){return X.every((x,u)=>x>=0&&x<4&&(G.L[u]&(1<<x)))&&G.E.every(([u,v,s])=>(X[u]^X[v])!==s);}
function lift(G,L,X){assert(degreeDec(G,L),"lift entry");while(L.some(m=>m>=0)){let u=L.findIndex(m=>m>=0),found=false;for(let c of colors(L[u])){let l=L.slice(),x=X.slice();l[u]=1<<c;if(close(G,l,x)&&degreeDec(G,l)){L=l;X=x;found=true;break;}}assert(found,"degree witness");}return X;}
function solve(G){const initial=deficit(G,G.L);function go(L,X,bound){C.nodes++;if(!close(G,L,X))return null;let k=deficit(G,L);assert(k<=bound,"deficit increased");let u=L.findIndex((m,u)=>m>=0&&pop(m)<deg(G,L,u));if(u<0){if(!degreeDec(G,L))return null;return lift(G,L,X);}C.branches++;for(let c of colors(L[u])){let l=L.slice(),x=X.slice();l[u]=1<<c;let ans=go(l,x,k-1);if(ans)return ans;}return null;}
 let x=go(G.L.slice(),Array(G.n).fill(-1),initial);if(x){assert(valid(G,x),"invalid source lift");C.lifts++;}return x;}
function brute(G){let X=Array(G.n).fill(-1);function go(u){C.referenceNodes++;if(u===G.n)return X.slice();for(let c of colors(G.L[u]))if(G.A[u].every(([v,s])=>X[v]<0||(X[v]^c)!==s)){X[u]=c;let a=go(u+1);if(a)return a;X[u]=-1;}return null;}return go(0);}
let seed=2080405;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;}
let summary={seed:2080405,random:{sat:0,unsat:0},degreeLists:{sat:0,unsat:0},controls:[],scaling:[]};
function check(G,label,ref=true){let x=solve(G);if(ref)assert(Boolean(x)===Boolean(brute(G)),label+" reference mismatch");return !!x;}
for(let t=0;t<300;t++){let n=2+rand(7),E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rand(100)<45)E.push([u,v,rand(4)]);let L=Array.from({length:n},()=>1+rand(15));let G=graph(n,E,L);summary.random[check(G,"random")?"sat":"unsat"]++;}
for(let t=0;t<250;t++){let n=2+rand(8),E=[],d=Array(n).fill(0);for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(d[u]<4&&d[v]<4&&rand(100)<40){E.push([u,v,rand(4)]);d[u]++;d[v]++;}let L=d.map(k=>{let a;do{a=1+rand(15)}while(pop(a)<k);return a;});let G=graph(n,E,L);summary.degreeLists[check(G,"degree lists")?"sat":"unsat"]++;}
const K=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)K.push([u,v,0]);assert(!check(graph(5,K),"K5"),"K5");let del=0,tw=0;for(let i=0;i<K.length;i++){assert(check(graph(5,K.filter((e,j)=>i!==j)),"K5-e"),"neighbor");del++;let E=K.map(e=>e.slice());E[i][2]=1;assert(check(graph(5,E),"twist"),"signed neighbor");tw++;}summary.controls.push({K5:"UNSAT",deletionSAT:del,twistSAT:tw});
for(let n of [3,4,5,6,31,32])for(let twist of [0,1]){let E=Array.from({length:n},(_,u)=>[u,(u+1)%n,u===n-1?twist:0]);let sat=check(graph(n,E,Array(n).fill(3)),"cycle",n<7);assert(sat===((n%2)===twist),"cycle parity");summary.controls.push({cycle:n,twist,sat});}
for(let k of [3,8,32,64]){let E=[];for(let i=0;i<k;i++){E.push([i,(i+1)%k,rand(4)],[k+i,k+(i+1)%k,rand(4)],[i,k+i,rand(4)]);}let trials=k===3?4096:12;let before={...C};for(let t=0;t<trials;t++){let L=Array.from({length:2*k},(_,u)=>15&~(1<<(k===3?((t>>>(2*u))&3):rand(4))));let G=graph(2*k,E,L);assert(check(G,"ladder universal",k===3),"ladder projection");}summary.scaling.push({interior:2*k,boundaryPorts:2*k,tests:trials,degreeCalls:C.degreeCalls-before.degreeCalls,nonGDP:C.nonGDP-before.nonGDP,lifts:C.lifts-before.lifts});}
summary.counters=C;return summary;
}
console.log(JSON.stringify(run(),null,2));
