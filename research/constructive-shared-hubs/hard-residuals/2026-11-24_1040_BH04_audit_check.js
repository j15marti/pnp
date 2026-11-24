function main(){
"use strict";
const check=(b,msg)=>{if(!b)throw Error(msg)};
let seed=20261124;const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
const stats={localWords:0,closureScans:0,forced:0,matchingEdgeVisits:0,coreEdges:0,cycleEdgeVisits:0,liftChecks:0,referenceWords:0,coreProjectionChecks:0};
const value=(l,x)=>l[0]<0?l[1]:x[l[0]]^l[1];
const ok=(c,x)=>c.some(l=>value(l,x)!==value(c[0],x));
const plain=E=>E.map(c=>c.map(v=>[v,0]));
const verify=(C,x,pins)=>{stats.liftChecks+=C.length;return C.every(c=>ok(c,x))&&Object.entries(pins).every(([v,b])=>x[v]===b)};
function close(n,C,pins){
let x=Array(n).fill(-1);for(const [v,b] of Object.entries(pins))x[v]=b;
for(;;){let changed=false, active=[];for(let i=0;i<C.length;i++){
stats.closureScans++;let c=C[i],vs=[...new Set(c.map(l=>l[0]).filter(v=>v>=0&&x[v]<0))],mask=Array(vs.length).fill(0),good=0;
for(let w=0;w<2**vs.length;w++){stats.localWords++;let y=x.slice();vs.forEach((v,j)=>y[v]=(w>>j)&1);if(ok(c,y)){good++;vs.forEach((v,j)=>mask[j]|=1<<y[v])}}
if(!good)return {unsat:true};if(good!==2**vs.length)active.push(i);
let j=mask.findIndex(a=>a===1||a===2);if(j>=0){x[vs[j]]=mask[j]===1?0:1;stats.forced++;changed=true;break}
}if(!changed)return {x,active}}
}
function matching(adj,n){
let mv=Array(n).fill(-1),mc=Array(adj.length).fill(-1);
function aug(i,seen){for(const v of adj[i]){stats.matchingEdgeVisits++;if(seen.has(v))continue;seen.add(v);if(mv[v]<0||aug(mv[v],seen)){mv[v]=i;mc[i]=v;return true}}return false}
for(let i=0;i<adj.length;i++)aug(i,new Set());
let J=new Set(),V=new Set(),q=[];mc.forEach((v,i)=>{if(v<0){J.add(i);q.push(i)}});
for(let k=0;k<q.length;k++)for(const v of adj[q[k]]){stats.coreEdges++;if(V.has(v))continue;V.add(v);check(mv[v]>=0,"augmenting path");if(!J.has(mv[v])){J.add(mv[v]);q.push(mv[v])}}
check(J.size-V.size===mc.filter(v=>v<0).length,"Hall deficit");return {mc,J,V}
}
function scc(A){
let n=A.length,I=Array(n).fill(-1),low=Array(n),on=Array(n).fill(false),stack=[],parts=[],id=Array(n),t=0;
function dfs(v){I[v]=low[v]=t++;stack.push(v);on[v]=true;for(const [u] of A[v]){if(I[u]<0){dfs(u);low[v]=Math.min(low[v],low[u])}else if(on[u])low[v]=Math.min(low[v],I[u])}if(low[v]===I[v]){let a=[],u;do{u=stack.pop();on[u]=false;id[u]=parts.length;a.push(u)}while(u!==v);parts.push(a)}}
for(let v=0;v<n;v++)if(I[v]<0)dfs(v);return {parts,id}
}
// Test backend ONLY: bounded exhaustive search of simple directed cycles.
// The paper's polynomial algorithm uses RST even-cycle recognition instead.
function cycle(A,part,id,limit){
let count=0,done=false,found=null,seen=new Set(),path=[];
for(const start of part.slice().sort((a,b)=>a-b)){
seen.add(start);
function dfs(v,p){for(const e of A[v]){let [u,b]=e;if(id[u]!==id[start]||u<start)continue;stats.cycleEdgeVisits++;if(++count>limit){done=true;return}if(u===start){if((p^b)===0){found=path.concat([[v,u,b]]);return}}else if(!seen.has(u)){seen.add(u);path.push([v,u,b]);dfs(u,p^b);path.pop();seen.delete(u);if(found||done)return}}}
dfs(start,0);seen.delete(start);if(found||done)break
}return {found,unknown:done,count}
}
function prepare(n,C,pins={},limit=250000){
const z=close(n,C,pins);if(z.unsat)return {status:"UNSAT",reason:"closure"};
let {x,active}=z,adj=active.map(i=>[...new Set(C[i].map(l=>l[0]).filter(v=>v>=0&&x[v]<0))]),{mc,J,V}=matching(adj,n);
let A=Array.from({length:n+1},()=>[]),core=[...J].map(i=>active[i]);
for(let i=0;i<active.length;i++){if(J.has(i))continue;let r=mc[i];check(r>=0&&!V.has(r),"exterior matching");let c=C[active[i]],s=c.find(l=>l[0]===r)[1];for(const l of c){if(l[0]===r)continue;let v=l[0];if(v<0||x[v]>=0)A[r].push([n,1^s^value(l,x)]);else A[r].push([v,1^s^l[1]])}check(A[r].length>0,"nonempty arcs")}
let {parts,id}=scc(A),cycles=[],roots=[],examined=0;
for(let i=0;i<parts.length;i++){let P=parts[i];if(P.some(v=>A[v].some(([u])=>id[u]!==i)))continue;if(P.length===1&&!A[P[0]].length){roots.push(P[0]);continue}
let q=cycle(A,P,id,limit);examined+=q.count;
if(q.unknown)return {status:"UNKNOWN",reason:"cycle cap",examined,coreSize:core.length};
if(!q.found)return {status:"UNSAT",reason:"closed SCC has no parity-zero simple cycle",examined,coreSize:core.length};cycles.push(q.found)
}
function lift(coreAssignment={}){
let y=x.concat([0]);for(const v of V){check(coreAssignment[v]===0||coreAssignment[v]===1,"core assignment missing");y[v]=coreAssignment[v]}
for(const r of roots)if(y[r]<0)y[r]=0;
for(const cyc of cycles){let v=cyc[0][0];check(y[v]<0,"cycle disjoint");y[v]=0;for(const [a,b,p] of cyc){let w=y[a]^p;if(y[b]>=0)check(y[b]===w,"cycle parity");else y[b]=w}}
let R=Array.from({length:n+1},()=>[]);A.forEach((es,v)=>es.forEach(([u,p])=>R[u].push([v,p])));
let q=[];y.forEach((b,v)=>{if(b>=0)q.push(v)});for(let k=0;k<q.length;k++){let u=q[k];for(const [v,p] of R[u])if(y[v]<0){y[v]=y[u]^p;q.push(v)}}
check(y.every(b=>b>=0),"unreached node");y.pop();check(verify(C,y,pins),"source witness mismatch");return y
}
if(!core.length)return {status:"SAT",witness:lift(),examined,cycleCount:cycles.length,coreSize:0};
return {status:"CORE",core,coreV:[...V],x,lift,examined,cycleCount:cycles.length,coreSize:core.length}
}
function ref(n,C,pins={}){let count=0;for(let w=0;w<2**n;w++){stats.referenceWords++;let x=Array.from({length:n},(_,v)=>(w>>v)&1);if(Object.entries(pins).every(([v,b])=>x[v]===b)&&C.every(c=>ok(c,x)))count++}return count}
function audit(n,C,pins={}){
let ct=ref(n,C,pins),r=prepare(n,C,pins),projected=0;
check(r.status!=="UNKNOWN","small test cap");if(r.status==="CORE"){for(let w=0;w<2**r.coreV.length;w++){let y=r.x.slice(),a={};r.coreV.forEach((v,j)=>y[v]=a[v]=(w>>j)&1);stats.coreProjectionChecks++;if(r.core.every(i=>ok(C[i],y))){r.lift(a);projected++}}check((ct>0)===(projected>0),"core projection")}else check((ct>0)===(r.status==="SAT"),"terminal mismatch");return {models:ct,status:r.status,coreSize:r.coreSize??0,projected}
}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let F=plain(fano),fanoRoot=audit(7,F),fanoNeighbors=[];
for(let i=0;i<7;i++)for(let b=0;b<2;b++){let C=F.map((c,j)=>j===i?c.concat([[-1,b]]):c);let a=audit(7,C);check(a.models===5&&a.status==="SAT","Fano neighbor");fanoNeighbors.push(a)}
let random={SAT:0,UNSAT:0,CORE:0,referenceSAT:0,referenceUNSAT:0,coreSAT:0,coreUNSAT:0};
for(let t=0;t<320;t++){let n=3+rnd(6),m=1+rnd(12),C=[],pins={};for(let i=0;i<m;i++){let k=2+rnd(Math.min(3,n-1)),vs=[];while(vs.length<k){let v=rnd(n);if(!vs.includes(v))vs.push(v)}let c=vs.map(v=>[v,rnd(2)]);if(rnd(4)===0)c.push([-1,rnd(2)]);C.push(c)}if(t%3===0)pins[rnd(n)]=rnd(2);let a=audit(n,C,pins);random[a.status]++;random[a.models?"referenceSAT":"referenceUNSAT"]++;if(a.status==="CORE")random[a.models?"coreSAT":"coreUNSAT"]++}
function chain(){let n=1,E=[];function eq(a,b){let p=n++,w=n++,x=n++,y=n++,z=n++;E.push([a,w,x],[a,y,z],[b,w,y],[b,x,z],[p,w,z],[p,x,y])}let ends=[];for(let k=0;k<2;k++){let a=0;for(let i=0;i<4;i++){let b=n++;eq(a,b);a=b}ends.push(a)}E.push([0,...ends]);return {n,E}}
function stretch(G){let n=G.n,E=[];function eq(a,b){let p=n++,w=n++,x=n++,y=n++,z=n++;E.push([a,w,x],[a,y,z],[b,w,y],[b,x,z],[p,w,z],[p,x,y])}for(const e of G.E){let copy=[];for(const a of e){let b=n++;copy.push(b);eq(a,b)}E.push(copy)}return {n,E}}
function stretchedTests(G,which,cap){let C=plain(G.E),r=prepare(G.n,C,{},cap);check(r.status==="UNSAT"||r.status==="UNKNOWN","critical root");let a={n:G.n,m:C.length,root:r.status,rootReason:r.reason,rootCycleVisits:r.examined,neighbors:{SAT:0,UNSAT:0,CORE:0,UNKNOWN:0}};for(let i of which)for(let b=0;b<2;b++){let D=C.map((c,j)=>i===j?c.concat([[-1,b]]):c);let s=prepare(G.n,D,{},cap);check(s.status==="SAT"||s.status==="UNKNOWN","critical neighbor");a.neighbors[s.status]++}return a}
let G=chain(),H=stretch(G),scales=[stretchedTests(G,[...G.E.keys()],250000),stretchedTests(H,[0,Math.floor(H.E.length/2),H.E.length-1],250000)];
// Generalized quadrangle GQ(2,2): K6 edges as points, perfect matchings as triples.
let pairs=[];for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)pairs.push([a,b]);
let lines=[];function pm(V,es){if(!V.length){lines.push(es);return}let a=V[0];for(let b of V.slice(1)){let idx=pairs.findIndex(p=>p[0]===a&&p[1]===b);pm(V.filter(v=>v!==a&&v!==b),es.concat(idx))}}pm([0,1,2,3,4,5],[]);
let covers=[];for(let k of [1,8,32,64]){let E=[];let maps=lines.map(c=>c.map(v=>{let p=Array.from({length:k},(_,i)=>i);for(let i=k-1;i>0;i--){let j=rnd(i+1);[p[i],p[j]]=[p[j],p[i]]}return p}));for(let j=0;j<lines.length;j++)for(let i=0;i<k;i++)E.push(lines[j].map((v,t)=>v*k+maps[j][t][i]));let n=15*k, C=plain(E);let planted=Array.from({length:n},(_,v)=>pairs[Math.floor(v/k)].includes(0)?1:0);check(verify(C,planted,{}),"planted cover");let r=prepare(n,C,{},250000);check(r.status==="SAT"||r.status==="UNKNOWN","cover");covers.push({n,m:E.length,status:r.status,cycleVisits:r.examined,cycleCount:r.cycleCount??null})}
return {seed:20261124,fanoRoot,fanoNeighbors,random,scales,covers,stats,backend:"bounded exhaustive simple directed cycle search, not RST",discrepancies:0}
}
console.log(JSON.stringify(main(),null,2));
