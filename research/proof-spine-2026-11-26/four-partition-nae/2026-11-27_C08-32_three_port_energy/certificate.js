'use strict';
function certificate(){
const rs=[[[3,0],[4,0],[2,0]],[[2,0],[1,0],[0,0]],[[3,0],[0,0],[5,0]],[[1,0],[0,0],[4,0]],[[1,0],[3,0],[0,1]],[[0,1],[5,0],[4,0]],[[5,0],[0,1],[2,0]]];
const eq=(a,b)=>+(a===b);
const d={};let constant=0;
for(const r of rs)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let [u,a]=r[i],[v,b]=r[j],k=[u,v].sort().join(",");(d[k]??=[0,0])[a^b]++}
for(const k of Object.keys(d))if(d[k][0]===d[k][1]){constant+=d[k][0];delete d[k]}
const path=[0,1].map(z=>Math.min(...[0,1].map(x=>d["0,1"][x]+d["0,5"][x^z])));
if(JSON.stringify(path)!=="[3,2]")throw Error("path");
delete d["0,1"];delete d["0,5"];d["1,5"]=path;
const e=Object.values(d);
const offset=constant+e.reduce((s,t)=>s+t[1],0);
if(e.length!==10||e.some(t=>t[0]-t[1]!==1)||offset!==5)throw Error("clique");
let countChecks=0;const bin=n=>n*(n-1)/2;
for(let i=0;i<32;i++){let x=Array.from({length:5},(_,j)=>(i>>j)&1),a=x.reduce((s,t)=>s+t,0),actual=constant+Object.entries(d).reduce((s,[k,t])=>{let [u,v]=k.split(",").map(Number);return s+t[x[u-1]^x[v-1]]},0);if(actual!==5+bin(a)+bin(5-a))throw Error("clique energy");countChecks++}
let min=Math.min(...Array.from({length:6},(_,a)=>offset+bin(a)+bin(5-a)));
if(min!==9)throw Error("minimum");
return {canceledConstant:constant,pathMinCosts:path,uniformCliqueOrder:5,offset,minimum:min,threshold:7,minimumViolations:(min-7)/2,countChecks,edgeTables:d};
}
console.log(JSON.stringify(certificate(),null,2));
