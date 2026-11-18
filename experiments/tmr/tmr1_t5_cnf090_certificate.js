'use strict';
// TMR-1/090 independent compact certificate; only built-in Node.js.
const assert = require('node:assert/strict');
const beat=(a,b)=>[1,3].includes((b-a+5)%5);
let tests=0, graphs=0, candidates=0;
const ck=(x,m='certificate')=>{tests++;assert.ok(x,m)};
function compile(n,edges){
 const c=[],y=(v,a)=>7*v+a+1, p=v=>7*v+6, q=v=>7*v+7;
 for(let v=0;v<n;v++){
  for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)c.push([-y(v,a),-y(v,b)]);
  c.push([-p(v),y(v,0),y(v,1)],[p(v),-y(v,0)],[p(v),-y(v,1)]);
  c.push([-q(v),y(v,2),y(v,3)],[q(v),-y(v,2)],[q(v),-y(v,3)]);
  c.push([p(v),q(v),y(v,4)]);
 }
 for(const [u,v] of edges)for(let a=0;a<5;a++)
  c.push([-y(u,a),y(v,(a+1)%5),y(v,(a+3)%5)]);
 return {N:7*n,c};
}
function boolOf(x){const b=Array(7*x.length).fill(false);
 for(let v=0;v<x.length;v++){b[7*v+x[v]]=true;b[7*v+5]=x[v]<2;b[7*v+6]=x[v]===2||x[v]===3}return b}
const sat=(F,b)=>F.c.every(cl=>cl.some(l=>l>0?b[l-1]:!b[-l-1]));
const w=n=>Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
function audit(n,edges){
 graphs++;const F=compile(n,edges),m=edges.length;
 ck(F.N===7*n);ck(F.c.length===17*n+5*m);
 ck(F.c.filter(cl=>cl.length===2).length===14*n);
 ck(F.c.filter(cl=>cl.length===3).length===3*n+5*m);
 ck(F.c.every(cl=>cl.every(l=>Math.abs(l)>=1&&Math.abs(l)<=F.N)));
 const active=[...new Set(edges.flat())].sort((a,b)=>a-b),k=active.length;
 const L=n+m+2+2*m*w(n);
 const out=58*k+15*m+2+(37*k+15*m)*(w(7*k)+1);
 ck(k<=2*m);ck(out<=200*L,'bit bound');
 const rel=new Map(active.map((v,i)=>[v,i]));
 const H=compile(k,edges.map(([u,v])=>[rel.get(u),rel.get(v)]));
 let nsol=0,ksol=0;
 for(let z=0;z<5**n;z++){
  let t=z;const x=Array.from({length:n},()=>{const a=t%5;t=Math.floor(t/5);return a});
  const truth=edges.every(([u,v])=>beat(x[u],x[v]));
  ck(sat(F,boolOf(x))===truth);
  if(truth)nsol++;candidates++;
 }
 for(let z=0;z<5**k;z++){
  let t=z;const x=Array.from({length:k},()=>{const a=t%5;t=Math.floor(t/5);return a});
  if(sat(H,boolOf(x)))ksol++;
 }
 ck(nsol===5**(n-k)*ksol,'isolate factor');
}
for(let n=0;n<=3;n++){
 const arcs=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)arcs.push([u,v]);
 for(let mask=0;mask<2**arcs.length;mask++)audit(n,arcs.filter((_,i)=>(mask&(1<<i))!==0));
}
for(let a=0;a<5;a++)for(let b=0;b<5;b++){
 const F=compile(2,[[0,1]]);ck(sat(F,boolOf([a,b]))===beat(a,b));
}
const F=compile(1,[]);
for(let a=0;a<5;a++){
 let good=0;for(let t=0;t<4;t++){
  const b=Array(7).fill(false);b[a]=true;b[5]=!!(t&1);b[6]=!!(t&2);
  if(sat(F,b))good++;
 }ck(good===1,'auxiliary uniqueness');
}
console.log(JSON.stringify({theorem:'C1-T5-3CNF-PARSIMONIOUS-ISOLATE-OPT090',
 graphs,candidates,tests,failures:0,scope:'finite computational verification'}));
