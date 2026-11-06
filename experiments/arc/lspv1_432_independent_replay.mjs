// LSPV-1/432 public compact replay. Run: node experiments/arc/lspv1_432_independent_replay.mjs
import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const raw=JSON.parse(readFileSync(new URL('../../results/raw/arc/2026-11-05_1900_LSPV1_AFFINE_HULL_ORACLE432_summary.json',import.meta.url)));
let checks=0;
function check(x){checks++;assert.ok(x)}
function sat(cs,a){return cs.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))}
function models(cs,n){return Array.from({length:2**n},(_,i)=>i).filter(x=>sat(cs,x))}
function rank(vec,n){const rows=vec.slice();let r=0;for(let k=0;k<n;k++){
 let j=r;while(j<rows.length&&!((rows[j]>>k)&1))j++;
 if(j===rows.length)continue;
 [rows[j],rows[r]]=[rows[r],rows[j]];
 for(let i=0;i<rows.length;i++)if(i!==r&&((rows[i]>>k)&1))rows[i]^=rows[r];r++;
 }return r}
function spanRank(ms,n){return ms.length?rank(ms.slice(1).map(x=>x^ms[0]),n):null}
const clauses=Array.from({length:8},(_,k)=>[1,2,3].map((v,i)=>((k>>(2-i))&1)?-v:v));
let satisfiable=0,unsat=0,maxQueries=0;
for(let mask=0;mask<256;mask++){
 const cnf=clauses.filter((_,i)=>(mask>>i)&1);
 const ms=models(cnf,3),r=spanRank(ms,3);
 const queries=ms.length?(r===3?4:r+2):1;
 if(ms.length)satisfiable++;else unsat++;
 maxQueries=Math.max(maxQueries,queries);
 check(queries<=4);
 check(ms.length===0 || r>=0&&r<=3);
}
check(satisfiable===raw.all3_satisfiable);
check(unsat===raw.all3_unsatisfiable);
check(maxQueries===raw.maximum_three_var_queries);
function parity(x){let t=0;while(x){t^=x&1;x>>>=1}return t}
function tseitin(edges,odd){let h=1+Math.max(...edges.flat());const inc=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});
 let cs=[];for(let v=0;v<h;v++)for(let b=0;b<8;b++)if(parity(b)!==(odd&&v===0?1:0))
 cs.push(inc[v].map((x,i)=>((b>>i)&1)?-x:x));return cs}
const K4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
const K33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)K33.push([i,j]);
for(const rec of raw.actual_originals){let cs=[];
 if(rec.family.startsWith('K4_'))cs=tseitin(K4,rec.unsat);
 else if(rec.family.startsWith('K33_'))cs=tseitin(K33,rec.unsat);
 else if(rec.family==='PHP_4_3'){
  for(let i=0;i<4;i++)cs.push([i*3+1,i*3+2,i*3+3]);
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)for(let k=0;k<3;k++)cs.push([-(i*3+k+1),-(j*3+k+1)]);
 }else if(rec.family==='Horn_chain3')cs=[[1],[-1,2],[-2,3]];
 else throw new Error(rec.family);
 const ms=models(cs,rec.original_variables),r=spanRank(ms,rec.original_variables);
 check(cs.length===rec.clauses);check((ms.length===0)===rec.unsat);
 if(!rec.unsat){check(r===rec.hull_rank);
 const w=rec.actual_witness_masks;
 check(w.every(x=>ms.includes(x)));check(spanRank(w,rec.original_variables)===r);
 }
}
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let z=0;z<2;z++){
 const val=x=>x>0?[a,b,z][x-1]:1-[a,b,z][-x-1];
 const good=cs=>cs.every(c=>c.some(x=>val(x)));
 check(good([[1,2,-3],[1,-2,3],[-1,2,3],[-1,-2,-3]])===(z===(a^b)));
 check(good([[-1,3],[-2,3],[1,2,-3]])===(z===(a|b)));
}
check(raw.sparse_dimacs_header_id===2**42);
check(raw.sparse_dimacs_actual_occurring_variable_count===1);
check(raw.parser_malformed_rejections===6);
console.log(JSON.stringify({status:'PASS',assertions:checks,all3:256,satisfiable,unsat,controls:raw.actual_originals.length}));
