"use strict";
// LSPV-4 SINGLE_CHILD_ORACLE_LEDGER208, independent JS finite reproduction.
// Run: node research/agents/lspv-4/2026-10-28_1736_LSPV-4_SINGLE_CHILD_ORACLE_LEDGER208_repro.js
// Only arithmetic and finite truth-table tests, NOT a uniform SAT lower bound.
let assertions=0;
function check(ok,message){assertions++;if(!ok)throw new Error("FAIL: "+message);}
function bit(mask,j){return (mask>>>j)&1;}
function AB(mask,t){
 let a=[],b=[];
 for(let i=0;i<t;i++)a.push(Boolean(bit(mask,2*i)||bit(mask,2*i+1)));
 for(let j=0;j<t;j++)b.push(Boolean(bit(mask,2*t+2*j)||bit(mask,2*t+2*j+1)));
 return {a,b};
}
function projected(mask,t){const {a,b}=AB(mask,t);return a.every(Boolean)||b.every(Boolean);}
function expanded(mask,t){const {a,b}=AB(mask,t);return a.every(x=>b.every(y=>x||y));}
function selector(mask,t,z){const {a,b}=AB(mask,t);return a.every(x=>z||x)&&b.every(y=>!z||y);}
function textPNP(t,k,compact){
 const z=4*t+1,nv=z+3*k,clauses=[];
 if(!compact){for(let i=0;i<t;i++)for(let j=0;j<t;j++)clauses.push([2*i+1,2*i+2,2*t+2*j+1,2*t+2*j+2]);}
 else {for(let i=0;i<t;i++)clauses.push([z,2*i+1,2*i+2]);for(let j=0;j<t;j++)clauses.push([-z,2*t+2*j+1,2*t+2*j+2]);}
 for(let h=0;h<k;h++)clauses.push([z+1+3*h,z+2+3*h,z+3+3*h]);
 return "p cnf "+nv+" "+clauses.length+"\n"+clauses.map(c=>c.join(" ")+" 0\n").join("");
}
function run(){
 const exhaust=[];
 for(let t=1;t<=4;t++){
  const count=1<<(4*t);
  for(let mask=0;mask<count;mask++){
   const v=expanded(mask,t);
   check(v===projected(mask,t),"factor t="+t+" mask="+mask);
   check(v===(selector(mask,t,0)||selector(mask,t,1)),"exists t="+t+" mask="+mask);
   const neg=AB(mask,t); check((!v)===(neg.a.some(x=>!x)&&neg.b.some(y=>!y)),"De Morgan t="+t+" mask="+mask);
  }
  exhaust.push({t,assignments:count});
 }
 check(exhaust.reduce((s,o)=>s+o.assignments,0)===69904,"exhaust total");
 const length128={t:128,expanded_bytes:textPNP(128,0,false).length,selector_bytes:textPNP(128,0,true).length};
 const ctx=[];
 for(let k of [0,1,4,16,64,256,1024,4096]){
  const a=textPNP(4,k,false),b=textPNP(4,k,true);
  check(a.startsWith("p cnf ")&&b.startsWith("p cnf "),"headers");
  check(a.length>=b.length,"length");
  ctx.push({k,input_bytes:a.length,child_bytes:b.length,ratio:b.length/a.length});
 }
 const lengths=[64,8,3,2];
 let s=Array.from({length:64},(_,i)=>(i*i+7*i+3)&1),layers=[s];
 for(const n of lengths.slice(1)){
  const parity=s.reduce((v,x)=>v^x,0);
  s=Array.from({length:n},(_,j)=>parity^(j&1));
  layers.push(s);
 }
 let leafCalls=0;
 function virtual(level,j){
  if(level===0){leafCalls++;return layers[0][j];}
  let p=j&1;
  for(let x=0;x<lengths[level-1];x++)p^=virtual(level-1,x);
  return p;
 }
 for(let j=0;j<2;j++)check(virtual(3,j)===layers[3][j],"nested parity "+j);
 const explicitTotalReads=lengths.slice(1).reduce((s,n,i)=>s+n*lengths[i],0);
 const explicitSourceReads=lengths[1]*lengths[0];
 check(explicitTotalReads===542&&explicitSourceReads===512,"materialized count");
 check(leafCalls===3072,"virtual multiplication");
 const data={run_id:"SINGLE_CHILD_ORACLE_LEDGER208_JS_INDEPENDENT",status:"COMPUTATIONAL only; P vs NP OPEN",assertions,exhaust,length128,context_t4:ctx,virtual:{lengths,unmemoized_original_source_probes:leafCalls,materialized_all_level_reads:explicitTotalReads,materialized_source_probes:explicitSourceReads},seed:"none; exhaustive and deterministic"};
 return data;
}
if(typeof module!=="undefined" && require.main===module)console.log(JSON.stringify(run(),null,2));
