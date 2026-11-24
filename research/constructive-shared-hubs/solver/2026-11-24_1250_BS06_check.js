const experiment = function experiment(){
const stats={closurePass:0,rowTests:0,deletions:0,graphEdges:0,cutNodes:0,pinAttempts:0,forestCalls:0,matchingCalls:0,matchingAttempts:0,affineCalls:0,dagCalls:0,dagEdges:0,dagDeclines:0,peakDAG:0,sourceChecks:0,bruteTuples:0}; const assert=(x,m)=>{if(!x)throw Error(m)};
const fresh=()=>({B:[],P:[],R:[]}); // row = {c:BigInt[],p:BigInt, id:number}
function input(B,P,R){return {B:B.map(BigInt),P:P.map(Number),R:R.map(rs=>rs.map((r,id)=>({c:r[0].map(BigInt),p:BigInt(r[1]),id})))}}
const bit=(x,j)=>Number((x>>BigInt(j))&1n);
function valid(F,rows){if(!rows||rows.length!==F.R.length)return false;let p=0n,c=F.B.map(()=>0n);for(let i=0;i<rows.length;i++){const r=rows[i];if(!F.R[i].includes(r))return false;p^=r.p;r.c.forEach((x,j)=>c[j]+=x)}return c.every((x,j)=>x<=F.B[j])&&F.P.every((x,j)=>bit(p,j)===x)}
function closure(F,R){R=R.map(a=>a.slice());for(;;){stats.closurePass++;if(R.some(a=>!a.length))return null;
let min=R.map(a=>F.B.map((_,j)=>a.reduce((x,r)=>r.c[j]<x?r.c[j]:x,a[0].c[j]))), sum=F.B.map((_,j)=>min.reduce((x,a)=>x+a[j],0n));
if(sum.some((x,j)=>x>F.B[j]))return null;
let base=R.map(a=>a[0].p), variable=R.map((a,i)=>a.reduce((x,r)=>x|(r.p^base[i]),0n)), total=base.reduce((x,y)=>x^y,0n), counts=F.P.map((_,j)=>variable.reduce((x,v)=>x+bit(v,j),0));
if(F.P.some((v,j)=>!counts[j]&&bit(total,j)!==v))return null;
let changed=false; outer:for(let i=0;i<R.length;i++)for(let k=0;k<R[i].length;k++){let r=R[i][k];stats.rowTests++;if(r.c.some((x,j)=>sum[j]-min[i][j]+x>F.B[j])||F.P.some((v,j)=>counts[j]===bit(variable[i],j)&&bit(total^base[i]^r.p,j)!==v)){R[i].splice(k,1);stats.deletions++;changed=true;break outer}}
if(!changed)return R}}
function graph(F,R){let E=[];for(let i=0;i<R.length;i++){for(let j=0;j<F.B.length+F.P.length;j++){const val=r=>j<F.B.length?r.c[j]:BigInt(bit(r.p,j-F.B.length));let D=[...new Set(R[i].map(val))];if(D.length>1)E.push({i,j,D})}}stats.graphEdges+=E.length;return E}
function cutset(F,R){let E=graph(F,R),n=R.length+F.B.length+F.P.length,p=Array.from({length:n},(_,i)=>i);function root(i){while(p[i]!==i)i=p[i];return i}let C=[];E.sort((a,b)=>b.D.length-a.D.length||a.i-b.i||a.j-b.j);for(let e of E){let x=root(e.i),y=root(R.length+e.j);if(x===y)C.push(e);else p[x]=y}return C}
function forest(F,R){stats.forestCalls++;for(let i=0;i<R.length;i++){if(R[i].length>1){let Q=R.slice();Q[i]=[R[i][0]];R=closure(F,Q);assert(R,"forest arbitrary row must extend")}}let w=R.map(a=>a[0]);assert(valid(F,w),"forest witness");return w}
const UNKNOWN=Symbol();
function matching(F,R){ // normalized rows choose one unit owner or zero; no varying parity
if(R.some(a=>a.some(r=>r.p!==a[0].p)))return UNKNOWN;
let mins=R.map(a=>F.B.map((_,j)=>a.reduce((x,r)=>r.c[j]<x?r.c[j]:x,a[0].c[j]))), cap=F.B.map((b,j)=>b-mins.reduce((s,a)=>s+a[j],0n));if(cap.some(c=>c<0n))return null;
let options=R.map((a,i)=>a.map(r=>{let d=r.c.map((v,j)=>v-mins[i][j]),nz=d.map((v,j)=>v?j:-1).filter(j=>j>=0);return nz.length===0?-1:nz.length===1&&d[nz[0]]===1n?nz[0]:-2}));if(options.some(a=>a.includes(-2)))return UNKNOWN;stats.matchingCalls++;
let slots=[],choice=Array(R.length).fill(-1);for(let j=0;j<cap.length;j++)for(let k=0;k<Number(cap[j]>BigInt(R.length)?BigInt(R.length):cap[j]);k++)slots.push(j);let occ=slots.map(()=>-1);
function aug(i,seen){for(let k=0;k<slots.length;k++){stats.matchingAttempts++;let a=options[i].indexOf(slots[k]);if(a<0||seen.has(k))continue;seen.add(k);if(occ[k]<0||aug(occ[k],seen)){occ[k]=i;choice[i]=a;return true}}return false}
for(let i=0;i<R.length;i++){let free=options[i].indexOf(-1);if(free>=0)choice[i]=free;else if(!aug(i,new Set()))return null}return R.map((a,i)=>a[choice[i]])}
function affine(F,R){if(F.B.some((b,j)=>R.reduce((s,a)=>s+a.reduce((v,r)=>r.c[j]>v?r.c[j]:v,0n),0n)>b))return UNKNOWN;
let base=new Map(), origins=[], anchor=0n, target=F.P.reduce((x,b,j)=>x|(BigInt(b)<<BigInt(j)),0n);
function add(M,v,k){while(v){let h=v.toString(2).length-1;if(!M.has(h)){M.set(h,[v,k]);return true}let a=M.get(h);v^=a[0];k^=a[1]}return false}
for(let i=0;i<R.length;i++){let a=R[i],z=a[0].p;anchor^=z;let M=new Map(),S=new Set(a.map(r=>r.p));for(let r of a){let d=r.p^z;if(add(M,d,0n)){let k=origins.length;origins.push([i,d]);add(base,d,1n<<BigInt(k))}}if(BigInt(S.size)!==(1n<<BigInt(M.size)))return UNKNOWN}
stats.affineCalls++;let v=target^anchor,k=0n;while(v){let a=base.get(v.toString(2).length-1);if(!a)return null;v^=a[0];k^=a[1]}let t=R.map(a=>a[0].p);origins.forEach(([i,d],j)=>{if((k>>BigInt(j))&1n)t[i]^=d});return R.map((a,i)=>a.find(r=>r.p===t[i]))}
function dag(F,R,limit=256){stats.dagCalls++;let M=new Map([["0|"+F.B.map(()=>0n).join(","),{p:0n,c:F.B.map(()=>0n),w:[]}]]);for(let a of R){let Q=new Map();for(let s of M.values())for(let r of a){stats.dagEdges++;let c=s.c.map((v,j)=>v+r.c[j]);if(c.some((v,j)=>v>F.B[j]))continue;let p=s.p^r.p,key=p+"|"+c.join(",");if(!Q.has(key))Q.set(key,{p,c,w:[...s.w,r]});stats.peakDAG=Math.max(stats.peakDAG,Q.size);if(Q.size>limit){stats.dagDeclines++;return UNKNOWN}}M=Q}let t=F.P.reduce((x,b,j)=>x|(BigInt(b)<<BigInt(j)),0n);for(let s of M.values())if(s.p===t)return s.w;return null}
function solve(F,opt={}){let root=closure(F,F.R);if(!root)return null;let C=cutset(F,root);
function go(R,k){stats.cutNodes++;R=closure(F,R);if(!R)return null;
if(!opt.cutOnly){for(let t of [matching,affine]){let w=t(F,R);if(w!==UNKNOWN)return w}if(!C.slice(k).length)return forest(F,R);let w=dag(F,R,opt.limit??256);if(w!==UNKNOWN)return w}
if(k===C.length)return forest(F,R);
let e=C[k],val=r=>e.j<F.B.length?r.c[e.j]:BigInt(bit(r.p,e.j-F.B.length));let D=[...new Set(R[e.i].map(val))];for(let d of D){stats.pinAttempts++;let Q=R.slice();Q[e.i]=Q[e.i].filter(r=>val(r)===d);let w=go(Q,k+1);if(w)return w}return null}
let w=go(root,0);if(w){stats.sourceChecks++;assert(valid(F,w),"solver witness")}return w}
function brute(F){let w=[];function rec(i){if(i===F.R.length){stats.bruteTuples++;return valid(F,w)}for(let r of F.R[i]){w.push(r);if(rec(i+1))return true;w.pop()}return false}return rec(0)}

function iteration(){
const ledger={roots:0,blocks:0,localQueries:0,budgetBisections:0,parityQueries:0,rowQueries:0,joins:0,peakWitnessEntries:0,capDeclines:0,exactFallbacks:0};
const cases={random:{SAT:0,UNSAT:0},cube:{SAT:0,UNSAT:0},fano:{SAT:0,UNSAT:0},wheel:{SAT:0,UNSAT:0},scaling:[],declines:[]};
function blockSolve(F,cap=4096n,force=false){
 ledger.roots++; let root=closure(F,F.R); if(!root)return {w:null,reason:"closure"};
 const n=root.length,b=F.B.length,q=F.P.length,N=n+b+q;
 const B=F.B.slice(),P=F.P.slice(),E=[],adj=Array.from({length:N},()=>[]);
 const R=root.map(a=>a.map(r=>({id:r.id,v:[],original:r})));
 for(let i=0;i<n;i++)for(let j=0;j<b+q;j++){
  const values=root[i].map(r=>j<b?r.c[j]:BigInt(bit(r.p,j-b)));
  const c=j<b?values.reduce((a,x)=>x<a?x:a):values[0];
  if(j<b)B[j]-=c;else P[j-b]^=Number(c);
  const v=values.map(x=>j<b?x-c:x^c);
  R[i].forEach((r,k)=>r.v[j]=v[k]);
  if(new Set(v).size>1){let id=E.length;E.push({i,j,u:i,v:n+j,d:new Set(v).size});adj[i].push(id);adj[n+j].push(id)}
 }
 let dfsn=0,disc=Array(N).fill(0),low=Array(N).fill(0),stack=[],blocks=[];
 function dfs(u,parent){disc[u]=low[u]=++dfsn;for(const id of adj[u]){if(id===parent)continue;const e=E[id],v=e.u===u?e.v:e.u;if(!disc[v]){stack.push(id);dfs(v,id);low[u]=Math.min(low[u],low[v]);if(low[v]>=disc[u]){let a=[],x;do{x=stack.pop();a.push(x)}while(x!==id);blocks.push(a)}}else if(disc[v]<disc[u]){stack.push(id);low[u]=Math.min(low[u],disc[v])}}}
 for(let u=0;u<N;u++)if(!disc[u])dfs(u,-1);
 const incident=Array.from({length:N},()=>[]),V=[],volumes=[];
 for(let k=0;k<blocks.length;k++){
  const vertices=[...new Set(blocks[k].flatMap(id=>[E[id].u,E[id].v]))].sort((x,y)=>x-y);V.push(vertices);vertices.forEach(u=>incident[u].push(k));
  let par=new Map(vertices.map(u=>[u,u]));function find(u){while(par.get(u)!==u)u=par.get(u);return u}
  let vol=1n;for(let id of blocks[k].slice().sort((a,c)=>E[c].d-E[a].d||a-c)){let e=E[id],x=find(e.u),y=find(e.v);if(x===y)vol*=BigInt(e.d);else par.set(x,y)}volumes.push(vol);
 }
 let sum=volumes.reduce((s,x)=>s+x,0n),product=volumes.reduce((s,x)=>s*x,1n);
 let info={blocks:blocks.length,sum:String(sum),product:String(product),max:String(volumes.reduce((a,x)=>a>x?a:x,1n)),rootRows:root.reduce((s,a)=>s+a.length,0)};
 ledger.blocks+=blocks.length;
 if(sum>cap&&!force){ledger.capDeclines++;ledger.exactFallbacks++;let w=solve(F,{limit:64});return {...info,w,reason:"cap fallback"}}
 const seen=new Set();
 function merge(a,c){let w=new Map(a);for(let [i,r] of c){assert(!w.has(i)||w.get(i)===r,"inconsistent articulation");w.set(i,r)}ledger.joins++;ledger.peakWitnessEntries=Math.max(ledger.peakWitnessEntries,w.size);return w}
 function vertex(u,parent){
  seen.add(u);let children=incident[u].filter(k=>k!==parent).map(k=>block(k,u));
  if(u<n){let M=new Map();for(let r of R[u]){let w=new Map([[u,r.original]]),ok=true;for(let C of children){if(!C.has(r.id)){ok=false;break}w=merge(w,C.get(r.id))}if(ok)M.set(r.id,w)}return M}
  if(u<n+b){let cost=0n,w=new Map();for(let C of children){if(!C)return null;cost+=C.cost;w=merge(w,C.w)}return {cost,w}}
  let M=new Map([[0,new Map()]]);for(let C of children){let Q=new Map();for(let [a,w] of M)for(let [c,v] of C)if(!Q.has(a^c))Q.set(a^c,merge(w,v));M=Q}return M
 }
 function block(k,parent){
  const vertices=V[k],rows=vertices.filter(u=>u<n),owners=vertices.filter(u=>u>=n);
  const children=new Map(vertices.filter(u=>u!==parent).map(u=>[u,vertex(u,k)]));
  const edgeSet=new Set(blocks[k].map(id=>E[id].i+","+E[id].j));
  const val=(r,i,j)=>edgeSet.has(i+","+j)?r.v[j]:0n;
  const domains=rows.map(i=>i===parent?R[i]:R[i].filter(r=>children.get(i).has(r.id)));
  const budgets=owners.filter(u=>u<n+b),parities=owners.filter(u=>u>=n+b);
  if(domains.some(a=>!a.length)||budgets.some(u=>u!==parent&&!children.get(u))||parities.some(u=>u!==parent&&!children.get(u).size)){
   return parent>=n&&parent<n+b?null:new Map();
  }
  function query(pin,threshold,target){
   ledger.localQueries++;
   const D=domains.map((a,l)=>rows[l]===parent?a.filter(r=>r.id===pin):a);
   const Q=parities.filter(u=>u===parent||children.get(u).size===1);
   const caps=budgets.map(u=>u===parent?threshold:B[u-n]-children.get(u).cost);
   const tags=Q.map(u=>u===parent?target:P[u-n-b]^[...children.get(u).keys()][0]);
   const local=input(caps,tags,D.map((a,l)=>a.map(r=>[budgets.map(u=>val(r,rows[l],u-n)),Q.reduce((p,u,j)=>p|(val(r,rows[l],u-n)<<BigInt(j)),0n)])));
   let localw=solve(local,{limit:64});if(!localw)return null;
   const chosen=localw.map((r,l)=>D[l][r.id]);let w=new Map();
   for(let l=0;l<rows.length;l++){let i=rows[l],r=chosen[l];w=merge(w,i===parent?new Map([[i,r.original]]):children.get(i).get(r.id))}
   for(let u of budgets)if(u!==parent)w=merge(w,children.get(u).w);
   for(let u of parities)if(u!==parent){let p=chosen.reduce((s,r,l)=>s^Number(val(r,rows[l],u-n)),0);let child=children.get(u).get(P[u-n-b]^p);assert(child,"parity child lift");w=merge(w,child)}
   return w
  }
  if(parent<n){let M=new Map();for(let r of R[parent]){ledger.rowQueries++;let w=query(r.id,null,null);if(w)M.set(r.id,w)}return M}
  if(parent>=n+b){let M=new Map();for(let t=0;t<2;t++){ledger.parityQueries++;let w=query(null,null,t);if(w)M.set(t,w)}return M}
  let hi=domains.reduce((s,a,l)=>s+a.reduce((m,r)=>val(r,rows[l],parent-n)>m?val(r,rows[l],parent-n):m,0n),0n);
  let w=query(null,hi,null);if(!w)return null;let lo=0n;
  while(lo<hi){ledger.budgetBisections++;let mid=(lo+hi)/2n,v=query(null,mid,null);if(v){hi=mid;w=v}else lo=mid+1n}
  // w remains feasible at hi; minimality ensures exact contribution hi.
  return {cost:hi,w}
 }
 let w=new Map();
 for(let u=0;u<N;u++)if(!seen.has(u)){
  let M=vertex(u,-1),v;
  if(u<n){v=M.values().next().value;if(!v)return {...info,w:null,reason:"block"}}
  else if(u<n+b){if(!M||M.cost>B[u-n])return {...info,w:null,reason:"block"};v=M.w}
  else{v=M.get(P[u-n-b]);if(!v)return {...info,w:null,reason:"block"}}
  w=merge(w,v)
 }
 const answer=F.R.map((_,i)=>w.get(i));assert(valid(F,answer),"original source rows");return {...info,w:answer,reason:"block"}
}
let seed=628071;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function check(F,expected,group){let a=blockSolve(F);assert(!!a.w===expected,group+" label");cases[group][a.w?"SAT":"UNSAT"]++;return a}
function cnf(n,cs){return input(cs.map(c=>c.length-1),[],Array.from({length:n},(_,i)=>[0,1].map(v=>[cs.map(c=>c.filter(l=>Math.abs(l)===i+1&&((l>0?1:0)!==v)).length),0])))}
for(let k=0;k<180;k++){
 let n=2+rnd(5),b=1+rnd(4),q=rnd(4),R=Array.from({length:n},()=>Array.from({length:2+rnd(3)},()=>[Array.from({length:b},()=>rnd(3)),rnd(1<<q)]));
 let B=Array.from({length:b},()=>rnd(2*n+1)),P=Array.from({length:q},()=>rnd(2));
 if(k%2===0){let a=R.map(rs=>rs[rnd(rs.length)]);B=B.map((_,j)=>a.reduce((s,r)=>s+r[0][j],0));let p=a.reduce((s,r)=>s^r[1],0);P=P.map((_,j)=>(p>>j)&1)}
 let F=input(B,P,R);check(F,brute(F),"random")
}
let cube=Array.from({length:8},(_,x)=>[0,1,2].map(i=>((x>>i)&1)?-(i+1):i+1));
for(let mask=0;mask<256;mask++)check(cnf(3,cube.filter((_,j)=>(mask>>j)&1)),mask!==255,"cube");
let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(a=>[a,a.map(v=>-v)]);
for(let j=-1;j<14;j++){let F=cnf(7,fano.filter((_,k)=>j!==k));assert(brute(F)===(j>=0),"Fano reference");check(F,j>=0,"fano")}
function rim(a,b,s){for(let z=0;z<64;z++){let x=[z&3,(z>>2)&3,(z>>4)&3];if(x.every((v,i)=>v!==x[(i+1)%3]&&v!==(a^(i===1?1:0))&&v!==(b^s^(i===1?0:1))))return x}return null}
function color(n,E){let q=4*E.length,vr=Array.from({length:n},()=>Array.from({length:4},()=>0n)),rr=[];E.forEach(([u,v,s],i)=>{for(let x=0;x<4;x++){vr[u][x]|=BigInt(x)<<BigInt(4*i);vr[v][x]|=BigInt(x)<<BigInt(4*i+2)}let a=[];for(let x=0;x<4;x++)for(let y=0;y<4;y++)if(rim(x,y,s))a.push([[],BigInt(x|(y<<2))<<BigInt(4*i)]);rr.push(a)});return input([],Array(q).fill(0),[...vr.map(a=>a.map(t=>[[],t])),...rr])}
for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let s=0;s<4;s++)assert(!!rim(a,b,s)===((a^b)!==s),"wheel projection");
for(let E of [[[0,1,0],[1,2,0],[0,2,0],[0,1,0]],[[0,1,0],[0,1,1],[0,1,2],[0,1,3]]]){
 let sat=E[1][0]===1,a=check(color(sat?3:2,E),sat,"wheel");if(a.w)for(let [u,v,s] of E)assert(rim(a.w[u].id,a.w[v].id,s),"wheel source lift")
}
for(let k of [4,16,64]){
 for(let type of ["budget-owner","parity-owner","row-articulation"])for(let sat of [true,false]){
  let F;
  if(type==="budget-owner"){
   let R=Array.from({length:2*k},(_,i)=>[0,1].map(x=>[[BigInt(x)*(1n<<65n)],BigInt(x)<<BigInt(i>>1)]));
   F=input([BigInt(k-(sat?0:1))*(1n<<65n)],Array(k).fill(1),R)
  }else if(type==="parity-owner"){
   let R=Array.from({length:2*k},(_,i)=>[0,1].map(x=>[Array.from({length:2*k},(_,j)=>j===2*(i>>1)?x:j===2*(i>>1)+1?1-x:0),x]));
   F=input(Array(2*k).fill(1),[(k%2)^(sat?0:1)],R)
  }else{
   let R=Array.from({length:k+1},(_,i)=>[0,1].map(x=>[Array.from({length:k},(_,j)=>i===j||i===j+1?x:0),((i>0?1n<<BigInt(i-1):0n)^(i<k?1n<<BigInt(i):0n))*BigInt(x)]));
   let P=Array(k).fill(0);if(!sat)P[1]=1;F=input(Array(k).fill(1),P,R)
  }
  const a=blockSolve(F);assert(!!a.w===sat,"scale "+type+" "+k);assert(a.reason==="block","scale should use block backend");
  cases.scaling.push({type,k,sat,blocks:a.blocks,sum:a.sum,product:a.product,max:a.max,rootRows:a.rootRows})
 }
}
let capF=input([1,1],[],[[[[1,0],0],[[0,1],0]],[[[1,0],0],[[0,1],0]]]);let capR=blockSolve(capF,0n);assert(capR.w&&capR.reason==="cap fallback","cap fallback");cases.declines.push({reason:capR.reason,sat:!!capR.w});
return {seed:628071,cases,ledger,BS05stats:stats,limitations:"No strict physical replay, S06 scaled exception or BD06 modular/DP07 peeling integration; no measured memory bytes or cumulative memory. Prior BS05 code reused as local exact oracle."}
}
return iteration();
};
console.log(JSON.stringify(experiment(),null,2));
