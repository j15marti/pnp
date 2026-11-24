function experiment(){
const B=BigInt, Z=0n, O=1n, abs=x=>x<Z?-x:x, mod=(x,m)=>(x%m+m)%m, gcd=(a,b)=>{a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b]}return a}, lcm=(a,b)=>a/gcd(a,b)*b, floor=(a,b)=>(a-mod(a,b))/b, ceil=(a,b)=>-floor(-a,b);
let state=20261124;const rnd=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n};
const stats={flowCalls:0,augmentations:0,latticeCalls:0,columnOps:0,fixedArcs:0,roundingBlocks:0,basisBlocks:0,thinBlocks:0,roundingLifts:0,bruteTuples:0};
const zeros=n=>Array(n).fill(Z), same=(a,b)=>a.every((v,i)=>v===b[i]), assert=(v,s)=>{if(!v)throw Error(s)};
function balance(n,E,x){let a=zeros(n);E.forEach((e,i)=>{a[e.u]-=x[i];a[e.v]+=x[i]});return a}
function tag(E,x,M){let a=zeros(M.length);E.forEach((e,i)=>e.g.forEach((g,j)=>a[j]=mod(a[j]+g*x[i],M[j])));return a}
function flow(n,E,b,lo,hi){
 stats.flowCalls++;if(lo.some((x,i)=>x>hi[i]))return null;
 const s=n,t=n+1, G=Array.from({length:n+2},()=>[]), ptr=[];
 function add(u,v,c){let a={v,c,rev:G[v].length},d={v:u,c:Z,rev:G[u].length};G[u].push(a);G[v].push(d);return a}
 E.forEach((e,i)=>{ptr.push(e.u===e.v?null:add(e.u,e.v,hi[i]-lo[i]))});
 let base=balance(n,E,lo), total=Z, need=Z;
 for(let i=0;i<n;i++){let v=b[i]-base[i];if(v<Z){add(s,i,-v);total-=v}else if(v>Z){add(i,t,v);need+=v}}
 if(total!==need)return null;
 let done=Z;
 while(done<total){let p=Array(n+2).fill(null),q=[s];p[s]=[-1,null];
 for(let k=0;k<q.length&&!p[t];k++){let u=q[k];for(let a of G[u])if(a.c>Z&&!p[a.v]){p[a.v]=[u,a];q.push(a.v)}}
 if(!p[t])return null;let d=total-done;
 for(let v=t;v!==s;){let [u,a]=p[v];if(a.c<d)d=a.c;v=u}
 for(let v=t;v!==s;){let [u,a]=p[v];a.c-=d;G[v][a.rev].c+=d;v=u}
 done+=d;stats.augmentations++;
 }
 return lo.map((v,i)=>ptr[i]?hi[i]-ptr[i].c:v)
}
function basis(n,E,active){
 const par=Array.from({length:n},(_,i)=>i),find=i=>{while(par[i]!==i)i=par[i];return i};
 const adj=Array.from({length:n},()=>[]),C=[];
 E.forEach((e,i)=>{if(!active[i])return;let a=find(e.u),b=find(e.v);
 if(a!==b){par[a]=b;adj[e.u].push([e.v,i,O]);adj[e.v].push([e.u,i,-O]);return}
 let c=zeros(E.length);c[i]=O;let q=[e.v],p=Array(n).fill(null);p[e.v]=[-1,-1,Z];
 for(let k=0;k<q.length&&!p[e.u];k++)for(let [v,j,sg] of adj[q[k]])if(!p[v]){p[v]=[q[k],j,sg];q.push(v)}
 assert(p[e.u]!==null,"tree path");for(let v=e.u;v!==e.v;){let [u,j,sg]=p[v];c[j]=sg;v=u}
 assert(balance(n,E,c).every(v=>v===Z),"cycle");C.push(c)
 });return C
}
function order(g,M){return g.reduce((r,x,i)=>lcm(r,M[i]/gcd(M[i],x)),O)}
// Unrestricted integer membership with preimage: elementary column operations.
// Polynomial-bit theoretical backend is HNF/SNF, not a bit-complexity claim for this routine.
function lattice(gs,M,t){
 stats.latticeCalls++;let k=gs.length,q=M.length, cols=gs.map(v=>v.slice()), P=gs.map((_,i)=>zeros(k).map((_,j)=>i===j?O:Z));
 M.forEach((m,i)=>{let c=zeros(q);c[i]=m;cols.push(c);P.push(zeros(k))});
 let r=t.slice(),out=zeros(k);
 function swap(i,j){[cols[i],cols[j]]=[cols[j],cols[i]];[P[i],P[j]]=[P[j],P[i]]}
 function sub(i,j,f){cols[i]=cols[i].map((x,h)=>x-f*cols[j][h]);P[i]=P[i].map((x,h)=>x-f*P[j][h]);stats.columnOps++}
 for(let i=0;i<q;i++){
 let j=cols.findIndex((v,j)=>j>=i&&v[i]!==Z);assert(j>=0,"mod diagonal rank");swap(i,j);
 for(j=i+1;j<cols.length;j++)while(cols[j][i]!==Z){let a=cols[i][i]/cols[j][i];sub(i,j,a);swap(i,j)}
 let p=cols[i][i];if(r[i]%p!==Z)return null;let f=r[i]/p;r=r.map((x,h)=>x-f*cols[i][h]);out=out.map((x,h)=>x+f*P[i][h])
 }
 assert(r.every(x=>x===Z),"remainder");
 assert(t.every((x,i)=>mod(gs.reduce((a,g,j)=>a+g[i]*out[j],Z)-x,M[i])===Z),"lattice lift");return out
}
function prepare(n,E,b,M){
 let lo=zeros(E.length),hi=E.map(e=>e.cap),f=flow(n,E,b,lo,hi);if(!f)return null;
 let active=E.map((_,i)=>{let h=hi.slice(),l=lo.slice();h[i]=f[i]-O;l[i]=f[i]+O;
 let a=flow(n,E,b,lo,h),d=flow(n,E,b,l,hi);if(!a&&!d){stats.fixedArcs++;return false}return true});
 const C=basis(n,E,active),par=Array.from({length:C.length},(_,i)=>i),find=i=>{while(par[i]!==i)i=par[i];return i}, seen=Array(E.length).fill(-1);
 C.forEach((c,i)=>c.forEach((x,e)=>{if(x!==Z){if(seen[e]>=0)par[find(i)]=find(seen[e]);seen[e]=i}}));
 let dict=new Map();C.forEach((c,i)=>{let k=find(i);if(!dict.has(k))dict.set(k,[]);dict.get(k).push(c)});
 let blocks=[];
 for(let cs of dict.values()){
 let idx=E.map((_,i)=>i).filter(i=>cs.some(c=>c[i]!==Z)),es=idx.map(i=>E[i]),fs=idx.map(i=>f[i]),cycles=cs.map(c=>idx.map(i=>c[i])),gs=cycles.map(c=>tag(es,c,M)),orders=gs.map(g=>order(g,M)),L=orders.reduce(lcm,O), bb=balance(n,es,fs);
 let basisMargins=es.map((_,i)=>cycles.reduce((s,c,j)=>s+abs(c[i])*(orders[j]/2n),Z)),rMargins=es.map(()=>L-O);
 function mid(m){return flow(n,es,bb,m,es.map((e,i)=>e.cap-m[i]))}
 let midpoint=mid(rMargins),method="round";
 if(!midpoint){midpoint=mid(basisMargins);method="basis"}
 if(!midpoint){method="thin";stats.thinBlocks++}else{
   if(method==="round")stats.roundingBlocks++;else stats.basisBlocks++;
   fs=midpoint;idx.forEach((i,j)=>f[i]=fs[j])
 }
 blocks.push({idx,es,fs,cycles,gs,orders,L,method})
 }
 return {f,blocks,all:blocks.flatMap(a=>a.gs),good:blocks.filter(a=>a.method!=="thin").flatMap(a=>a.gs)}
}
function decide(n,E,b,M,t,P){
 if(!P)return {status:"UNSAT"};
 let delta=t.map((v,i)=>mod(v-tag(E,P.f,M)[i],M[i]));
 let a=lattice(P.good,M,delta);
 if(!a)return {status:lattice(P.all,M,delta)?"UNKNOWN":"UNSAT"};
 let x=P.f.slice(),off=0;
 for(let Q of P.blocks){if(Q.method==="thin")continue;let {cycles,orders,L,es,fs,idx}=Q;
 let coeff=a.slice(off,off+cycles.length).map((v,j)=>{let r=mod(v,orders[j]);return r>orders[j]/2n?r-orders[j]:r});off+=cycles.length;
 let d=es.map((_,i)=>cycles.reduce((s,c,j)=>s+c[i]*coeff[j],Z));
 if(Q.method==="round"){let z=flow(n,es,zeros(n),d.map(v=>floor(v,L)),d.map(v=>ceil(v,L)));assert(z,"rounding feasibility");
 d=d.map((v,i)=>v-L*z[i]);stats.roundingLifts++}
 idx.forEach((e,i)=>x[e]=fs[i]+d[i])
 }
 assert(x.every((v,i)=>v>=Z&&v<=E[i].cap)&&same(balance(n,E,x),b)&&same(tag(E,x,M),t),"invalid witness");
 return {status:"SAT",x}
}
function brute(n,E,b,M){let S=new Set(),x=zeros(E.length);
 function rec(i){if(i===E.length){stats.bruteTuples++;if(same(balance(n,E,x),b))S.add(tag(E,x,M).join(","));return}for(let j=Z;j<=E[i].cap;j++){x[i]=j;rec(i+1)}}rec(0);return S}
