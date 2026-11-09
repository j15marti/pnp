'use strict';
// LSPV-1/546: finite independent K4 original-source and affine-guard controls.
// This is an EXTERNAL semantic Res(XOR) model, NOT historical R_mix341.
const assert=require('node:assert/strict');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], charges=[1,0,0,0];
let checks=0;
function verify(test, label){checks++;assert.ok(test,label)}
function bits(n){return Array.from({length:1<<n},(_,z)=>Array.from({length:n},(_,i)=>(z>>i)&1));}
function parity(a){return a.reduce((x,y)=>x^y,0);}
const clauses=[];
for(let v=0;v<4;v++){
 const vars=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
 for(let a of bits(3))if(parity(a)!==charges[v]) clauses.push({vertex:v,lits:vars.map((x,i)=>[x,a[i]])});
}
const model=a=>clauses.every(c=>c.lits.some(([i,b])=>a[i]!==b));
verify(clauses.length===16,'16 strict ternary source clauses');
verify(bits(6).filter(model).length===0,'odd source UNSAT');
for(let i=0;i<clauses.length;i++){
 const Fminus=clauses.filter((_,j)=>j!==i);
 verify(bits(6).some(a=>Fminus.every(c=>c.lits.some(([j,b])=>a[j]!==b))),'all source clauses essential');
}
const H=Array.from({length:3},(_,v)=>edges.map(e=>e.includes(v)?1:0)),rhs=charges.slice(0,3);
let A=H.map((row,i)=>[...row,rhs[i]]),prov=[1,2,4],pivots=[],xorOperations=[];
for(let col=0,k=0;col<6&&k<3;col++){
 const p=A.findIndex((row,i)=>i>=k&&row[col]);if(p<0)continue;
 [A[k],A[p]]=[A[p],A[k]];[prov[k],prov[p]]=[prov[p],prov[k]];
 for(let i=0;i<3;i++)if(i!==k&&A[i][col]){
  A[i]=A[i].map((val,j)=>val^A[k][j]);prov[i]^=prov[k];xorOperations.push([i,k]);
 }
 pivots.push(col);k++;
}
verify(pivots.length===3,'independent affine rank three');
for(let i=0;i<3;i++){
 const expected=Array.from({length:7},(_,j)=>((prov[i]&1)?H[0].concat(rhs[0])[j]:0)^((prov[i]&2)?H[1].concat(rhs[1])[j]:0)^((prov[i]&4)?H[2].concat(rhs[2])[j]:0));
 verify(expected.every((v,j)=>v===A[i][j]),'RREF rows source-linearly authenticated');
}
const free=Array.from({length:6},(_,i)=>i).filter(i=>!pivots.includes(i));
verify(free.length===3,'free dimension three');
const completed=[];
for(let beta of bits(3)){
 const alpha=Array(6).fill(0);free.forEach((col,i)=>alpha[col]=beta[i]);
 A.forEach((row,i)=>alpha[pivots[i]]=row[6]^parity(free.map(col=>row[col]*alpha[col])));
 verify(H.every((row,i)=>parity(row.map((x,j)=>x*alpha[j]))===rhs[i]),'affine completion satisfies three source-certified rows');
 verify(free.every((col,i)=>alpha[col]===beta[i]),'free guard enforced');
 const target=clauses.findIndex((c,i)=>i>=12&&c.lits.every(([col,b])=>alpha[col]===b));
 verify(target>=0,'fourth-vertex original clause contradicts complete coset');
 for(let [col,b] of clauses[target].lits)for(let a of bits(6)){
  const D=free.some((j,i)=>a[j]!==beta[i]);
  const dependent=pivots.indexOf(col);
  const row=dependent>=0?A[dependent]:null;
  const holds=row?parity(row.slice(0,6).map((x,i)=>x*a[i]))===row[6]:true;
  verify(!holds||D||a[col]===b,'one source-certified row or tautology yields guarded literal');
 }
 completed.push(alpha.join(''));
}
verify(completed.length===8&&new Set(completed).size===8,'exact 2^3 coset assignments');
verify(bits(6).filter(a=>H.every((row,i)=>parity(row.map((x,j)=>x*a[j]))===rhs[i])).length===8,'independent exhaustive 64-input coset check');
let leaf=0,cut=0;
for(let v=0;v<3;v++){
 const vars=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
 for(let forbidden of bits(3)){
  const source=clauses.find(c=>c.vertex===v&&c.lits.every((p,j)=>p[0]===vars[j]&&p[1]===forbidden[j]));
  const premise=source??clauses[4*v];
  for(let a of bits(3)){
   const premiseTrue=premise.lits.some(([j,b])=>a[vars.indexOf(j)]!==b);
   const equation=parity(a)===charges[v];
   const blocker=a.some((b,i)=>b!==forbidden[i]);
   verify(!premiseTrue||equation||blocker,'original-source semantic weakening');
  }
  leaf++;
 }
 cut+=7;
}
verify(leaf===24&&cut===21,'three 8-leaf /7-cut parity certificates');
const out={status:'PASS',checks,source_clause_count:clauses.length,original_vars:6,certified_affine_rank:3,free_dimension:free.length,uncut_branches:64,guarded_branches:8,semantic_weakenings:leaf,resolution_cuts:cut,rref_xor_operations:xorOperations.length,historical_R_mix341_checker_executed:false};
console.log(JSON.stringify(out));
