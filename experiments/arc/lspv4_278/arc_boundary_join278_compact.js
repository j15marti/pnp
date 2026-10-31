#!/usr/bin/env node
"use strict";
// LSPV-4 ARC-BOUNDARY-JOIN-STREAM-INDEX278 compact original-source verifier.
// Full independent Python verifier and original-indexed raw are in expanded ZIP.
const assert=require("node:assert/strict");
const cases=[
 ["SAT-overlap",3,[0,3],[0],true],
 ["UNSAT-disjoint",3,[0,3],[5],false],
 ["UNSAT-witness-gap",3,[0],[1,2,3,4,5,6,7],false],
 ["SAT-gap-perturbed",3,[0,6],[1,2,3,4,5,6,7],true],
 ["SAT-b4",4,[0,7],[0,15],true],
 ["UNSAT-b4",4,[0,7],[3,15],false]
];
function make(b,S,T){
 let n=b,clauses=[],pins=[]; const m=2**b;
 for(const [side,list] of [["H",S],["E",T]]){
  let member=new Set(list);
  for(let a=0;a<m;a++){
   const g=++n,u=++n,v=++n, pin=member.has(a)?g:-g;
   pins.push({side,a,pin,member:member.has(a),firstClause:clauses.length});
   for(let su of [1,-1])for(let sv of [1,-1])clauses.push([pin,su*u,sv*v]);
   const wide=[g,...Array.from({length:b},(_,j)=>((a>>(b-j-1))&1)?-(j+1):(j+1))];
   const z=Array.from({length:b-2},()=>++n);
   clauses.push([wide[0],wide[1],z[0]]);
   for(let j=1;j<z.length;j++)clauses.push([-z[j-1],wide[j+1],z[j]]);
   clauses.push([-z[z.length-1],wide[wide.length-2],wide[wide.length-1]]);
  }
 }
 assert.equal(n,b+2*m*(b+1));
 assert.equal(clauses.length,2*m*(b+3));
 assert(clauses.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3));
 const w=Math.ceil(Math.log2(n+1)),recordBits=3*(w+1);
 const source=Array(64).fill("0");
 for(const c of clauses)for(const lit of c)source.push(lit<0?"1":"0",...Math.abs(lit).toString(2).padStart(w,"0"));
 const bits=source.join("");
 for(const p of pins){const first=64+p.firstClause*recordBits;assert.equal(Number(bits[first]),p.member?0:1);}
 const countAt=mask=>clauses.map(c=>c.filter(l=>Boolean((mask>>BigInt(Math.abs(l)-1))&1n)===(l>0)).length);
 const zeros=countAt(0n),ones=countAt((1n<<BigInt(n))-1n);
 for(let j=0;j<clauses.length;j++)assert.equal(zeros[j]+ones[j],3);
 const modes=[0,0,0,0];
 if(b===3)for(let i=0;i<clauses.length;i++)for(let j=i+1;j<clauses.length;j++){
  const p=new Map(clauses[i].map(l=>[Math.abs(l),Math.sign(l)]));
  let same=false,opposite=false;
  for(const l of clauses[j])if(p.has(Math.abs(l))){if(p.get(Math.abs(l))===Math.sign(l))same=true;else opposite=true;}
  modes[0]+=Number(!opposite);modes[1]+=Number(!same);modes[2]+=Number(!same);modes[3]+=Number(!opposite);
 }
 const A=new Set(S),B=new Set(T),witness=[...A].find(x=>B.has(x));
 return {label:witness===undefined?"UNSAT":"SAT",sourceBits:bits.length,nvars:n,originalClauses:clauses.length,
   boundaryModels:[...A].filter(x=>B.has(x)).length,firstWitness:witness??null,
   endpointFalseClauses:{zeros:zeros.filter(x=>x===0).length,ones:ones.filter(x=>x===0).length},
   compatibleExtremesSS_SU_US_UU:b===3?modes:null,
   pinOffsets:pins.slice(0,2).map(p=>64+p.firstClause*recordBits)};
}
const out=cases.map(([name,b,S,T,expected])=>{
 let r=make(b,S,T);assert.equal(r.label==="SAT",expected);
 assert.equal(r.sourceBits,b===3?2368:6112);
 return {name,b,S,T,...r};
});
let checks=0;
for(let s=0;s<256;s++)for(let sp=s+1;sp<256;sp++){
 let diff=s^sp;assert(diff!==0);
 let bit=diff&-diff;assert.equal(Boolean(s&bit),!Boolean(sp&bit));checks++;
}
assert.equal(checks,32640);
process.stdout.write(JSON.stringify({
 run:"ARC-BOUNDARY-JOIN-STREAM-INDEX278",status:"COMPUTATIONAL",canonical_cases:out,
 first_stream_pair_checks:checks,
 full_producer_sha256:"dab30ffc95cceb8fea9c95607f5c8b7024ea2ccf7937d9860a1d0adaeb20b273",
 flmv:{c6_5:"23/45",c241_200:"11642479/23232400",unique_k:2,tail_first:4},
 open:"all-input hereditary arbitrary-A to Phi(A) contraction"
},null,2)+"\n");
