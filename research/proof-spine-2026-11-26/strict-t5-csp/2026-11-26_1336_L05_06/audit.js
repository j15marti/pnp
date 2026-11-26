function assert(v,m){if(!v)throw Error(m)}

function C(a,b,c){return a!==b&&b!==c&&a!==c&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>(x-i+5)%5<=2))}

function R(a,b,c){const w=(x,y)=>[1,3].includes((y-x+5)%5);return a!==b&&b!==c&&a!==c&&w(a,b)!==w(a,c)}

function source(ell,positive,labels,guards,compact=false){
 const H=2**ell,P=H+1,V=[],K=[],a=[0,1,2,3,4].map(nv),pairs=[],outs=[],neg=new Map();let comparators=0;
 function nv(v){V.push(v);return V.length-1}
 function add(i,j,k){assert(i!==j&&j!==k&&i!==k,"distinct IDs");K.push([i,j,k])}
 for(let i=0;i<5;i++)add(a[i],a[(i+1)%5],a[(i+2)%5]);
 function wire(v){const p=nv(v);for(const j of [2,3,4])add(a[j],p,nv([0,1,2,3,4].find(t=>C(j,v,t))));return p}
 function pin(p,v){if(v)add(a[0],a[2],p);else add(a[1],a[4],p)}
 function or(p,q){const z=wire(V[p]|V[q]),u=nv(V[p]===0?3:0),w=nv(V[q]===0?4:2);add(a[1],a[2],u);add(a[0],a[1],w);add(a[4],p,u);add(a[3],q,w);add(z,u,w);return z}
 function nt(p){if(!neg.has(p)){const z=wire(1-V[p]);add(a[2],p,z);neg.set(p,z);neg.set(z,p)}return neg.get(p)}
 function and(p,q){return nt(or(nt(p),nt(q)))}
 function xor(p,q){const z=wire(V[p]^V[q]);for(let w=0;w<8;w++){const b=[w&1,(w>>1)&1,(w>>2)&1];if((b[0]^b[1]^b[2])===0)continue;const ids=[p,q,z].map((u,t)=>b[t]?nt(u):u);pin(or(or(ids[0],ids[1]),ids[2]),1)}return z}
 const raw=Array.from({length:P},(_,i)=>Array.from({length:ell},(_,j)=>wire((labels[i]>>j)&1)));
 if(!compact){
 for(let i=0;i<P;i++)for(let j=i+1;j<P;j++){neg.clear();const ds=raw[i].map((p,t)=>xor(p,raw[j][t]));let f=ds[0];for(let t=1;t<ell;t++)f=or(f,ds[t]);pin(f,positive&&i===0&&j===1?0:1);pairs.push(f)}
 }else{
 const zero=wire(0),one=wire(1),mode=wire(positive?0:1);pin(zero,0);pin(one,1);
 function less(p,q){let t=zero;for(let j=0;j<p.length;j++)t=or(and(nt(p[j]),q[j]),and(or(nt(p[j]),q[j]),t));return t}
 function mux(s,p,q){return or(and(nt(s),p),and(s,q))}
 const aeq=nt(or(less(raw[0],raw[1]),less(raw[1],raw[0])));pin(or(mode,aeq),1);
 const A=raw.map((r,i)=>i===1?[...r.map(p=>and(mode,p)),nt(mode)]:[...r,zero]);while(A.length<2*H)A.push([...Array(ell).fill(zero),one]);
 for(let size=2;size<=A.length;size*=2)for(let stride=size/2;stride>=1;stride/=2)for(let i=0;i<A.length;i++){const j=i^stride;if(j<=i)continue;const p=A[i],q=A[j],s=(i&size)===0?less(q,p):less(p,q);A[i]=p.map((v,k)=>mux(s,v,q[k]));A[j]=q.map((v,k)=>mux(s,v,p[k]));comparators++}
 for(let i=0;i<H;i++){pin(A[i][ell],0);if(i>0)pin(less(A[i-1].slice(0,ell),A[i].slice(0,ell)),1)}
 pin(or(nt(mode),nt(A[H][ell])),1);pin(or(nt(mode),less(A[H-1].slice(0,ell),A[H].slice(0,ell))),1);
 outs.push(...A.map(w=>w.reduce((s,p,j)=>s+V[p]*2**j,0)));pin(mode,positive?0:1)
 }
 for(const [i,j,b] of guards)pin(raw[i][j],b);
 const n=V.length,m=K.length,N=n+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(n+1));
 return {V,K,a,raw,n,m,N,pairs,outs,comparators,ell,positive,guards}
}

