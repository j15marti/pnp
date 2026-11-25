function run(){
const stats={decisions:0,scans:0,forced:0,nonbrick:0,brick:0,transitions:0,bruteWords:0,checks:0};
const all=[0,1,2,3];
function adj(n,E){const a=Array.from({length:n},()=>new Map());for(const [u,v,s] of E){if(u===v)throw Error("loop");if(!a[u].has(v))a[u].set(v,[]);if(!a[v].has(u))a[v].set(u,[]);a[u].get(v).push(s);a[v].get(u).push(s)}return a}
function allowed(a,u,v,x,y){stats.transitions++;return !(a[u].get(v)||[]).includes(x^y)}
function decide(n,E,lists){
stats.decisions++;const a=adj(n,E), L=lists.map(x=>x.slice()),live=new Set(all.slice(0,0));for(let v=0;v<n;v++)live.add(v);
if(a.some(m=>[...m.values()].reduce((s,t)=>s+t.length,0)>4))return null;
while(true){stats.scans++;let v=-1;for(const u of live){if(!L[u].length)return false;if(L[u].length===1){v=u;break}}if(v<0)break;stats.forced++;const x=L[v][0];live.delete(v);for(const [w,ss] of a[v])if(live.has(w))L[w]=L[w].filter(y=>!ss.includes(x^y))}
for(const v of live){let d=0;for(const [w,ss] of a[v])if(live.has(w))d+=ss.length;if(L[v].length<d)return null}
const disc=Array(n).fill(0),low=Array(n).fill(0),stack=[],blocks=[],roots=[];let tm=0;
function dfs(u,p){disc[u]=low[u]=++tm;for(const v of a[u].keys()){if(!live.has(v))continue;if(!disc[v]){stack.push([u,v]);dfs(v,u);low[u]=Math.min(low[u],low[v]);if(low[v]>=disc[u]){let es=[],e;do{e=stack.pop();es.push(e)}while(e[0]!==u||e[1]!==v);blocks.push(es)}}else if(v!==p&&disc[v]<disc[u]){stack.push([u,v]);low[u]=Math.min(low[u],disc[v])}}}
for(const v of live)if(!disc[v]){roots.push(v);dfs(v,-1)}
const B=blocks.map(es=>{const V=[...new Set(es.flat())],G=new Map(V.map(v=>[v,[]]));for(const [u,v] of es){G.get(u).push(v);G.get(v).push(u)}const k=a[es[0][0]].get(es[0][1]).length;const uniform=es.every(([u,v])=>a[u].get(v).length===k);const clique=uniform&&es.length===V.length*(V.length-1)/2,cycle=uniform&&V.length>=3&&V.every(v=>G.get(v).length===2);return {V,G,clique,cycle}});
const incidence=Array.from({length:n},()=>[]);B.forEach((b,i)=>b.V.forEach(v=>incidence[v].push(i)));
function component(v){const seenV=new Set([v]),seenB=new Set(),q=[v];for(let i=0;i<q.length;i++)for(const j of incidence[q[i]])if(!seenB.has(j)){seenB.add(j);for(const w of B[j].V)if(!seenV.has(w)){seenV.add(w);q.push(w)}}return seenB}
function vm(v,p){let D=L[v].slice();for(const j of incidence[v])if(j!==p){const S=bm(j,v);D=D.filter(x=>S.includes(x))}return D}
function bm(j,p){const b=B[j],D=new Map(b.V.filter(v=>v!==p).map(v=>[v,vm(v,j)]));let out=[];
for(const x of L[p]){D.set(p,[x]);let ok=false;
if(b.clique){const V=[p,...b.V.filter(v=>v!==p)],chosen=[];function rec(i){if(i===V.length)return true;const v=V[i];for(const y of D.get(v))if(chosen.every((z,t)=>allowed(a,V[t],v,z,y))){chosen.push(y);if(rec(i+1))return true;chosen.pop()}return false}ok=rec(0)}
else {const order=[p];let prev=-1,u=p;while(order.length<b.V.length){const v=b.G.get(u).find(w=>w!==prev&&w!==p);if(v===undefined)throw Error("cycle order");order.push(v);prev=u;u=v}let S=[x];for(let i=1;i<order.length;i++){const u=order[i-1],v=order[i];S=D.get(v).filter(y=>S.some(z=>allowed(a,u,v,z,y)))}ok=S.some(y=>allowed(a,order.at(-1),p,y,x))}
if(ok)out.push(x)}return out}
for(const v of roots){const bs=component(v);if([...bs].some(j=>!B[j].clique&&!B[j].cycle)){stats.nonbrick++;continue}stats.brick++;if(!vm(v,-1).length)return false}return true
}
function solve(n,E,L){let d=decide(n,E,L);if(d!==true)return d;const P=L.map(x=>x.slice());for(let v=0;v<n;v++){let found=false;for(const x of P[v]){const Q=P.map(z=>z.slice());Q[v]=[x];if(decide(n,E,Q)===true){P[v]=[x];found=true;break}}if(!found)throw Error("self reduction failed")}return P.map(x=>x[0])}
function brute(n,E,L){let x=[];function rec(i){if(i===n){stats.bruteWords++;return E.every(([u,v,s])=>(x[u]^x[v])!==s)}for(const z of L[i]){x[i]=z;if(rec(i+1))return true}return false}return rec(0)}
const check=(b)=>{stats.checks++;if(!b)throw Error("assertion")};const full=n=>Array.from({length:n},()=>all.slice());let seed=20261124;function rand(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
let sat=0,unsat=0,unknown=0;function test(n,E,L,ref){const w=solve(n,E,L);const d=Array.isArray(w)?true:w;if(ref!==null)check(d===ref);else check(d===null);if(d===true){sat++;check(w.every((x,i)=>L[i].includes(x)));check(E.every(([u,v,s])=>(w[u]^w[v])!==s))}else if(d===false)unsat++;else unknown++;return d}
for(let t=0;t<300;t++){let n=2+rand(6),E=[],deg=Array(n).fill(0);for(let j=0;j<20;j++){let u=rand(n),v=rand(n),s=rand(4);if(u!==v&&deg[u]<4&&deg[v]<4){E.push([u,v,s]);deg[u]++;deg[v]++}}let L=full(n);for(let i=0;i<n;i++){if(rand(5)===0)L[i]=[rand(4)];else if(deg[i]<4&&rand(3)===0)L[i]=all.slice(0,Math.max(2,deg[i]))}test(n,E,L,brute(n,E,L))}
const cycles=[];for(const k of [3,5,9,33,129])for(const fix of [false,true]){let E=[];for(let i=0;i<k;i++){const s=fix&&i===k-1?1:0;E.push([i,(i+1)%k,s],[i,(i+1)%k,s^2])}cycles.push({k,fix,result:test(k,E,full(k),fix)})}
test(2,all.map(s=>[0,1,s]),full(2),false);
const stars=[];for(const n of [3,4,7,16,64,128]){let E=[];for(let i=0;i<n;i++){const a=i,b=(i+1)%n,c=(i+2)%n,y=n+i,s=rand(2),t=rand(2),u=rand(2),v=rand(2);E.push([a,y,s],[a,y,s^2],[b,y,t^1],[c,y,u^3^(2*v)])}stars.push({n,result:test(2*n,E,full(2*n),true)})}
const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let piv=[];function pm(i,used){if(i===7)return true;for(const p of F[i])if(!used.has(p)){used.add(p);piv[i]=p;if(pm(i+1,used))return true;used.delete(p)}return false}check(pm(0,new Set()));let E=[];for(let i=0;i<7;i++){const a=piv[i],[b,c]=F[i].filter(x=>x!==a);E.push([a,7+i,0],[a,7+i,2],[b,7+i,1],[c,7+i,3])}const fanoNative=test(14,E,full(14),true);const doubled=E.concat(E.map(([u,v,s],i)=>[u,v+7,i%4===3?s^2:s]));const fanoDoubled=test(21,doubled,full(21),null);
let fano=0,neighbors=[];for(let variant=-1;variant<21;variant++){let ct=0;for(let x=0;x<128;x++)if(F.every((e,i)=>{const a=e.map((v,j)=>((x>>v)&1)^Number(variant===3*i+j));return a.some(v=>v!==a[0])}))ct++;if(variant<0){fano=ct;check(ct===0)}else{neighbors.push(ct);check(ct===10)}}
let budgetNeighbors=[];for(let j=0;j<14;j++){let ct=0;for(let x=0;x<128;x++)if(F.every((e,i)=>{const a=e.map(v=>(x>>v)&1);return a.some(v=>v!==a[0])||(i===Math.floor(j/2)&&a[0]===j%2)}))ct++;budgetNeighbors.push(ct);check(ct===5)}
return {seed:20261124,sat,unsat,unknown,cycles,stars,fanoNative,fanoDoubled,fano,neighbors,budgetNeighbors,stats}
}
console.log(JSON.stringify(run(),null,2));
