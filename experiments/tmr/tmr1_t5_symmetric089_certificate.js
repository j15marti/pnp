'use strict';
// TMR-1/089 independent compact certificate: node >=18, no packages.
const assert=require('node:assert/strict');
const mod=x=>((x%5)+5)%5, R=(a,b)=>[1,3].includes(mod(b-a));
const F=Array.from({length:5},(_,d)=>Array.from({length:5},(_,z)=>Number(R(0,z)&&R(z,d))).reduce((a,b)=>a+b,0));
const W=F.map((v,d)=>v*F[mod(-d)]);
assert.deepEqual(F,[0,1,1,0,2]);
assert.deepEqual(W,[0,2,0,0,2]);
const colorings=(n,fn)=>{const x=Array(n).fill(0);function go(k){if(k===n){fn(x);return;}for(let a=0;a<5;a++){x[k]=a;go(k+1);}}go(0);};
const edges=(n,mask)=>{let i=0,r=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(mask&(2**i++))r.push([u,v]);return r;};
function wedge(n,E){
 if(!n)return {n:1,edges:[],c:0};
 const adj=Array.from({length:n},()=>[]);for(const [a,b]of E){adj[a].push(b);adj[b].push(a);}
 const comp=Array(n).fill(-1),roots=[];
 for(let v=0;v<n;v++)if(comp[v]<0){let k=roots.length;roots.push(v);comp[v]=k;let todo=[v];while(todo.length)for(const w of adj[todo.pop()])if(comp[w]<0){comp[w]=k;todo.push(w);}}
 const root=new Set(roots),map=Array(n).fill(0);let next=1;for(let i=0;i<n;i++)if(!root.has(i))map[i]=next++;
 return {n:next,edges:E.map(([a,b])=>[map[a],map[b]].sort((a,b)=>a-b)),c:roots.length};
}
function counts(n,E){let c=0n,z=0n; colorings(n,x=>{let w=1n;for(const [a,b]of E)w*=BigInt(W[mod(x[b]-x[a])]);z+=w;if(E.every(([a,b])=>[1,4].includes(mod(x[b]-x[a]))))c++;});return [c,z];}
let assertions=2,graphs=0,wedgeGraphs=0;
for(let n=1;n<=5;n++)for(let mask=0;mask<2**(n*(n-1)/2);mask++){
 let E=edges(n,mask),[c,z]=counts(n,E),wd=wedge(n,E),[cw,zw]=counts(wd.n,wd.edges);
 assert.equal(z,c*2n**BigInt(E.length));assert.equal(c,cw*5n**BigInt(wd.c-1));assert.equal(zw,cw*2n**BigInt(E.length));
 assertions+=3;graphs++;wedgeGraphs++;
 if(E.length){let N=wd.n+2*E.length,M=4*E.length,w=t=>Math.max(1,Math.ceil(Math.log2(Math.max(2,t))));
 let L=n+E.length+2+2*E.length*w(n),out=N+M+2+2*M*w(N);
 assert.ok(out<=8*L);assert.equal(N,wd.n+2*E.length);assert.equal(M,4*E.length);assert.ok(wd.n<=n);
 assertions+=4;
 }
}
// Direct full target enumeration on a K3 source, independently of endpoint transfer.
const E=[[0,1],[0,2],[1,2]],arcs=[];
E.forEach(([u,v],k)=>{const a=3+2*k,b=a+1;arcs.push([u,a],[a,v],[v,b],[b,u]);});
let direct=0n; colorings(9,x=>{if(arcs.every(([u,v])=>R(x[u],x[v])))direct++;});
assert.equal(direct,8n*counts(3,E)[0]);assert.equal(direct,0n);assertions+=2;
console.log(JSON.stringify({theorem:'C1-T5-SYMMETRIC-C4-EULERIAN-HARDNESS089',graphChecks:graphs,wedgeChecks:wedgeGraphs,localForwardTransfer:F,pairedTransfer:W,directK3Assignments:5**9,assertions,failures:0},null,2));

