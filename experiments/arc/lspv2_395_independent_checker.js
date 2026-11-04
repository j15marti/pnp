"use strict";
// LSPV2/395 independent, from-scratch truth-table checker. No imports from producer.
const fs=require("fs");
function must(x,t){if(!x)throw Error(t);}
function lit(l,m){let v=((m>>(Math.abs(l)-1))&1)===1;return l>0?v:!v;}
function evalCNF(F,m){return F.every(C=>C.some(l=>lit(l,m)));}
function buildIndependent(F,k){let n=Math.max(...F.flat().map(Math.abs));let v=n;let grid=[];for(let q=0;q<k*k;q++)grid.push(++v);
let bank=grid.map(x=>[-x]);let edges=0;
function addAnd(a,b){let z=++v;bank.push([-z,a],[-z,b],[z,-a,-b]);}
for(let i=0;i<k;i++)for(let j=0;j<k;j++){let a=grid[i*k+j];if(i+1<k){addAnd(a,grid[(i+1)*k+j]);edges++;}if(j+1<k){addAnd(a,grid[i*k+j+1]);edges++;}}
addAnd(Math.abs(F[0][0]),grid[0]);return {bank,n,v,edges};}
const cases={blocker:[[1,2],[1,-2],[-1,2],[-1,-2]],odd:[[1,2],[-1,-2],[2,3],[-2,-3],[1,3],[-1,-3]],even:[[1,2],[-1,-2],[2,3],[-2,-3],[1,-3],[-1,3]],sat:[[1]]};
function check(){let tests=0,unique=0;for(let [name,F]of Object.entries(cases)){let T=buildIndependent(F,2);let oldModels=0,bothModels=0;
for(let old=0;old<(1<<T.n);old++){let ways=0;for(let ext=0;ext<(1<<(T.v-T.n));ext++){let bits=old|(ext<<T.n);if(evalCNF(T.bank,bits)){ways++;must(ext===0,"unexpected auxiliary witness");if(evalCNF(F,old))bothModels++;}}must(ways===1,"nonunique extension");unique++;if(evalCNF(F,old))oldModels++;}must(oldModels===bothModels,"projection label mismatch");must(T.edges===4,"grid edges");tests++;}
for(let k of [3,4,5])for(let [name,F]of Object.entries(cases)){let T=buildIndependent(F,k);let x=0;for(let old=0;old<(1<<T.n);old++)must(evalCNF(T.bank,old),"neutral section failed");must(T.bank.length===k*k+3*(2*k*(k-1)+1),"formula size mismatch");tests++;}
return {tests,uniqueAssignmentsChecked:unique,malformedControlsChecked:0};}
if(require.main===module){const x=check();console.log(JSON.stringify(x,null,2));}
module.exports={check};
