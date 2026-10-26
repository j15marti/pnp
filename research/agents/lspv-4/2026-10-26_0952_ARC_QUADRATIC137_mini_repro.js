#!/usr/bin/env node
"use strict";
// Standalone exact finite source-authenticated quadratic/2-level audit (Node 18+).
// Matches the restricted grammar, NOT a proof of P != NP.
const audit137=function audit137(){
  const A=(v,msg)=>{if(!v)throw Error(msg)};
  function xor3(v,b){const out=[];for(let z=0;z<8;z++){const bits=v.map((_,i)=>(z>>i)&1);if((bits.reduce((a,x)=>a+x,0)&1)===b)continue;out.push(v.map((id,i)=>bits[i]?-id:id))}return out}
  const mixed=[...xor3([1,2,3],0),[1,2,4],[-1,-2,4],[1,2,-4],[-1,-2,-4],[-3,5,6],[-3,5,-6],[-3,-5,6],[-3,-5,-6]];
  const n=6;
  const Wraw=`-1 3 -14 2 -8 9 10 -13 14 3 7 -13 -4 -9 -11 5 8 -14 4 -8 -11 1 7 13 1 -7 10 -5 -6 -15 -2 -6 12 -4 9 -10 -2 5 -12 -3 6 -15 6 -7 11 2 -9 11 4 8 -10 -3 12 15 -5 -12 15 -1 13 14`;
  const wl=Wraw.split(/\s+/).map(Number),W=[];for(let i=0;i<wl.length;i+=3)W.push(wl.slice(i,i+3));
  function ring(n){const monos=[[]];for(let v=1;v<=n;v++)monos.push([v]);for(let a=1;a<=n;a++)for(let b=a+1;b<=n;b++)monos.push([a,b]);const pos=new Map(monos.map((m,i)=>[m.join(","),i]));function bit(m){return 1n<<BigInt(pos.get(m.join(",")))};function mult(x,y){let z=0n;for(let i=0;i<monos.length;i++)if((x>>BigInt(i))&1n)for(let j=0;j<monos.length;j++)if((y>>BigInt(j))&1n){const m=[...new Set([...monos[i],...monos[j]])].sort((a,b)=>a-b);if(m.length>2)throw Error("degree overflow");z ^= bit(m)}return z};return {n,monos,bit,mult}}
  function falsePoly(C,alpha,R){let p=1n;for(const l of C){const v=Math.abs(l);if(v in alpha){if(alpha[v]===Number(l>0))return null;continue}p=R.mult(p,l<0?R.bit([v]):(1n^R.bit([v])))}return p}
  function macros(Cs){const groups=new Map();for(const C of Cs){const names=C.map(Math.abs).sort((a,b)=>a-b),k=names.join(",");if(!groups.has(k))groups.set(k,{names,pats:new Map()});const signs=new Map(C.map(x=>[Math.abs(x),Number(x<0)]));const p=names.map(v=>signs.get(v)).join("");groups.get(k).pats.set(p,true)}const out=[];for(const g of groups.values())for(let b=0;b<=1;b++){let valid=true;for(let mask=0;mask<8;mask++){const z=[mask&1,(mask>>1)&1,(mask>>2)&1];if((z[0]+z[1]+z[2])%2!==b && !g.pats.has(z.join("")))valid=false}if(valid)out.push({vs:g.names,b})}return out}
  function hasSpan(cs,n,alpha,R,allowed="both"){const pols=[];
    if(allowed!=="xor"){for(const C of cs){const count=C.reduce((s,l)=>s+Number(!(Math.abs(l) in alpha)),0);if(count<=2){const p=falsePoly(C,alpha,R);if(p!==null)pols.push(p)}}}
    if(allowed!=="clause"){for(const {vs,b} of macros(cs)){let p=BigInt(b);for(const v of vs)p ^= (v in alpha)?BigInt(alpha[v]):R.bit([v]);pols.push(p)}}
    const terms=[];for(const p of pols){terms.push(p);if((p>>BigInt(n+1))===0n)for(let v=1;v<=n;v++)if(!(v in alpha))terms.push(R.mult(p,R.bit([v])))}
    const B=new Map();function high(p){return p.toString(2).length-1}
    for(let p of terms){while(p!==0n){const k=high(p);if(!B.has(k)){B.set(k,p);break}p ^= B.get(k)}}
    let x=1n;while(x!==0n){const k=high(x);if(!B.has(k))return false;x ^= B.get(k)}return true;
  }
  function satisfiable(cs,n){for(let x=0;x<(1<<n);x++){let yes=true;for(const C of cs){if(!C.some(l=>Number((x>>(Math.abs(l)-1))&1)===Number(l>0))){yes=false;break}}if(yes)return true}return false}
  function connected(cs,n){const adj=Array.from({length:n+1},()=>new Set());for(const C of cs){const vs=C.map(Math.abs);for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){adj[vs[i]].add(vs[j]);adj[vs[j]].add(vs[i])}}const seen=new Set([1]),stack=[1];while(stack.length){const v=stack.pop();for(const w of adj[v])if(!seen.has(w)){seen.add(w);stack.push(w)}}return seen.size===n}
  function twoDepth(cs,n){const R=ring(n),cache=new Map();function solve(alpha){const key=Object.entries(alpha).sort((a,b)=>Number(a[0])-Number(b[0])).map(e=>e.join(":")).join(",");if(!cache.has(key))cache.set(key,hasSpan(cs,n,alpha,R));return cache.get(key)}
    for(let v=1;v<=n;v++){let ok=true;for(const b of [0,1]){let found=false;for(let w=1;w<=n;w++)if(w!==v&&solve({[v]:b,[w]:0})&&solve({[v]:b,[w]:1})){found=true;break}if(!found){ok=false;break}}if(ok)return {exists:true,root:v,checks:cache.size}}return {exists:false,checks:cache.size}}
  const R=ring(6);A(mixed.length===12,"12 clauses");A(connected(mixed,6),"connected mixed");A(!satisfiable(mixed,6),"mixed UNSAT");
  A(!hasSpan(mixed,6,{},R),"root no identity");
  for(const t of [0,1]){A(!hasSpan(mixed,6,{4:t},R),"u-only no identity");A(!hasSpan(mixed,6,{5:t},R),"v-only no identity")}
  const leafResults=[];for(const x of [0,1])for(const y of [0,1]){const alpha={4:x,5:y};
    A(hasSpan(mixed,6,alpha,R),"leaf identity");A(!hasSpan(mixed,6,alpha,R,"clause"),"nonlinear alone consistent");A(!hasSpan(mixed,6,alpha,R,"xor"),"affine alone consistent");
    const Ais=x===0?[4,5]:[6,7], Bis=y===0?[8,9]:[10,11];
    let p=0n;for(const id of [...Ais,...Bis])p ^= falsePoly(mixed[id],alpha,R);
    const quartet=macros(mixed).find(g=>g.vs.join(",")==="1,2,3"&&g.b===0);A(!!quartet,"authenticated XOR quartet");
    for(const v of quartet.vs)p ^= (v in alpha)?BigInt(alpha[v]):R.bit([v]);A(p===1n,"explicit 5-term identity");
    leafResults.push({branch:`${x}${y}`,mixed_identity:true,authenticated_clause_ids:[...Ais,...Bis],xor_clause_ids:[0,1,2,3]})
  }
  const positive=Array(16).fill(0),negative=Array(16).fill(0);
  for(const C of W)for(const l of C)(l>0?positive:negative)[Math.abs(l)]++;
  A(W.length===20,"W20 count");A(connected(W,15),"W20 connected");A(!satisfiable(W,15),"W20 UNSAT");
  for(let v=1;v<=15;v++)A(positive[v]===2&&negative[v]===2,"W20 signed exactly 2,2");
  const hostile=twoDepth(W,15);A(!hostile.exists,"W20 escaped depth2 bounded grammar");
  const sourceText=`p cnf 6 12\n`+mixed.map(C=>C.join(" ")+" 0\n").join("");
  return {run_id:"ARC-QUADRATIC-SOURCE137",checked_in:"GitHub mini-reproducer",source_chars:sourceText.length,source_bits:sourceText.length*8,
    mixed:{clauses:12,variables:6,connected:true,sat:false,root_cert:false,first_level_cert:false,leaves:leafResults},
    w20:{variables:15,clauses:20,signed_exact22:true,connected:true,sat:false,two_adaptive_levels_possible:hostile.exists,span_calls:hostile.checks},
    warning:"Finite exact tests only. Restricted syntactic degree-two grammar; not an arbitrary SAT lower bound."};
};
console.log(JSON.stringify(audit137(),null,2));
