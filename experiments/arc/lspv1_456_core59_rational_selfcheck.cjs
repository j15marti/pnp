#!/usr/bin/env node
'use strict';
// LSPV-1/456: independent exact-integer 1/59 rational threshold check.
// The probabilistic theorem additionally requires the paper/report's
// symbolic Tarsi + binomial union bound; this numeric script is NOT itself
// a proof of asymptotic hardness, and not a historical Rmix verifier.
const assert=require('node:assert/strict');
function gcd(a,b){while(b){[a,b]=[b,a%b];}return a;}
let tests=0;
function eq(x,y){tests++;assert.equal(x,y)}
function ok(x){tests++;assert.ok(x)}
const e68=68n, e25=25n, den=118n;
const num=8n*e68**2n*(2n*den*den-2n*den+1n);
const denom=59n*e25**2n*2n*den**2n;
const g=gcd(num,denom);
eq((num/g).toString(),'127682512');
eq((denom/g).toString(),'128361875');
ok(num<denom);
// Verify elementary series e upper bound:
// e <= sum_{j=0}^5 (1/j!) + sum_{j>=6} 1/j!
//   < 163/60 + (1/720)(1-1/7)^{-1} = 163/60+7/4320.
ok(163n*4320n*25n + 7n*60n*25n < 68n*60n*4320n);
const target=Number(num)/Number(denom);
for(const n of [590,5900,59000,590000]){
 const r=n/59, x=r/n;
 const f=8*Math.E**2*x*Math.exp(-x/2);
 ok(f<target+1e-13);
 ok(f<1);
}
console.log(JSON.stringify({status:'PASS',checks:tests,
  provable_rational_upper:'127682512/128361875',
  rational_upper:Number(num)/Number(denom),
  model:'random proper signed 3-CNF, 8n iid indexed clauses',
  scope:'arithmetic diagnostic only; proof in LSPV1/456 markdown'}));
