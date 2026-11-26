function audit(){
const assert=(b,m)=>{if(!b)throw Error(m)};
const C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x)));
const R=(a,b,c)=>new Set([a,b,c]).size===3&&([1,3].includes((b-a+5)%5)!==[1,3].includes((c-a+5)%5));
let rel=0;const allowed=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C/R");if(C(a,b,c))allowed.push([a,b,c]);rel++}
function graph(n){let seed=12345+n;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};const edges=Array.from({length:n},(_,i)=>new Set([i]));for(let k=0;k<3;k++){const p=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){const j=rand()%(i+1);[p[i],p[j]]=[p[j],p[i]]}for(let i=0;i<n;i++)edges[i].add(p[i])}return edges.map(s=>[...s].sort((a,b)=>a-b))}
function build(G,mode,guards=[]){const n=G.length,clauses=[],f=[],support=[],raw=[],owners=[];const add=(fn,s=[])=>{f.push(fn);support.push([...new Set(s)]);return f.length-1};const row=(...a)=>{assert(new Set(a).size===3,"distinct names");clauses.push(a)};const a=Array.from({length:5},(_,i)=>add(()=>i));for(let i=0;i<5;i++)row(a[i],a[(i+1)%5],a[(i+2)%5]);function wire(fn,s){const p=add(fn,s);for(const j of [2,3,4]){const h=add(v=>[0,1,2,3,4].find(z=>C(j,fn(v),z)),s);row(a[j],p,h)}return p}
function not(p){const z=wire(v=>1-f[p](v),support[p]);row(a[2],p,z);return z}
function or(p,q){const s=[...support[p],...support[q]],z=wire(v=>f[p](v)|f[q](v),s),u=add(v=>f[p](v)?0:3,support[p]),w=add(v=>f[q](v)?2:4,support[q]);row(a[1],a[2],u);row(a[0],a[1],w);row(a[4],p,u);row(a[3],q,w);row(z,u,w);return z}
const pin=(p,b)=>b?row(a[0],a[2],p):row(a[1],a[4],p);
const t=wire(v=>mode,[]);pin(t,mode);
const edgeIds=G.map((r,i)=>r.map(j=>{const k=raw.length;raw.push([i,j]);return wire(v=>v[k], [k])}));
function sourceClause(lits){const begin=clauses.length;const vs=lits.map(([i,j,b])=>b?edgeIds[i][G[i].indexOf(j)]:not(edgeIds[i][G[i].indexOf(j)]));let p=vs[0];for(const q of vs.slice(1))p=or(p,q);pin(p,1);owners.push({begin,end:clauses.length,lits})}
for(let i=0;i<n;i++){sourceClause(G[i].map(j=>[i,j,1]));for(let u=0;u<G[i].length;u++)for(let v=u+1;v<G[i].length;v++)sourceClause([[i,G[i][u],0],[i,G[i][v],0]])}
for(let j=0;j<n;j++){const I=G.map((r,i)=>r.includes(j)?i:-1).filter(i=>i>=0);for(let u=0;u<I.length;u++)for(let v=u+1;v<I.length;v++)sourceClause([[I[u],j,0],[I[v],j,0]])}
for(let i=0;i<n;i++)if(G[i].includes(n-1)){const p=edgeIds[i][G[i].indexOf(n-1)];pin(or(t,not(p)),1)}
for(const [i,j,b] of guards)pin(edgeIds[i][G[i].indexOf(j)],b);
const nv=f.length,m=clauses.length,N=nv+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(nv+1));let hash=2166136261;for(const r of clauses)for(const x of r)hash=Math.imul(hash^x,16777619)>>>0;
return {n,G,mode,guards,clauses,f,support,raw,edgeIds,owners,nv,m,N,hash}}
function verify(F,M){const v=F.raw.map(([i,j])=>+(M[i]===j));const y=F.f.map(fn=>fn(v));return F.clauses.every(r=>C(...r.map(x=>y[x])))}
function close(F,pins=[]){const D=Array(F.nv).fill(31);for(let i=0;i<5;i++)D[i]=1<<i;for(const [i,j,b] of pins)D[F.edgeIds[i][F.G[i].indexOf(j)]]=1<<b;const occ=Array.from({length:F.nv},()=>[]);F.clauses.forEach((r,i)=>r.forEach(x=>occ[x].push(i)));const Q=F.clauses.map((_,i)=>i),pending=new Uint8Array(F.m).fill(1);let checks=0,head=0;while(head<Q.length){const i=Q[head++];pending[i]=0;const r=F.clauses[i],m=[0,0,0];for(const t of allowed){checks++;if(t.every((x,k)=>D[r[k]]&(1<<x)))for(let k=0;k<3;k++)m[k]|=1<<t[k]}for(let k=0;k<3;k++){const x=r[k],d=D[x]&m[k];if(!d)return {no:true,checks,D};if(d!==D[x]){D[x]=d;for(const j of occ[x])if(!pending[j]){pending[j]=1;Q.push(j)}}}}return {no:false,checks,D}}
function domain(F,pins=[]){const G=F.G.map(r=>r.filter(j=>F.mode||j!==F.n-1));for(const [i,j,b] of [...F.guards,...pins])G[i]=G[i].filter(h=>b?h===j:h!==j);return G}
function matching(G){const n=G.length,H=Array(n).fill(-1),M=Array(n).fill(-1);let scans=0;for(let i=0;i<n;i++){const L=new Set([i]),Y=new Set();function go(u){for(const v of G[u]){scans++;if(Y.has(v))continue;Y.add(v);if(H[v]<0||(L.add(H[v]),go(H[v]))){H[v]=u;M[u]=v;return true}}return false}if(!go(i))return {no:true,L:[...L],Y:[...Y],scans};}return {no:false,M,scans}}
function checkHall(G,r){const Y=new Set(r.L.flatMap(i=>G[i]));return Y.size===r.Y.length&&r.Y.every(j=>Y.has(j))&&Y.size<r.L.length}
function search(G,cap){let visits=0,aborted=false,M=Array(G.length).fill(-1),used=new Set();function rec(i){if(i===G.length)return true;for(const j of G[i]){if(visits>=cap){aborted=true;return false}visits++;if(used.has(j))continue;M[i]=j;used.add(j);if(rec(i+1))return true;used.delete(j);if(aborted)return false}return false}return {status:rec(0)?"YES":aborted?"UNKNOWN":"NO",visits,M}}
function adversary(G){let count=0,visits=0;const a=[];function go(i){if(i===G.length){count++;return}for(const j of G[i]){visits++;if(!a.includes(j)){a.push(j);go(i+1);a.pop()}}}go(0);return {count,visits}}
const result={relationChecks:rel,tests:[],substitutionChecks:0,smallExact:0,invalidCertificates:0};
for(const n of [4,6,8,16,32,64,128]){
const G=graph(n);
for(const mode of [0,1]){
const F=build(G,mode),G0=domain(F),initial=close(F),A=initial.no?{status:"NO",visits:0}:search(G0,4096),B=matching(G0);assert(B.no?!mode:!!mode,"known neighbor");if(B.no){assert(checkHall(G0,B),"Hall certificate");const bad={...B,Y:B.Y.slice(1)};if(!checkHall(G0,bad))result.invalidCertificates++}else assert(verify(F,B.M),"native B witness");if(A.status==="YES")assert(verify(F,A.M),"native A witness");assert(A.status==="UNKNOWN"||((A.status==="NO")===B.no),"A agreement");let Cstatus="UNKNOWN",cvisits=0;if(n<=8){const r=adversary(G0);Cstatus=r.count?"YES":"NO";cvisits=r.visits;assert(!!r.count===!B.no,"C reference");result.smallExact++}else if(!mode){Cstatus="NO";assert(new Set(G0.flat()).size<n,"count certificate")}else if(G0.every((r,i)=>r.includes(i))){Cstatus="YES";assert(verify(F,G0.map((_,i)=>i)),"diagonal witness")}
let imports=[],queries=0,oracleScans=0,integrated=A;if(!B.no){for(let i=0;i<n;i++){const j=B.M[i],r=matching(domain(F,[[i,j,0]]));queries++;oracleScans+=r.scans;if(r.no){assert(checkHall(domain(F,[[i,j,0]]),r),"guarded Hall");imports.push([i,j,1])}}let closeChecks=0;for(let j=0;j<imports.length;j++){const cl=close(F,imports.slice(0,j+1));closeChecks+=cl.checks;assert(!cl.no,"valid import")}integrated=search(domain(F,imports),4096);integrated.closeChecks=closeChecks;if(integrated.status==="YES")assert(verify(F,integrated.M),"combined witness")}
else integrated={status:"NO",visits:0,closeChecks:0};
// Independent per-clause local semantic audit: source clauses own exactly their gate rows.
// Disabled-hole edges are set to zero for negative mode; check all local raw words.
for(const o of F.owners){const ids=[...new Set(o.lits.map(([i,j])=>F.raw.findIndex(([u,v])=>u===i&&v===j)))];for(let mask=0;mask<2**ids.length;mask++){const x=Array(F.raw.length).fill(0);ids.forEach((id,k)=>x[id]=(mask>>k)&1);if(!mode)F.raw.forEach(([i,j],k)=>{if(j===n-1)x[k]=0});const sat=o.lits.some(([i,j,b])=>x[F.raw.findIndex(([u,v])=>i===u&&j===v)]===b);if(sat)for(let k=o.begin;k<o.end;k++){assert(C(...F.clauses[k].map(id=>F.f[id](x))),"local substituted axiom");result.substitutionChecks++}}}
result.tests.push({n,mode,nv:F.nv,m:F.m,N:F.N,hash:F.hash,initialNo:initial.no,closureChecks:initial.checks,A:A.status,visits:A.visits,B:B.no?"NO":"YES",Bscans:B.scans,C:Cstatus,Cvisits:cvisits,imports:imports.length,queries,oracleScans,combined:integrated.status,combinedVisits:integrated.visits,reclosureChecks:integrated.closeChecks??0})
}}
return result;
}
console.log(JSON.stringify(audit(),null,2));
