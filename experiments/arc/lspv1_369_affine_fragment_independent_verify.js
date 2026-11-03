// Independently authored LSPV-1 369 referee, zero dependencies.
"use strict";
function independentlyVerify(raw){
let nchecks=0;function ok(c,t){nchecks++;if(!c)throw Error("referee failure "+t)}
const trueClause=(c,a)=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0));
for(let record of raw.bit_php){
 let ell=record.ell,n=1<<ell,p=n+1,v=ell*p,F=[],meta=[];
 for(let h=0;h<n;h++)for(let i=0;i<p;i++)for(let j=i+1;j<p;j++){
  let c=[];for(let k of [i,j])for(let t=0;t<ell;t++){let z=k*ell+t+1;c.push((h>>t)&1?-z:z)}
  F.push(c);meta.push({h,i,j})
 }
 ok(F.length===record.clauses&&v===record.variables,"source dimensions");
 let nmodels=0;
 for(let a=0;a<(1<<v);a++){
  let ids=[];for(let i=0;i<p;i++){let x=0;for(let t=0;t<ell;t++)x|=((a>>(i*ell+t))&1)<<t;ids.push(x)}
  let distinct=new Set(ids).size===p,model=F.every(c=>trueClause(c,a));
  ok(distinct===model,"injection equivalent to all clauses");
  if(model)nmodels++
 }
 ok(nmodels===0&&record.models===0,"UNSAT outcome");
 let repairs=0;
 for(let r=0;r<F.length;r++){
  let {h,i,j}=meta[r],ids=Array(p).fill(-1);ids[i]=h;ids[j]=h;
  let unused=[];for(let k=0;k<n;k++)if(k!==h)unused.push(k);
  let u=0;for(let k=0;k<p;k++)if(ids[k]===-1)ids[k]=unused[u++];
  let a=0;for(let k=0;k<p;k++)for(let t=0;t<ell;t++)a|=((ids[k]>>t)&1)<<(k*ell+t);
  for(let k=0;k<F.length;k++)ok(trueClause(F[k],a)===(k!==r),"exactly one source false");
  for(let t=0;t<F[r].length;t++){let c=F[r].slice();c[t]=-c[t];ok(trueClause(c,a),"sign repair");repairs++}
 }
 ok(record.deletion_sat_witnesses===F.length&&record.sign_flip_sat_witnesses===repairs,"witness totals")
}
let E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
for(let ch of [0,1]){
 let models=0;
 for(let a=0;a<64;a++){
  let yes=true;for(let v=0;v<4;v++){
   let parity=0;for(let e=0;e<6;e++)if(E[e].includes(v))parity^=(a>>e)&1;
   if(parity!==(v===0?ch:0))yes=false
  }
  if(yes)models++
 }
 ok(models===(ch===0?8:0),"K4 charge label")
}
// Each odd-parity forbidden assignment yields one genuine signed blocker.
let sourceClauses=[[1,-2,3],[1,2,-3],[-1,2,3],[-1,-2,-3]];
for(let a=0;a<8;a++){
 let x=a&1,y=(a>>1)&1,z=(a>>2)&1;
 let p=sourceClauses.slice(0,2).every(c=>trueClause(c,a));
 let q=sourceClauses.slice(2).every(c=>trueClause(c,a));
 let r=x===1||y===z,s=x===0||y!==z;
 ok(!p||r,"first semantic step");ok(!q||s,"second semantic step");
 ok(!(r&&s)||((x^y^z)===0),"third semantic step")
}
ok(raw.status==="PASS"&&raw.semantic_local_steps===3&&raw.res_oplus_row_sum_steps===2,"macro contract");
ok(raw.malformed_rejected===7&&raw.corrupted_semantic_steps_rejected===2,"negative controls");
return {status:"PASS",checks:nchecks,bit_php_cases:raw.bit_php.length,K4_odd_models:0,K4_even_models:8,limitations:"Finite tests, not a verification of the asymptotic lower bound."}
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(!process.argv[2])throw Error("pass raw JSON path");
 process.stdout.write(JSON.stringify(independentlyVerify(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2)+"\n")
}
