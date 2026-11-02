#!/usr/bin/env node
"use strict";
/* LSPV-4 GATE325 independent verifier, NO importing producer functions.
 * Usage: node independent_gate_referee325.js summary325.json
 */
const fs=require("fs");
const d=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
function check(x,msg){if(!x)throw Error(msg)}
function valid(C,n){
 if(n<3||n%3||3*C.length!==4*n)return false;
 const cnt=Array.from({length:n+1},()=>[0,0]),keys=new Set();
 for(const c of C){
  if(!Array.isArray(c)||c.length!==3||c.some(x=>!Number.isSafeInteger(x)||!x||Math.abs(x)>n))return false;
  if(new Set(c.map(Math.abs)).size!==3||c.some(x=>(x>0)!==(c[0]>0)))return false;
  const k=c.slice().sort((a,b)=>a-b).join(",");if(keys.has(k))return false;keys.add(k);
  for(const x of c)cnt[Math.abs(x)][x>0?1:0]++;
 }
 return cnt.slice(1).every(([a,b])=>a===2&&b===2);
}
function formula(C,z){return C.every(c=>c.some(x=>Boolean((z>>(Math.abs(x)-1))&1)===(x>0)))}
function network(n,gs,out,z){
 const v=Array(n+gs.length+1).fill(0);
 for(let j=1;j<=n;j++)v[j]=(z>>(j-1))&1;
 gs.forEach(([op,a,b],i)=>{
  const k=n+i+1;check(["AND","OR","NAND"].includes(op)&&a>=1&&b>=1&&a<k&&b<k,"bad gate");
  v[k]=op==="AND"?(v[a]&&v[b]?1:0):op==="OR"?(v[a]||v[b]?1:0):(!v[a]||!v[b]?1:0);
 });
 return v[out]===1;
}
function edges(C){
 const w=new Map(),deg=Array(C.length).fill(0);
 for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){
  if((C[i][0]>0)!==(C[j][0]>0))continue;
  const r=C[i].filter(x=>C[j].includes(x)).length;
  if(r){check(r<=2,"duplicate triple");w.set(i+","+j,r);deg[i]+=r;deg[j]+=r;}
 }
 check(deg.every(x=>x===3),"not cubic");return w;
}
function opt(C,E){
 let ans=0;
 for(const s of [true,false]){
  const idx=C.map((c,i)=>[c[0]>0,i]).filter(x=>x[0]===s).map(x=>x[1]);
  check(idx.length<=12,"finite optimum outside bound");
  const cache=new Map();
  function f(bits){
   if(!bits)return 0;if(cache.has(bits))return cache.get(bits);
   let a=0;while(!((bits>>a)&1))a++;
   const rest=bits&~(1<<a);let best=f(rest);
   for(let b=a+1;b<idx.length;b++)if((rest>>b)&1){
    const u=Math.min(idx[a],idx[b]),v=Math.max(idx[a],idx[b]),w=E.get(u+","+v)||0;
    if(w)best=Math.max(best,w+f(rest&~(1<<b)));
   }
   cache.set(bits,best);return best;
  }ans+=f((1<<idx.length)-1);
 }return ans;
}
function pins(C,n,p){
 const free=Array.from({length:n},(_,i)=>i+1).filter(j=>p[j]===undefined);
 let sum=0;for(let z=0;z<(1<<free.length);z++){
  let mask=0;for(const [k,v] of Object.entries(p))mask|=v<<(Number(k)-1);
  free.forEach((k,i)=>mask|=((z>>i)&1)<<(k-1));
  sum+=Number(formula(C,mask));
 }return sum;
}
let checks=0,rows=0;
const metrics={};
for(const [name,f] of Object.entries(d.fixtures)){
 const {n,m,original_clauses:C,pairs_1based:P,gates,output}=f;
 check(valid(C,n),"invalid original "+name);checks++;
 const E=edges(C);check([...E.values()].reduce((a,b)=>a+b,0)===2*n,"signed-edge count");checks++;
 const used=new Set();let w=0;
 for(const [a1,b1,x] of P){
  const a=a1-1,b=b1-1,k=Math.min(a,b)+","+Math.max(a,b);
  check(a>=0&&b<m&&a!==b&&!used.has(a)&&!used.has(b),"invalid matching");
  check(E.get(k)===x,"wrong intersection");used.add(a);used.add(b);w+=x;checks+=2;
 }
 for(const k of E.keys()){const [a,b]=k.split(",").map(Number);check(used.has(a)||used.has(b),"not maximal");checks++;}
 check(10*P.length>=3*m&&w===f.matching_weight&&gates.length===3*m-1-w,"guarantee or gate count");checks++;
 check(opt(C,E)===f.optimal_matching_weight_exact_finite,"wrong optimal comparison");checks++;
 let models=0;for(let z=0;z<(1<<n);z++){
  const b=formula(C,z);check(b===network(n,gates,output,z),"truth disagreement "+name+" "+z);
  models+=Number(b);checks++;
 }
 check(models===f.original_models,"wrong original model count");checks++;
 metrics[name]={matches:P.length,weight:w,gates:gates.length,optimal_weight:f.optimal_matching_weight_exact_finite,models};
 rows+=1<<n;
}
const F9=d.fixtures.F9.original_clauses,c={3:0,5:1,6:0,7:0,8:0};
check(pins(F9,9,{...c,1:0})===2&&pins(F9,9,{...c,1:1})===0,"same-original labels");checks++;
let modes=0;const ext=[0,0,0,0];
for(let i=0;i<F9.length;i++)for(let j=i+1;j<F9.length;j++){
 let observed=[false,false,false,false];
 for(let z=0;z<512;z++){
  const all=(C,want)=>C.every(l=>Boolean((z>>(Math.abs(l)-1))&1)===(want?(l>0):(l<0)));
  const a=all(F9[i],true),b=all(F9[i],false),p=all(F9[j],true),q=all(F9[j],false);
  const v=[a&&p,a&&q,b&&p,b&&q];observed=observed.map((x,k)=>x||v[k]);
 }
 const same=F9[i].some(x=>F9[j].includes(x)),opp=F9[i].some(x=>F9[j].includes(-x));
 const pred=[!opp,!same,!same,!opp];
 pred.forEach((x,k)=>{check(observed[k]===x,"S/U incompatibility");ext[k]+=Number(x);checks++;modes++;});
}
check(modes===264&&JSON.stringify(ext)===JSON.stringify([37,49,49,37]),"source S/U extremes");checks++;
const bad=[F9.slice(1),F9.concat([F9[0]]),[[1,-5,6],...F9.slice(1)],
 [[1,1,5],...F9.slice(1)],[[0,5,6],...F9.slice(1)],[[1,5,10],...F9.slice(1)],
 [[1,5,6],[6,5,1],...F9.slice(2)],[[1,5,6],[-1,5,3],...F9.slice(2)]];
bad.forEach(B=>{check(!valid(B,9),"malformed accepted");checks++;});
check(rows===66112&&metrics.TIGHT15.gates===53&&metrics.F9.gates===29,"fixture controls");checks++;
process.stdout.write(JSON.stringify({PASS:true,assertions:checks,all_rows:rows,source_F9_extreme_modes:modes,
 source_F9_feasible_SSUU:ext,metrics,P_vs_NP:"OPEN"},null,2)+"\n");