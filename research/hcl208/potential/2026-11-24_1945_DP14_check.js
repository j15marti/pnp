"use strict";
function main(){
const ledger={queries:0,closurePasses:0,removedLabels:0,entriesRead:0,emitted:0,switches:0,maxTable:0,assertions:0};
function ck(b){ledger.assertions++;if(!b)throw Error("assertion "+ledger.assertions)}
function prod(a){return a.reduce((x,y)=>x*BigInt(y),1n)}
function add(M,k,v){ledger.emitted++;if(v===0n)return;let z=(M.get(k)||0n)+v;if(z===0n)M.delete(k);else M.set(k,z);ledger.maxTable=Math.max(ledger.maxTable,M.size)}
function prep(G,order){let n=G.a.length,E=G.e,pos=[];order.forEach((v,i)=>pos[v]=i);
let edges=E.map(e=>{if(pos[e.u]<pos[e.v])return e;return {u:e.v,v:e.u,U:e.V,V:e.U}});
let future=Array.from({length:n+1},(_,i)=>Array.from({length:n},(_,u)=>edges.map((e,j)=>e.u===u&&pos[u]<i&&pos[e.v]>=i?j:-1).filter(j=>j>=0)));
let sizes=G.a.map(a=>a.length), choices=future.map(F=>F.map((e,u)=>e.length&&prod(e.map(j=>edges[j].U[0].length))>BigInt(sizes[u])?"label":"rank"));
let bounds=future.map((F,i)=>prod(F.map((e,u)=>choices[i][u]==="label"?sizes[u]:prod(e.map(j=>edges[j].U[0].length)))));
return {edges,future,choices,bounds,pos};
}
function K(e,a,b){let s=0n;for(let k=0;k<e.U[a].length;k++)s+=BigInt(e.U[a][k])*BigInt(e.V[b][k]);return s}
function solve(G,order,guard={}){
ledger.queries++;let n=G.a.length,{edges,future,choices,bounds}=prep(G,order),m=edges.length;
let A=G.a.map((a,u)=>a.map((w,t)=>w!==0&&(guard[u]===undefined||guard[u]===t)?t:-1).filter(t=>t>=0));
while(true){ledger.closurePasses++;let changed=false;
for(let e of edges){for(let side=0;side<2;side++){let u=side?e.v:e.u,v=side?e.u:e.v;let old=A[u];A[u]=old.filter(a=>A[v].some(b=>side?K(e,b,a)!==0n:K(e,a,b)!==0n));ledger.removedLabels+=old.length-A[u].length;if(A[u].length!==old.length){changed=true;break}}if(changed)break}
if(A.some(a=>!a.length))return {z:0n,bounds,peak:0};if(!changed)break}
let blank=Array(n+m).fill(-1),M=new Map([[blank.join(","),1n]]),peak=1;
const checkSize=(M,B)=>{ck(BigInt(M.size)<=B);peak=Math.max(peak,M.size)};
for(let i=0;i<n;i++){let v=order[i],N=new Map();
for(let [key,w] of M){ledger.entriesRead++;let a=key.split(",").map(Number);for(let t of A[v]){let b=a.slice(),z=w*BigInt(G.a[v][t]);b[v]=t;
for(let j=0;j<m;j++){let e=edges[j];if(e.v!==v)continue;if(a[e.u]>=0)z*=K(e,a[e.u],t);else{ck(a[n+j]>=0);z*=BigInt(e.V[t][a[n+j]]);b[n+j]=-1}}
add(N,b.join(","),z)}}
M=N;checkSize(M,bounds[i]*BigInt(G.a[v].length));
for(let u=0;u<n;u++){if(u!==v&&choices[i][u]!=="label")continue;if(choices[i+1][u]==="label")continue;
let F=future[i+1][u];if(F.length)ledger.switches++;
N=new Map();
for(let [key,w] of M){ledger.entriesRead++;let a=key.split(",").map(Number),t=a[u];ck(t>=0);a[u]=-1;
function rec(h,z){if(h===F.length){add(N,a.join(","),z);return}let j=F[h],r=edges[j].U[t].length;for(let k=0;k<r;k++){a[n+j]=k;rec(h+1,z*BigInt(edges[j].U[t][k]))}a[n+j]=-1}
rec(0,w)}
M=N;checkSize(M,bounds[i]*BigInt(G.a[v].length))}
checkSize(M,bounds[i+1]);
}
ck(M.size<=1);let z=M.get(blank.join(","))||0n;return {z,bounds,peak};
}
function brute(G){let z=0n,t=[];function f(i,w){if(i===G.a.length){for(let e of G.e)w*=K(e,t[e.u],t[e.v]);z+=w;return}for(let j=0;j<G.a[i].length;j++){t[i]=j;f(i+1,w*BigInt(G.a[i][j]))}}f(0,1n);return z}
function physical(n,pairs,allowed){let inc=Array.from({length:n},()=>[]);pairs.forEach(([u,v],j)=>{inc[u].push(j);inc[v].push(j)});let labels=inc.map((a,u)=>Array.from({length:2**a.length},(_,x)=>Array.from({length:a.length},(_,j)=>(x>>j)&1)).filter(b=>allowed(u,b)));let G={a:labels.map(l=>l.map(()=>1)),e:pairs.map(([u,v],j)=>({u,v,U:labels[u].map(b=>b[inc[u].indexOf(j)]?[0,1]:[1,0]),V:labels[v].map(b=>b[inc[v].indexOf(j)]?[0,1]:[1,0])}))};return {G,labels}}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let F=[];for(let edit=-1;edit<21;edit++){let pairs=fano.flatMap((c,i)=>c.map(v=>[v,7+i]));let {G,labels}=physical(14,pairs,(u,b)=>{if(u<7)return b.every(x=>x===b[0]);let a=b.map((x,j)=>x^Number(edit===3*(u-7)+j));return !a.every(x=>x===a[0])});let order=Array.from({length:14},(_,i)=>i),r=solve(G,order);let ref=0;for(let w=0;w<128;w++){if(fano.every((c,i)=>{let b=c.map((v,j)=>((w>>v)&1)^Number(edit===3*i+j));return !b.every(x=>x===b[0])}))ref++}
ck(r.z===BigInt(ref));ck(ref===(edit<0?0:10));let witness=null;if(r.z>0n){let pins={};for(let u=0;u<7;u++){let q=solve(G,order,{...pins,[u]:0});pins[u]=q.z>0n?0:1}witness=Array.from({length:7},(_,i)=>labels[i][pins[i]][0]);ck(fano.every((c,i)=>{let b=c.map((v,j)=>witness[v]^Number(edit===3*i+j));return !b.every(x=>x===b[0])}))}F.push({edit,count:String(r.z),maxBound:String(r.bounds.reduce((a,b)=>a>b?a:b)),peak:r.peak,witness})}
let ladders=[];for(let k of [2,4,8,32,128]){let pairs=[];for(let j=0;j<k;j++){pairs.push([2*j,2*j+1]);if(j+1<k)pairs.push([2*j,2*j+2],[2*j+1,2*j+3])}for(let odd of [0,1]){let {G}=physical(2*k,pairs,(u,b)=>b.reduce((a,x)=>a^x,0)===(u===0?odd:0));let r=solve(G,Array.from({length:2*k},(_,i)=>i));let expected=odd?0n:2n**BigInt(k-1);ck(r.z===expected);ladders.push({columns:k,odd,count:String(r.z),maxBound:String(r.bounds.reduce((a,b)=>a>b?a:b)),peak:r.peak,feedback:String(2n**BigInt(k-1))})}}
let seed=170325;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let random=[];for(let trial=0;trial<60;trial++){let n=3+rnd(4),a=Array.from({length:n},()=>Array.from({length:2+rnd(3)},()=>rnd(5)-2)),e=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(3)!==0){let r=1+rnd(3);e.push({u,v,U:a[u].map(()=>Array.from({length:r},()=>rnd(5)-2)),V:a[v].map(()=>Array.from({length:r},()=>rnd(5)-2))})}let G={a,e},order=Array.from({length:n},(_,i)=>trial%2?i:n-1-i),got=solve(G,order),ref=brute(G);ck(got.z===ref);random.push({trial,count:String(got.z),peak:got.peak})}
return {seed:170325,ledger,fano:F,ladders,random};
}
console.log(JSON.stringify(main(),null,2));
