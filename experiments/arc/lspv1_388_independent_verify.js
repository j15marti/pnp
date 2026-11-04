#!/usr/bin/env node
// Independently verifies the published finite toy ledger; NOT Blum's theorem.
"use strict";
const fs=require("fs"),assert=require("assert");
const raw=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
const label=x=>(!x || (x[0]==="0"&&x!=="0"))?"M":
 ((x.split("").filter(y=>y==="1").length%2)?"UNSAT":"SAT");
function runTime(x) {
 const n=x.length;
 return label(x)==="M"?[3+n,2+n*n,4+n,2]:
 [2**(n+5),2**(2*n+2),2**(n+6)+n,n+2];
}
const all=[""];
for(let n=1;n<=8;n++)for(let k=0;k<(1<<n);k++)
 all.push(k.toString(2).padStart(n,"0"));
let checks=0;
assert.equal(all.length,511);checks++;
const totals={SAT:0,UNSAT:0,M:0};
for(const s of all) totals[label(s)]++;
assert.deepStrictEqual(raw.both_labels,totals);checks++;
for(let n=1;n<=8;n++){
 const inputs=all.filter(x=>x.length<=n);
 const wc=[0,0,0,0];
 for(const x of inputs){const time=runTime(x);
 for(let j=0;j<4;j++)wc[j]=Math.max(wc[j],time[j]);}
 const row=raw.rows[n-1];
 assert.equal(row.N,n);checks++;
 assert.equal(row.all_binary_count,inputs.length);checks++;
 assert.deepStrictEqual(row.worst,wc);checks++;
 assert.equal(row.strict_toy_improvement,wc[3]<Math.min(...wc.slice(0,3)));checks++;
}
for(const bad of ["","00","01","000","010"]){
 assert.equal(label(bad),"M");checks++;
}
for(const good of ["0","1","10","11","101"]){
 assert.notEqual(label(good),"M");checks++;
}
console.log(JSON.stringify({status:"independent toy ledger verified",checks,labels:totals}));
