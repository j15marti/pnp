// P3SW05 deterministic reproducible audit. Run with node.
function audit(){
 const assert=(x,m)=>{if(!x)throw Error(m);counts.assertions++};
 const counts={assertions:0,matchingCalls:0,gaussCalls:0,enumerated:0};
 const parse=s=>s.split(" ").map(t=>[...t].map(Number));
 const key=(c,x)=>`${c}:${x}`;
 function rows(n,T){const R=Array.from({length:3*n},()=>[]);T.forEach((t,i)=>t.forEach((v,c)=>R[c*n+v].push(i)));return R}
 function valid(n,T,W){const r=Array(3*n).fill(0);for(const i of W)T[i].forEach((v,c)=>r[c*n+v]++);return r.every(x=>x===1)}
 function brute(n,T){const R=rows(n,T),covered=new Set(),W=[];function go(){if(covered.size===3*n)return W.slice();let best=null;for(let v=0;v<3*n;v++)if(!covered.has(v)){const q=R[v].filter(i=>T[i].every((x,c)=>!covered.has(c*n+x)));if(best===null||q.length<best.length)best=q;if(!q.length)return null}for(const i of best){W.push(i);T[i].forEach((x,c)=>covered.add(c*n+x));const w=go();if(w)return w;W.pop();T[i].forEach((x,c)=>covered.delete(c*n+x))}return null}return go()}
 function closure(n,T,pins=new Map()){
  let active=Array(3*n).fill(true),live=T.map((_,i)=>i),selected=[];
  function select(i){if(!live.includes(i))return false;const vs=T[i].map((x,c)=>c*n+x);if(vs.some(v=>!active[v]))return false;selected.push(i);for(const v of vs)active[v]=false;live=live.filter(j=>T[j].every((x,c)=>active[c*n+x]));return true}
  for(const [i,b] of pins)if(!b)live=live.filter(j=>j!==i);
  for(const [i,b] of pins)if(b&&!select(i))return null;
  while(true){
   const R=Array.from({length:3*n},()=>[]);for(const i of live)T[i].forEach((x,c)=>R[c*n+x].push(i));
   let forced=-1;for(let v=0;v<R.length;v++)if(active[v]){if(!R[v].length)return null;if(R[v].length===1)forced=R[v][0]}
   if(forced>=0){if(!select(forced))return null;continue}
   if(!live.length)return {n:0,T:[],ids:[],selected};
   const dead=new Set();
   for(const [a,b] of [[0,1],[0,2],[1,2]]){
    counts.matchingCalls++;
    const L=Array.from({length:n},(_,i)=>i).filter(i=>active[a*n+i]);
    const adj=Array.from({length:n},()=>[]);for(const i of live)adj[T[i][a]].push(T[i][b]);
    const mate=Array(n).fill(-1);
    function aug(x,seen){for(const y of adj[x])if(!seen[y]){seen[y]=1;if(mate[y]<0||aug(mate[y],seen)){mate[y]=x;return true}}return false}
    for(const x of L)if(!aug(x,Array(n).fill(0)))return null;
    const arcs=adj.map(ys=>ys.map(y=>mate[y]));
    const reach=new Map();for(const x of L){const S=new Set([x]),Q=[x];for(let k=0;k<Q.length;k++)for(const y of arcs[Q[k]])if(!S.has(y)){S.add(y);Q.push(y)}reach.set(x,S)}
    for(const i of live)if(!reach.get(mate[T[i][b]]).has(T[i][a]))dead.add(i);
   }
   if(dead.size){live=live.filter(i=>!dead.has(i));continue}
   const maps=[0,1,2].map(c=>new Map(Array.from({length:n},(_,i)=>i).filter(i=>active[c*n+i]).map((x,j)=>[x,j])));
   return {n:maps[0].size,T:live.map(i=>T[i].map((x,c)=>maps[c].get(x))),ids:live,selected};
  }
 }
 function gaussian(eq,k,pin=new Map()){
  counts.gaussCalls++;
  const piv=Array(k).fill(null);const input=eq.concat([...pin].map(([j,b])=>[1n<<BigInt(j),b]));
  for(let [a,b] of input){for(let j=0;j<k&&a;j++)if((a>>BigInt(j))&1n){if(piv[j]){a^=piv[j][0];b^=piv[j][1]}else{piv[j]=[a,b];a=0n;b=0;break}}if(!a&&b)return null}
  const x=Array(k).fill(0);for(let j=k-1;j>=0;j--)if(piv[j]){let b=piv[j][1];for(let i=j+1;i<k;i++)if((piv[j][0]>>BigInt(i))&1n)b^=x[i];x[j]=b}return x
 }
 function compile(n,T,reverse=false){
  const R=rows(n,T),m=T.length;if(R.some(x=>!x.length))return {no:"empty"};
  const adj=Array.from({length:m},()=>[]);for(const r of R)if(r.length===2){adj[r[0]].push(r[1]);adj[r[1]].push(r[0])}
  const phase=Array(m).fill(-1),sg=Array(m).fill(0),P=[];
  for(let i=0;i<m;i++)if(phase[i]<0){const j=P.length,Q=[i];P.push(Q);phase[i]=j;for(let q=0;q<Q.length;q++){const t=Q[q];for(const u of adj[t]){if(phase[u]<0){phase[u]=j;sg[u]=sg[t]^1;Q.push(u)}else if(sg[u]===sg[t])return {no:"odd-degree2"}}}}
  const delta=P.map(Q=>Q.reduce((a,t)=>a+(sg[t]?-1:1),0));
  for(let j=0;j<P.length;j++)if(delta[j]<0){delta[j]=-delta[j];for(const t of P[j])sg[t]^=1}
  const U=delta.flatMap((d,i)=>d?[i]:[]),eq=[],groups=[],stats={phases:P.length,unbalanced:U.length,balanced:P.length-U.length,pairs:0,trees:0,unicyclic:0,maxTokens:0,quota:[]};
  for(let v=0;v<R.length;v++)if(R[v].length!==2){let a=0n,b=1;for(const t of R[v]){a^=1n<<BigInt(phase[t]);b^=sg[t]}eq.push([a,b])}
  for(let c=0;c<3;c++){
   const vs=Array.from({length:n},(_,i)=>c*n+i).filter(v=>R[v].length!==2),parent=new Map(vs.map(v=>[v,v])),edges=[],tokens=[];
   const root=v=>{while(parent.get(v)!==v){parent.set(v,parent.get(parent.get(v)));v=parent.get(v)}return v};
   const ports=P.map(()=>[[],[]]);for(const v of vs)for(const t of R[v])ports[phase[t]][sg[t]].push(v);
   for(let j=0;j<P.length;j++){const [pos,neg]=ports[j];assert(pos.length-neg.length===delta[j],"color conservation");if(reverse)pos.reverse();for(let i=0;i<neg.length;i++){const a=pos[i],b=neg[i];edges.push([a,b]);parent.set(root(a),root(b))}for(let i=neg.length;i<pos.length;i++)tokens.push([pos[i],j])}
   const C=new Map();for(const v of vs){const r=root(v);if(!C.has(r))C.set(r,{v:0,e:0,t:[]});C.get(r).v++}
   for(const [a,b] of edges){assert(root(a)===root(b),"edge comp");C.get(root(a)).e++}
   for(const [a,j] of tokens)C.get(root(a)).t.push(j);
   let q=0;for(const z of C.values()){const target=z.v-z.e;if(target<0)return {no:"overfull-pair-component",stats};assert(target<=1,"connected");q+=target;stats[target?"trees":"unicyclic"]++;stats.maxTokens=Math.max(stats.maxTokens,z.t.length);groups.push({target,t:z.t})}
   stats.pairs+=edges.length;stats.quota.push(q);
  }
  assert(stats.quota.every(x=>x===stats.quota[0]),"common quota");
  return {P,phase,sg,delta,U,eq,groups,stats}
 }
 function solve(n,T,Q,cap=18){
  if(Q.no)return {status:"NO",mode:Q.no};
  const {P,phase,sg,U,eq,groups}=Q,k=P.length;
  const pins=new Map();let conflict=false;
  function pin(j,b){if(pins.has(j)&&pins.get(j)!==b)conflict=true;pins.set(j,b)}
  const reduced=[];for(const g of groups){const mult=new Map();for(const j of g.t)mult.set(j,(mult.get(j)||0)+1);for(const [j,c] of mult)if(g.target===0||c>1)pin(j,0);if(g.target===1)reduced.push([...mult].filter(([j,c])=>c===1).map(([j])=>j))}
  // Reapply exact-one and affine pin deduction until fixed.
  let E=eq.slice(),change=true;
  while(change&&!conflict){const old=pins.size;for(const r of reduced){const ones=r.filter(j=>pins.get(j)===1),free=r.filter(j=>!pins.has(j));if(ones.length>1||!ones.length&&!free.length){conflict=true;break}if(ones.length)free.forEach(j=>pin(j,0));else if(free.length===1)pin(free[0],1)}
   if(conflict)break;const x=gaussian(E,k,pins);if(!x){conflict=true;break}
   for(const j of U)if(!pins.has(j)){const test=new Map(pins);test.set(j,1-x[j]);if(!gaussian(E,k,test))pin(j,x[j])}
   change=pins.size!==old
  }
  if(conflict)return {status:"NO",mode:"token-affine-closure"};
  const check=x=>groups.every(g=>g.t.reduce((a,j)=>a+x[j],0)===g.target);
  const lift=(x,mode)=>{assert(check(x),"token sums");const W=T.flatMap((_,i)=>(x[phase[i]]^sg[i])?[i]:[]);assert(valid(n,T,W),"source lift");return {status:"YES",mode,W}};
  let affine=true;for(const r of reduced){if(r.some(j=>pins.get(j)===1))continue;const free=r.filter(j=>!pins.has(j));if(free.length>2){affine=false;break}let a=0n;for(const j of free)a^=1n<<BigInt(j);E.push([a,1])}
  if(affine){const x=gaussian(E,k,pins);return x?lift(x,"affine-terminal"):{status:"NO",mode:"affine-terminal"}}
  E=eq;const x0=gaussian(E,k,pins);if(!x0)return {status:"NO",mode:"parity"};if(check(x0))return lift(x0,"parity-witness");
  const free=U.filter(j=>!pins.has(j));if(free.length>cap)return {status:"UNKNOWN",mode:"cap"};
  for(let b=0;b<2**free.length;b++){counts.enumerated++;const f=new Map(pins);free.forEach((j,i)=>f.set(j,(b>>i)&1));if(!groups.every(g=>g.t.reduce((a,j)=>a+f.get(j),0)===g.target))continue;const x=gaussian(E,k,f);if(x)return lift(x,"unbalanced-enumeration")}
  return {status:"NO",mode:"unbalanced-enumeration"}
 }
 function expand(n,T,i,c,L){T=T.map(t=>t.slice());for(let k=0;k<L;k++){const old=T[i][c],a=n++,u=[a,a,a],v=[a,a,a];u[c]=a;v[c]=old;T[i][c]=a;T.push(u,v);i=T.length-1}return {n,T}}
 // The expansion above inserts a degree-two element on the original edge and two triples sharing the other two new degree-two elements.
 const fixtures=[["R03-U",4,parse("000 003 111 112 221 230 323 332")],["R03-V",4,parse("000 003 111 112 221 230 323 332 220")],["ES05-U",4,parse("013 021 110 113 221 222 231 300 302 330")],["ES05-V",4,parse("013 021 110 113 221 222 231 300 302 330 002")],["MF03-U",3,parse("000 002 010 011 021 022 100 101 111 201 202 221")],["MF03-V",3,parse("000 002 010 011 021 022 100 101 111 201 202 221 110")]];
 const summary={cube:{YES:0,NO:0,rawModes:{},closedModes:{},alternateComparisons:0},fixtures:[],scaled:[]};
 function test(n,T,want,reverse=false){const Q=compile(n,T,reverse),S=solve(n,T,Q);assert(S.status!=="UNKNOWN","small cap");assert((S.status==="YES")===want,"source decision");if(S.W)assert(valid(n,T,S.W),"direct lift");return {status:S.status,mode:S.mode,stats:Q.stats||null}}
 function closed(n,T,want){const C=closure(n,T);if(!C){assert(!want,"closure false NO");return {status:"NO",mode:"initial-closure"}}const Q=compile(C.n,C.T),S=solve(C.n,C.T,Q);assert(S.status!=="UNKNOWN","closed cap");assert((S.status==="YES")===want,"closed decision");if(S.W)assert(valid(n,T,C.selected.concat(S.W.map(i=>C.ids[i]))),"closed source lift");return {status:S.status,mode:S.mode,stats:Q.stats||null,live:C.T.length}}
 const cube=Array.from({length:8},(_,i)=>[(i>>2)&1,(i>>1)&1,i&1]);
 for(let mask=0;mask<256;mask++){const T=cube.filter((_,i)=>(mask>>i)&1),want=brute(2,T)!==null;const a=test(2,T,want),b=test(2,T,want,true),c=closed(2,T,want);summary.cube[want?"YES":"NO"]++;summary.cube.rawModes[a.mode]=(summary.cube.rawModes[a.mode]||0)+1;summary.cube.closedModes[c.mode]=(summary.cube.closedModes[c.mode]||0)+1;summary.cube.alternateComparisons++}
 for(const [name,n,T] of fixtures){const want=brute(n,T)!==null;summary.fixtures.push({name,n,m:T.length,want,raw:test(n,T,want),alternate:test(n,T,want,true),closed:closed(n,T,want)});for(const L of [16,64,128]){const G=expand(n,T,0,0,L);summary.scaled.push({name,L,n:G.n,m:G.T.length,want,raw:test(G.n,G.T,want),closed:closed(G.n,G.T,want)})}}
 // Independent cube atoms have arbitrarily many unbalanced phases and quotas. Not a connected obstruction.
 return {counts,summary,notes:"All 256 cube subinstances planar by deleting face centers of the octahedral radial graph. Named bases supplied by peer and independently checked with NetworkX outside this JS; relay expansion planar by strip replacement. Brute reference only small originals; scaled truth via proved relay lift. Full projected affine elimination and repeated source-pin reclosure after quotient deductions are theorem-level, not executed."}
}
console.log(JSON.stringify(audit(),null,2));
