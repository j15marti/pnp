"use strict";
// TMR-3/049: standalone BigInt exact-rational forbidden-region and hierarchy checks.
// Requires only Node.js >=14. No network, no libraries, no actual MajMajSAT/SAT solver.
function audit(){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let x=a%b;a=b;b=x}return a};
 const q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d};const g=gcd(n,d);return {n:n/g,d:d/g}};
 const add=(x,y)=>q(x.n*y.d+y.n*x.d,x.d*y.d);
 const mul=(x,y)=>q(x.n*y.n,x.d*y.d);
 const cmp=(x,y)=>x.n*y.d<y.n*x.d?-1:x.n*y.d>y.n*x.d?1:0;
 const max=(x,y)=>cmp(x,y)>=0?x:y;
 const fmt=x=>x.d===1n?x.n.toString():x.n+"/"+x.d;
 const one=q(1),two=q(2),half=q(1,2),threeQuarters=q(3,4);
 const quarter=q(1,4),eighth=q(1,8);
 let checks=0, violations=0, sampleCount=0, kCount=0;
 const assert=(v,msg)=>{checks++;if(!v){violations++;throw Error(msg)}};
 for(let i=1;i<=1024;i++){
   const g=q(i,4096),target=add(one,g),r=add(one,mul(g,eighth));
   const t=add(one,mul(g,quarter)),h=mul(g,quarter);
   const virtTime=max(r,add(t,h)),virtSpace=half;
   const matTime=max(r,t),matSpace=one;
   const manyTime=max(r,add(one,add(t,h)));
   const slowTime=max(r,add(t,g));
   assert(cmp(g,quarter)<=0,"g range");
   assert(cmp(virtTime,target)<0,"virtual time slack");
   assert(cmp(virtSpace,threeQuarters)<0,"virtual space slack");
   assert(cmp(matTime,target)<0,"materialized time");
   assert(cmp(matSpace,threeQuarters)>0,"materialized space firewall");
   assert(cmp(manyTime,target)>0,"N-query upper bound not certified");
   assert(cmp(slowTime,target)>0,"high virtual access overhead");
   assert(fmt(add(t,h))===fmt(add(one,mul(g,half))),"exact virtual exponent");
   sampleCount++;
 }
 for(let k=2;k<=160;k++){
   const d=q(4*(k-1)+1,4*(k-1));
   let pow=one;for(let j=0;j<k-1;j++)pow=mul(pow,d);
   assert(cmp(d,one)>0,"d>1");
   assert(cmp(pow,q(4,3))<0,"rational speedup stronger bound");
   assert(cmp(pow,q(3,2))<0,"hierarchy gap 3/2");
   kCount++;
 }
 const pyes=q(17,32);const pjoint=mul(pyes,pyes);
 assert(cmp(pyes,half)>0,"weak PP one-query yes");
 assert(cmp(pjoint,half)<0,"two weak PP AND fails");
 assert(cmp(add(one,q(-17,32)),half)<0,"one-query inversion");
 return {id:"TMR3_ALLENDER_ONEQUERY049_V8",status:"COMPUTATIONAL_EXACT_RATIONAL",gamma_grid:"i/4096, i=1..1024 (synthetic parameter, NOT published gamma)",symbolic_speedup_k:"k=2..160",gamma_samples:sampleCount,k_checks:kCount,assertions:checks,failures:violations,onequery_exponents:{time:"1+g/2",space:"1/2",source_threshold_time:"1+g",source_threshold_space:"3/4"},materialized_space_exponent:"1",N_queries_time_ledger:"2+g/2",slow_generator_time_ledger:"1+5g/4",speedup_rational_d:"1+1/(4(k-1))",bound_on_d_power:"d^(k-1)<4/3<3/2",unbounded_error_AND_counterexample:{p_yes:fmt(pyes),p_and:fmt(pjoint),p_inverted:fmt(add(one,q(-17,32)))},theorem_status:"CONDITIONAL one-query classical virtualization + primary-source quantum simulation; algebraic-amplitude/constructibility and uniform model obligations explicit"};
}
console.log(JSON.stringify(audit(),null,2));
