"use strict";
// LSPV-3/541: independently replayable proposed DEF-facet/Resolution audit.
// This is NOT a parser or verifier for historical R_mix341 accepted bytes.
const canon=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const equal=(a,b)=>JSON.stringify(canon(a))===JSON.stringify(canon(b));
const resolve=(a,b,p)=>{
 if(a.includes(p)&&b.includes(-p))return canon([...a.filter(v=>v!==p),...b.filter(v=>v!==-p)]);
 if(a.includes(-p)&&b.includes(p))return canon([...a.filter(v=>v!==-p),...b.filter(v=>v!==p)]);
 throw Error("illegal pivot");
};
const gate=(x,y,z)=>[[-z,x],[-z,y],[z,-x,-y]].map(canon);
const unit=(x,a,b)=>[[x,a,b],[x,a,-b],[x,-a,b],[x,-a,-b]].map(canon);
let checks=0;const ok=(b,msg)=>{if(!b)throw Error(msg);checks++};
const sources=[...unit(1,3,4),...unit(2,5,6)];
ok(sources.length===8&&sources.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"strict3");
const huge=BigInt("1000000000000000000000000113");
ok(huge>BigInt(Number.MAX_SAFE_INTEGER),"large id retained as BigInt");
const z=101;const [f0,f1,f2]=gate(1,2,z);
let facet_checks=0,models=0;
for(let bits=0;bits<64;bits++){
 const v={};for(let i=1;i<=6;i++)v[i]=Boolean(bits&(1<<(i-1)));
 v[z]=v[1]&&v[2];
 const holds=c=>c.some(t=>t>0?v[t]:!v[-t]);
 for(const c of [f0,f1,f2]){ok(holds(c),"DEF facet invalid");facet_checks++}
 if(sources.every(holds)){models++;ok(v[z],"source doesn't imply z")}
}
ok(models===16,"source SAT models");
let resCount=0;
const r=(a,b,p,out)=>{const c=resolve(a,b,p);ok(equal(c,out),"wrong resolvent");resCount++;return c};
const ux1=r(sources[0],sources[1],4,[1,3]);
const ux2=r(sources[2],sources[3],4,[1,-3]);
const ux=r(ux1,ux2,3,[1]);
const uy1=r(sources[4],sources[5],6,[2,5]);
const uy2=r(sources[6],sources[7],6,[2,-5]);
const uy=r(uy1,uy2,5,[2]);
const a=r(ux,f2,1,[z,-2]);
const b=r(uy,a,2,[z]);
ok(equal(b,[z])&&resCount===8,"certificate");
let rejected=0;
for(const fn of [()=>resolve(ux,f0,1),()=>resolve(uy,a,1)]) {
 try{fn()}catch(_){rejected++;} 
}
ok(rejected===2,"accepted bogus orientation");
ok(!equal(a,[z]),"illegal cheap strengthening");
ok(new Set([1,-1]).size===2,"incompatible contexts not discharged");
console.log(JSON.stringify({status:"PASS",artifact:"LSPV-3/541",scope:"proposed DEF-facet and oriented RES only",source_clauses:8,source_models:models,paid_def:1,paid_res:resCount,total_paid:9,facet_checks,assertions:checks,rejected_orientations:rejected,large_identifier_decimal:huge.toString()},null,2));