function fp(F){let a=2166136261,b=0x9e3779b9;for(const v of [F.n,F.m,...F.K.flat()]){a=Math.imul(a^v,16777619);b=Math.imul(b^v,2246822519)}return (a>>>0).toString(16).padStart(8,"0")+(b>>>0).toString(16).padStart(8,"0")}

function close(F){const D=Array(F.n).fill(31);F.a.forEach((p,i)=>D[p]=1<<i);const W=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)if(C(a,b,c))W.push([1<<a,1<<b,1<<c]);let passes=0,checks=0,deleted=0;for(;;){passes++;let change=false;for(const [i,j,k] of F.K){let a=0,b=0,c=0;for(const w of W){checks++;if((w[0]&D[i])&&(w[1]&D[j])&&(w[2]&D[k])){a|=w[0];b|=w[1];c|=w[2]}}if(!a)return {NO:true,passes,checks,deleted};for(const [p,s] of [[i,a],[j,b],[k,c]])if(D[p]!==s){D[p]=s;deleted++;change=true}}if(!change)return {NO:false,passes,checks,deleted,rawBoth:F.raw.flat().filter(p=>D[p]===3).length,forced:F.raw.flatMap((row,i)=>row.flatMap((p,j)=>D[p]===1?[[i,j,0]]:D[p]===2?[[i,j,1]]:[]))}}}

function valid(labels,positive,guards){if(guards.some(([i,j,b])=>((labels[i]>>j)&1)!==b))return false;for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++)if((labels[i]===labels[j])!==(positive&&i===0&&j===1))return false;return true}

function domains(ell,positive,guards){const H=2**ell,P=H+1,G=positive?[[0,1],...Array.from({length:P-2},(_,i)=>[i+2])]:Array.from({length:P},(_,i)=>[i]);const D=G.map(g=>Array.from({length:H},(_,x)=>x).filter(x=>guards.every(([i,j,b])=>!g.includes(i)||((x>>j)&1)===b)));return {H,P,G,D}}

function lift(G,chosen,P){const a=Array(P).fill(-1);G.forEach((g,i)=>g.forEach(j=>a[j]=chosen[i]));return a}

function laneA(ell,pos,guards,cap){const {H,P,G,D}=domains(ell,pos,guards);if(G.length>H)return {answer:"NO",nodes:0,certificate:"strict chain longer than label domain"};let nodes=0,used=new Set(),x=[],stop=false;function dfs(i){if(i===G.length)return true;for(const t of D[i]){if(nodes>=cap){stop=true;return false}nodes++;if(used.has(t))continue;used.add(t);x[i]=t;if(dfs(i+1))return true;used.delete(t);if(stop)return false}return false}const yes=dfs(0);return {answer:yes?"YES":stop?"UNKNOWN":"NO",nodes,labels:yes?lift(G,x,P):undefined}}

function laneB(ell,pos,guards){const {H,P,G,D}=domains(ell,pos,guards),own=Array(H).fill(-1);let probes=0;function aug(i,seen){for(const t of D[i]){probes++;if(seen.has(t))continue;seen.add(t);if(own[t]<0||aug(own[t],seen)){own[t]=i;return true}}return false}for(let i=0;i<G.length;i++){if(!aug(i,new Set())){const X=new Set([i]),Y=new Set(),Q=[i];for(let h=0;h<Q.length;h++)for(const t of D[Q[h]]){probes++;if(Y.has(t))continue;Y.add(t);if(own[t]>=0&&!X.has(own[t])){X.add(own[t]);Q.push(own[t])}}assert(Y.size<X.size,"Hall certificate");return {answer:"NO",probes,hall:{groups:[...X],labels:[...Y]}}}}const x=Array(G.length).fill(-1);own.forEach((i,t)=>{if(i>=0)x[i]=t});return {answer:"YES",probes,labels:lift(G,x,P)}}

