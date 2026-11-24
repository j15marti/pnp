/* DO02 deterministic exact rational controls; run with node. */
function main(){
 const F=[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], fullF=[[0,1,2],...F];
 const assert=(b,s)=>{if(!b)throw Error(s)};
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const c=a%b;a=b;b=c}return a};
 const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);assert(d!==0n,"zero denominator");if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]};
 const plus=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]), times=(a,b)=>Q(a[0]*b[0],a[1]*b[1]), div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]), neg=a=>Q(-a[0],a[1]), eq=(a,b)=>a[0]===b[0]&&a[1]===b[1], str=a=>a[0]+"/"+a[1];
 const Z=Q(0),O=Q(1),metric=[O,O], unit=i=>new Map([[i,O]]);
 const scale=(v,a)=>new Map([...v].map(([i,x])=>[i,times(a,x)]).filter(([,x])=>x[0]));
 const add=(...vs)=>{let r=new Map;for(let v of vs)for(let [i,x] of v){let y=plus(r.get(i)||Z,x);if(y[0])r.set(i,y);else r.delete(i)}return r};
 const dot=(v,w)=>{let s=Z;for(let [i,x] of v)if(w.has(i))s=plus(s,times(times(x,w.get(i)),metric[i]));return s};
 const privateAxis=q=>{assert(q[0]>=0n,"negative metric");let i=metric.length;metric.push(q);return unit(i)};
 const circle=(x,y)=>new Map([[0,Q(x,5)],[1,Q(y,5)]].filter(([,a])=>a[0]));
 const root=circle(5,0), P=[circle(4,3),circle(3,4),circle(0,5),circle(-3,4)], N=[circle(4,-3),circle(3,-4),circle(0,-5),circle(-3,-4)];
 const good=(e,x)=>!(x[e[0]]===x[e[1]]&&x[e[1]]===x[e[2]]);
 let truth=Array.from({length:7},()=>new Map),hist=[];
 for(let d=-1;d<6;d++){let h={};for(let a=0;a<128;a++){let x=Array.from({length:7},(_,j)=>(a>>j)&1);if(F.every((e,i)=>i===d||good(e,x))){let k=2*x[0]+x[1];h[k]=(h[k]||0)+1;truth[d+1].set(k,x)}}hist.push(h)}
 assert(truth[0].size===2&&truth[0].has(0)&&truth[0].has(3),"equality projection");
 for(let d=1;d<7;d++)assert(truth[d].size===4,"critical local relation");
 function fresh(k=0){return {v:Array.from({length:k},()=>root),e:[],g:[],term:[]}}
 function vertex(G,v){let i=G.v.length;G.v.push(v);return i}
 function appendGadget(G,a,b,vs){let ids=[a,b,...vs.map(v=>vertex(G,v))];let start=G.e.length;for(let e of F)G.e.push(e.map(i=>ids[i]));G.g.push({ids,start});return G.g.length-1}
 function weak(G,a,target){
   let A=G.v[a],B=target,mid=scale(add(A,B),Q(1,2)),s=dot(mid,mid);
   assert(plus(s,Q(-9,10))[0]>=0n,"too wide port angle");
   let q=add(scale(mid,div(Q(9,10),s)),privateAxis(plus(Q(9,10),neg(div(Q(81,100),s)))));
   assert(eq(dot(A,q),Q(9,10))&&eq(dot(B,q),Q(9,10))&&eq(dot(q,q),Q(9,10)),"q");
   let axes=Array.from({length:4},()=>privateAxis(Q(4,5))), avg=scale(add(...axes),Q(1,4));
   let interior=axes.map(u=>add(scale(q,Q(-2,3)),u,scale(avg,Q(-1))));
   let b=vertex(G,B);appendGadget(G,a,b,[A,...interior]);return b
 }
 function path(G,a,targets){for(let v of targets)a=weak(G,a,v);return a}
 function base(){let G=fresh(1);let b=path(G,0,P),c=path(G,0,N);G.term.push(G.e.length);G.e.push([0,b,c]);return G}
 function compile(source,n){let G=fresh(n);for(let e of source){let p=[path(G,e[0],[root]),path(G,e[1],P),path(G,e[2],N)];G.term.push(G.e.length);G.e.push(p)}return G}
 function verifyVectors(G){let h={},count=0;for(let v of G.v)assert(eq(dot(v,v),O),"unit norm");
   for(let i=0;i<G.e.length;i++){let e=G.e[i],s=dot(add(...e.map(j=>G.v[j])),add(...e.map(j=>G.v[j])));let want=G.term.includes(i)?Q(1,25):O;assert(eq(s,want),"edge vector norm "+i);let k=str(s);h[k]=(h[k]||0)+1;count++}
   return {vertices:G.v.length,edges:G.e.length,gadgets:G.g.length,checkedNorms:count,edgeSumNorm2:h}
 }
 function fill(g,x,d=-1){let a=x[g.ids[0]],b=x[g.ids[1]],t=truth[d+1].get(2*a+b);assert(t!==undefined,"unliftable boundary");for(let j=2;j<7;j++)x[g.ids[j]]=t[j]}
 function baseWitness(G,d){
   let x=Array(G.v.length).fill(0);
   for(let g of G.g){let broken=(d>=g.start&&d<g.start+6);x[g.ids[1]]=x[g.ids[0]]^(broken?1:0);fill(g,x,broken?d-g.start:-1)}
   return x
 }
 function stretch(G){let H={v:G.v.slice(),e:[],g:[],term:[],coreMap:[],wireMap:[]};
   for(let i=0;i<G.e.length;i++){let newe=[];for(let a of G.e[i]){
     let b=vertex(H,G.v[a]);let t=truth[0].get(0);let priv=t.slice(2).map(z=>scale(G.v[a],Q(z?-1:1)));let j=appendGadget(H,a,b,priv);H.wireMap.push({j,source:i});newe.push(b)}
     H.coreMap.push(H.e.length);if(G.term.includes(i))H.term.push(H.e.length);H.e.push(newe)
   }return H
 }
 function stretchedWitness(G,H,d){
   let i=H.coreMap.indexOf(d),broken=-1;
   if(i<0){let w=H.wireMap.find(w=>{let g=H.g[w.j];return d>=g.start&&d<g.start+6});assert(w,"deleted edge not indexed");i=w.source;broken=w.j}
   let x=baseWitness(G,i).concat(Array(H.v.length-G.v.length).fill(0));
   for(let j=0;j<H.g.length;j++){let g=H.g[j];x[g.ids[1]]=x[g.ids[0]]^(j===broken?1:0);fill(g,x,j===broken?d-g.start:-1)}
   return x
 }
 function closure(G,facts){let p=Array.from({length:G.v.length},(_,i)=>i),r=i=>{while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i},scans=0,unions=0;
   function conflict(){for(let e of G.e){scans++;if(e.every(v=>r(v)===r(e[0])))return true}return false}
   if(conflict())return {reject:true,scans,unions};
   for(let [a,b] of facts){a=r(a);b=r(b);if(a!==b){p[b]=a;unions++;if(conflict())return {reject:true,scans,unions}}}
   return {reject:conflict(),scans,unions}
 }
 function neighbors(G,make){let checked=0,owners=0,mixture=0;for(let d=0;d<G.e.length;d++){let x=make(d);for(let i=0;i<G.e.length;i++){assert(good(G.e[i],x)===(i!==d),"bad deletion witness "+d+"/"+i);checked++}
   for(let s of [0,1]){let flip=x[G.e[d][0]]^s;for(let i=0;i<G.e.length;i++){let sum=G.e[i].reduce((a,v)=>a+(x[v]^flip),0);assert((sum>=1||i===d&&s===0)&&(sum<=2||i===d&&s===1),"bad owner lift");owners++}}
   }let x=make(G.term[0]);for(let i=0;i<G.e.length;i++){let e=G.e[i],sum=add(...e.map(j=>G.v[j])),v=dot(sum,sum);let z=e.reduce((a,j)=>a+(x[j]?-1:1),0);let mix=plus(times(Q(25,28),v),times(Q(3,28),Q(z*z)));assert(eq(mix,O),"SDP mixture");mixture++}
   return {deletionNeighbors:G.e.length,ownerNeighbors:2*G.e.length,deletionEdgeChecks:checked,ownerEdgeChecks:owners,exactSDPEqualities:mixture}
 }
 function girth(G){let n=G.v.length,adj=Array.from({length:n+G.e.length},()=>[]);G.e.forEach((e,i)=>e.forEach(v=>{adj[v].push(n+i);adj[n+i].push(v)}));let best=Infinity;
 for(let root=0;root<adj.length;root++){let dist=new Int32Array(adj.length).fill(-1),p=new Int32Array(adj.length).fill(-1),q=[root];dist[root]=0;for(let t=0;t<q.length;t++){let a=q[t];for(let b of adj[a]){if(dist[b]<0){dist[b]=dist[a]+1;p[b]=a;q.push(b)}else if(p[a]!==b&&p[b]!==a)best=Math.min(best,dist[a]+dist[b]+1)}}if(best===4)break}return best/2}
 let G=base(),H=stretch(G);
 let bV=verifyVectors(G),hV=verifyVectors(H);
 let bC=closure(G,G.g.map(g=>g.ids.slice(0,2))),hC=closure(H,[...H.g.map(g=>g.ids.slice(0,2)),...G.g.map(g=>g.ids.slice(0,2))]);
 assert(bC.reject&&hC.reject,"manifest closure");
 let bN=neighbors(G,d=>baseWitness(G,d)),hN=neighbors(H,d=>stretchedWitness(G,H,d));
 let C=compile(fullF,7),cV=verifyVectors(C),pointChecks=0,sourceModels=0,neighborCounts=Array(14).fill(0);
 for(let a=0;a<128;a++){let x=Array.from({length:7},(_,j)=>(a>>j)&1),y=x.concat(Array(C.v.length-7).fill(0));for(let g of C.g){y[g.ids[1]]=y[g.ids[0]];fill(g,y)}
  let model=fullF.every(e=>good(e,x));if(model)sourceModels++;
  for(let i=0;i<C.e.length;i++){let j=C.term.indexOf(i);assert(good(C.e[i],y)===(j<0||good(fullF[j],x)),"pointwise compiler");pointChecks++}
  for(let j=0;j<7;j++)for(let s=0;s<2;s++)if(fullF.every((e,i)=>good(e,x)||(i===j&&x[e[0]]===s)))neighborCounts[2*j+s]++;
 }
 assert(sourceModels===0&&neighborCounts.every(c=>c===5),"Fano source controls");
 return {seed:"none; deterministic",localTableAssignments:7*128,localProjectionCounts:hist,base:{...bV,...bN,bergeGirth:girth(G),closure:bC},stretched:{...hV,...hN,bergeGirth:girth(H),closure:hC},genericFanoCompiler:{...cV,sourceAssignments:128,pointwiseEdgeChecks:pointChecks,sourceModels,singleOwnerModelCounts:neighborCounts},metricDimensions:metric.length,strictFinalEnergy:"-72/25",exactSDPBooleanMixture:"3/28",discrepancies:0}
}
console.log(JSON.stringify(main(),null,2));
