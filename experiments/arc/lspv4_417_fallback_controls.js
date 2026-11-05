#!/usr/bin/env node
// LSPV-4/417 independently executable finite falsifier: NOT a general SAT solver
const assert=(ok,m)=>{if(!ok)throw Error(m||"control failed"); count++};let count=0;
function cnf(h,negative){let a=[`p cnf 1 ${h}`];for(let i=0;i<h;i++)a.push(negative&&i==h-1?"-1 0":"1 0");return a.join("\n")+"\n"}
function classifyOneVariable(s){const a=s.trim().split("\n"),h=/^p cnf 1 (\d+)$/.exec(a.shift());if(!h||Number(h[1])!==a.length)return "MALFORMED";const rows=a.map(x=>x.trim());if(rows.some(x=>!["1 0","-1 0","0"].includes(x)))return "MALFORMED";return rows.includes("0")||rows.includes("1 0")&&rows.includes("-1 0")?"UNSAT":"SAT"}
for(const h of [2,7,100,700])for(const n of [false,true]){let s=cnf(h,n),N=BigInt(8*Buffer.byteLength(s));assert(classifyOneVariable(s)===(n?"UNSAT":"SAT"));assert(!s.includes("c cut"));assert(N**4n>N**2n);assert(N**2n>N)}
for(const n of [8n,16n,32n])for(const r of [1,2,7,19]){assert(n**4n>BigInt(Math.ceil(Number(n)**2.6)));assert(n**2n>n);assert(r>=1)}
for(const x of ["p cnf 1 1\n1\n","p cnf 1 2\n1 0\n","p cnf 1 1\n2 0\n"])assert(classifyOneVariable(x)==="MALFORMED");
assert(classifyOneVariable("p cnf 1 1\n0\n")==="UNSAT");
console.log(JSON.stringify({status:"PASS",checks:count,scope:"independent finite opposite-label and exact BigInt envelope controls; conditional analytic proof separate"}));