function targets(M){let out=[];function rec(a){if(a.length===M.length){out.push(a);return}for(let v=Z;v<M[a.length];v++)rec(a.concat(v))}rec([]);return out}
const summary={randomNetworks:160,queries:0,referenceSAT:0,referenceUNSAT:0,definiteSAT:0,definiteUNSAT:0,unknownSAT:0,unknownUNSAT:0,fullySaturated:0,disagreements:0};
for(let k=0;k<summary.randomNetworks;k++){
 let n=2+rnd(3),m=3+rnd(3),M=[[2n],[3n],[2n,2n],[2n,3n],[4n],[3n,4n]][rnd(6)],E=Array.from({length:m},()=>({u:rnd(n),v:rnd(n),cap:B(rnd(7)),g:M.map(p=>B(rnd(Number(p))))}));
 let x=E.map(e=>B(rnd(Number(e.cap)+1))),b=balance(n,E,x);if(k%11===0){b[0]+=20n;b[1]-=20n}
 let P=prepare(n,E,b,M),S=brute(n,E,b,M);if(P&&P.blocks.every(a=>a.method!=="thin"))summary.fullySaturated++;
 for(let t of targets(M)){let ref=S.has(t.join(",")),r=decide(n,E,b,M,t,P).status;summary.queries++;summary[ref?"referenceSAT":"referenceUNSAT"]++;
 if(r==="UNKNOWN")summary[ref?"unknownSAT":"unknownUNSAT"]++;else{summary[r==="SAT"?"definiteSAT":"definiteUNSAT"]++;assert((r==="SAT")===ref,"wrong definite");}
 if(P&&P.blocks.every(a=>a.method!=="thin"))assert(r!=="UNKNOWN","saturated incomplete")
 }
}
let sharp=[];
for(let L=3;L<=8;L++){
 const M=Array(L).fill(B(L)),E=Array.from({length:L},(_,i)=>({u:0,v:1,cap:B(2*(L-2)),g:M.map((_,j)=>i===j?O:Z)})),f=E.map(()=>B(L-2)),b=balance(2,E,f),P=prepare(2,E,b,M),bad=M.map(()=>B(L-1)),good=f.slice();good[0]++;good[1]--;
 let rb=decide(2,E,b,M,bad,P),rg=decide(2,E,b,M,good,P);
 assert(rb.status==="UNKNOWN","sharp bad must be in hull but not certified");assert(rg.status!=="UNSAT","neighbor");assert(same(balance(2,E,good),b)&&good.every((x,i)=>x>=Z&&x<=E[i].cap),"neighbor witness");
 sharp.push({modulus:L,margin:L-2,bad:rb.status,knownBad:"UNSAT (unique per-coordinate residues exceed demand)",good:rg.status,knownGood:"SAT (explicit witness)"})
}
// Basis-only certificate: loops are independent; modulus may have >100 bits.
const huge=(2n**60n)*(3n**40n),scale=[];
for(let k of [1,4,16,32]){
 let M=Array(k).fill(huge).concat(2n), E=Array.from({length:k},(_,i)=>({u:i,v:i,cap:2n*(huge/2n),g:M.map((_,j)=>j===i?O:Z)})),b=zeros(k),P=prepare(k,E,b,M),target=M.map((m,i)=>i===k?Z:mod(huge-1n-B(i),m)),bad=target.slice();bad[k]=O;
 assert(P.blocks.every(v=>v.method==="basis"),"basis-only expected");
 assert(decide(k,E,b,M,target,P).status==="SAT"&&decide(k,E,b,M,bad,P).status==="UNSAT","scale");
 scale.push({blocks:k,modulusBits:huge.toString(2).length,method:"basis",groupOrderBits:(huge**B(k)).toString(2).length,sat:"SAT",unsat:"UNSAT"})
}
// Dense parallel block: basis margins exceed available tree capacity, uniform rounding succeeds.
let M=[huge,huge,2n],E=Array.from({length:6},(_,i)=>({u:0,v:1,cap:2n*(huge-O),g:[i%2?O:Z,i%3===0?O:Z,Z]})),f=E.map(()=>huge-O),b=balance(2,E,f),P=prepare(2,E,b,M);
let x=f.slice();x[0]+=huge-O;x[1]-=huge-O;let t=tag(E,x,M),bad=t.slice();bad[2]=O;
assert(P.blocks.length===1&&P.blocks[0].method==="round","round scaling");assert(decide(2,E,b,M,t,P).status==="SAT"&&decide(2,E,b,M,bad,P).status==="UNSAT","round scaling pair");
scale.push({blocks:1,parallelArcs:6,modulusBits:huge.toString(2).length,method:"round",sat:"SAT",unsat:"UNSAT"});
return {seed:20261124,summary,sharp,scale,stats}
}
console.log(JSON.stringify(experiment(),null,2));
