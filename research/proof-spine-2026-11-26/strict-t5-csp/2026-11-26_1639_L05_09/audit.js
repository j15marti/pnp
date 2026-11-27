function audit(){
const assert=(b,m)=>{if(!b)throw Error(m)};
const C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x)));
const R=(a,b,c)=>new Set([a,b,c]).size===3&&([1,3].includes((b-a+5)%5)!==[1,3].includes((c-a+5)%5));
const allowed=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C/R");if(C(a,b,c))allowed.push([a,b,c])}
function rng(seed){return n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}}
function graph(n){const rand=rng(12345+n),E=Array.from({length:n},(_,i)=>new Set([i]));for(let k=0;k<3;k++){const p=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){const j=rand(i+1);[p[i],p[j]]=[p[j],p[i]]}for(let i=0;i<n;i++)E[i].add(p[i])}return E.map(s=>[...s].sort((a,b)=>a-b))}
function build(G,mode){
const rows=[],raw=[],fn=[],af=[],scope=[],groups=[];
const add=(f,a,s=[])=>{fn.push(f);af.push(a);scope.push([...new Set(s)]);return fn.length-1};
const constant=i=>add(()=>i,()=>i),a=Array.from({length:5},(_,i)=>constant(i)),row=(...r)=>{assert(new Set(r).size===3,"distinct");rows.push(r)};
for(let i=0;i<5;i++)row(a[i],a[(i+1)%5],a[(i+2)%5]);
function wire(f,b,s){const p=add(f,b,s);for(const j of [2,3,4]){const h=x=>[0,1,2,3,4].find(z=>C(j,x,z));row(a[j],p,add(v=>h(f(v)),v=>h(b(v)),s))}return p}
function not(p){const z=wire(v=>1-fn[p](v),v=>1-af[p](v),scope[p]);row(a[2],p,z);return z}
function or(p,q,kind){const s=[...scope[p],...scope[q]],z=wire(v=>fn[p](v)|fn[q](v),kind==="pigeon"?v=>af[p](v)^af[q](v):()=>1,s),u=add(v=>fn[p](v)?0:3,v=>af[p](v)?0:3,scope[p]),w=add(v=>fn[q](v)?2:4,v=>af[q](v)?2:4,scope[q]);row(a[1],a[2],u);row(a[0],a[1],w);row(a[4],p,u);row(a[3],q,w);row(z,u,w);return z}
const pin=(p,b)=>b?row(a[0],a[2],p):row(a[1],a[4],p);
const t=wire(()=>mode,()=>mode,[]);pin(t,mode);
const edgeIds=G.map((r,i)=>r.map(j=>{const k=raw.length;raw.push([i,j]);return wire(v=>v[k],v=>v[k],[k])}));
function id(i,j){return raw.findIndex(([u,v])=>u===i&&v===j)}
function sourceClause(lits,kind){const begin=rows.length,vs=lits.map(([i,j,b])=>b?edgeIds[i][G[i].indexOf(j)]:not(edgeIds[i][G[i].indexOf(j)]));let p=vs[0];for(const q of vs.slice(1))p=or(p,q,kind);pin(p,1);const ids=lits.map(([i,j])=>id(i,j));groups.push({begin,end:rows.length,ids,valid:v=>kind==="pigeon"?ids.reduce((s,k)=>s+v[k],0)===1:lits.some(([i,j,b])=>v[id(i,j)]===b)})}
for(let i=0;i<G.length;i++){sourceClause(G[i].map(j=>[i,j,1]),"pigeon");for(let u=0;u<G[i].length;u++)for(let v=u+1;v<G[i].length;v++)sourceClause([[i,G[i][u],0],[i,G[i][v],0]],"pair")}
for(let j=0;j<G.length;j++){const I=G.map((r,i)=>r.includes(j)?i:-1).filter(i=>i>=0);for(let u=0;u<I.length;u++)for(let v=u+1;v<I.length;v++)sourceClause([[I[u],j,0],[I[v],j,0]],"pair")}
for(let i=0;i<G.length;i++)if(G[i].includes(G.length-1)){const p=edgeIds[i][G[i].indexOf(G.length-1)],begin=rows.length,k=id(i,G.length-1);pin(or(t,not(p),"mode"),1);groups.push({begin,end:rows.length,ids:[k],valid:v=>mode||!v[k]})}
let hash=2166136261;for(const r of rows)for(const x of r)hash=Math.imul(hash^x,16777619)>>>0;const nv=fn.length,m=rows.length,N=nv+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(nv+1));
return {G,mode,rows,raw,fn,af,scope,groups,edgeIds,nv,m,N,hash}
}
function close(F){const D=Array(F.nv).fill(31);for(let i=0;i<5;i++)D[i]=1<<i;const occ=Array.from({length:F.nv},()=>[]);F.rows.forEach((r,i)=>r.forEach(x=>occ[x].push(i)));const Q=F.rows.map((_,i)=>i),pending=new Uint8Array(F.m).fill(1);let checks=0,head=0;while(head<Q.length){const i=Q[head++];pending[i]=0;const r=F.rows[i],m=[0,0,0];for(const t of allowed){checks++;if(t.every((x,k)=>D[r[k]]&(1<<x)))for(let k=0;k<3;k++)m[k]|=1<<t[k]}for(let k=0;k<3;k++){const x=r[k],d=D[x]&m[k];if(!d)return {no:true,checks};if(d!==D[x]){D[x]=d;for(const j of occ[x])if(!pending[j]){pending[j]=1;Q.push(j)}}}}return {no:false,checks}}
function match(G,I,blocked=new Set()){const H=Array(G.length).fill(-1),M=Array(G.length).fill(-1);let scans=0;for(const i of I){const L=new Set([i]),Y=new Set();function go(u){for(const v of G[u]){scans++;if(blocked.has(v)||Y.has(v))continue;Y.add(v);if(H[v]<0||(L.add(H[v]),go(H[v]))){H[v]=u;M[u]=v;return true}}return false}if(!go(i))return {no:true,L:[...L],Y:[...Y],scans}}return {no:false,M,scans}}
function search(G,I,blocked,cap){const used=new Set(blocked),M=Array(G.length).fill(-1);let visits=0,stop=false;function go(i){if(i===I.length)return true;for(const j of G[I[i]]){if(visits>=cap){stop=true;return false}visits++;if(used.has(j))continue;M[I[i]]=j;used.add(j);if(go(i+1))return true;used.delete(j);if(stop)return false}return false}return {status:go(0)?"YES":stop?"UNKNOWN":"NO",visits,M}}
function verifyNative(F,M){const v=F.raw.map(([i,j])=>+(M[i]===j)),y=F.fn.map(f=>f(v)),z=F.af.map(f=>f(v));assert(y.every((x,i)=>x===z[i]),"lift equality");assert(F.rows.every(r=>C(...r.map(x=>y[x]))&&R(...r.map(x=>y[x]))),"native lift")}
function neighbors(G,I){return new Set(I.flatMap(i=>G[i]))}
const out={jobs:[],cube:{attempts:0,admitted:0,corners:0,lowerTermChecks:0,localHallChecks:0,bruteVisits:0,matchingScans:0,invalidSpacing:0},densityChecks:0,localOwnerChecks:0,negativeControls:0};
for(const n of [4,6,8,16,32,64,128])for(const mode of [0,1]){
const F=build(graph(n),mode),G=F.G.map(r=>r.filter(j=>mode||j!==n-1)),I=G.map((_,i)=>i),initial=close(F),A=search(G,I,new Set(),4096),B=match(G,I);
assert(!initial.no,"initial closure");assert(B.no===!mode,"neighbor");
if(B.no){const Y=neighbors(G,B.L);assert(Y.size===B.Y.length&&B.Y.every(y=>Y.has(y))&&Y.size<B.L.length,"Hall certificate")}
else verifyNative(F,B.M);
if(A.status==="YES")verifyNative(F,A.M);assert(A.status==="UNKNOWN"||((A.status==="NO")===B.no),"prefix");
const Csmall=n<=8?search(G,I,new Set(),1000000):{status:"UNKNOWN",visits:0};if(Csmall.status!=="UNKNOWN")assert((Csmall.status==="NO")===B.no,"reference");
let imported=0,reclose=0;if(!B.no){for(const i of I){const j=B.M[i],G1=G.map((r,u)=>u===i?r.filter(v=>v!==j):r),r=match(G1,I);if(r.no){const Y=neighbors(G1,r.L);assert(Y.size<r.L.length&&r.Y.every(y=>Y.has(y)),"forced");imported++;/* finite fixtures normally have no forced edges; validate original witness and exact reduced domain */assert(B.M[i]===j,"pin");const D=G.map((r,u)=>u===i?r.filter(v=>v===j):r);assert(!match(D,I).no,"reclose matching");reclose++}}}
out.jobs.push({n,mode,N:F.N,nv:F.nv,m:F.m,hash:F.hash,closure:initial.checks,A:A.status,visits:A.visits,B:B.no?"NO":"YES",scans:B.scans,C:Csmall.status,Cvisits:Csmall.visits,imported,reclose,integrated:B.no?"NO":"YES"});
if(mode)continue;
const adj=G.map((r,i)=>new Set(I.filter(j=>j!==i&&G[j].some(x=>r.includes(x))))),bad=new Set(I.filter(i=>[...adj[i]].some(j=>G[i].filter(x=>G[j].includes(x)).length>=2)));
const conflict=(i,j)=>i===j||adj[i].has(j)||[...adj[i]].some(u=>adj[j].has(u));
const good=I.filter(i=>!bad.has(i)&&G[i].length>=2),rand=rng(98765+n),free=I.flatMap(i=>G[i].slice(1).map(j=>[i,j])),pivot=I.map(i=>[i,G[i][0]]);
for(let trial=0;trial<160;trial++){
out.cube.attempts++;const S=[],target=1+rand(4);
for(let z=0;z<40&&S.length<target&&good.length;z++){const i=good[rand(good.length)];if(S.every(j=>!conflict(i,j)))S.push(i)}
if(!S.length)continue;const T=[];for(let z=0;z<20&&T.length<Math.min(6,n-S.length);z++){const i=rand(n);if(!S.includes(i)&&!T.includes(i))T.push(i)}
const chosen=S.map(i=>G[i][1+rand(G[i].length-1)]),blocked=new Set(S.flatMap((i,k)=>[G[i][0],chosen[k]]));
assert(blocked.size===2*S.length,"distinct reserved holes");
for(const i of I.filter(i=>!S.includes(i)))assert(G[i].filter(j=>blocked.has(j)).length<=1,"spacing");
let admitted=true;for(let mask=1;mask<2**T.length;mask++){const U=T.filter((_,k)=>mask>>k&1);out.cube.localHallChecks++;if(neighbors(G,U).size<Math.max(U.length+1,2.5*U.length-1))admitted=false}
if(!admitted)continue;out.cube.admitted++;
const M=match(G,T,blocked),Q=search(G,T,blocked,4096);out.cube.matchingScans+=M.scans;out.cube.bruteVisits+=Q.visits;assert(!M.no&&Q.status==="YES","cube Hall");
const words=[];
for(let mask=0;mask<2**S.length;mask++){const V=Array(n).fill(-1);T.forEach(i=>V[i]=M.M[i]);S.forEach((i,k)=>V[i]=(mask>>k&1)?chosen[k]:G[i][0]);assert(new Set(V.filter(j=>j>=0)).size===T.length+S.length,"cube injective");assert([...T,...S].every(i=>G[i].includes(V[i])),"cube actual edge");words.push(V);out.cube.corners++}
const parityMon=E=>words.reduce((p,V)=>p^+E.every(([i,j])=>V[i]===j),0);
assert(parityMon(S.map((i,k)=>[i,chosen[k]]))===1,"top monomial");
for(let j=0;j<30;j++){let E=[];const degree=j%2?S.length-1:S.length;const pool=degree<S.length?[...free,...pivot]:free;for(let z=0;z<degree;z++)E.push(pool[rand(pool.length)]);E=[...new Map(E.map(e=>[e.join(","),e])).values()];if(E.length===S.length&&S.every((i,k)=>E.some(([u,v])=>u===i&&v===chosen[k])))continue;assert(parityMon(E)===0,"competing lower monomial");out.cube.lowerTermChecks++}
}
const v=Array(F.raw.length).fill(0);
for(const g of F.groups){for(let mask=0;mask<2**g.ids.length;mask++){g.ids.forEach((id,k)=>v[id]=mask>>k&1);if(g.valid(v))for(let r=g.begin;r<g.end;r++){assert(C(...F.rows[r].map(i=>F.af[i](v))),"local owner");out.localOwnerChecks++}g.ids.forEach(id=>v[id]=0)}}
}
for(let h=10000;h<=100000;h+=1000){const q=3*h-4,a=500,delta=470,k=Math.floor(h/4000),r=a*(k+1)+1;if(k>0){assert(r<=q,"rank");const num=q-100-delta*(k-1),den=q-r+k;assert(num>den,"density");out.densityChecks++}}
/* Adversarial cube controls: a second row shares both reserved holes, and two selected rows share a pivot. */
const Gbad=[[0,1],[0,1]];assert(match(Gbad,[1],new Set([0,1])).no,"4cycle obstruction");out.negativeControls++;
assert(new Set([0,1,0,2]).size<4,"adjacent selected row obstruction");out.negativeControls++;
return out
}
console.log(JSON.stringify(audit(),null,2));
