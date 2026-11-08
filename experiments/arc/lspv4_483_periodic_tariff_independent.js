"use strict";
// LSPV-4/483 independent JavaScript verifier. Numeric checks are FINITE only.
const b=x=>((x+2)/(x*x)-x)/2;
const f=(x,d)=>Math.max(1.1+d,.6+d+(.5+d)*x);
const s=(x,d)=>Math.max(.5+d,(.5+d)*x);
const ce=d=>(1.8+d)/(1.5-d);
const numerator=d=>500*d**3-2250*d*d+14265*d-54;
const den=d=>20*(2*d-3)*(5*d+9)**2;
let checks=0;let errors=[];
function check(ok,msg){checks++;if(!ok)errors.push(msg)}
let lo=0,hi=.01; for(let i=0;i<105;i++){const mid=(lo+hi)/2;if(b(ce(mid))-.5>0)lo=mid;else hi=mid}
const crit=(lo+hi)/2;
for(let i=0;i<=500;i++){const d=i/50000;const g=b(ce(d))-.5;check(Math.abs(g-numerator(d)/den(d))<2e-14,"factor "+i);}
for(const d of [0,.0001,.001,.003,.0035,.00375,.0038,.004,.01]){
 for(const [t0,s0] of [[1,0],[2,2],[10,10],[10000,10000]]){
  let t=t0,v=s0;
  for(let j=0;j<90;j++){t=f(f(t,d),0);v=s(s(v,d),0)}
  check(Math.abs(t-ce(d))<1e-8,"time convergence "+d);
  check(Math.abs(v-.5)<1e-8,"space convergence "+d);
  check((b(t)-v>1e-11)===(b(ce(d))-.5>1e-11),"margin "+d);
 }
 const tOdd=f(ce(d),d),sOdd=s(.5,d);
 check(Math.abs(f(tOdd,0)-ce(d))<1e-12,"two phase time "+d);
 check(Math.abs(s(sOdd,0)-.5)<1e-12,"two phase space "+d);
}
const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
let sat=0,unsat=0,malformedRejected=0;
for(let mask=0;mask<16;mask++){
 const clauses=[];
 for(let v=0;v<4;v++){
  const ids=edges.map(([u,w],i)=>u===v||w===v?i+1:0).filter(Boolean);
  for(let m=0;m<8;m++){
   const parity=((m&1)+((m>>1)&1)+((m>>2)&1))&1;
   if(parity===((mask>>v)&1))continue;
   clauses.push(ids.map((id,k)=>((m>>k)&1)?-id:id));
  }
 }
 let models=0;for(let a=0;a<64;a++){
  if(clauses.every(c=>c.some(l=>(l>0?((a>>(l-1))&1):!((a>>(-l-1))&1)))))models++;
 }
 check(clauses.length===16,"16 clauses "+mask);
 check(models===(mask.toString(2).split('1').length%2===0?0:8),"SAT count "+mask);
 if(models)sat++;else unsat++;
}
for(const bad of [[1,1,-2],[0,2,3],[1,2,7],[1,2],['1',2,3],[]]){
 const valid=bad.length===3&&bad.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=6)&&new Set(bad.map(Math.abs)).size===3;
 check(!valid,"malformed control");if(!valid)malformedRejected++;
}
check(Math.abs(crit-.0037877499958675668)<2e-14,"critical threshold");
const out={run:"LSPV-4/483",independent:"JS Number and K4 exhaustive",checks,failures:errors.length,errors:errors.slice(0,5),h_critical:crit,k4_sat:sat,k4_unsat:unsat,malformed_rejections:malformedRejected,native_FLMV:false};
if(errors.length)throw Error(JSON.stringify(out));console.log(JSON.stringify(out,null,2));