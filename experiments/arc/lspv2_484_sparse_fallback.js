'use strict';
// LSPV-2/484: finite controls for sparse-exception direct fallback.
// Not an authoritative R_mix341 checker or native FLMV machine.
const assert = require('node:assert/strict');
const edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0,calls=0,paddingWrites=0,maxPadding=0;
function ok(x,msg){assert.ok(x,msg);checks++;}
function formula(charges,t=0){
 const clauses=[];
 for(let v=0;v<4;v++){
  const es=[];for(let e=0;e<6;e++)if(edges[e].includes(v))es.push(e+1);
  ok(es.length===3,'cubic K4');
  for(let bits=0;bits<8;bits++){
   const b=[bits&1,(bits>>1)&1,(bits>>2)&1];
   if((b[0]^b[1]^b[2])!==charges[v])clauses.push(es.map((e,i)=>b[i]===0?e:-e));
  }
 }
 for(let j=0;j<t;j++)clauses.push([7+3*j,8+3*j,9+3*j]);
 return {n:6+3*t,clauses};
}
function canonicalBitLength(F){const n=F.n,m=F.clauses.length;const gamma=x=>2*Math.floor(Math.log2(x))+1;const w=Math.ceil(Math.log2(n+1));return gamma(n+1)+gamma(m+1)+m*3*(1+w);}
function valid(F){return F&&Number.isSafeInteger(F.n)&&F.n>=0&&Array.isArray(F.clauses)&&F.clauses.every(c=>Array.isArray(c)&&c.length===3&&c.every(z=>Number.isSafeInteger(z)&&z!==0&&Math.abs(z)<=F.n)&&new Set(c.map(z=>Math.abs(z))).size===3);}
function countModels(F){if(!valid(F))return 'MALFORMED';if(F.n>17)throw Error('finite oracle out of scope');let m=0;for(let a=0;a<2**F.n;a++){let good=true;for(const c of F.clauses){let sat=false;for(const l of c){const v=(a>>(Math.abs(l)-1))&1;if((l>0&&v===1)||(l<0&&v===0)){sat=true;break;}}if(!sat){good=false;break;}}if(good)m++;}return m;}
function decideFinite(F){const c=countModels(F);return c==='MALFORMED'?c:c>0?'SAT':'UNSAT';}
function exceptional(F,t){return JSON.stringify(F)===JSON.stringify(formula([1,0,0,0],t));}
function paddedFinite(F,k=2){
 const n=8*Buffer.byteLength(JSON.stringify(F),'utf8'),sz=n**k;
 if(sz>6_000_000)throw Error('host memory cap');
 const a=new Uint8Array(sz);
 for(let i=0;i<sz;i++){a[i]=i&255;paddingWrites++;}
 ok(a[sz-1]===((sz-1)&255),'last cell written');
 calls++;maxPadding=Math.max(maxPadding,sz);
 return decideFinite(F);
}
function hybrid(F,t){return exceptional(F,t)?paddedFinite(F):decideFinite(F);}
const stats=[];
for(let t=0;t<=2;t++){
 let sat=0,unsat=0,escape=0;
 for(let mask=0;mask<16;mask++){
  const charges=[0,1,2,3].map(i=>(mask>>i)&1),F=formula(charges,t);
  ok(valid(F),'proper source');
  ok(F.clauses.length===16+t,'source clauses');
  const alt=JSON.parse(JSON.stringify(F));for(let j=0;j<t;j++)alt.clauses[16+j][0]*=-1;
  ok(canonicalBitLength(F)===canonicalBitLength(alt),'fixed sign bit length');
  const model=countModels(F),odd=charges.reduce((a,b)=>a^b,0);
  ok(model===(odd?0:8*7**t),'Tseitin and fresh side-clause models');
  const out=hybrid(F,t);ok(out===(odd?'UNSAT':'SAT'),'labels');
  if(out==='SAT')sat++;else unsat++;
  if(exceptional(F,t))escape++;
 }
 ok(sat===8&&unsat===8&&escape===1,'one escaped source per family slice');
 stats.push({t,sourceClauses:16+t,sat,unsat,exceptionCount:escape});
}
const bads=[{n:3,clauses:[[1,1,2]]},{n:3,clauses:[[1,2,4]]},{n:3,clauses:[[1,2,0]]},{n:3,clauses:[[1,2]]}];
for(const b of bads)ok(decideFinite(b)==='MALFORMED','malformed');
for(const k of [2,3,4,8]){
 const tGoal=Math.max(1.1,0.6+k/2),sGoal=Math.max(0.5,k/2);
 ok(k>tGoal&&k>sGoal,'full fallback exceeds contract');
 ok(k/2<=sGoal&&0.6+k/2<=tGoal,'half-size exact threshold');
}
console.log(JSON.stringify({role:'LSPV-2/484',scope:'finite host check only',checks,controls:stats,malformedRejected:bads.length,exceptionGuestCalls:calls,paddingWrites,maxPaddingBytes:maxPadding,formalSATinP:'CONDITIONAL ONLY',nativeFLMV:false,historicalMix341:false,proofStatus:'PROVED/RESTRICTED; P vs NP OPEN'},null,2));