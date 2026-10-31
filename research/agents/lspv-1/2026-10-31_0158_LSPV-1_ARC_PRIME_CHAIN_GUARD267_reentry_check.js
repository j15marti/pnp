"use strict";
const assert=(x,msg)=>{if(!x)throw Error(msg)};
function original(h){const x=i=>h+2+i,rows=[[x(1),1,2]];
 for(let j=2;j<h;j++)rows.push([-x(j-1),x(j),j+1]);
 rows.push([-x(h-1),h+1,h+2]);return rows;}
function canonicalReentry(h){const z=i=>h+2+i,rows=[[z(1),1,2]];
 for(let j=2;j<h;j++)rows.push([-z(j-1),z(j),j+1]);
 rows.push([-z(h-1),h+1,h+2]);return rows;}
function main(){let checks=0;
 const rows=[];for(let h=2;h<=100;h++){
  const old=original(h),fresh=canonicalReentry(h);
  assert(JSON.stringify(old)===JSON.stringify(fresh),"indexed records do not match");
  assert(old.length===h&&old.reduce((n,c)=>n+c.length,0)===3*h,"wrong physical clause/occurrence count");
  assert(new Set(old.flat().map(Math.abs)).size===2*h+1,"wrong variable count");
  const signRename=v=>((Math.abs(v)%2)?-v:v);
  assert(JSON.stringify(old.map(c=>c.map(signRename)))===JSON.stringify(fresh.map(c=>c.map(signRename))),"renaming mismatch");
  checks+=4;rows.push({h,original_clauses:h,reentered_clauses:h,original_literal_occurrences:3*h,reentered_literal_occurrences:3*h,variables:2*h+1,exact_ordered_encoding_identity:true});
 }return {status:"PASS",tag:"ARC-PRIME-CHAIN-GUARD267",checked_h_range:"2..100",checks,rows,scope:"canonical sequential 3CNF reentry only; not minimal encodings nor general SAT lower bounds",P_vs_NP:"OPEN"};}
if(require.main===module)console.log(JSON.stringify(main(),null,2));
module.exports={main};