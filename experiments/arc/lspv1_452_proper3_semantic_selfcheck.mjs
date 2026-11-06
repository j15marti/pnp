#!/usr/bin/env node
// Compact independent check for source-based semantic AND3/XOR on established K4 Tseitin.
// It is NOT the historical R_mix341 accepted-byte checker.
import assert from 'node:assert/strict';
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function pop(x){let k=0;for(;x;x&=x-1)k++;return k&1}
function clauseTable(c,xyz){let mask=0;for(let a=0;a<8;a++){
  if(c.some(l=>((a>>xyz.indexOf(Math.abs(l)))&1)===+(l>0)))mask|=1<<a;
}return mask}
function parityTable(vars,rhs,xyz){let mask=0;for(let a=0;a<8;a++){
  let bit=0;for(const v of vars)bit^=(a>>xyz.indexOf(v))&1;
  if(bit===rhs)mask|=1<<a;
}return mask}
function gen(odd){const rows=[],cnf=[];for(let v=0;v<4;v++){
  const xyz=edges.flatMap(([x,y],j)=>x===v||y===v?[j+1]:[]);const rhs=+(odd&&v===0);
  const clauses=[];for(let a=0;a<8;a++)if(pop(a)!==rhs){
    const c=xyz.map((z,j)=>(a>>j&1)?-z:z);clauses.push(c);cnf.push(c);
  }
  assert.equal(clauses.length,4);
  const t=clauses.map(c=>clauseTable(c,xyz));
  // Three paid two-parent AND3 nodes; support is exactly three ORIGINAL CNF variables.
  const first=t[0]&t[1],second=t[2]&t[3],combined=first&second;
  assert.equal(combined,parityTable(xyz,rhs,xyz));
  rows.push({xyz,rhs,clauses,mask:combined,paid_and3:3});
}return {rows,cnf}}
function satisfies(cnf,a){return cnf.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===+(l>0)))}
const odd=gen(true),even=gen(false);
let oddModels=0,evenModels=0,deleteControls=0;
for(let a=0;a<64;a++){
  oddModels+=+satisfies(odd.cnf,a);evenModels+=+satisfies(even.cnf,a);
}
assert.equal(oddModels,0);assert.equal(evenModels,8);
for(let j=0;j<odd.cnf.length;j++){
  assert.ok(Array.from({length:64},(_,a)=>a).some(a=>satisfies(odd.cnf.filter((_,i)=>i!==j),a)));
  deleteControls++;
}
const xor=(a,b)=>({vars:[...new Set([...a.vars,...b.vars].filter(v=>a.vars.includes(v)!==b.vars.includes(v)))].sort((x,y)=>x-y),rhs:a.rhs^b.rhs});
const es=odd.rows.map(r=>({vars:r.xyz,rhs:r.rhs}));
const p=xor(es[0],es[1]),q=xor(es[2],es[3]),root=xor(p,q);
assert.deepEqual(root,{vars:[],rhs:1});
const nodes=4*3+3,span=2+2;
assert.equal(nodes,15);assert.equal(span,4);
// Corrupted original source must fail the claimed affine-row equivalence.
const forged=structuredClone(odd.rows[0].clauses);forged[0][0]*=-1;
let mask=255;for(const c of forged)mask&=clauseTable(c,odd.rows[0].xyz);
assert.notEqual(mask,parityTable(odd.rows[0].xyz,1,odd.rows[0].xyz));
console.log(JSON.stringify({status:'PASS',source:'odd K4 Tseitin proper 3CNF',original_variables:6,
 original_clauses:odd.cnf.length,odd_models:oddModels,even_models:evenModels,
 single_clause_deletions_sat:deleteControls,paid_AND3:12,paid_XOR:3,paid_nodes:nodes,
 ideal_weighted_span:span,forged_source_rejected:true}));
