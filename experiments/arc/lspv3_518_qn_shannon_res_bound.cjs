"use strict";
/* LSPV-3/518 original-source Shannon Resolution audit.
   Plain ECMAScript; node experiments/arc/lspv3_518_qn_shannon_res_bound.cjs
   Separate RES-only semantics, not a historical R_mix341 byte checker. */
const ck=(p,s)=>{if(!p)throw Error(s)},uniq=a=>[...new Set(a)],norm=a=>uniq(a).sort((x,y)=>Math.abs(x)-Math.abs(y));
const bit=x=>Math.log2(x),pop=x=>{let v=0;for(;x;x>>>=1)v+=x&1;return v};
function source(n,M){
 let N=1<<n,es=[];ck(M.length===N,"length");
 for(let a=0;a<N;a++){let b=M[a],j=bit(a^b);ck(b>=0&&b<N&&M[b]===a&&b!==a&&pop(a^b)===1,"matching");
  if(a<b){let c=[];for(let k=0;k<n;k++)if(k!==j)c.push(a&(1<<k)?-(k+1):k+1);es.push({a,b,j,c})}}
 es.sort((x,y)=>x.a-y.a||x.b-y.b);ck(es.length===N/2,"count");
 let by=Array(N).fill(-1),ds=Array(n).fill(0);
 es.forEach((e,i)=>{by[e.a]=by[e.b]=i;ds[e.j]++});
 return {n,N,m:es.length,es,by,ds};
}
const falseAt=(c,v)=>c.every(l=>((v>>(Math.abs(l)-1))&1)!==Number(l>0));
function originalAudit(S){
 for(let v=0;v<S.N;v++){let bad=[];for(let j=0;j<S.m;j++)if(falseAt(S.es[j].c,v))bad.push(j);
  ck(bad.length===1&&bad[0]===S.by[v],"source assignment partition")}
 for(let e of S.es){let w=[];for(let v=0;v<S.N;v++)if(falseAt(e.c,v))w.push(v);
  ck(w.length===2&&w[0]===e.a&&w[1]===e.b,"source deletion witnesses")}
}
function gen(S,order){
 let m=S.m,t=[];
 const get=id=>id<m?S.es[id].c:t[id-m].c;
 function step(d,prefix){
  if(d===S.n)return S.by[prefix];
  let v=order[d],lo=step(d+1,prefix),hi=step(d+1,prefix|(1<<v));
  let a=get(lo),b=get(hi),p=v+1;
  if(!a.includes(p)&&!a.includes(-p))return lo;
  if(!b.includes(p)&&!b.includes(-p))return hi;
  ck(a.includes(p)&&b.includes(-p),"oriented pivot");
  let c=norm([...a.filter(z=>z!==p),...b.filter(z=>z!==-p)]);
  ck(!c.some(z=>c.includes(-z)),"tautological proof line");
  let id=m+t.length;t.push({a:lo,b:hi,p,c});return id;
 }
 let root=step(0,0);ck(get(root).length===0,"nonempty");
 let used=new Set();function visit(id){if(id<m||used.has(id))return;used.add(id);visit(t[id-m].a);visit(t[id-m].b)}
 visit(root);
 let kept=[...used].sort((a,b)=>a-b),remap=new Map(kept.map((id,i)=>[id,m+i]));
 let nodes=kept.map(id=>{let x=t[id-m];return {a:x.a<m?x.a:remap.get(x.a),b:x.b<m?x.b:remap.get(x.b),p:x.p,c:x.c}});
 return {nodes,root:root<m?root:remap.get(root),order,generated:t.length};
}
function check(S,P){
 let m=S.m,a=S.es.map(e=>e.c),depth=Array(m).fill(0);
 for(let i=0;i<P.nodes.length;i++){
  let x=P.nodes[i];ck(x.a>=0&&x.b>=0&&x.a<m+i&&x.b<m+i,"parent refs");
  ck(x.p>=1&&x.p<=S.n&&a[x.a].includes(x.p)&&a[x.b].includes(-x.p),"signed RES");
  let c=norm([...a[x.a].filter(z=>z!==x.p),...a[x.b].filter(z=>z!==-x.p)]);
  ck(c.length===x.c.length&&c.every((z,k)=>z===x.c[k]),"output RES");
  a.push(c);depth.push(1+Math.max(depth[x.a],depth[x.b]));
 }
 ck(P.root===a.length-1&&a[P.root].length===0,"empty root");
 let used=new Set(),walk=id=>{if(used.has(id))return;used.add(id);if(id>=m){walk(P.nodes[id-m].a);walk(P.nodes[id-m].b)}};walk(P.root);
 ck(used.size===a.length,"source missing or unreachable node");
 return {q:P.nodes.length,depth:depth[P.root]};
}
function orders(a){if(a.length<2)return [a];let z=[];for(let i=0;i<a.length;i++)for(let t of orders(a.filter((_,j)=>j!==i)))z.push([a[i],...t]);return z}
function matchings4(){let M=Array(16).fill(-1),out=[];
 function rec(){let u=M.indexOf(-1);if(u<0){out.push(M.slice());return}
  for(let j=0;j<4;j++){let v=u^(1<<j);if(M[v]<0){M[u]=v;M[v]=u;rec();M[u]=M[v]=-1}}}
 rec();return out;
}
function rng(seed){let x=seed>>>0;return ()=>x=(Math.imul(x,1664525)+1013904223)>>>0}
function randomM(n,seed){
 let N=1<<n,M=Array.from({length:N},(_,v)=>v^1),r=rng(seed);
 for(let k=0;k<3500;k++){let i=r()%n,j=r()%(n-1);if(j>=i)j++;
  let a=r()%N;a&=~((1<<i)|(1<<j));let b=a^(1<<i),c=a^(1<<j),d=b^(1<<j);
  if(M[a]===b&&M[c]===d){M[a]=c;M[c]=a;M[b]=d;M[d]=b}
  else if(M[a]===c&&M[b]===d){M[a]=b;M[b]=a;M[c]=d;M[d]=c}
 }return M;
}
function test(n,M,allOrders){
 let S=source(n,M);originalAudit(S);
 let most=S.ds.indexOf(Math.max(...S.ds)),order=[...Array(n).keys()].filter(j=>j!==most).concat(most);
 let base=gen(S,order),baseV=check(S,base);
 let UB=2*S.m-1-S.ds[most];
 ck(baseV.q>=S.m-1&&baseV.q<=UB,"claimed source-work bounds");
 let best=baseV.q,dep=baseV.depth;
 if(allOrders)for(let ord of orders([...Array(n).keys()])){let v=check(S,gen(S,ord));if(v.q<best){best=v.q;dep=v.depth}}
 let tamper=JSON.parse(JSON.stringify(base));tamper.nodes.at(-1).p=n+1;
 let fails=0;try{check(S,tamper)}catch(e){fails++}
 tamper=JSON.parse(JSON.stringify(base));tamper.nodes.at(-1).c=[1];
 try{check(S,tamper)}catch(e){fails++}
 let corrupted=source(n,M);corrupted.es[0].c[0]*=-1;
 try{originalAudit(corrupted)}catch(e){fails++}
 ck(fails===3,"negative controls");
 return {n,m:S.m,directions:S.ds,max_direction:S.ds[most],q_heuristic:baseV.q,q_best_order:best,depth_best:dep,upper_bound:UB,negative_rejects:fails};
}
const all4=matchings4();ck(all4.length===272,"all 272 matchings");
let hist={},maxHeuristic=0,tight=0;
for(let M of all4){let t=test(4,M,true);hist[t.q_best_order]=(hist[t.q_best_order]||0)+1;
 maxHeuristic=Math.max(maxHeuristic,t.q_heuristic);if(t.q_heuristic===t.upper_bound)tight++}
let others=[];
for(let n=5;n<=8;n++)for(let i=0;i<(n===8?5:n===7?7:n===6?10:12);i++)others.push(test(n,randomM(n,n*10001+i*19+77),false));
const results={run:"LSPV3-518-QN-RES-SHANNON-v1",status:"PASS",q4_matchings:272,q4_best_order_histogram:hist,q4_heuristic_max:maxHeuristic,q4_bound_equal_count:tight,additional_samples:others.length,additional_results:others,negative_rejections:3*(272+others.length),scope:"Original signed clauses plus ordinary binary Resolution; not an R_mix341 byte acceptance test",theorem:"For any perfect hypercube matching: m-1 <= W_RES <= 2m-1-max_j d_j <= (2-1/n)m-1. With m=2^(n-1), only n=4 is strict 3-CNF."};
if(typeof console!=="undefined")console.log(JSON.stringify(results));
