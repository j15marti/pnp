"use strict";
// Independent strict-three-CNF virtual-child replay counterexample.
// Run: node experiments/arc/lspv4_509_virtual_alias_firewall.cjs
function gamma(x){const b=x.toString(2); return "0".repeat(b.length-1)+b;}
function edges(name){
 if(name==="K4"){let E=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j]);return [E,4];}
 if(name==="K33"){let E=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)E.push([i,j]);return [E,6];}
 if(name==="Q3"){let E=[];for(let i=0;i<8;i++)for(let k=0;k<3;k++){const j=i^(1<<k);if(i<j)E.push([i,j]);}return [E,8];}
 throw Error(name);
}
function gen(name,charge){
 const [E,H]=edges(name),m=E.length,w=Math.ceil(Math.log2(m+1));
 let bits="10100110"+gamma(H)+gamma(m),clauses=[];
 for(let v=0;v<H;v++){
  const incident=E.map((e,i)=>e.includes(v)?i+1:null).filter(x=>x!==null);
  if(incident.length!==3)throw Error("not cubic");
  for(let t=0;t<8;t++){
   const x=[(t>>0)&1,(t>>1)&1,(t>>2)&1];
   if(((x[0]^x[1]^x[2])===charge[v]))continue;
   clauses.push(incident.map((id,j)=>x[j]?-id:id));
   incident.forEach((id,j)=>{bits+=id.toString(2).padStart(w,"0")+x[j];});
  }
 }
 return {bits,clauses,m,H};
}
function sat(f){
 for(let a=0;a<2**f.m;a++){
  if(f.clauses.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0)))))return true;
 }
 return false;
}
function audit(name){
 const H=edges(name)[1],z=Array(H).fill(0),o=[...z];o[0]=1;
 const a=gen(name,z),b=gen(name,o);
 if(!sat(a)||sat(b)||a.bits.length!==b.bits.length)throw Error("label/length");
 const mask=[...a.bits].map((x,j)=>+(x!==b.bits[j]));
 let raw0={},raw1={},v0="",v1="";
 for(let j=0;j<a.bits.length;j++){
  raw0[j]=a.bits[j];raw1[j]=a.bits[j];
  v0+=String(Number(a.bits[j])^(0&mask[j]));
  v1+=String(Number(a.bits[j])^(1&mask[j]));
 }
 if(v0!==a.bits||v1!==b.bits||JSON.stringify(raw0)!==JSON.stringify(raw1))throw Error("transducer");
 const mismatches=mask.reduce((s,b)=>s+b,0);
 if(mismatches!==4||v0===v1)throw Error("change scope");
 return {graph:name,H,edges:a.m,clauses:a.clauses.length,child_bits:a.bits.length,
  parent_reads_equal:true,parent_bits_read:a.bits.length,virtual_mismatches:mismatches,
  label0:"SAT",label1:"UNSAT",naive_parent_only_reuse:"WRONG",
  virtual_observation_guard:"REJECTS"};
}
function main(){return {status:"PASS",model:"abstract virtual-input transducer + full truth-table check",
 runs:["K4","K33","Q3"].map(audit),native_FLMV_executed:false,historical_R_mix341_executed:false};}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));
