#!/usr/bin/env node
'use strict';
/* LSPV-1/480: published-theorem application finite controls only;
   not Pang asymptotic proof, FACET-A original checker, or R_mix341. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
let checks = 0;
function check(v, msg) { checks++; assert.ok(v, msg); }
function isPower2(n) { return n >= 4 && (n & (n-1)) === 0; }
function metrics(n) {
  check(isPower2(n), 'hole count must be a power of 2 >= 4');
  const H = BigInt(n), ell = BigInt(Math.log2(n)), m = H + 1n;
  const A = H * m * H / 2n;
  const S = A * (2n*ell - 2n);
  const V = m*ell + A*(2n*ell - 3n);
  const Q = A*(4n*ell-3n) + (H+1n)*(2n*H*ell-9n)
          + H*(H+1n)*(27n*H*H+11n*H-14n)/24n;
  check(A === H*H*(H+1n)/2n, 'original collision clauses');
  check(S === A * (2n*ell-2n), 'strict source clauses');
  check(V > m*ell && Q > 0n, 'counts positive');
  if(n >= 256) {
    check(S <= H**4n, 'source count bound');
    check(Q <= 2n*H**4n, 'FACET count bound');
    check(Q+S <= 3n*H**4n, 'total distinct node bound');
  }
  return { n, ell:Number(ell), originalVars:(m*ell).toString(),
    originalClauses:A.toString(), strictVariables:V.toString(),
    strictClauses:S.toString(), facetPaid:Q.toString(),
    upperInputNodes:(3n*H**4n).toString(),
    decimalLog10N:Number((S*(3n*BigInt(V.toString(2).length)+1n)).toString().length-1) };
}
function litTruth(l, mask) {return l > 0 ? !!(mask & (1<<(l-1))) : !(mask & (1<<(-l-1)));}
function chain(w) {
  const inner = Array.from({length:w-3},(_,i)=>w+i+1);
  const clauses = [[1,2,inner[0]]];
  for(let i=1;i<inner.length;i++) clauses.push([-inner[i-1],i+2,inner[i]]);
  clauses.push([-inner[inner.length-1],w-1,w]);
  return {clauses,inner};
}
function checkChain(w) {
 const {clauses,inner} = chain(w);
 check(clauses.length===w-2, 'chain clause count');
 for(const C of clauses) {
   check(C.length===3, 'strict-3 width');
   check(new Set(C.map(x=>Math.abs(x))).size===3, 'strict proper support');
 }
 let checked=0, trueOriginal=0, trueEncoded=0;
 for(let original=0; original < (1<<w); original++) {
   const sourceSAT=original!==0;
   let extensionSAT=false;
   for(let z=0; z < (1<<inner.length); z++) {
     const mask=original | (z<<w);
     if(clauses.every(C=>C.some(l=>litTruth(l,mask)))) extensionSAT=true;
   }
   checked++;
   if(sourceSAT)trueOriginal++;
   if(extensionSAT)trueEncoded++;
   check(extensionSAT===sourceSAT, 'projection failure w=' + w + ' bits=' + original);
 }
 return {w,checked,originalSAT:trueOriginal,extensionSAT:trueEncoded};
}
function originalBphp(n) {
 const ell=Math.log2(n), m=n+1; let parents=0, signedControls=0;
 const pvar=(p,b)=>1+p*ell+b;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let hole=0;hole<n;hole++){
   const clause=[];
   for(const p of [i,j])for(let b=0;b<ell;b++) {
     clause.push(((hole>>b)&1) ? -pvar(p,b) : pvar(p,b));
   }
   check(clause.length===2*ell, 'original width');
   check(new Set(clause.map(Math.abs)).size===2*ell, 'original properness');
   const collisionAssignment=(lit)=>(((hole>>( (Math.abs(lit)-1)%ell))&1)===1)===(lit>0);
   check(clause.every(lit=>!collisionAssignment(lit)),'source collision falsified');
   parents++;signedControls++;
 }
 check(parents===n*n*(n+1)/2,'all pair-hole source clauses enumerated');
 return {n,parents,signedControls};
}
const result={result:'COMPUTATIONAL_FINITE_CONTROLS_ONLY', premise:'Pang arXiv:2610.00837v2 Theorem 7.2(e), fixed p=2,r=1; no asymptotic proof executed',
 metrics:[4,8,16,32,256,1024,4096].map(metrics),
 chains:[4,6,8,10].map(checkChain),
 collision:[4,8,16].map(originalBphp),
 failures_rejected:0};
for(const bad of [0,1,2,3,5,6,9,24,255]) {try { metrics(bad); } catch(e) {result.failures_rejected++;} }
check(result.failures_rejected===9, 'all invalid hole counts reject');
result.assertions=checks;
const output=JSON.stringify(result,null,2)+'\n';
if (require.main===module) {
  fs.writeFileSync(process.argv[2]||'lspv1_480_raw.json',output);
  process.stdout.write(output);
}
module.exports={metrics,checkChain,originalBphp};
