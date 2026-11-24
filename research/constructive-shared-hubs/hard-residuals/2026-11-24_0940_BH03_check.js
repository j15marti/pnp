"use strict";
console.log(JSON.stringify((function experiment(){
 const stats={miCalls:0,oracleCalls:0,exchangeTests:0,augmentations:0,closureScans:0,forcedPins:0,coreSearchNodes:0,verifiedLifts:0,referenceAssignments:0,subsetChecks:0};
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const range=n=>Array.from({length:n},(_,i)=>i);
 const ds=n=>{const p=range(n);const find=x=>{while(p[x]!==x){p[x]=p[p[x]];x=p[x]}return x};return {find,join(a,b){a=find(a);b=find(b);if(a===b)return false;p[b]=a;return true}}};
 const pairs=c=>[[c[0],c[1],1^(c[3]&1)^((c[3]>>1)&1)],[c[0],c[2],1^(c[3]&1)^((c[3]>>2)&1)],[c[1],c[2],1^((c[3]>>1)&1)^((c[3]>>2)&1)]];
 const good=(c,x)=>{const v=c.slice(0,3).map((u,i)=>x[u]^((c[3]>>i)&1));return v[0]!==v[1]||v[1]!==v[2]};
 const pinEdges=(n,p)=>p.flatMap((b,v)=>b<0?[]:[[n,v,b]]);
 function closure(n,C,p){
  p=p.slice();for(;;){let change=false;for(const c of C){stats.closureScans++;const rows=range(8).filter(r=>{const b=range(3).map(i=>(r>>i)&1);return b.every((v,i)=>p[c[i]]<0||p[c[i]]===v)&&((r^c[3])!==0&&(r^c[3])!==7)});if(!rows.length)return null;
   for(let i=0;i<3;i++)if(p[c[i]]<0&&rows.every(r=>((r>>i)&1)===((rows[0]>>i)&1))){p[c[i]]=(rows[0]>>i)&1;stats.forcedPins++;change=true;break}if(change)break}if(!change)return p}
 }
 function mi(n,C,ids,base){
  stats.miCalls++;const ground=ids.flatMap(j=>pairs(C[j]).map(e=>({j,e})));let I=[];
  const independent=ids=>{stats.oracleCalls++;const d=ds(n+1);for(const e of base)d.join(e[0],e[1]);for(const i of ids){const e=ground[i].e;if(!d.join(e[0],e[1]))return false}return true};
  while(true){
   const inI=new Set(I),owner=new Map(I.map(i=>[ground[i].j,i])),prev=new Map(),q=[];
   for(let x=0;x<ground.length;x++)if(!inI.has(x)&&!owner.has(ground[x].j)){prev.set(x,-1);q.push(x)}
   let end=-1;for(let h=0;h<q.length;h++){const x=q[h];if(!inI.has(x)){
    if(independent(I.concat(x))){end=x;break}
    for(const y of I)if(!prev.has(y)){stats.exchangeTests++;if(independent(I.filter(i=>i!==y).concat(x))){prev.set(y,x);q.push(y)}}
   }else{for(let y=0;y<ground.length;y++)if(!inI.has(y)&&!prev.has(y)){stats.exchangeTests++;const o=owner.get(ground[y].j);if(o===undefined||o===x){prev.set(y,x);q.push(y)}}}}
   if(end<0)return I.map(i=>ground[i]);
   for(let x=end;x!==-1;x=prev.get(x)){if(inI.has(x))inI.delete(x);else inI.add(x)}I=[...inI];stats.augmentations++;assert(independent(I)&&new Set(I.map(i=>ground[i].j)).size===I.length,"bad augment")
  }
 }
 function core(n,C,p){
  const base=pinEdges(n,p),ids=range(C.length),M=mi(n,C,ids,base),delta=ids.length-M.length;
  if(!delta)return {delta,X:[],selected:M};
  const X=ids.filter(j=>{const J=ids.filter(i=>i!==j);return J.length-mi(n,C,J,base).length<delta});
  const set=new Set(X),outside=ids.filter(j=>!set.has(j)),B=base.concat(X.flatMap(j=>pairs(C[j]))),selected=mi(n,C,outside,B);
  assert(selected.length===outside.length,"nonextendible core");return {delta,X,selected}
 }
 function lift(n,C,p,K,x){
  const edges=pinEdges(n,p).concat(K.X.flatMap(j=>pairs(C[j]).map(([u,v])=>[u,v,x[u]^x[v]])),K.selected.map(t=>t.e));
  const adj=Array.from({length:n+1},()=>[]);for(const [u,v,b] of edges){adj[u].push([v,b]);adj[v].push([u,b])}
  const out=Array(n+1).fill(-1);for(const root of [n,...range(n)])if(out[root]<0){out[root]=0;const q=[root];for(let h=0;h<q.length;h++)for(const [v,b] of adj[q[h]]){const a=out[q[h]]^b;if(out[v]<0){out[v]=a;q.push(v)}else assert(out[v]===a,"inconsistent lift")}}
  out.pop();assert(C.every(c=>good(c,out))&&p.every((b,v)=>b<0||b===out[v]),"invalid source witness");stats.verifiedLifts++;return out
 }
 function dpll(n,C,p,active){
  stats.coreSearchNodes++;p=closure(n,C,p);if(!p)return null;const v=active.find(i=>p[i]<0);if(v===undefined){const x=p.map(b=>Math.max(0,b));return C.every(c=>good(c,x))?x:null}
  for(const b of [0,1]){const q=p.slice();q[v]=b;const x=dpll(n,C,q,active);if(x)return x}return null
 }
 function solve(n,C,p){
  p=closure(n,C,p);if(!p)return {x:null,delta:null,core:null};const K=core(n,C,p),D=K.X.map(j=>C[j]),active=[...new Set(D.flatMap(c=>c.slice(0,3)))],x=D.length?dpll(n,D,p,active):p.map(b=>Math.max(0,b));
  return {x:x?lift(n,C,p,K,x):null,delta:K.delta,core:K.X.length,K,p};
 }
 function brute(n,C,p,accept=()=>true){let count=0;for(let i=0;i<2**n;i++){stats.referenceAssignments++;const x=range(n).map(j=>(i>>j)&1);if(p.every((b,v)=>b<0||b===x[v])&&C.every(c=>good(c,x))&&accept(x))count++}return count}
 function subsetRef(n,C,p,K){let best=-1,meet=(1<<C.length)-1;for(let mask=0;mask<1<<C.length;mask++){stats.subsetChecks++;const d=ds(n+1);for(const e of pinEdges(n,p))d.join(e[0],e[1]);let r=0,k=0;for(let i=0;i<C.length;i++)if(mask>>i&1){k++;for(const [a,b] of pairs(C[i]))if(d.join(a,b))r++}const f=k-r;if(f>best){best=f;meet=mask}else if(f===best)meet&=mask}assert(best===K.delta&&K.X.join(",")===range(C.length).filter(i=>meet>>i&1).join(","),"wrong minimal core")}
 let seed=271824;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const random={cases:0,sat:0,unsat:0,zeroCore:0,properCore:0,closureReject:0};
 for(let t=0;t<160;t++){const n=4+rand(5),m=2+rand(9),C=range(m).map(()=>{const a=[];while(a.length<3){const v=rand(n);if(!a.includes(v))a.push(v)}return a.concat(rand(8))}),p=range(n).map(()=>rand(5)===0?rand(2):-1);
  const r=solve(n,C,p),b=brute(n,C,p);assert(!!r.x===!!b,"random decision");random.cases++;random[b?"sat":"unsat"]++;if(r.core===null)random.closureReject++;else{if(r.core===0)random.zeroCore++;else if(r.core<m)random.properCore++;subsetRef(n,C,r.p,r.K)}
 }
 const F=[[0,1,2,0],[0,3,4,0],[0,5,6,0],[1,3,5,0],[1,4,6,0],[2,3,6,0],[2,4,5,0]],free=n=>Array(n).fill(-1),root=solve(7,F,free(7));assert(!root.x&&root.delta===1&&root.core===7&&brute(7,F,free(7))===0,"Fano");
 const neighbors=[];for(let i=0;i<F.length;i++){const C=F.filter((_,j)=>j!==i),r=solve(7,C,free(7));assert(r.x&&r.delta===0,"forest neighbor");for(const b of [0,1]){let x=r.x.slice();if(x[F[i][0]]!==b)x=x.map(v=>v^1);assert(F[i].slice(0,3).every(v=>x[v]===b)&&C.every(c=>good(c,x)),"single owner lift");const count=brute(7,C,free(7),x=>F[i].slice(0,3).some(v=>x[v]===b));assert(count===5,"owner count");neighbors.push({edge:i,requiredLiteralValue:b,count})}}
 const scales=[];for(const k of [8,16,32,64,128]){const C=range(k).map(i=>[i,(i+1)%k,k+i,rand(8)]),r=solve(2*k,C,free(2*k));assert(r.x&&r.delta===0,"loose high-girth cycle");scales.push({kind:"loose cycle",n:2*k,m:k,bergeGirth:k,core:r.core})}
 for(const k of [4,8,16]){const C=F.concat(range(k).map(i=>[i===0?0:7+2*(i-1),7+2*i,8+2*i,rand(8)]));const r=solve(7+2*k,C,free(7+2*k));assert(!r.x&&r.core===7&&r.delta===1,"dense core fringe");scales.push({kind:"Fano plus sparse fringe",n:7+2*k,m:C.length,core:r.core})}
 const K4=[[0,1,2,0],[0,1,3,0],[0,2,3,0],[1,2,3,0]],sat=solve(4,K4,free(4));assert(sat.x&&sat.delta===1&&sat.core===4,"deficiency nonnecessity");
 const badForest=[0,1,1,1];assert(K4.slice(0,3).every(c=>good(c,badForest))&&!good(K4[3],badForest),"bad forest counterexample");
 return {seed:271824,random,Fano:{delta:root.delta,core:root.core,models:0,neighbors},scales,deficiencyOneSat:{models:brute(4,K4,free(4)),delta:sat.delta,badForest},stats}
})(),null,2));
