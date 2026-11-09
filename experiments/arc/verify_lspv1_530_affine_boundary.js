'use strict';
// Independent exact GF(2) matrix verifier for LSPV-1/530. Not a historical Rmix checker.
const fs = require('fs');
const assert = require('node:assert/strict');
const data = JSON.parse(fs.readFileSync(process.argv[2] || __dirname + '/lspv1_530_affine_boundary_raw.json','utf8'));
let assertions = 0;
function ok(cond, why) { assertions++; assert.ok(cond, why); }
function tuples(q,b) {
  const out=[];
  for(let k=0;k<q**b;k++){
    let z=k, row=[];
    for(let i=0;i<b;i++){row.push(z%q);z=Math.floor(z/q);}
    out.push(row);
  }
  return out;
}
function indicator(x,q){
  let v=0n;
  for(let i=0;i<x.length;i++)v |= 1n << BigInt(q*i+x[i]);
  return v;
}
function basis(vecs) {
  const out=new Map();
  for(let v of vecs)while(v) {
    const i=v.toString(2).length-1;
    if(!out.has(i)){out.set(i,v);break;}
    v ^= out.get(i);
  }
  return out;
}
function residual(v,B) {
  for(const i of [...B.keys()].sort((x,y)=>y-x)) {
    if((v >> BigInt(i)) & 1n)v ^= B.get(i);
  }
  return v;
}
function parity(n) {let p=0;while(n){p^=1;n &= n-1;}return p;}
for(const c of data.cases){
  const all=tuples(c.q,c.b);
  const good=all.filter(x=>(x.reduce((s,y,i)=>s+y*c.signs[i],0)%c.q+c.q)%c.q===c.c);
  ok(good.length===c.models,'good tuple count');
  const anchor=indicator(good[0],c.q);
  const B=basis(good.slice(1).map(x=>indicator(x,c.q)^anchor));
  ok(B.size===c.expected && B.size===c.dimension,'exact affine dimension');
  let wrong=0, inHull=0;
  for(const x of all) {
    if((x.reduce((s,y,i)=>s+y*c.signs[i],0)%c.q+c.q)%c.q!==c.c){
      wrong++;if(residual(indicator(x,c.q)^anchor,B)===0n)inHull++;
    }
  }
  ok(wrong===c.wrong,'invalid boundary count');
  ok(inHull===c.wrong_in_affine_hull,'hull membership');
}
// Exhaustive independent check of all 2^12 affine coefficient vectors for q=3,b=4.
// A valid row has the same F2 parity on every charge-respecting assignment.
const q=3,b=4,charge=1,signs=[1,-1,1,-1];
const sat=tuples(q,b).filter(x=>(x.reduce((s,y,i)=>s+y*signs[i],0)%q+q)%q===charge);
const onehot=sat.map(x=>Number(indicator(x,q)));
let validMasks=0;
for(let mask=0;mask<(1<<(q*b));mask++){
  const p=parity(mask&onehot[0]);
  if(onehot.every(z=>parity(mask&z)===p))validMasks++;
}
ok(validMasks===16,'only the four per-group parity choices are valid');
ok(data.cases.length===32,'raw schema case count');
ok(data.cases.every(z=>z.q>=2 && z.b>=2 && z.signs.length===z.b),'raw schema bounds');
// Two hostile controls must NOT be misreported as odd-q,b>=3.
ok(data.cases.find(x=>x.q===3&&x.b===2&&x.c===0).dimension===2,'b2 countercontrol');
ok(data.cases.find(x=>x.q===2&&x.b===3&&x.c===0).dimension===2,'even-q countercontrol');
console.log(JSON.stringify({cases:data.cases.length,assertions,exhaustive_masks:4096,
 valid_masks:validMasks,total_wrong:data.summary.total_wrong_examined},null,2));
