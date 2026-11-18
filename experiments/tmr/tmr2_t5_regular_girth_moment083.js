#!/usr/bin/env node
'use strict';
const audit = function audit(){
"use strict";
const REV="tmr2-t5-regular-girth-moment083.v1",SEED=202611180507;
let checks=0,forestCases=0,treeDPCases=0,cycleCases=0;
function ck(ok,msg){checks++;if(!ok)throw Error(msg)}
let rngState=SEED>>>0;
function rand(){rngState^=rngState<<13;rngState^=rngState>>>17;rngState^=rngState<<5;return rngState>>>0}
function beat(x,y){return (y-x+5)%5===1||(y-x+5)%5===3}
function countBrute(n,e){
const a=Array(n).fill(0);let z=0;
for(let id=0;id<5**n;id++){
let q=id;for(let j=0;j<n;j++){a[j]=q%5;q=Math.floor(q/5)}
let good=true;
for(const x of e){const from=x.dir===0?x.u:x.v,to=x.dir===0?x.v:x.u;if(!beat(a[from],a[to])){good=false;break}}
if(good)z++
}return z
}
function dsu(n){
const par=Array.from({length:n},(_,i)=>i);
function find(x){while(par[x]!==x){par[x]=par[par[x]];x=par[x]}return x}
return{find,join(x,y){x=find(x);y=find(y);if(x===y)return false;par[x]=y;return true}}
}
function countForestDP(n,ee){
const adj=new Map(),seen=new Set();
for(const e of ee){
if(!adj.has(e.u))adj.set(e.u,[]);
if(!adj.has(e.v))adj.set(e.v,[]);
adj.get(e.u).push({j:e.v,e});adj.get(e.v).push({j:e.u,e});seen.add(e.u);seen.add(e.v)
}
const visited=new Set();
function dfs(i,parent){
visited.add(i);let arr=Array(5).fill(1n);
for(const {j,e} of adj.get(i)||[]){
if(j===parent)continue;
if(visited.has(j))throw Error("not forest");
const child=dfs(j,i),next=Array(5).fill(0n);
for(let c=0;c<5;c++){
let sum=0n;
for(let d=0;d<5;d++){
const from=e.dir===0?e.u:e.v;
const good=from===i?beat(c,d):beat(d,c);
if(good)sum+=child[d]
}next[c]=arr[c]*sum
}arr=next
}return arr
}
let ans=5n**BigInt(n-seen.size);
for(const i of seen)if(!visited.has(i))ans*=dfs(i,-1).reduce((a,b)=>a+b,0n);
return ans
}
for(let n=2;n<=6;n++)for(let trial=0;trial<42;trial++){
let combos=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)combos.push([i,j]);
for(let i=combos.length-1;i>0;i--){const j=rand()%(i+1);[combos[i],combos[j]]=[combos[j],combos[i]]}
const uf=dsu(n),edges=[];
for(const [u,v] of combos)if(rand()%4!==0&&uf.join(u,v))edges.push({u,v,dir:rand()%2});
const goal=5n**BigInt(n-edges.length)*2n**BigInt(edges.length);
ck(BigInt(countBrute(n,edges))===goal,`forest brute ${n}/${trial}`);
ck(countForestDP(n,edges)===goal,`forest DP ${n}/${trial}`);
forestCases++
}
function binomial(n,k){let z=1;for(let i=1;i<=k;i++)z=z*(n-k+i)/i;return Math.round(z)}
function cycleFormula(len,bits){
let q=0;for(let i=0;i<len;i++)if(bits&(1<<i))q++;
const p=len-q;let s=0;
for(let k=0;k<=len;k++)if((p+2*q+2*k)%5===0)s+=binomial(len,k);
return 5*s
}
function cycleDP(len,bits){
let a=[1,0,0,0,0];
for(let j=0;j<len-1;j++){
const b=Array(5).fill(0),reverse=Boolean(bits&(1<<j));
for(let x=0;x<5;x++)for(let y=0;y<5;y++)if(reverse?beat(y,x):beat(x,y))b[y]+=a[x];
a=b
}
const reverse=Boolean(bits&(1<<(len-1)));let sum=0;
for(let x=0;x<5;x++)if(reverse?beat(0,x):beat(x,0))sum+=a[x];
return 5*sum
}
for(const len of [4,6,8])for(let bits=0;bits<1<<len;bits++){
ck(cycleFormula(len,bits)===cycleDP(len,bits),`cycle ${len},${bits}`);cycleCases++
}
const cy8a=Array.from({length:8},(_,i)=>({u:i,v:(i+1)%8,dir:0}));
const cy8b=Array.from({length:8},(_,i)=>({u:i,v:(i+1)%8,dir:i%2}));
ck(countBrute(8,cy8a)===180,"8cycle clockwise");
ck(countBrute(8,cy8b)===350,"8cycle alternating");
const mult=[[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]],inv=[0,1,3,2];
function norm(v){let idx=v.findIndex(x=>x!==0);if(idx<0)throw Error("zero");return v.map(x=>mult[inv[v[idx]]][x])}
function key(v){return v.join("")}
const pmap=new Map();
for(let n=1;n<256;n++){
const v=[n&3,(n>>2)&3,(n>>4)&3,(n>>6)&3];const w=norm(v);pmap.set(key(w),w)
}
const pp=[...pmap.keys()].sort();ck(pp.length===85,"85 points");
const points=pp.map(k=>pmap.get(k)),pidx=new Map(pp.map((p,i)=>[p,i]));
function dot(a,b){return mult[a[0]][b[2]]^mult[a[2]][b[0]]^mult[a[1]][b[3]]^mult[a[3]][b[1]]}
const lines=new Map();
for(let i=0;i<85;i++)for(let j=i+1;j<85;j++){
if(dot(points[i],points[j])!==0)continue;
const L=new Set([j]);
for(let t=0;t<4;t++){
const v=points[i].map((x,k)=>x^mult[t][points[j][k]]);
L.add(pidx.get(key(norm(v))))
}
ck(L.size===5&&!L.has(undefined),"GF4 line");
const ids=[...L].sort((a,b)=>a-b);lines.set(ids.join(","),ids)
}
const ll=[...lines.values()].sort((a,b)=>a.join(",").localeCompare(b.join(",")));
ck(ll.length===85,"85 lines");
const edge0=[];for(let j=0;j<85;j++)for(const i of ll[j])edge0.push({u:i,v:85+j,dir:0});
edge0.sort((a,b)=>a.u-b.u||a.v-b.v);ck(edge0.length===425,"425 edges");
const deg=Array(170).fill(0),adj=Array.from({length:170},()=>[]);
for(const e of edge0){deg[e.u]++;deg[e.v]++;adj[e.u].push(e.v);adj[e.v].push(e.u)}
ck(deg.every(v=>v===5),"5-regular");
let girth=Infinity;
for(let root=0;root<170;root++){
const dist=Array(170).fill(-1),par=Array(170).fill(-1),Q=[root];dist[root]=0;
for(let h=0;h<Q.length;h++){
const i=Q[h];
for(const j of adj[i]){
if(dist[j]===-1){dist[j]=dist[i]+1;par[j]=i;Q.push(j)}
else if(par[i]!==j)girth=Math.min(girth,dist[i]+dist[j]+1)
}
}
ck(Q.length===170,"connected")
}
ck(girth===8,"girth8");
const randomEdges=edge0.map(e=>({...e,dir:rand()%2}));
for(let size=0;size<=7;size++)for(let trial=0;trial<35;trial++){
const ix=new Set();while(ix.size<size)ix.add(rand()%425);
const ids=[...ix],p=dsu(170);
for(const i of ids)ck(p.join(edge0[i].u,edge0[i].v),"forest <=7");
const expected=5n**BigInt(170-size)*2n**BigInt(size);
for(const E of [edge0,randomEdges]){
ck(countForestDP(170,ids.map(i=>E[i]))===expected,"W34 coefficient");treeDPCases++
}
}
function fnv(str){let h=2166136261>>>0;for(let i=0;i<str.length;i++){h^=str.charCodeAt(i);h=Math.imul(h,16777619)>>>0}return h.toString(16).padStart(8,"0")}
const orientBits=randomEdges.map(e=>e.dir).join("");
const witnessBound=5/4*2**(-170/2);
ck(witnessBound<4e-26,"probability bound");
return{revision:REV,seed:SEED,assertions:checks,failures:0,independent_bruteforce_forest_cases:forestCases,full_cycle_orientation_cases:cycleCases,four_six_eight_cycle_formula_matches:true,oriented_eight_cycle_first_cycle_counts:{directed:180,bipartite:350},W34:{vertices:170,edges:425,regular_degree:5,undirected_girth:girth,connected:true,projective_points:85,isotropic_lines:85,fingerprint_FNV32:fnv(edge0.map(e=>`${e.u}:${e.v}`).join(";")),random_orientation_FNV32:fnv(orientBits),exact_forest_subgraph_DP_cases:treeDPCases,forest_queries_per_orientation:8*35,mathematical_random_orientation_SAT_probability_upper_bound:witnessBound,random_orientation_SAT_status:"NOT CERTIFIED (only universal probability bound)"},result:"forest moment identity and high-girth same-skeleton randomized NO existence have symbolic proofs; finite tests computational",independent_math_review:"OPEN",unrestricted_lower_bound:"OPEN",P_vs_NP:"OPEN"}
};
process.stdout.write(JSON.stringify(audit(),null,2)+'\n');
