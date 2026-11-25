function audit(){
const bit=i=>1n<<BigInt(i), par=x=>{let p=0;while(x){p^=1;x&=x-1n}return p}, assert=(x,s)=>{if(!x)throw Error(s)};
let seed=20261125, checks=0, flowCalls=0, closureRounds=0, probes=0; const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
function lin(n,rows){let a=rows.slice(),r=0, piv=[];for(let j=0;j<n;j++){let k=a.findIndex((x,i)=>i>=r&&!!(x&bit(j)));if(k<0)continue;[a[r],a[k]]=[a[k],a[r]];for(let i=0;i<a.length;i++)if(i!==r&&(a[i]&bit(j)))a[i]^=a[r];piv.push(j);r++}if(a.some(x=>x===bit(n)))return null; a=a.slice(0,r);let base=0n;for(let i=0;i<r;i++)if(a[i]&bit(n))base|=bit(piv[i]);let dirs=[];for(let j=0;j<n;j++)if(!piv.includes(j)){let d=bit(j);for(let i=0;i<r;i++)if(a[i]&bit(j))d|=bit(piv[i]);dirs.push(d)}return {rows:a,base,dirs}}
const eq=(n,mask,rhs)=>mask|(rhs?bit(n):0n);
function entails(n,A,mask,rhs){return par(A.base&mask)===rhs&&A.dirs.every(d=>!par(d&mask))}
function hull(n,points,dirs=[]){if(!points.length)return null;let base=points[0];let span=points.slice(1).map(p=>p^base).concat(dirs);let annih=lin(n,span);return lin(n,annih.dirs.map(d=>eq(n,d,par(d&base))))}
const has=(A,x,n)=>A!==null&&A.rows.every(r=>par((r&(bit(n)-1n))&x)===Number(!!(r&bit(n))));
function sideHull(n,P,Q,pins){flowCalls++;let k=P.length,H=2*k,V=H+1,SS=V,TT=V+1,W=V+2, arcs=[],L=[],R=[];P.forEach((c,i)=>c.forEach(v=>L[v]=i));Q.forEach((c,i)=>c.forEach(v=>R[v]=k+i));
for(let i=0;i<n;i++)arcs.push([L[i],R[i],pins[i]??0,pins[i]??1]);
for(let i=0;i<k;i++)arcs.push([H,i,1,2]);for(let i=0;i<k;i++)arcs.push([k+i,H,1,2]);
let g=Array.from({length:W},()=>[]), bal=Array(V).fill(0),refs=[];
function add(u,v,c){let a={v,c,rev:g[v].length},b={v:u,c:0,rev:g[u].length};g[u].push(a);g[v].push(b);return a}
for(const [u,v,l,h] of arcs){refs.push(add(u,v,h-l));bal[v]+=l;bal[u]-=l}let total=0;for(let i=0;i<V;i++){if(bal[i]>0){add(SS,i,bal[i]);total+=bal[i]}if(bal[i]<0)add(i,TT,-bal[i])}
let got=0;while(true){let p=Array(W).fill(null),q=[SS];p[SS]=[-1,-1];for(let j=0;j<q.length&&!p[TT];j++){let u=q[j];g[u].forEach((e,i)=>{if(e.c>0&&!p[e.v]){p[e.v]=[u,i];q.push(e.v)}})}if(!p[TT])break;let d=Infinity;for(let v=TT;v!==SS;){let [u,i]=p[v];d=Math.min(d,g[u][i].c);v=u}for(let v=TT;v!==SS;){let [u,i]=p[v],e=g[u][i];e.c-=d;g[v][e.rev].c+=d;v=u}got+=d}
if(got!==total)return null;let f=arcs.map((a,i)=>a[3]-refs[i].c), reach=Array.from({length:V},(_,i)=>Array.from({length:V},(_,j)=>i===j));
for(let i=0;i<arcs.length;i++){let [u,v,l,h]=arcs[i];if(f[i]<h)reach[u][v]=true;if(f[i]>l)reach[v][u]=true}
for(let k=0;k<V;k++)for(let i=0;i<V;i++)if(reach[i][k])for(let j=0;j<V;j++)if(reach[k][j])reach[i][j]=true;
let rows=[];for(let i=0;i<arcs.length;i++){let [u,v,l,h]=arcs[i];if(l===h||!reach[u][v]||!reach[v][u]){let mask=i<n?bit(i):(i<n+k?P[i-n]:Q[i-n-k]).reduce((s,v)=>s|bit(v),0n);rows.push(eq(n,mask,f[i]&1))}}
let A=lin(n,rows);assert(A!==null,"flow hull inconsistent");let w=f.slice(0,n).reduce((s,v,i)=>s|(v?bit(i):0n),0n);assert(has(A,w,n),"anchor");checks+=2;return A}
const good=(c,w)=>{let k=c.reduce((s,v)=>s+Number(!!(w&bit(v))),0);return k===1||k===2};
const valid=(n,P)=>P.every(p=>p.flat().length===n&&new Set(p.flat()).size===n&&p.every(c=>c.length===3&&new Set(c).size===3))&&(()=>{let s=new Set;for(const c of P.flat())for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=[c[i],c[j]].sort((a,b)=>a-b).join(",");if(s.has(k))return false;s.add(k)}return true})();
function close(n,P,A){if(!A)return null;while(true){closureRounds++;let rows=A.rows.slice(),pins=Array(n).fill(null);for(let v=0;v<n;v++)for(let b=0;b<2;b++)if(entails(n,A,bit(v),b))pins[v]=b;for(let p=0;p<4;p+=2){let B=sideHull(n,P[p],P[p+1],pins);if(!B)return null;rows.push(...B.rows)}for(const [a,b,c] of P.flat())for(const [u,v,w] of [[a,b,c],[a,c,b],[b,c,a]])if(entails(n,A,bit(u)^bit(v),0))rows.push(eq(n,bit(u)^bit(w),1));let B=lin(n,rows);if(!B)return null;if(B.rows.length===A.rows.length)return B;A=B}}
function solve(n,P){let A=close(n,P,lin(n,[eq(n,1n,0)]));if(!A)return "UNSAT";while(true){if(P.flat().every(c=>good(c,A.base)))return "SAT";let progress=false;for(let v=0;v<n;v++){if(A.dirs.every(d=>!(d&bit(v))))continue;probes++;let B=[0,1].map(b=>close(n,P,lin(n,A.rows.concat(eq(n,bit(v),b)))));if(!B[0]&&!B[1])return "UNSAT";let C=B[0]&&B[1]?hull(n,B.map(z=>z.base),B.flatMap(z=>z.dirs)):B[0]||B[1];assert(C.rows.length>=A.rows.length,"rank monotonic");checks++;if(C.rows.length>A.rows.length){A=close(n,P,C);if(!A)return "UNSAT";progress=true;break}}if(!progress)return "UNKNOWN"}}
const plane=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const layered=q=>Array.from({length:4},(_,p)=>Array.from({length:q},(_,i)=>[i,q+(i+p)%q,2*q+(i+2*p)%q]));
let instances=[{name:"affine_plane",n:9,P:plane},{name:"layered_5",n:15,P:layered(5)}]; 
// Random genuinely linear partitions; no planted witnesses supplied to algorithm.
for(let z=0;z<12;z++){let n=15,P=[],seen=new Set;for(let p=0;p<4;p++){let ok=false;for(let t=0;t<2500;t++){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i;i--){let j=rnd()%(i+1);[a[i],a[j]]=[a[j],a[i]]}let triples=Array.from({length:n/3},(_,j)=>a.slice(3*j,3*j+3)),pairs=triples.flatMap(c=>[[c[0],c[1]],[c[0],c[2]],[c[1],c[2]]].map(x=>x.sort((a,b)=>a-b).join(",")));if(pairs.every(x=>!seen.has(x))){P.push(triples);pairs.forEach(x=>seen.add(x));ok=true;break}}if(!ok)break}if(P.length===4)instances.push({name:"random_"+z,n,P})}
let results=[], hullQueries=0;for(const {name,n,P} of instances){assert(valid(n,P),"geometry");checks++;let words=Array.from({length:2**n},(_,i)=>BigInt(i)), full=words.filter(w=>P.flat().every(c=>good(c,w)));let outcome=solve(n,P);assert(outcome==="UNKNOWN"||outcome===(full.length?"SAT":"UNSAT"),"wrong terminal");checks++;
for(const [a,b] of [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]){let feasible=words.filter(w=>P[a].concat(P[b]).every(c=>good(c,w)));for(let t=0;t<22;t++){let pins=Array(n).fill(null);if(t>0){for(let j=0;j<(t%7)+1;j++)pins[rnd()%n]=rnd()%2}let expected=hull(n,feasible.filter(w=>pins.every((p,i)=>p===null||Number(!!(w&bit(i)))===p)));let actual=sideHull(n,P[a],P[b],pins);assert(!!actual===!!expected,"side feasible");checks++;if(actual){assert(actual.rows.length===expected.rows.length&&actual.rows.every(r=>entails(n,expected,r&(bit(n)-1n),Number(!!(r&bit(n))))),"hull wrong");checks++}hullQueries++}}
results.push({name,n,clauses:P,models:full.length,outcome})}
return {seed:20261125,checks,flowCalls,closureRounds,probes,hullQueries,results}}
console.log(JSON.stringify(audit(),null,2));
