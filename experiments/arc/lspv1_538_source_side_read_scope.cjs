"use strict";
// LSPV-1/538. SIDE_TABLE is a DISTINCT hypothetical calculus, never historical R_mix341.
function ok(p,msg){if(!p)throw Error(msg);}
function edges(kind){
 if(kind==="K4")return [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 if(kind==="prism3")return [[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]];
 if(kind==="cube"){let a=[];for(let v=0;v<8;v++)for(let k=0;k<3;k++){
 const u=v^(1<<k);if(v<u)a.push([v,u]);}return a;}
 throw Error("unknown graph");
}
function tseitin(kind,odd){
 const E=edges(kind),h=Math.max(...E.flat())+1,n=E.length,clauses=[];
 for(let v=0;v<h;v++){
  const I=[];E.forEach(([a,b],i)=>{if(a===v||b===v)I.push(i+1);});
  ok(I.length===3,"noncubic");
  for(let m=0;m<8;m++){
   const parity=((m&1)!==0)^((m&2)!==0)^((m&4)!==0);
   if(Number(parity)!==Number(Boolean(odd&&v===0)))
    clauses.push(I.map((id,k)=>((m>>k)&1)?-id:id));
  }
 }
 return {h,n,clauses};
}
function falseClause(c,a){return c.every(l=>{const bit=(a>>(Math.abs(l)-1))&1;return !(l>0?bit:1-bit);});}
function satCount(F){let q=0;for(let a=0;a<2**F.n;a++){
 if(F.clauses.every(c=>!falseClause(c,a)))q++;}return q;}
function witness(F){const arr=[];for(let a=0;a<2**F.n;a++){
 const j=F.clauses.findIndex(c=>falseClause(c,a));if(j<0)return null;arr.push(j);
}return arr;}
function verify(F,arr){return Array.isArray(arr)&&arr.length===2**F.n&&arr.every((j,a)=>
 Number.isSafeInteger(j)&&j>=0&&j<F.clauses.length&&falseClause(F.clauses[j],a));}
function deletionModel(F,i){for(let a=0;a<2**F.n;a++)if(falseClause(F.clauses[i],a)&&
 F.clauses.every((c,j)=>j===i||!falseClause(c,a)))return a;return -1;}
function dimacs(F){return "p cnf "+F.n+" "+F.clauses.length+"\n"+
 F.clauses.map(c=>c.join(" ")+" 0\n").join("");}
function parse(s){const lines=s.trim().split(/\n/),head=lines.shift().trim().split(/\s+/);
 if(head.length!==4||head[0]!=="p"||head[1]!=="cnf"||! /^\d+$/.test(head[2])||
 ! /^\d+$/.test(head[3]))throw Error("bad header");
 const n=Number(head[2]),m=Number(head[3]);
 if(n<1||n>20||m!==lines.length)throw Error("bad counts");
 const clauses=lines.map(line=>{
  const t=line.trim().split(/\s+/);if(t.length<2||t[t.length-1]!=="0")throw Error("terminator");
  const c=t.slice(0,-1).map(Number);
  if(c.some(z=>!Number.isSafeInteger(z)||z===0||Math.abs(z)>n))throw Error("literal");
  return c;
 });
 return {n,clauses};
}
function hash(arr){let h=2166136261;for(const a of arr)h=Math.imul((h^a)>>>0,16777619)>>>0;
 return h.toString(16).padStart(8,"0");}
function main(){
 const rows=[];
 for(const kind of ["K4","prism3","cube"]){
  const F=tseitin(kind,true),even=tseitin(kind,false),m=F.clauses.length;
  ok(JSON.stringify(parse(dimacs(F)).clauses)===JSON.stringify(F.clauses),"parse mismatch");
  ok(satCount(F)===0,"odd SAT");
  const q=2**(F.n-F.h+1);
  ok(satCount(even)===q,"even models");
  const table=witness(F);
  ok(table!==null&&verify(F,table),"invalid UNSAT certificate");
  ok(witness(even)===null,"SAT false refutation");
  const used=new Set(table),del=F.clauses.map((_,i)=>deletionModel(F,i));
  ok(used.size===m && del.every(x=>x>=0),"source coverage/essentiality");
  for(let i=0;i<m;i++)ok(table[del[i]]===i,"source exclusive witness");
  const corrupted=table.slice();
  const wrong=F.clauses.findIndex(c=>!falseClause(c,0));
  corrupted[0]=wrong;ok(!verify(F,corrupted),"corrupt accepted");
  ok(!verify(F,table.slice(1)),"short accepted");
  ok(!verify(F,table.concat([0])),"long accepted");
  corrupted[0]=m;ok(!verify(F,corrupted),"bad index accepted");
  rows.push({graph:kind,h:F.h,n:F.n,m,source_ascii_bytes:dimacs(F).length,
   odd_models:0,even_models:q,essential_clause_witnesses:del.length,
   source_ids_in_table:used.size,syntactic_named_parents:1,
   exhaustive_source_dependencies:m,logical_paid_nodes_SIDE_TABLE:1,
   declared_Rmix341_source_minimum:m-1,
   source_partition_kappa_initial:m,source_partition_kappa_final:1,
   source_partition_kappa_plus_nodes_final:2,
   witness_bits:2**F.n*Math.max(1,Math.ceil(Math.log2(m))),
   fnv32:hash(table)});
 }
 const malformed=["p cnf 2 1\n1 2\n","p cnf 2 2\n1 0\n",
  "p cnf two 1\n1 0\n","p cnf 2 1\n3 0\n","p cnf 2 1\n1 0\n2 0\n"];
 for(const [i,s] of malformed.entries()){
  let rejected=false;try{parse(s);}catch(e){rejected=true;}
  ok(rejected,"malformed accepted "+i);
 }
 return {status:"PASS",timestamp:"2026-11-09 09:00 PST",
  scope:"separate SIDE_TABLE calculus, not the historical R_mix341",
  rows,malformed_rejections:malformed.length,
  historical_checker_executed:false,
  theorem:"syntactic named-parent arity does not bound exhaustive source-bearing dependency arity",
  label:"PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL controls; P vs NP OPEN"};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));

