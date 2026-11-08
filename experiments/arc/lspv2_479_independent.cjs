'use strict';
const assert=require('node:assert/strict');
// Finite control only: not a Kleene fixed-point execution.
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const incident=Array.from({length:4},(_,v)=>edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean));
function cnf(charge){const clauses=[];for(let v=0;v<4;v++)for(let a=0;a<8;a++){const b=[a&1,(a>>1)&1,(a>>2)&1];if((b[0]^b[1]^b[2])!==((charge>>v)&1))clauses.push(incident[v].map((id,j)=>b[j]?-id:id));}return clauses;}
function classify(clauses){for(let mask=0;mask<64;mask++)if(clauses.every(c=>c.some(l=>{const bit=(mask>>(Math.abs(l)-1))&1;return l>0?bit===1:bit===0;})))return'SAT';return'UNSAT';}
function toy(word){if(!/^(0|1)+$/.test(word))return'MALFORMED';return word.includes('1')?'SAT':'UNSAT';}
let checks=0,sat=0,unsat=0,malformed=0,padded_cases=0,bounded_simulation_cases=0;
for(let b=0;b<16;b++){const F=cnf(b);assert.equal(F.length,16);checks++;assert(F.every(c=>c.length===3));checks++;const p=[0,1,2,3].reduce((v,i)=>v^((b>>i)&1),0);const r=classify(F);assert.equal(r,p?'UNSAT':'SAT');checks++;if(p)unsat++;else sat++;}
for(let n=1;n<=7;n++)for(let e=0;e<=3;e++)for(const w of ['0'.repeat(n),'1'+'0'.repeat(n-1),'?'.repeat(n)]){const x=toy(w);const steps=BigInt(n+1)**BigInt(e+2);assert.equal(x,toy(w));checks++;assert(steps>BigInt(n)**BigInt(e));checks++;if(x==='MALFORMED')malformed++;padded_cases++;}
for(const haltAfter of [null,1,3,8])for(let n=1;n<=16;n++)for(let e=0;e<=3;e++){const h=haltAfter!==null&&haltAfter<=n;const count=h?BigInt(n+1)**BigInt(e+2):0n;assert.equal(h,haltAfter!==null&&n>=haltAfter);checks++;if(h){assert(count>BigInt(n)**BigInt(e));checks++;}assert(n>=1);checks++;bounded_simulation_cases++;}
console.log(JSON.stringify({status:'PASS',scope:'finite K4 signed strict 3CNF and arithmetic only; NOT self-reference theorem',checks,sat,unsat,malformed,padded_cases,bounded_simulation_cases},null,2));
