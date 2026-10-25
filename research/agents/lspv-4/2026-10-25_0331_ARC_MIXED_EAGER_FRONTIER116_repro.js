"use strict";
// ARC-MIXED-EAGER-FRONTIER116: exact exponent envelopes and ordinary two-level
// SAT/UNSAT controls. Run: node 2026-10-25_0331_ARC_MIXED_EAGER_FRONTIER116_repro.js
// Finite bit counters are serialization operations, NOT matched FLMV TM cycles.
let runAssertions=0;
function check(ok,msg,detail){if(!ok)throw Error(msg+" "+JSON.stringify(detail||{}));runAssertions++;}
function bits(v,w){let s=v.toString(2);if(s.length>w||v<0)throw Error("bit width");return "0".repeat(w-s.length)+s;}
function taut(c){let set=new Set(c);return c.some(v=>set.has(-v));}
function pad(clauses,target){let c=clauses.filter(x=>!taut(x)).map(x=>x.slice());check(c.length<=target,"core too long",{size:c.length,target});while(c.length<target)c.push([4,-4,5]);return c;}
function restrict(clauses,v,b){let out=[];for(const c of clauses){if(taut(c))continue;let satisfied=false;const d=[];for(const l of c){if(Math.abs(l)===v){if((l>0)===(b===1))satisfied=true;}else d.push(l);}if(!satisfied)out.push(d);}return out;}
function writeFormula(c,ctr){let out="1100"+bits(5,4)+bits(c.length,16)+bits(0,8);
 for(const clause of c){check(clause.length<=3,"record arity");out+=bits(clause.length,3);for(let i=0;i<3;i++){let l=clause[i]||0;out+=(l<0?"1":"0")+bits(Math.abs(l),3);}}
 ctr.write+=out.length;ctr.ones+=out.split("1").length-1;ctr.zeros+=out.length-(out.split("1").length-1);return out;}
function readFormula(s,ctr){ctr.read+=s.length;check(s.length>=32&&s.slice(0,4)==="1100","header");
 let n=parseInt(s.slice(4,8),2),m=parseInt(s.slice(8,24),2);
 check(n===5&&s.length===32+15*m,"encoded length",{n,m,len:s.length});
 const a=[];for(let j=0;j<m;j++){let p=32+j*15,arity=parseInt(s.slice(p,p+3),2);check(arity<=3,"arity");let c=[];
 for(let h=0;h<3;h++){let v=parseInt(s.slice(p+3+4*h+1,p+3+4*h+4),2),neg=s[p+3+4*h]==="1";
 if(h<arity){check(v>0&&v<=5,"literal range");c.push(neg?-v:v);}else check(v===0&&!neg,"padding");}a.push(c);}return a;}
function sat(clauses){for(let assignment=0;assignment<32;assignment++){let ok=true;for(const c of clauses){let good=false;for(const l of c){let v=(assignment>>(Math.abs(l)-1))&1;if((l>0&&v===1)||(l<0&&v===0)){good=true;break;}}if(!good){ok=false;break;}}if(ok)return true;}return false;}
function cores(){let full=[];for(let b=0;b<8;b++)full.push([1,2,3].map((v,i)=>((b>>i)&1)?-v:v));
 let affine=[];for(let b=0;b<8;b++){let p=((b&1)+((b>>1)&1)+((b>>2)&1))%2;if(p===1)affine.push([1,2,3].map((v,i)=>((b>>i)&1)?-v:v));}
 return {SAT:[[1,2,3],[-1,2,3]],UNSAT_FULL:full,HORN_SAT:[[-1,-2,3],[-3,1],[-1]],AFFINE_SAT:affine,SCC_UNSAT:[[1,2],[-1,2],[1,-2],[-1,-2]],DIRECT_UNSAT:[[3],[-3]]};}
// Integer exponent units = 1/10000. g1,g2 grid arguments are hundredths.
function score(g1,g2){let e1=11000+100*g1,z=11500+50*g2,guest=12000;return {
 EE:Math.max(e1,z,guest),EL:Math.max(e1,12000+50*g2),
 LE:Math.max(11500+50*g2+100*g1,guest),LL:12000+50*g2+100*g1};}
