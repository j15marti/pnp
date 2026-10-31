// Independent adversarial grammar/fallback controls for LSPV4 272.
"use strict";
const {build,solver}=require("./arc_multipin_cache272.js");
function copy(f,clauses,n=f.n){return{...f,n,c:clauses.map(c=>c.slice())}}
function variants(f){let shift=f.c.map(c=>c.map(l=>Math.abs(l)===1?-l:l));let swap=f.c.map(c=>c.slice());[swap[0],swap[8]]=[swap[8],swap[0]];return[["canonical",f],["signed_rename",copy(f,shift)],["reorder",copy(f,swap)],["filler_extension",copy(f,[...f.c,[7,8,9]])]]}
function recognized(f){if(f.n!==12)return false;let b=[];for(let j=0;j<3;j++){let c=f.c[j+8];if(!c||Math.abs(c[0])!==1)return false;b.push(c[0]>0)}return JSON.stringify(f.c)===JSON.stringify(build(3,b).c)}
function models(f){let k=0;for(let a=0;a<2**f.n;a++){if(f.c.every(c=>c.some(l=>((a>>>(Math.abs(l)-1))&1)===(l>0?1:0))))k++}return k}
function parity(v){let out=[];for(let a=0;a<8;a++){const bits=[a&1,(a>>1)&1,(a>>2)&1];if((bits[0]^bits[1]^bits[2])!==v)out.push(bits.map((b,j)=>b?-(j+1):j+1))}return out}
const rows=[];
function add(f,name,expected,canonical=null){const s=solver(f),m=models(f);if(s.sat!==expected||(m>0)!==expected||canonical!==null&&recognized(f)!==canonical)throw Error(name);
 rows.push({name,n:f.n,clauses:f.c.length,expected,sat:s.sat,models:m,nodes:s.nodes,literalTests:s.tests,canonical:canonical===null?null:recognized(f)})}
for(let b of [[false,false,false],[false,false,true]])for(let [n,f] of variants(build(3,b)))add(f,"source_"+b.map(Number).join("")+"_"+n,b.some(Boolean),n==="canonical");
const tests=[["xor_sat",parity(0),3,true],["xor_unsat",[...parity(0),...parity(1)],3,false],
 ["2sat_sat",[[1,2],[-1,2],[1,-2]],2,true],["2sat_unsat",[[1],[-1]],1,false],
 ["horn_sat",[[-1,-2,3],[1],[-3,2]],3,true],["horn_unsat",[[1],[2],[3],[-1,-2,-3]],3,false],
 ["dense_sat",[...parity(0),[1,2,3]],3,true],["dense_unsat",[...parity(0),...parity(1)],3,false]];
for(let [name,c,n,label]of tests)add({n,c},name,label);
let seed=20261031>>>0;function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
function randomClause(planted){const vars=[];while(vars.length<3){let v=1+rnd()%6;if(!vars.includes(v))vars.push(v)}
 const out=vars.map(v=>(rnd()&1)?v:-v);if(planted&&!out.some(l=>l>0))out[0]=Math.abs(out[0]);return out;}
const rs=Array.from({length:40},()=>randomClause(true));add({n:6,c:rs},"seeded_dense_planted_sat",true);
const triples=[];for(let mask=0;mask<8;mask++)triples.push([1,4,6].map((v,i)=>((mask>>i)&1)?-v:v));
for(let i=7;i>0;i--){let j=rnd()%(i+1);[triples[i],triples[j]]=[triples[j],triples[i]];}
const rn=[...triples,...Array.from({length:40},()=>randomClause(false))];add({n:6,c:rn},"seeded_dense_forced_unsat",false);
const result={title:"ARC-MULTIPIN-WARM-CACHE272_HOSTILE",testType:"exhaustive original labels, deterministic xorshift32 dense controls seed 20261031",cases:rows.length,rows,
 note:"Canonical recognition only. Nonmembers retain source labels but require a charged fallback or new sound policy. Native FLMV timing unmeasured."};
if(typeof module!=="undefined"&&module.exports)module.exports={result};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(result,null,2)+"\n");
