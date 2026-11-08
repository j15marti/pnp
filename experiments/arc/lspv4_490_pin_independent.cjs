'use strict';
/* LSPV-4/490: independent finite gadget audit, NOT a native FLMV simulator. */
const assert=require('assert');
let counts={guardTruthRows:0,pinnedProjectionRows:0,pinTruthRows:0,pinMinimalityChecks:0,recurrenceChecks:0,malformedScopeGuards:0};
const lit=(x,v)=>x>0?!!v:!v;
const clause3=(arr,vals)=>arr.some(l=>lit(l,vals[Math.abs(l)]));
for(let U=0;U<=1;U++)for(let V=0;V<=1;V++)for(let W=0;W<=1;W++)for(let Z=0;Z<=1;Z++){
  let wanted=!!(U||V||W||Z),got=false;
  for(let A=0;A<=1;A++)if((U||V||A)&&(!A||W||Z))got=true;
  assert.strictEqual(got,wanted);counts.guardTruthRows++;
  let pinned=false;
  for(let A=0;A<=1;A++)for(let P=0;P<=1;P++)for(let Q=0;Q<=1;Q++){
    let pin=[[-4,5,6],[-4,5,-6],[-4,-5,6],[-4,-5,-6]];
    let pinok=pin.every(c=>clause3(c,{4:Z,5:P,6:Q}));
    if(pinok&&(U||V||A)&&(!A||W||Z))pinned=true;
  }
  assert.strictEqual(pinned,Z===0 && !!(U||V||W));counts.pinnedProjectionRows++;
}
for(let z=0;z<=1;z++)for(let p=0;p<=1;p++)for(let q=0;q<=1;q++){
 const F=[[-4,5,6],[-4,5,-6],[-4,-5,6],[-4,-5,-6]];
 assert.strictEqual(F.every(c=>clause3(c,{4:z,5:p,6:q})),z===0);counts.pinTruthRows++;
}
const pin=[[-4,5,6],[-4,5,-6],[-4,-5,6],[-4,-5,-6]];
for(let mask=0;mask<16;mask++)if(mask!==15){
 const subset=pin.filter((_,i)=>(mask>>i)&1);
 assert(Array.from({length:4},(_,i)=>({4:1,5:i>>1,6:i&1})).some(vals=>subset.every(c=>clause3(c,vals))));
 counts.pinMinimalityChecks++;
}
for(let m0 of [0,1,3,11,101])for(let k=1;k<=11;k++){
 let mm=BigInt(m0);for(let i=0;i<k;i++)mm=16n*mm+4n;
 assert.strictEqual(mm,BigInt(m0)*16n**BigInt(k)+4n*(16n**BigInt(k)-1n)/15n);
 counts.recurrenceChecks++;
}
for(let m of [0,1,2,8]){
 let nOut=m?32*m+4:5,mOut=16*m+4;
 assert(nOut<=3*mOut+3 && mOut>=4);counts.malformedScopeGuards++;
}
console.log(JSON.stringify({status:'COMPUTATIONAL independent JS primitive checks',counts}));
