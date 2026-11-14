// TMR-1/018: exact executable finite padding-control audit. Hosted V8 execution first; Node-compatible.
const audit = function audit(){
"use strict";
const fail=(msg)=>{throw new Error(msg)};
const assert=(c,msg)=>{if(!c)fail(msg)};
const labelToy=(x)=>{let a=false,b=false;for(const ch of x){if(ch==="0")a=true;else if(ch==="1")b=true;else return "MALFORMED"}return a&&b?"UNSAT":"SAT"};
const pad=(x)=>"1".repeat(x.length)+"0"+x+"0".repeat(2**x.length);
const unpad=(y)=>{
 if(!/^[01]*$/.test(y))return null;
 let L=0;while(L<y.length&&y[L]==="1")L++;
 if(L===y.length||L>20)return null; // limit of finite executable, not symbolic theorem
 const start=L+1,finish=start+L;
 if(finish>y.length||y.length!==finish+2**L)return null;
 for(let j=finish;j<y.length;j++)if(y[j]!=="0")return null;
 return y.slice(start,finish)
};
const sat=(clauses)=>{
 let ids=[...new Set(clauses.flat().map(x=>Math.abs(x)))].sort((a,b)=>a-b);
 for(let mask=0;mask<2**ids.length;mask++){
  let val=new Map(ids.map((id,j)=>[id,(mask>>j)&1]));
  if(clauses.every(cl=>cl.some(lit=>val.get(Math.abs(lit))===(lit>0?1:0))))return true;
 }
 return false;
};
let tested=0,satCount=0,unsatCount=0,invalidChecks=0,bitsScanned=0;
const lengths=[];
for(let L=0;L<=10;L++){
 let per=0;
 for(let m=0;m<2**L;m++){
  const x=m.toString(2).padStart(L,"0").slice(L===0?1:0);
  assert(x.length===L,"source length");
  const y=pad(x),parsed=unpad(y);
  assert(parsed===x,"decode mismatch");
  assert(y.length===2*L+1+2**L,"precise N mismatch");
  let lbl=labelToy(x);
  assert(lbl==="SAT"||lbl==="UNSAT","bad source label");
  if(lbl==="SAT")satCount++;else unsatCount++;
  const bads=[y.slice(0,-1),y+"0",y.slice(0,-1)+"1"];
  for(const b of bads){assert(unpad(b)===null,`malformed suffix accepted L=${L}`);invalidChecks++}
  assert(2**L<=y.length,"enumeration count exceeds padded length");
  tested++;per++;bitsScanned+=y.length;
 }
 lengths.push({L,fixtures:per,N:2*L+1+2**L});
}
const controls=[
 {name:"horn-unit-contradiction",formula:[[1,1,1],[-1,-1,-1]],expected:false},
 {name:"single-clause-proper-3sat",formula:[[1,2,3]],expected:true},
 {name:"complete-eight-forbidden-masks",formula:Array.from({length:8},(_,m)=>[1,2,3].map((v,j)=>m&(1<<j)?v:-v)),expected:false},
 {name:"2sat-satisfiable",formula:[[1,2],[-1,2]],expected:true},
 {name:"2sat-unsatisfiable",formula:[[1,1],[-1,-1]],expected:false},
 {name:"xor-one-satisfiable",formula:[[1,2],[-1,-2]],expected:true},
 {name:"xor-both-incompatible",formula:[[1,2],[-1,-2],[1,-2],[-1,2]],expected:false},
 {name:"disjoint-product-sat",formula:[[1,2,3],[4,5,6]],expected:true},
 {name:"disjoint-product-unsat",formula:[[1,1,1],[-1,-1,-1],[4,5,6]],expected:false},
 {name:"auxiliary-existential-equivalence",formula:[[1,2,3],[1,2,-3]],expected:true},
];
for(const c of controls)assert(sat(c.formula)===c.expected,`formula control: ${c.name}`);
const result={
 id:"TMR1-PAD18",status:"COMPUTATIONAL",timestamp:"2026-11-14 04:00 PST",
 claimedTheoremStatus:"CANDIDATE/RESTRICTED pending peer review",
 sourceEncoding:"toy fixed-variable triple-clause sign stream, all binary words valid",
 padDefinition:"1^L 0 x 0^(2^L), N=2L+1+2^L",
 exhaustiveSourceLengths:"0..10",sourceTests:tested,SAT:satCount,UNSAT:unsatCount,
 malformedSuffixTests:invalidChecks,totalSourceAndPaddingBitObservations:bitsScanned,
 maxPaddedLength:lengths[lengths.length-1].N,lengths,
 algebraicAndStructuralControls:controls.map(({name,expected})=>({name,SAT:expected})),
 importantLimitations:[
 "Exhaustive finite tests apply to restricted toy 3CNF sign stream, not general 3SAT",
 "General padded-standard-3CNF polynomial algorithm is a symbolic theorem, not executed as a generic Turing-machine compiler",
 "No source formula of large L was physically padded in the executable",
 "Exponential padding is NOT polynomial-time constructible from original length L",
 "No general SAT polynomial-time algorithm or superpolynomial lower bound follows"
 ],assertionFailures:0
};
return result;
};
console.log(JSON.stringify(audit(),null,2));