function runAudit(){
 runAssertions=0;let counts={sources:0,sat:0,unsat:0,firstChildren:0,secondChildren:0,readBits:0,writeBits:0,zeroWritesOnFreshBody:0,oneWritesOnFreshBody:0};
 let examples=[];
 for(const k of [8,9,10,11])for(const [family,core] of Object.entries(cores())){
 const ctr={read:0,write:0,zeros:0,ones:0};
 let rootBits=writeFormula(pad(core,k**4),ctr),F=readFormula(rootBits,ctr);
 let rootSat=sat(F),firstTruth=[],leafTruth=[];
 check(rootSat===sat(core),"tautology padding altered root label",{family,k});
 for(let x=0;x<2;x++){
 let yBits=writeFormula(pad(restrict(F,1,x),k*k),ctr),Y=readFormula(yBits,ctr),ySat=sat(Y);
 check(yBits.length===32+15*k*k,"first ordinary child body");
 const leaves=[];
 for(let y=0;y<2;y++){
 let zBits=writeFormula(pad(restrict(Y,2,y),k),ctr),Z=readFormula(zBits,ctr),zSat=sat(Z);
 check(zBits.length===32+15*k,"second ordinary child body");
 check(sat(restrict(Y,2,y))===zSat,"second-child exact label",{k,family,x,y});
 leaves.push(zSat);leafTruth.push(zSat);counts.secondChildren++;
 }
 check(ySat===leaves.some(Boolean),"second-level compatible OR",{k,family,x});
 firstTruth.push(ySat);counts.firstChildren++;
 }
 check(rootSat===firstTruth.some(Boolean),"first-level compatible OR",{k,family});
 counts.sources++;counts[rootSat?"sat":"unsat"]++;
 counts.readBits+=ctr.read;counts.writeBits+=ctr.write;
 counts.zeroWritesOnFreshBody+=ctr.zeros;counts.oneWritesOnFreshBody+=ctr.ones;
 examples.push({k,family,rootSat,sourceBits:rootBits.length,firstBits:32+15*k*k,secondBits:32+15*k,firstTruth,leafTruth,serialization:ctr});
 }
 let grid={EE:0,EL:0,LE:0,LL:0},center={};
 for(let g1=0;g1<=20;g1++)for(let g2=0;g2<=20;g2++){
 let v=score(g1,g2);
 for(const key of Object.keys(grid))if(v[key]<12050)grid[key]++;
 check(v.EE<=v.EL&&v.EE<=v.LE&&v.LE<=v.LL,"mode dominance",{g1,g2,v});
 if(g1===10&&g2===10)center=v;
 }
 check(center.EE===12000&&center.EL===12500&&center.LE===13000&&center.LL===13500,"center exact",center);
 check(counts.sat>0&&counts.unsat>0&&counts.firstChildren===2*counts.sources&&counts.secondChildren===4*counts.sources,"label/child coverage");
 check(counts.readBits>0&&counts.writeBits===counts.readBits,"read and serialization accounting");
 check(counts.oneWritesOnFreshBody+counts.zeroWritesOnFreshBody===counts.writeBits,"write tally");
 return {
 tag:"ARC-MIXED-EAGER-FRONTIER116",
 status:"PROVED/EXACT conditional resource algebra, COMPUTATIONAL finite ordinary-SAT controls. ARC-EDGE-90 and P versus NP OPEN.",
 grammar:"Finite prototype only: 32-bit header and 15-bit three-slot records for 5 names; k=8,9,10,11; all tautological filler clauses are true.",
 parameters:{a1:"3/5",theta1:"1/2",a2:"3/5",theta2:"1/2",guest_t:"6/5",guest_s:"1/2",g1:"1/10",g2:"1/10",exponent_unit:"1/10000",flmv_time_strict:"241/200",flmv_space_strict:"11642479/23232400"},
 center,gridFeasibleStrictTime:grid,gridSize:441,counts,assertions:runAssertions,failures:0,examples,
 limitations:"Finite prototype fixed 16-bit count field: no asymptotic benchmark or matched FLMV machine trace. Exponent model is separately proved algebraically under hypothetical exact typed contractors. Counts exclude actual FLMV tape control/index/arithmetic/erasure cycles, caching, policy discovery, and physical circuit measurements. Source families are easy."};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module){console.log(JSON.stringify(runAudit(),null,2));}
