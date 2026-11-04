/* LSPV-1/396. Explicit two-input Resolution row audit encoded succinctly by CNF D.
   No packages. Creates the complete 2-variable, 256-CNF control ledger. */
'use strict';
const fs = require('fs');
const SRC = [[1,2],[1,-2],[-1]];
const U = [[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function literal(l,a) {const bit=(a>>(Math.abs(l)-1))&1; return l>0 ? bit===1 : bit===0;}
function evalCNF(D,a) {return D.every(c=>c.some(l=>literal(l,a)));}
function res(left,right,pivot) {
  if (!left.includes(pivot)||!right.includes(-pivot)) return null;
  const terms=[...new Set([...left.filter(l=>l!==pivot),...right.filter(l=>l!==-pivot)])];
  if (terms.some(l=>terms.includes(-l))) return null;
  return terms.sort((a,b)=>a-b);
}
function rowOK(D,a) {
  // The circuit for D chooses source 3 exactly on satisfying assignments.
  const left=evalCNF(D,a)?SRC[2]:SRC[0];
  return JSON.stringify(res(left,SRC[1],2))===JSON.stringify([1]);
}
function makeRaw(){
  const cases=[]; let sat=0,unsat=0,checks=0;
  for(let mask=0;mask<256;mask++) {
    const D=U.filter((_,k)=>((mask>>k)&1)===1);
    let invalid=0;
    for(let a=0;a<4;a++) { const semantic=evalCNF(D,a); const legal=rowOK(D,a);
      if(semantic===legal) throw new Error('local row reduction contradiction');
      if(!legal) invalid++; checks+=2;
    }
    const isSAT=invalid>0; if(isSAT)sat++;else unsat++;
    cases.push({mask,cnf:D,sat:isSAT,invalid_rows:invalid,all_rows_legal:!isSAT});
    checks+=3;
  }
  if (sat!==95||unsat!==161) throw new Error('catalogue mismatch');
  if(rowOK([[1],[-1]],0)===false) throw new Error('UNSAT check failed');
  if(rowOK([[1]],1)===true) throw new Error('SAT check failed');
  return {schema:'LSPV1-396-compressed-rows-v1',source:SRC,clause_universe:U,cases,summary:{cases:256,sat,unsat,producer_checks:checks+2}};
}
if (require.main===module) {
 const out=process.argv[2]||'lspv1_396_implicit_row_raw.json';
 const raw=makeRaw(); fs.writeFileSync(out,JSON.stringify(raw)+'\n');
 console.log(JSON.stringify(raw.summary));
}
module.exports={makeRaw};
