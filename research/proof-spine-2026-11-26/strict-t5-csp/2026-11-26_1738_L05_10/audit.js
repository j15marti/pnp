function runAudit(){
const assert=(x,m)=>{if(!x)throw Error(m)};
const C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x)));
const R=(a,b,c)=>new Set([a,b,c]).size===3&&([1,3].includes((b-a+5)%5)!==[1,3].includes((c-a+5)%5));
const T=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C/R");if(C(a,b,c))T.push([a,b,c])}
const out={equality:{frames:0,endpointPairs:0,validExtensions:0,affineLiftChecks:0},jobs:[],invalidHall:0};
function frameRows(a){return a.map((_,i)=>[a[i],a[(i+1)%5],a[(i+2)%5]])}
for(let f=0;f<3125;f++){let v=Array.from({length:5},(_,i)=>Math.floor(f/5**i)%5);if(!frameRows([0,1,2,3,4]).every(r=>C(...r.map(i=>v[i]))))continue;out.equality.frames++;
for(let x=0;x<5;x++)for(let y=0;y<5;y++){out.equality.endpointPairs++;if(C(v[0],v[2],x)&&C(v[0],v[2],y)){assert(x===y,"equality");out.equality.validExtensions++}}}
for(let x=0;x<5;x++){let a=Array.from({length:5},(_,i)=>(x+i+4)%5);assert(frameRows([0,1,2,3,4]).every(r=>C(...r.map(i=>a[i])))&&C(a[0],a[2],x),"lift");for(let i=0;i<5;i++)for(let j=0;j<5;j++){assert(+(a[i]===j)===+(x===(j-i+6)%5),"affine");out.equality.affineLiftChecks++}}
function graph(n){let seed=12345+n;function rng(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}let E=Array.from({length:n},(_,i)=>new Set([i]));for(let k=0;k<3;k++){let p=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rng(i+1);[p[i],p[j]]=[p[j],p[i]]}for(let i=0;i<n;i++)E[i].add(p[i])}return E.map(s=>[...s].sort((a,b)=>a-b))}
function build(G){let rows=[],fn=[],raw=[],owner=[];
const add=f=>(fn.push(f),fn.length-1),a=Array.from({length:5},(_,i)=>add(()=>i)),row=(...r)=>(assert(new Set(r).size===3,"distinct"),rows.push(r));
for(let r of frameRows(a))row(...r);
function wire(f){let p=add(f);for(let j of [2,3,4])row(a[j],p,add(v=>[0,1,2,3,4].find(z=>C(j,f(v),z))));return p}
function not(p){let z=wire(v=>1-fn[p](v));row(a[2],p,z);return z}
function or(p,q){let z=wire(v=>fn[p](v)|fn[q](v)),u=add(v=>fn[p](v)?0:3),w=add(v=>fn[q](v)?2:4);row(a[1],a[2],u);row(a[0],a[1],w);row(a[4],p,u);row(a[3],q,w);row(z,u,w);return z}
const pin=(p,b)=>b?row(a[0],a[2],p):row(a[1],a[4],p);
let t=wire(v=>v.mode),sw=rows.length;pin(t,1);
let E=G.map((r,i)=>r.map(j=>{let k=raw.length;raw.push([i,j]);return wire(v=>v.bits[k])}));
function clause(lits){let p=lits.map(([i,j,b])=>b?E[i][G[i].indexOf(j)]:not(E[i][G[i].indexOf(j)]));let z=p[0];for(let q of p.slice(1))z=or(z,q);pin(z,1)}
for(let i=0;i<G.length;i++){clause(G[i].map(j=>[i,j,1]));for(let u=0;u<G[i].length;u++)for(let v=u+1;v<G[i].length;v++)clause([[i,G[i][u],0],[i,G[i][v],0]])}
for(let j=0;j<G.length;j++){let I=G.map((r,i)=>r.includes(j)?i:-1).filter(i=>i>=0);for(let u=0;u<I.length;u++)for(let v=u+1;v<I.length;v++)clause([[I[u],j,0],[I[v],j,0]])}
for(let i=0;i<G.length;i++)if(G[i].includes(G.length-1))pin(or(t,not(E[i][G[i].indexOf(G.length-1)])),1);
return {rows,fn,raw,E,sw,off:[a[1],a[4],t],on:[a[0],a[2],t],nv:fn.length}}
function split(F){let lists=Array.from({length:F.nv},()=>[]),map=[],links=[],rows=[],next=0;
const cp=x=>{let i=next++;lists[x].push(i);map[i]=x;return i};
let on,off;for(let j=0;j<F.rows.length;j++){if(j===F.sw){let pool=new Map();for(let x of [...F.on,...F.off])if(!pool.has(x))pool.set(x,cp(x));on=F.on.map(x=>pool.get(x));off=F.off.map(x=>pool.get(x));rows.push(on)}else rows.push(F.rows[j].map(cp))}
for(let i=0;i<F.nv;i++){if(!lists[i].length)cp(i);for(let k=1;k<lists[i].length;k++){let x=lists[i][k-1],y=lists[i][k],a=Array.from({length:5},()=>next++);links.push({x,y,a});rows.push(...frameRows(a),[a[0],a[2],x],[a[0],a[2],y])}}
let counts=Array(next).fill(0);for(let r of rows)for(let x of r)counts[x]++;assert(Math.max(...counts.slice(0,Math.min(counts.length,10000)))<=5,"degree prefix");assert(counts.every(x=>x<=5),"degree");
return {rows,lists,map,links,nv:next,on,off,max:counts.reduce((a,b)=>Math.max(a,b),0)}}
function close(S,rows,pins){let D=Array(S.nv).fill(31),occ=Array.from({length:S.nv},()=>[]);for(let [i,x] of pins)D[i]&=1<<x;rows.forEach((r,i)=>r.forEach(x=>occ[x].push(i)));let Q=rows.map((_,i)=>i),pending=new Uint8Array(rows.length).fill(1),checks=0,head=0;while(head<Q.length){let i=Q[head++];pending[i]=0;let r=rows[i],m=[0,0,0];for(let t of T){checks++;if(t.every((x,k)=>D[r[k]]&(1<<x)))for(let k=0;k<3;k++)m[k]|=1<<t[k]}for(let k=0;k<3;k++){let x=r[k],d=D[x]&m[k];if(!d)return {no:true,checks};if(d!==D[x]){D[x]=d;for(let j of occ[x])if(!pending[j]){pending[j]=1;Q.push(j)}}}}return {no:false,checks,D}}
function matching(G){let n=G.length,M=Array(n).fill(-1),H=Array(n).fill(-1),scans=0;for(let i=0;i<n;i++){let L=new Set([i]),Y=new Set();function go(u){for(let v of G[u]){scans++;if(Y.has(v))continue;Y.add(v);if(H[v]<0||(L.add(H[v]),go(H[v]))){H[v]=u;M[u]=v;return true}}return false}if(!go(i))return {no:true,L:[...L],Y:[...Y],scans}}return {no:false,M,scans}}
function verifyHall(G,H){let Y=new Set(H.L.flatMap(i=>G[i]));return H.L.length>Y.size&&Y.size===H.Y.length&&H.Y.every(j=>Y.has(j))}
function dfs(G,cap){let used=new Set(),M=[],visits=0,stop=false;function go(i){if(i===G.length)return true;for(let j of G[i]){if(visits>=cap){stop=true;return false}visits++;if(used.has(j))continue;used.add(j);M[i]=j;if(go(i+1))return true;used.delete(j);if(stop)return false}return false}return {status:go(0)?"YES":stop?"UNKNOWN":"NO",visits,M}}
function bitDP(G,cap){let dp=new Set([0]),work=0;for(let r of G){let next=new Set();for(let m of dp)for(let j of r){if(work++>=cap)return {status:"UNKNOWN",work};if(!(m&(1<<j)))next.add(m|(1<<j))}dp=next;if(!dp.size)return {status:"NO",work}}return {status:"YES",work}}
function lift(F,S,rows,M,mode){let raw={mode,bits:F.raw.map(([i,j])=>+(M[i]===j))},v=F.fn.map(f=>f(raw)),z=Array(S.nv);for(let i=0;i<S.map.length;i++)z[i]=v[S.map[i]];for(let {x,y,a} of S.links){assert(z[x]===z[y],"copies");a.forEach((id,i)=>z[id]=(z[x]+i+4)%5)}assert(z.every(x=>Number.isInteger(x)),"complete lift");assert(rows.every(r=>C(...r.map(i=>z[i]))&&R(...r.map(i=>z[i]))&&R(z[r[1]],z[r[0]],z[r[2]])),"native verify");for(let i=0;i<F.nv;i++)assert(z[S.lists[i][0]]===v[i],"retract");return z}
function hash(rows){let h=2166136261;for(let r of rows)for(let x of r)h=Math.imul(h^x,16777619)>>>0;return h}
function bits(n,m){return n+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(n+1))}
for(let h of [4,6,8,16,32,64,128]){let G=graph(h),F=build(G),S=split(F);for(let mode of [0,1]){let rows=S.rows.slice();rows[F.sw]=mode?S.on:S.off;let raw=G.map(r=>r.filter(j=>mode||j!==h-1));let pins=Array.from({length:5},(_,i)=>[S.lists[i][0],i]);let cl=close(S,rows,pins);assert(!cl.no,"initial closure");
let A=dfs(raw,4096),B=matching(raw),D=h<=16?bitDP(raw,4096):{status:"UNKNOWN",work:0};assert(B.no===!mode,"neighbor");assert(A.status==="UNKNOWN"||((A.status==="NO")===B.no),"A");assert(D.status==="UNKNOWN"||((D.status==="NO")===B.no),"C");
let imported=0,reclose=0;if(B.no){assert(verifyHall(raw,B),"Hall");assert(!verifyHall(raw,{L:B.L.slice(1),Y:B.Y}),"corrupt Hall");out.invalidHall++}else{lift(F,S,rows,B.M,mode);if(A.status==="YES")lift(F,S,rows,A.M,mode);for(let i=0;i<h;i++){let j=B.M[i],raw2=raw.map((r,k)=>k===i?r.filter(v=>v!==j):r),q=matching(raw2);if(q.no){assert(verifyHall(raw2,q),"force");let p=S.lists[F.E[i][G[i].indexOf(j)]][0];if(cl.D[p]!==2){pins.push([p,1]);cl=close(S,rows,pins);assert(!cl.no,"import");reclose+=cl.checks;imported++}}}}
let counts=Array(S.nv).fill(0);for(let r of rows)for(let x of r)counts[x]++;assert(counts.every(x=>x<=5),"both modes degree");out.jobs.push({h,mode,originalN:bits(F.nv,F.rows.length),originalHash:hash(F.rows.map((r,i)=>i===F.sw?(mode?F.on:F.off):r)),n:S.nv,m:rows.length,N:bits(S.nv,rows.length),hash:hash(rows),maxDegree:counts.reduce((a,b)=>Math.max(a,b),0),links:S.links.length,closure:cl.checks,A:A.status,visits:A.visits,B:B.no?"NO":"YES",scans:B.scans,C:D.status,Cwork:D.work,imported,reclose,integrated:B.no?"NO":"YES"})}}
return out
}
console.log(JSON.stringify(runAudit(),null,2));