function laneC(ell,pos,guards,cap){const H=2**ell,P=H+1,a=Array(P).fill(0);let tried=0;while(tried<cap){tried++;if(valid(a,pos,guards))return {answer:"YES",tried,labels:a.slice()};let j=P-1;while(j>=0&&++a[j]===H){a[j]=0;j--}if(j<0)return {answer:"NO",tried}}return {answer:"UNKNOWN",tried}}

function bitonic(A){A=A.slice();for(let size=2;size<=A.length;size*=2)for(let stride=size/2;stride>=1;stride/=2)for(let i=0;i<A.length;i++){const j=i^stride;if(j<=i)continue;if(((i&size)===0&&A[i]>A[j])||((i&size)!==0&&A[i]<A[j]))[A[i],A[j]]=[A[j],A[i]]}return A}

function audit(){
 const output={scales:[],jobs:[],zeroOne:0,semanticComparisons:0,strictBoundChecks:0,graphDeletionChecks:0,gateChecks:0,frameChecks:0,source:C.toString(),cap:4096};
 for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C/R");output.gateChecks++}
 for(let w=0;w<3125;w++){let t=w,a=[];for(let i=0;i<5;i++){a.push(t%5);t=Math.floor(t/5)}if(a.every((v,i)=>C(v,a[(i+1)%5],a[(i+2)%5]))){assert([1,4].some(d=>a.every((v,i)=>v===(a[0]+d*i)%5)),"frame");output.frameChecks++}}assert(output.frameChecks===10,"frames");
 for(let p=0;p<2;p++)for(let q=0;q<2;q++)for(let z=0;z<2;z++){let n=0;for(let u=0;u<5;u++)for(let v=0;v<5;v++){output.gateChecks++;if(C(1,2,u)&&C(0,1,v)&&C(4,p,u)&&C(3,q,v)&&C(z,u,v))n++}assert(n===Number(z===(p|q)),"OR")}
 for(const K of [2,4,8,16])for(let w=0;w<2**K;w++){const a=Array.from({length:K},(_,i)=>(w>>i)&1),b=bitonic(a);assert(b.every((x,i)=>i===0||b[i-1]<=x)&&a.reduce((s,x)=>s+x,0)===b.reduce((s,x)=>s+x,0),"network");output.zeroOne++}
 let rng=1739241;function rand(n){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%n}
 for(const ell of [1,2,3,4,5]){
 const H=2**ell,P=H+1,canonical=Array.from({length:P},(_,i)=>Math.max(0,i-1));
 const y=source(ell,true,canonical,[]),u=source(ell,false,canonical,[]),cy=source(ell,true,canonical,[],true),cu=source(ell,false,canonical,[],true);
 const bad=f=>f.K.reduce((s,c)=>s+Number(!C(...c.map(i=>f.V[i]))),0);
 assert(bad(y)===0&&bad(u)===1&&bad(cy)===0&&bad(cu)>0,"native neighbors");
 assert(y.K.filter((c,i)=>c.join()!==u.K[i].join()).length===1&&cy.K.filter((c,i)=>c.join()!==cu.K[i].join()).length===1,"one change");
 assert(y.raw.flat().join()===cy.raw.flat().join(),"source raw IDs");
 assert(cy.K.every(c=>{const [a,b,d]=c.map(i=>cy.V[i]);return R(a,b,d)&&R(b,a,d)}),"compact R");
 assert(cy.outs.join()===Array.from({length:2*H},(_,i)=>Math.min(i,H)).join(),"sorted lift");
 output.scales.push({ell,H,original:{n:y.n,m:y.m,N:y.N},compact:{n:cy.n,m:cy.m,N:cy.N,comparators:cy.comparators},sourceYES:fp(y),sourceNO:fp(u),compactYES:fp(cy),compactNO:fp(cu),negativeFailedClauses:bad(cu)});
 // Symbolic proof step checked as exact finite value implication (not native proof trace).
 for(let i=1;i<=H;i++)for(let v=0;v<i;v++)for(let t=i-1;t<H;t++){assert(!(t<v),"ordered bound");output.strictBoundChecks++}
 // Deleting one edge from complete pairwise inequality permits a collision on that pair.
 for(let i=0;i<H;i++)for(let j=i+1;j<H;j++){let lab=0;const a=Array.from({length:H},(_,k)=>k===j?-1:lab++);a[j]=a[i];let collisions=0;for(let p=0;p<H;p++)for(let q=p+1;q<H;q++)if(a[p]===a[q]){assert(p===i&&q===j,"wrong collision");collisions++}assert(collisions===1,"deletion");output.graphDeletionChecks++}
 const cases=[{positive:true,guards:[],name:"yes"},{positive:false,guards:[],name:"no"}];
 if(ell>=2){const hall=[];for(let i=2;i<=H/2+2;i++)hall.push([i,ell-1,0]);cases.push({positive:true,guards:hall,name:"guarded Hall NO"});cases.push({positive:true,guards:[[0,0,0],[1,0,1]],name:"opposite equality guard NO"});cases.push({positive:true,guards:[[0,0,0],[P-1,ell-1,1]],name:"guarded YES"})}
 for(const s of cases){const F=source(ell,s.positive,canonical,s.guards);const cap=Math.min(4096,F.N),fingerprint=fp(F);
 const initial=ell<=4?close(F):null;const guardMap=new Map(s.guards.map(g=>[g.slice(0,2).join(),g[2]]));for(const g of initial?.forced??[]){const key=g.slice(0,2).join();assert(!guardMap.has(key)||guardMap.get(key)===g[2],"closure guard");guardMap.set(key,g[2])}
 const guards=[...guardMap].map(([key,b])=>[...key.split(",").map(Number),b]);
 const A=initial?.NO?{answer:"NO",nodes:0}:laneA(ell,s.positive,guards,cap);
 const B=laneB(ell,s.positive,guards);
 const Cc=initial?.NO?{answer:"NO",tried:0}:laneC(ell,s.positive,guards,cap);
 for(const T of [A,Cc])assert(T.answer==="UNKNOWN"||T.answer===B.answer,"lane disagreement");
 if(B.answer==="NO"){const d=domains(ell,s.positive,guards);const Y=new Set(B.hall.groups.flatMap(i=>d.D[i]));assert(Y.size===B.hall.labels.length&&B.hall.labels.every(x=>Y.has(x))&&Y.size<B.hall.groups.length,"verify Hall")}
 let newN=null,reclosed=null;if(B.answer==="YES"){assert(valid(B.labels,s.positive,s.guards),"source witness");const old=source(ell,s.positive,B.labels,s.guards),newF=source(ell,s.positive,B.labels,s.guards,true);assert(bad(old)===0&&bad(newF)===0,"native integrated lift");newN=newF.N;if(ell<=4)reclosed=close(newF);assert(!reclosed?.NO,"reclosure")}
 output.jobs.push({ell,name:s.name,positive:s.positive,guards:s.guards,fingerprint,N:F.N,cap,initial:initial?{...initial,forced:initial.forced?.length}:null,A:{answer:A.answer,nodes:A.nodes},B:{answer:B.answer,probes:B.probes,hallSize:B.hall?[B.hall.groups.length,B.hall.labels.length]:null},C:{answer:Cc.answer,tried:Cc.tried},integrated:B.answer,newN,reclosed:reclosed?{...reclosed,forced:reclosed.forced?.length}:null})}
 // Independent finite raw semantic tests; compact gates checked on same raw assignments at small sizes.
 for(let trial=0;trial<40;trial++){const lab=Array.from({length:P},()=>rand(H)),pos=Boolean(trial%2);const sorted=bitonic([...lab.map((x,i)=>pos&&i===1?H:x),...Array(H-1).fill(H)]);const count=pos?H:P;const pred=(!pos||lab[0]===lab[1])&&sorted.slice(0,count).every((x,i)=>x<H&&(i===0||sorted[i-1]<x));assert(pred===valid(lab,pos,[]),"semantic projection");if(ell<=2){const f=source(ell,pos,lab,[],true),old=source(ell,pos,lab,[]);assert((bad(f)===0)===pred&&(bad(old)===0)===pred,"native differential")}output.semanticComparisons++}
 }
 return output
}
console.log(JSON.stringify(audit(),null,2));
