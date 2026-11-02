#!/usr/bin/env node
"use strict";
/* FINITE-REFLECTION337 independent finite toy checker, NO Python imports.
 * Reads published results JSON given on command line. Does NOT check PA proofs.
 */
const fs=require("fs");
const raw=JSON.parse(fs.readFileSync(process.argv[2]||"results337.json","utf8"));
let checks=0;
function check(b,msg){checks++;if(!b)throw Error("check "+checks+": "+msg);}
function encode(n,clauses,pad=0){return Buffer.from("0:"+JSON.stringify({n,clauses})+":"+"0".repeat(pad));}
function parse(b){
 const s=b.toString("ascii");if(!s.startsWith("0:"))return null;
 const pos=s.lastIndexOf(":");if(pos<2 || !/^0*$/.test(s.slice(pos+1)))return null;
 let f;try{f=JSON.parse(s.slice(2,pos));}catch(e){return null;}
 if(JSON.stringify(f)!==s.slice(2,pos)||Object.keys(f).sort().join(",")!=="clauses,n"||
 !Number.isInteger(f.n)||f.n<1||f.n>9||!Array.isArray(f.clauses)||f.clauses.length>64)return null;
 for(const c of f.clauses){if(!Array.isArray(c)||c.length>20||
 c.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>f.n))return null;}
 return f;
}
function models(f){
 if(f===null)return null;let m=0;
 for(let a=0;a<(1<<f.n);a++){
   if(f.clauses.every(c=>c.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0))))m++;
 }return m;
}
function K4(ch){
 let E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],cls=[];
 for(let v=0;v<4;v++){
   const ids=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
   for(let z=0;z<8;z++){
     const parity=((z&1)+((z>>1)&1)+((z>>2)&1))%2;
     if(parity===ch[v])continue;
     cls.push(ids.map((id,i)=>z&(1<<i)?-id:id));
   }
 }return cls;
}
const fixtures=[
 ["unit_sat",encode(1,[[1]]),"SAT"],
 ["unit_unsat",encode(1,[[1],[-1]]),"UNSAT"],
 ["horn_unsat",encode(3,[[1],[2],[-1,-2,3],[-3]]),"UNSAT"],
 ["horn_sat_flip",encode(3,[[1],[2],[-1,-2,3],[3]]),"SAT"],
 ["cube_unsat",encode(3,Array.from({length:8},(_,z)=>[z&1?-1:1,z&2?-2:2,z&4?-3:3])),"UNSAT"],
 ["k4_odd",encode(6,K4([1,0,0,0])),"UNSAT"],
 ["k4_even",encode(6,K4([0,0,0,0])),"SAT"],
 ["malformed_header",Buffer.from("1".repeat(50)),"INVALID"],
 ["malformed_literal",Buffer.from('0:{"n":1,"clauses":[[0]]}:','ascii'),"INVALID"],
 ["malformed_suffix",Buffer.concat([encode(1,[[1]]),Buffer.from("1")]),"INVALID"]
];
check(raw.fixture_results.length===fixtures.length,"10 fixture rows");
fixtures.forEach(([name,b,expected],i)=>{
 const m=models(parse(b)),label=m===null?"INVALID":m?"SAT":"UNSAT";
 check(label===expected,"truth "+name);
 check(raw.fixture_results[i].name===name,"name "+name);
 check(raw.fixture_results[i].encoded_length===b.length,"source bytes "+name);
 check(raw.fixture_results[i].model_count===m,"models "+name);
});
let n=raw.injected_bad_checker_code;
let base=encode(1,[[1]]),s=encode(1,[[1]],n-base.length);
check(s.length===n,"sentinel length");
check(models(parse(s))===1,"sentinel SAT");
check(raw.sentinel_label_baseline==="SAT","baseline correct");
check(raw.sentinel_label_fault_world==="UNSAT","deliberate incorrect label");
check(raw.checked_local_codes===raw.N+1,"all <=N codes enumerated");
function cert(N,a,bad=null){return a.length===N+1&&a.every((x,i)=>x===i&&x!==bad);}
let a=Array.from({length:raw.N+1},(_,i)=>i);
check(cert(raw.N,a),"consistent local checker");
check(!cert(raw.N,a.slice(0,-1)),"missing code refused");
check(!cert(raw.N,a.concat([raw.N+1])),"extra code refused");
check(!cert(raw.N,a,n),"inconsistency injected refused");
check(cert(n-1,Array.from({length:n},(_,i)=>i),n),"out-of-window code not yet active");
check(raw.status.startsWith("COMPUTATIONAL"),"finite experimental status");
console.log(JSON.stringify({verifier:"independent NodeJS",passed:true,assertions:checks,
fixture_cases:fixtures.length,toy_fault:n,formal_PA_proof_checked:false},null,2));
