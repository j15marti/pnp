function run(){
const assert=(b,m)=>{if(!b)throw Error(m)};
const C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x)));
const R=(a,b,c)=>new Set([a,b,c]).size===3&&([1,3].includes((b-a+5)%5)!==[1,3].includes((c-a+5)%5));
const allowed=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"relation");if(C(a,b,c))allowed.push([a,b,c])}
const result={rel:125,localChecks:0,affineIndicatorChecks:0,negativeControl:0,tests:[],imports:0,reference:0};
function graph(n){let seed=12345+n;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};const E=Array.from({length:n},(_,i)=>new Set([i]));for(let k=0;k<3;k++){const p=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){const j=rand()%(i+1);[p[i],p[j]]=[p[j],p[i]]}for(let i=0;i<n;i++)E[i].add(p[i])}return E.map(s=>[...s].sort((a,b)=>a-b))}
function build(G,mode,guards=[]){
const n=G.length,rows=[],raw=[],fn=[],af=[],scope=[],groups=[],allOwners=[];
const add=(f,a,s=[])=>{fn.push(f);af.push(a);scope.push([...new Set(s)]);return fn.length-1};
const constant=i=>add(()=>i,()=>i);
const a=Array.from({length:5},(_,i)=>constant(i));const row=(...r)=>{assert(new Set(r).size===3,"distinct");rows.push(r)};
for(let i=0;i<5;i++)row(a[i],a[(i+1)%5],a[(i+2)%5]);
function wire(f,b,s){const p=add(f,b,s);for(const j of [2,3,4]){const h=x=>[0,1,2,3,4].find(z=>C(j,x,z));row(a[j],p,add(v=>h(f(v)),v=>h(b(v)),s))}return p}
function not(p){const z=wire(v=>1-fn[p](v),v=>1-af[p](v),scope[p]);row(a[2],p,z);return z}
function or(p,q,kind){const s=[...scope[p],...scope[q]],z=wire(v=>fn[p](v)|fn[q](v),kind==="pigeon"?v=>af[p](v)^af[q](v):()=>1,s),u=add(v=>fn[p](v)?0:3,v=>af[p](v)?0:3,scope[p]),w=add(v=>fn[q](v)?2:4,v=>af[q](v)?2:4,scope[q]);row(a[1],a[2],u);row(a[0],a[1],w);row(a[4],p,u);row(a[3],q,w);row(z,u,w);return z}
const pin=(p,b)=>b?row(a[0],a[2],p):row(a[1],a[4],p);
const t=wire(()=>mode,()=>mode,[]);pin(t,mode);
const edgeIds=G.map((r,i)=>r.map(j=>{const k=raw.length;raw.push([i,j]);return wire(v=>v[k],v=>v[k],[k])}));
function id(i,j){return raw.findIndex(([u,v])=>u===i&&v===j)}
function sourceClause(lits,kind){const begin=rows.length;const vs=lits.map(([i,j,b])=>b?edgeIds[i][G[i].indexOf(j)]:not(edgeIds[i][G[i].indexOf(j)]));let p=vs[0];for(const q of vs.slice(1))p=or(p,q,kind);pin(p,1);const ids=lits.map(([i,j])=>id(i,j));groups.push({begin,end:rows.length,ids,valid:v=>kind==="pigeon"?ids.reduce((s,k)=>s+v[k],0)===1:lits.some(([i,j,b])=>v[id(i,j)]===b)});}
for(let i=0;i<n;i++){sourceClause(G[i].map(j=>[i,j,1]),"pigeon");for(let u=0;u<G[i].length;u++)for(let v=u+1;v<G[i].length;v++)sourceClause([[i,G[i][u],0],[i,G[i][v],0]],"pair")}
for(let j=0;j<n;j++){const I=G.map((r,i)=>r.includes(j)?i:-1).filter(i=>i>=0);for(let u=0;u<I.length;u++)for(let v=u+1;v<I.length;v++)sourceClause([[I[u],j,0],[I[v],j,0]],"pair")}
for(let i=0;i<n;i++)if(G[i].includes(n-1)){const p=edgeIds[i][G[i].indexOf(n-1)],begin=rows.length,k=id(i,n-1);pin(or(t,not(p),"mode"),1);groups.push({begin,end:rows.length,ids:[k],valid:v=>mode||!v[k]})}
for(const [i,j,b] of guards){const begin=rows.length,k=id(i,j);pin(edgeIds[i][G[i].indexOf(j)],b);groups.push({begin,end:rows.length,ids:[k],valid:v=>v[k]===b})}
let hash=2166136261;for(const r of rows)for(const x of r)hash=Math.imul(hash^x,16777619)>>>0;const nv=fn.length,m=rows.length,N=nv+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(nv+1));return {G,n,mode,guards,rows,fn,af,scope,groups,raw,edgeIds,nv,m,N,hash}}
function close(F,pins=[]){const D=Array(F.nv).fill(31);for(let i=0;i<5;i++)D[i]=1<<i;for(const [i,j,b] of pins)D[F.edgeIds[i][F.G[i].indexOf(j)]]=1<<b;const occ=Array.from({length:F.nv},()=>[]);F.rows.forEach((r,i)=>r.forEach(x=>occ[x].push(i)));const Q=F.rows.map((_,i)=>i),pending=new Uint8Array(F.m).fill(1);let checks=0,head=0;while(head<Q.length){const i=Q[head++];pending[i]=0;const r=F.rows[i],m=[0,0,0];for(const t of allowed){checks++;if(t.every((x,k)=>D[r[k]]&(1<<x)))for(let k=0;k<3;k++)m[k]|=1<<t[k]}for(let k=0;k<3;k++){const x=r[k],d=D[x]&m[k];if(!d)return {no:true,checks};if(d!==D[x]){D[x]=d;for(const j of occ[x])if(!pending[j]){pending[j]=1;Q.push(j)}}}}return {no:false,checks}}
function domain(F,pins=[]){const G=F.G.map(r=>r.filter(j=>F.mode||j!==F.n-1));for(const [i,j,b] of [...F.guards,...pins])G[i]=G[i].filter(h=>b?h===j:h!==j);return G}
function match(G){const n=G.length,H=Array(n).fill(-1),M=Array(n).fill(-1);let scans=0;for(let i=0;i<n;i++){const L=new Set([i]),Y=new Set();function go(u){for(const v of G[u]){scans++;if(Y.has(v))continue;Y.add(v);if(H[v]<0||(L.add(H[v]),go(H[v]))){H[v]=u;M[u]=v;return true}}return false}if(!go(i))return {no:true,L:[...L],Y:[...Y],scans}}return {no:false,M,scans}}
function hall(G,r){const Y=new Set(r.L.flatMap(i=>G[i]));return Y.size===r.Y.length&&r.Y.every(j=>Y.has(j))&&Y.size<r.L.length}
function search(G,cap){let visits=0,aborted=false,M=Array(G.length).fill(-1),used=new Set();function rec(i){if(i===G.length)return true;for(const j of G[i]){if(visits>=cap){aborted=true;return false}visits++;if(used.has(j))continue;M[i]=j;used.add(j);if(rec(i+1))return true;used.delete(j);if(aborted)return false}return false}return {status:rec(0)?"YES":aborted?"UNKNOWN":"NO",visits,M}}
function verify(F,M){const v=F.raw.map(([i,j])=>+(M[i]===j));const y=F.fn.map(fn=>fn(v)),z=F.af.map(fn=>fn(v));return y.every((c,i)=>c===z[i])&&F.rows.every(r=>C(...r.map(x=>y[x])))}
function local(F){
const zero=Array(F.raw.length).fill(0);
for(let i=0;i<F.nv;i++){const ids=F.scope[i],base=F.af[i](zero);const values=ids.map(j=>{zero[j]=1;const c=F.af[i](zero);zero[j]=0;return c});for(let mask=0;mask<2**ids.length;mask++){ids.forEach((j,k)=>zero[j]=mask>>k&1);const c=F.af[i](zero);for(let b=0;b<5;b++){let rhs=+(base===b);ids.forEach((j,k)=>{if(zero[j])rhs^=+(values[k]===b)^+(base===b)});assert(rhs===+(c===b),"affine indicator");result.affineIndicatorChecks++}ids.forEach(j=>zero[j]=0)}}
const owned=new Set();for(const g of F.groups){for(let r=g.begin;r<g.end;r++)owned.add(r);for(let mask=0;mask<2**g.ids.length;mask++){g.ids.forEach((j,k)=>zero[j]=mask>>k&1);if(g.valid(zero))for(let r=g.begin;r<g.end;r++){assert(C(...F.rows[r].map(i=>F.af[i](zero))),"owned affine axiom");result.localChecks++}g.ids.forEach(j=>zero[j]=0)}}
for(let r=0;r<F.m;r++)if(!owned.has(r)){const ids=[...new Set(F.rows[r].flatMap(i=>F.scope[i]))];for(let mask=0;mask<2**ids.length;mask++){ids.forEach((j,k)=>zero[j]=mask>>k&1);assert(C(...F.rows[r].map(i=>F.af[i](zero))),"unowned affine axiom");result.localChecks++;ids.forEach(j=>zero[j]=0)}}
}
for(const n of [4,6,8,16,32,64])for(const mode of [0,1]){
const G=graph(n),F=build(G,mode),G0=domain(F),initial=close(F),A=initial.no?{status:"NO",visits:0}:search(G0,4096),B=match(G0);
assert(B.no===!mode,"neighbor");if(B.no)assert(hall(G0,B),"Hall");else assert(verify(F,B.M),"native lift");
if(A.status==="YES")assert(verify(F,A.M),"A lift");assert(A.status==="UNKNOWN"||((A.status==="NO")===B.no),"A agreement");
local(F);let Cstat="UNKNOWN";if(n<=8){const c=search(G0,1000000);Cstat=c.status;assert(Cstat!=="UNKNOWN"&&((Cstat==="NO")===B.no),"reference");result.reference++}
let pins=[],scans=0,reclosure=0,combined=A;if(!B.no){for(let i=0;i<n;i++){const j=B.M[i],q=match(domain(F,[[i,j,0]]));scans+=q.scans;if(q.no){assert(hall(domain(F,[[i,j,0]]),q),"import proof");pins.push([i,j,1]);const c=close(F,pins);assert(!c.no,"import closure");reclosure+=c.checks;result.imports++}}combined=search(domain(F,pins),4096);if(combined.status==="YES")assert(verify(F,combined.M),"combined lift")}else combined={status:"NO",visits:0};
result.tests.push({n,mode,nv:F.nv,m:F.m,N:F.N,hash:F.hash,raw:F.raw.length,initial:initial.no?"NO":"OPEN",closure:initial.checks,A:A.status,visits:A.visits,B:B.no?"NO":"YES",scans:B.scans,C:Cstat,imports:pins.length,importScans:scans,reclosure,combined:combined.status,combinedVisits:combined.visits})
}
for(let k=2;k<=4;k++){const p=Array.from({length:k},(_,i)=>i);for(let mask=0;mask<2**k;mask++){const ones=p.reduce((s,i)=>s+((mask>>i)&1),0);if(ones>0&&ones%2===0)result.negativeControl++}}
return result;
}
console.log(JSON.stringify(run(),null,2));
