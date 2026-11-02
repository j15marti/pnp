#!/usr/bin/env node
"use strict";
/* LSPV-4 GATE325. Deterministic canonical same-original source-to-circuit
 * audit, independent of SAT label. Usage:
 * node cubic_matching_gate_audit325.js > summary325.json
 * Restricted evaluator upper bound only; P versus NP OPEN.
 */
const F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],
 [-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
const Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],
 [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
const P15=[[1,2,7],[1,3,8],[4,5,9],[4,6,10],[2,3,5],
 [6,11,12],[7,11,13],[8,12,14],[9,13,15],[10,14,15]];
const N15=[[1,2,11],[2,3,11],[1,3,12],[4,5,13],[5,6,14],
 [4,6,15],[7,8,12],[8,9,13],[9,10,14],[10,7,15]];
const F15=P15.concat(N15.map(c=>c.map(v=>-v)));
function requireTrue(ok,msg){if(!ok)throw Error(msg);}
function tight(){
 const edges=[[0,1],[2,3],[4,5]],six=[[6,7],[6,8],[6,9],[7,8],[7,9],[8,9]];
 for(let i=0;i<6;i++)for(const u of six[i])edges.push([i,u]);
 const pos=Array.from({length:10},()=>[]);
 edges.forEach(([a,b],i)=>{pos[a].push(i+1);pos[b].push(i+1);});
 return pos.concat(pos.map(c=>c.map(v=>-v)));
}
function canonical(C,n){
 if(n<3||n%3||3*C.length!==4*n)return false;
 const p=Array(n+1).fill(0),q=Array(n+1).fill(0),seen=new Set();
 for(const c of C){
  if(c.length!==3||c.some(v=>!Number.isInteger(v)||v===0||Math.abs(v)>n))return false;
  if(new Set(c.map(Math.abs)).size!==3||c.some(v=>(v>0)!==(c[0]>0)))return false;
  const key=c.slice().sort((x,y)=>x-y).join(",");if(seen.has(key))return false;seen.add(key);
  c.forEach(v=>(v>0?p:q)[Math.abs(v)]++);
 }
 return Array.from({length:n},(_,i)=>i+1).every(i=>p[i]===2&&q[i]===2);
}
function graph(C,n){
 requireTrue(canonical(C,n),"invalid original");
 const e=new Map(),weights=new Map(),degree=Array(C.length).fill(0);
 C.forEach((c,i)=>c.forEach(v=>{if(!e.has(v))e.set(v,[]);e.get(v).push(i);}));
 requireTrue(e.size===2*n,"signed edges");
 for(const [v,ids] of e){
  requireTrue(ids.length===2&&ids[0]!==ids[1],"bad signed two occurrences");
  const a=Math.min(...ids),b=Math.max(...ids),key=a+","+b;
  weights.set(key,(weights.get(key)||0)+1);degree[a]++;degree[b]++;
 }
 requireTrue(degree.every(d=>d===3),"noncubic");
 requireTrue([...weights.values()].every(w=>w<=2),"duplicate source clauses");
 return {e,weights};
}
function maximal(C,n){
 const {e,weights}=graph(C,n),used=new Set(),pairs=[];
 for(const s of [...e.keys()].sort((a,b)=>Math.abs(a)-Math.abs(b)||(b-a))){
  const [a,b]=e.get(s);
  if(!used.has(a)&&!used.has(b)){used.add(a);used.add(b);pairs.push([a,b,weights.get(Math.min(a,b)+","+Math.max(a,b))]);}
 }
 for(const key of weights.keys()){
  const [a,b]=key.split(",").map(Number);
  requireTrue(used.has(a)||used.has(b),"matching not maximal");
 }
 requireTrue(10*pairs.length>=3*C.length,"matching guarantee");
 return {pairs,weight:pairs.reduce((s,x)=>s+x[2],0),weights};
}
function optimum(C,weights){
 let result=0;
 for(const sign of [1,-1]){
  const ids=C.map((c,i)=>[c[0]>0?1:-1,i]).filter(v=>v[0]===sign).map(v=>v[1]);
  requireTrue(ids.length<=12,"finite exhaustive optimum limited to 12 clause vertices");
  const memo=new Map();
  function dp(mask){
   if(!mask)return 0;if(memo.has(mask))return memo.get(mask);
   const a=Math.floor(Math.log2(mask&-mask)),z=mask^(1<<a);
   let best=dp(z);
   for(let b=a+1;b<ids.length;b++)if((z>>b)&1){
    const x=Math.min(ids[a],ids[b]),y=Math.max(ids[a],ids[b]);
    const w=weights.get(x+","+y)||0;
    if(w)best=Math.max(best,w+dp(z^(1<<b)));
   }memo.set(mask,best);return best;
  }
  result+=dp((1<<ids.length)-1);
 }
 return result;
}
function compiler(C,n){
 const m=C.length,{pairs,weight,weights}=maximal(C,n),used=new Set(),gates=[],depth={};
 for(let i=1;i<=n;i++)depth[i]=0;
 const add=(op,a,b)=>{const k=n+gates.length+1;gates.push([op,a,b]);depth[k]=1+Math.max(depth[a],depth[b]);return k;};
 const group=(A,B)=>{
  const common=[...new Set(A.map(Math.abs))].filter(v=>B.some(w=>Math.abs(w)===v)).sort((a,b)=>a-b);
  const U=A.map(Math.abs).filter(v=>!common.includes(v)).sort((a,b)=>a-b);
  const V=B.map(Math.abs).filter(v=>!common.includes(v)).sort((a,b)=>a-b);
  if(A[0]>0&&common.length===2)return add("OR",add("OR",common[0],common[1]),add("AND",U[0],V[0]));
  if(A[0]>0)return add("OR",common[0],add("AND",add("OR",U[0],U[1]),add("OR",V[0],V[1])));
  if(common.length===2)return add("NAND",add("AND",common[0],common[1]),add("OR",U[0],V[0]));
  return add("NAND",common[0],add("OR",add("AND",U[0],U[1]),add("AND",V[0],V[1])));
 };
 const single=A=>{const v=A.map(Math.abs).sort((a,b)=>a-b);return A[0]>0
  ?add("OR",add("OR",v[0],v[1]),v[2])
  :add("NAND",add("AND",v[0],v[1]),v[2]);};
 let outs=[];
 for(const [a,b] of pairs){used.add(a);used.add(b);outs.push(group(C[a],C[b]));}
 C.forEach((c,i)=>{if(!used.has(i))outs.push(single(c));});
 while(outs.length>1){
  const next=[];for(let i=0;i<outs.length;i+=2)next.push(i+1<outs.length?add("AND",outs[i],outs[i+1]):outs[i]);outs=next;
 }
 const output=outs[0],g=gates.length,w=Math.ceil(Math.log2(n+g+1));
 requireTrue(g===3*m-1-weight&&g<=3*m-1-Math.ceil(3*m/10),"gate count");
 return {n,m,original_clauses:C,pairs_1based:pairs.map(([a,b,r])=>[a+1,b+1,r]),matching_size:pairs.length,
  matching_weight:weight,optimal_matching_weight_exact_finite:optimum(C,weights),gate_count:g,
  gates,output,depth:depth[output],fixed_gate_operand_width_bits:w,fixed_gate_descriptor_bits:g*(2*w+2)};
}
function original(C,mask){return C.every(row=>row.some(v=>Boolean((mask>>(Math.abs(v)-1))&1)===(v>0)));}
function evaluate(f,mask){
 const vals=Array(f.n+f.gates.length+1).fill(0);
 for(let i=1;i<=f.n;i++)vals[i]=(mask>>(i-1))&1;
 f.gates.forEach(([op,a,b],i)=>{vals[f.n+i+1]=op==="AND"?(vals[a]&vals[b]):op==="OR"?(vals[a]|vals[b]):1-(vals[a]&vals[b]);});
 return vals[f.output]===1;
}
function countPin(f,pins){
 const free=Array.from({length:f.n},(_,i)=>i+1).filter(i=>pins[i]===undefined);
 let count=0;for(let z=0;z<(1<<free.length);z++){
  let mask=0;Object.entries(pins).forEach(([i,v])=>mask|=v<<(Number(i)-1));
  free.forEach((i,j)=>mask|=((z>>j)&1)<<(i-1));
  requireTrue(original(f.original_clauses,mask)===evaluate(f,mask),"same original pins/circuit mismatch");
  count+=Number(original(f.original_clauses,mask));
 }return count;
}
const fixtures={Y6:compiler(Y6,6),F9:compiler(F9,9),F15:compiler(F15,15),TIGHT15:compiler(tight(),15)};
let allRows=0;
for(const f of Object.values(fixtures)){
 let sat=0;for(let z=0;z<(1<<f.n);z++){
  requireTrue(original(f.original_clauses,z)===evaluate(f,z),"original circuit mismatch at "+z);
  sat+=Number(original(f.original_clauses,z));
 }f.original_models=sat;allRows+=1<<f.n;
}
requireTrue(allRows===66112,"row count");
requireTrue(JSON.stringify(Object.values(fixtures).map(f=>[f.gate_count,f.matching_size,f.matching_weight,f.optimal_matching_weight_exact_finite,f.original_models]))
 ===JSON.stringify([[19,4,4,4,20],[29,5,6,7,70],[51,8,8,11,1032],[53,6,6,10,1686]]),"expected fixture metrics");
const common={3:0,5:1,6:0,7:0,8:0};
const both={SAT:countPin(fixtures.F9,{...common,1:0}),UNSAT:countPin(fixtures.F9,{...common,1:1})};
requireTrue(both.SAT===2&&both.UNSAT===0,"source both labels");
const output={run:"CUBIC_MAXIMAL_MATCH_GATE325",status:"PROVED restricted mathematical lemma; COMPUTATIONAL exhaustive fixtures; universal decision bound OPEN",
 canonical_only:true,matching_bound:"k >= ceil(3m/10)",gate_bound:"g <= 3m-1-ceil(3m/10)<=18n/5-1",
 output_not_sat_decision:true,all_rows:allRows,same_original_F9:both,fixtures,FLMV_native_simulation:false,P_vs_NP:"OPEN"};
process.stdout.write(JSON.stringify(output,null,2)+"\n");