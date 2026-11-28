// Grok 4.7 work 2026-11-28 20:47 KST.
// (1) Exhaustive check of the B4 lemma from the 03:00 UCAC report.
// (2) Reduction: positive 1-in-3-SAT -> SYN(H,b,M) with M a matching (block size <= 2),
//     cross-checked against brute force AND against upstream trellis.js (bf35811).
// (3) Exact minimum over block orders of the max trellis cut rank (subset DP), small sizes;
//     source-order and greedy-order widths for larger sizes (upper bounds only).
'use strict';
const {trellis}=require('./2026-11-28_2051_trellis_upstream_bf35811.js');
function rng(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
// ---- (1) B4 lemma
let b4ok=true;
for(let s=0;s<16;s++){const a=s&1,b=s>>1&1,c=s>>2&1,d=s>>3&1;
  const lhs=((a^b^c^d)===0)&&(((a^b)===1)||((a^c)===1)); const w=a+b+c+d; if(lhs!==(w===2))b4ok=false;}
console.log(JSON.stringify({B4_lemma_exhaustive_16:b4ok}));
// ---- (2) reduction
function gen(n,m,R){const C=[];for(let k=0;k<m;k++){let a,b,c;do{a=R()*n|0;b=R()*n|0;c=R()*n|0}while(a===b||b===c||a===c);C.push([a,b,c])}return C}
function reduce(n,C){ // columns: copy (k,pos) -> 3k+pos
  const m=3*C.length,H=[],edges=[];const last=Array(n).fill(-1);
  C.forEach((cl,k)=>{H.push(1n|(1n<<BigInt(3*k+1))|(1n<<BigInt(3*k+2))|(1n<<BigInt(3*k+3))); // z_a+z_b+z_c=1
    edges.push([3*k,3*k+1]); // NAND(z_a,z_b)
    cl.forEach((v,p)=>{const col=3*k+p;if(last[v]>=0)H.push((1n<<BigInt(last[v]+1))|(1n<<BigInt(col+1)));last[v]=col;});});
  return {H,edges,m};
}
function brute(n,C){for(let x=0;x<(1<<n);x++){if(C.every(([a,b,c])=>((x>>a&1)+(x>>b&1)+(x>>c&1))===1))return x}return -1}
function checkWitness(n,C,inst,hex){const z=BigInt('0x'+hex);const bit=i=>Number(z>>BigInt(i+1)&1n);
  for(const row of inst.H){let s=Number(row&1n);let t=0;for(let i=0;i<inst.m;i++)if(row>>BigInt(i+1)&1n)t^=bit(i);if(t!==s)return false}
  for(const [a,b] of inst.edges)if(bit(a)&&bit(b))return false;
  const x=Array(n).fill(null);for(let k=0;k<C.length;k++)for(let p=0;p<3;p++){const v=C[k][p],val=bit(3*k+p);if(x[v]!==null&&x[v]!==val)return false;x[v]=val}
  return C.every(cl=>cl.reduce((s,v)=>s+x[v],0)===1);}
const R=rng(20261128);let agree=0,dis=0,yes=0,no=0,wit=0,unk=0;
for(let trial=0;trial<400;trial++){const n=6+(trial%9),m=Math.max(2,Math.round(n*(0.4+0.6*R())));
  const C=gen(n,m,R),inst=reduce(n,C),bf=brute(n,C)>=0;const tr=trellis(inst.H,inst.edges,inst.m,64);
  if(tr.decision==='UNKNOWN'){unk++;continue}
  const t=tr.decision==='YES';if(t===bf)agree++;else dis++; if(t){yes++;if(checkWitness(n,C,inst,tr.witness))wit++}else no++;}
console.log(JSON.stringify({reduction_vs_bruteforce_via_upstream_trellis:{trials:400,agree,disagree:dis,yes,no,unknown:unk,yes_witness_lifted_and_checked:wit}}));
// ---- (3) widths
function rankOf(vecs){const B=new Map();let r=0;for(let v of vecs){while(v){const k=v&-v;if(!B.has(k)){B.set(k,v);r++;break}v^=B.get(k)}}return r}
function columns(inst){const cols=Array(inst.m).fill(0n);inst.H.forEach((row,j)=>{for(let i=0;i<inst.m;i++)if(row>>BigInt(i+1)&1n)cols[i]|=1n<<BigInt(j)});return cols}
function blocksOf(inst){const p=Array.from({length:inst.m},(_,i)=>i),root=i=>{while(p[i]!==i)i=p[i];return i};for(const [a,b] of inst.edges)p[root(a)]=root(b);
  const g=new Map();for(let i=0;i<inst.m;i++){const r=root(i);if(!g.has(r))g.set(r,[]);g.get(r).push(i)}return [...g.values()]}
function lambdaFn(cols,blocks){const rE=rankOf(cols);return S=>{const A=[],B=[];blocks.forEach((bl,i)=>{for(const j of bl)((S>>i)&1?A:B).push(cols[j])});return rankOf(A)+rankOf(B)-rE}}
function exactMinWidth(inst){const cols=columns(inst),bl=blocksOf(inst),k=bl.length,lam=lambdaFn(cols,bl),full=(1<<k)-1;
  const L=new Int32Array(1<<k);for(let S=0;S<=full;S++)L[S]=lam(S);
  const g=new Int32Array(1<<k).fill(1e9);g[0]=0;for(let S=1;S<=full;S++){let best=1e9;for(let i=0;i<k;i++)if(S>>i&1){const v=g[S^(1<<i)];if(v<best)best=v}g[S]=Math.max(best,L[S])}
  return {blocks:k,minWidth:g[full],rank:rankOf(cols)}}
function greedyWidth(inst){const cols=columns(inst),bl=blocksOf(inst),rE=rankOf(cols);let used=new Array(bl.length).fill(false),pref=[],worst=0;
  for(let step=0;step<bl.length;step++){let best=null,bw=1e9;for(let i=0;i<bl.length;i++)if(!used[i]){const A=pref.concat(bl[i].map(j=>cols[j])),Bv=[];bl.forEach((b,t)=>{if(!used[t]&&t!==i)for(const j of b)Bv.push(cols[j])});const w=rankOf(A)+rankOf(Bv)-rE;if(w<bw){bw=w;best=i}}
    used[best]=true;pref=pref.concat(bl[best].map(j=>cols[j]));worst=Math.max(worst,bw)}return worst}
const R2=rng(777);const small=[];
for(const m of [3,4,5,6,7,8,9]){let ws=[];for(let s=0;s<6;s++){const n=Math.ceil(m*1.6),C=gen(n,m,R2),inst=reduce(n,C);const e=exactMinWidth(inst);const src=trellis(inst.H,inst.edges,inst.m,0).maxWidth;ws.push([e.minWidth,src])}
  small.push({clauses:m,blocks:2*m,exact_min_width:ws.map(x=>x[0]),source_order_width:ws.map(x=>x[1])})}
console.log(JSON.stringify({exact_min_block_order_width_small:small}));
const R3=rng(4242);const large=[];
for(const m of [10,20,40,80,160]){let ws=[];for(let s=0;s<3;s++){const n=Math.ceil(m*1.6),C=gen(n,m,R3),inst=reduce(n,C);ws.push([trellis(inst.H,inst.edges,inst.m,0).maxWidth,greedyWidth(inst),3*m])}
  large.push({clauses:m,source_width:ws.map(x=>x[0]),greedy_width:ws.map(x=>x[1]),N_cols:3*m})}
console.log(JSON.stringify({upper_bound_widths_large:large}));
