#!/usr/bin/env node
// Independent strict-Resolution verifier for exhaustive LSPV-1/408 records.
// Usage: node lspv1_408_independent_verify.js <raw_json_path>
// Not a polynomial SAT solver; enumeration is restricted to two variables.
const fs=require("fs"),assert=require("assert");
const path=process.argv[2] || "results/raw/arc/2026-11-04_1956_LSPV1_PROOF_SEARCH408_raw.json";
const D=JSON.parse(fs.readFileSync(path,"utf8"));
const U=[[-1],[1],[-2],[2],[-1,-2],[-1,2],[1,-2],[1,2]];
const k=a=>JSON.stringify(a.slice().sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?1:-1)));
function normal(a){const s=new Set(a);for(const x of s)if(s.has(-x))return null;return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1))}
function res(a,b){let out=[];for(const p of [1,2])if((a.includes(p)&&b.includes(-p))||(a.includes(-p)&&b.includes(p))){const r=normal([...a,...b].filter(x=>x!==p&&x!==-p));if(r!==null)out.push([p,r])}return out}
function models(s){let n=0;for(let m=0;m<4;m++)if(s.every(cl=>cl.some(x=>Boolean(m&(1<<(Math.abs(x)-1)))===(x>0))))n++;return n}
function check(src,bits){if(typeof bits!=="string"||bits.length<4||!/^[01]+$/.test(bits))return false;const q=parseInt(bits.slice(0,4),2);if(bits.length!==4+9*q||q<1)return false;let nodes=src.map(c=>c.slice());for(let j=0;j<q;j++){const t=bits.slice(4+9*j,13+9*j),a=parseInt(t.slice(0,4),2),b=parseInt(t.slice(4,8),2),p=parseInt(t.slice(8),2)+1;if(a>=nodes.length||b>=nodes.length||a===b)return false;const got=res(nodes[a],nodes[b]).find(z=>z[0]===p);if(!got||nodes.some(c=>k(c)===k(got[1])))return false;nodes.push(got[1]);if(got[1].length===0)return j===q-1;}return false}
function enc(actions){return actions.length.toString(2).padStart(4,"0")+actions.map(([a,b,p])=>a.toString(2).padStart(4,"0")+b.toString(2).padStart(4,"0")+(p-1)).join("")}
function candidates(src,q){const found=new Set();function step(nodes,trace){if(trace.length===q){let code=enc(trace);if(check(src,code))found.add(code);return}for(let a=0;a<nodes.length;a++)for(let b=0;b<nodes.length;b++)if(a!==b)for(const [p,r] of res(nodes[a],nodes[b])){if(nodes.some(c=>k(c)===k(r)))continue;if((r.length===0)!==(trace.length===q-1))continue;step([...nodes,r],[...trace,[a,b,p]])}}step(src,[]);return [...found].sort()}
let verified=0,sat=0,unsat=0,cc=0,queries=0;
assert.equal(D.records.length,256);
for(let mask=0;mask<256;mask++){const x=D.records[mask];assert.equal(x.mask,mask);const src=U.filter((_,i)=>mask&(1<<i));const m=models(src);verified++;
if(m){sat++;assert.equal(x.label,"SAT");assert.equal(x.models,m);continue}
unsat++;assert.equal(x.label,"UNSAT");let q=1,cs=[];for(;q<=8;q++){cs=candidates(src,q);if(cs.length)break}
assert.equal(q,x.q);assert.equal(cs.length,x.candidate_proofs);assert.equal(x.code,cs[0]);assert.equal(x.bits,x.code.length);assert(check(src,x.code));cc+=cs.length;
let prefix="",count=0;for(let z=0;z<x.code.length;z++){count++;if(cs.some(s=>s.startsWith(prefix+"0")))prefix+="0";else{count++;assert(cs.some(s=>s.startsWith(prefix+"1")));prefix+="1"}}
assert.equal(prefix,x.code);assert.equal(count,x.prefix_queries);queries+=count;verified+=7;
}
assert.deepEqual([sat,unsat],[95,161]);assert.equal(cc,D.summary.enumerated_codes);assert.equal(queries,D.summary.prefix_queries);
for(const fake of ["","no","0000","0001","0001000000000","010000000000","1111",null]){assert(!check([[1],[-1]],fake));verified++}
console.log(JSON.stringify({independent_assertion_groups:verified,sat,unsat,certificate_codes:cc,prefix_queries:queries}));
