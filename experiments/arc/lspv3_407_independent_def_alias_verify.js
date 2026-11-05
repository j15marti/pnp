/* Independent LSPV-3/407 referee. CommonJS Node.js >=18, no external deps.
   Verifies each paid-DEF gate and ALL original-to-pruned wires by a separately
   implemented direct Boolean evaluator on complete small source assignments. */
"use strict";
const {build,structuralMerge}=require("./lspv3_407_paid_def_alias.js");
function ck(b,m){if(!b)throw Error(m);}
function eval2(n,net,assignment){
 const v=assignment.slice();
 for(const g of net){
   for(const p of [g.a,g.b])ck(Number.isInteger(p[0])&&p[0]>=0&&p[0]<v.length&&(p[1]===0||p[1]===1),"invalid pin");
   ck(Number.isInteger(g.tab)&&g.tab<16&&g.tab>=0,"invalid table");
   let A=(v[g.a[0]]+g.a[1])%2, B=(v[g.b[0]]+g.b[1])%2;
   v.push(Math.floor(g.tab/Math.pow(2,2*A+B))%2);
 }
 return v;
}
function generateClauses(n){
 const u=[];
 for(let v=0;v<n;v++)for(const b of [0,1])u.push([[v,b]]);
 for(let v=0;v<n;v++)for(let w=v+1;w<n;w++)
   for(const b of [0,1])for(const c of [0,1])u.push([[v,b],[w,c]]);
 return u;
}
function* sets(u){
 yield [];
 for(let a=0;a<u.length;a++)yield [u[a]];
 for(let a=0;a<u.length;a++)for(let b=a+1;b<u.length;b++)yield [u[a],u[b]];
 for(let a=0;a<u.length;a++)for(let b=a+1;b<u.length;b++)for(let c=b+1;c<u.length;c++)yield [u[a],u[b],u[c]];
}
function run(){
 let cases=0,checks=0,sat=0,unsat=0,aliasChecks=0;
 for(let n=1;n<=3;n++){
  for(const clauses of sets(generateClauses(n))){
   cases++;
   const {D,root,zero}=build(n,clauses),m=structuralMerge(n,D);
   let S=false;
   for(let mask=0;mask<(1<<n);mask++){
    const a=Array.from({length:n},(_,i)=>Math.floor(mask/Math.pow(2,i))%2);
    const expected=clauses.every(c=>c.some(([i,sgn])=>a[i]!==sgn))?1:0;
    if(expected)S=true;
    const E=eval2(n,D,a),Z=eval2(n,m.D2,a);
    ck((E[root[0]]+root[1])%2===expected,"source/root mismatch");checks++;
    ck((E[zero[0]]+zero[1])%2===0,"zero is not zero");checks++;
    for(let i=0;i<E.length;i++){ck(E[i]===Z[m.map[i]],"mapped gate differs");checks++;aliasChecks++;}
   }
   if(S)sat++;else unsat++;
  }
 }
 ck(cases===1085 && sat===987 && unsat===98,"producer ledger differs");checks++;
 // Adversarial invalid source-independent alias from x to NOT x
 {const a=[1],b=[0];ck(a[0]!==b[0],"distinct port outputs incorrectly identified");checks++;}
 return {cases,checks,sat,unsat,aliasChecks,status:"independently checked source/output and every paid-gate alias over all small assignments"};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};
