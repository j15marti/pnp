"use strict";
/* LSPV-4/495: independent anisotropic Route A exponent-envelope controls.
 * Node source: original proper signed K4 Tseitin 3-CNF.
 * Not an implementation of an FLMV machine or proof of P != NP.
 */
function audit() {
  const tests={passed:0, failed:0};
  function ok(p,m) {if(!p){tests.failed++;throw new Error(m)}tests.passed++;}
  function gcd(a,b){while(b){const r=a%b;a=b;b=r}return a;}
  function rat(p,q=1n){p=BigInt(p);q=BigInt(q);const g=gcd(p,q);return [p/g,q/g]}
  function betaGapSign(cp,cq,sp,sq){
    const p=BigInt(cp),q=BigInt(cq),a=BigInt(sp),b=BigInt(sq);
    return ((p+2n*q)*q*q-p*p*p)*b-2n*p*p*q*a;
  }
  function beta(c){return ((c+2)/(c*c)-c)/2}
  const bisection=(fn,lo,hi,n=120)=>{for(let i=0;i<n;i++){const mid=(lo+hi)/2;if(fn(mid)>0)lo=mid;else hi=mid;}return(lo+hi)/2};
  const root=bisection(c=>beta(c)-.5,1.2,1.21);
  ok(root>1.2055694304005 && root<1.2055694304007,"root bracket");
  ok(betaGapSign(6,5,1,2)===2n*1n /* not necessarily normalized */||betaGapSign(6,5,1,2)>0n,"1/90 positive");
  const base=beta(1.2)-.5;
  ok(Math.abs(base-1/90)<1e-12,"base beta margin 1/90");
  ok(betaGapSign(301,250,1,2)>0n,"theta=.002 safe: c=1.204");
  ok(betaGapSign(603,500,1,2)<0n,"theta=.003 unsafe: c=1.206");
  const baseParameters={rho:1.1,gamma:.6,lambda:.5,sigma:.5};
  const thetaCrit=(1-baseParameters.lambda)*root-baseParameters.gamma;
  const lambdaCrit=1-baseParameters.gamma/root;
  const gammaCrit=(1-baseParameters.lambda)*root;
  const sigmaCrit=beta(1.2);
  ok(thetaCrit>.0027847 && thetaCrit<.0027848,"per-call overhead critical");
  ok(lambdaCrit>.5023098 && lambdaCrit<.50231,"child exponent critical");
  ok(Math.abs(gammaCrit-.602784715200295)<1e-12,"branch exponent critical");
  ok(Math.abs(sigmaCrit-23/45)<1e-12,"peak space critical");
  const cases=[];
  for(const theta of [0,.001,.002,.0028,.003]){
    const c=Math.max(1.1,(.6+theta)/.5);
    const margin=beta(c)-.5;
    const predicted=(margin>0);
    let t=4,s=3;
    let firstEntry=null;
    for(let j=0;j<100;j++){
      if(s<beta(t)&&firstEntry===null)firstEntry=j;
      t=Math.max(1.1,.6+theta+.5*t);
      s=Math.max(.5,.5*s);
    }
    ok((firstEntry!==null)===predicted,"finite-entry prediction "+theta);
    cases.push({theta,time_fixed_point:c,space_fixed_point:.5,beta_margin:margin,first_entry_iteration_from_t4_s3:firstEntry});
  }
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const incident=Array.from({length:4},(_,v)=>edges.map((e,i)=>e.includes(v)?i:-1).filter(x=>x>=0));
  const bit=(a,i)=>(a>>i)&1;
  const parity=a=>{let p=0;while(a){p^=a&1;a>>=1}return p};
  let sourceCount=0,unsatCount=0,satCount=0,modelChecks=0,essentialClauses=0,parseControls=0;
  function validClause(C){return C.length===3&&new Set(C.map(x=>Math.abs(x))).size===3&&C.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=6)}
  function original(chi){let clauses=[];for(let v=0;v<4;v++){const ids=incident[v];for(let mask=0;mask<8;mask++){if(parity(mask)!==bit(chi,v)){const C=ids.map((idx,k)=>bit(mask,k)?-(idx+1):(idx+1));ok(validClause(C),"original proper signed 3CNF");clauses.push(C)}}}return clauses;}
  const sat=(clauses,assignment)=>clauses.every(C=>C.some(lit=>lit>0?bit(assignment,lit-1)===1:bit(assignment,-lit-1)===0));
  for(let chi=0;chi<16;chi++){
    const clauses=original(chi);
    ok(clauses.length===16,"sixteen clauses K4");
    const models=Array.from({length:64},(_,a)=>a).filter(a=>sat(clauses,a));
    const expectSat=parity(chi)===0;
    ok((models.length>0)===expectSat,"charge parity SAT iff even");
    sourceCount++;modelChecks+=64;
    if(expectSat){satCount++;ok(models.length===8,"connected K4 even-charge 8 models")}
    else{
      unsatCount++;
      for(let j=0;j<clauses.length;j++){
        const missing=clauses.filter((_,k)=>k!==j);
        const witness=Array.from({length:64},(_,a)=>a).find(a=>sat(missing,a));
        ok(witness!==undefined,"odd-charge original clause essential");
        essentialClauses++;
      }
    }
  }
  ok(!validClause([1,-1,2]),"duplicate variable malformed");parseControls++;
  ok(!validClause([1,2]),"truncated clause malformed");parseControls++;
  ok(!validClause([0,2,3]),"zero literal malformed");parseControls++;
  ok(!validClause([1,2,7]),"out of range original source malformed");parseControls++;
  const raw={
    role:"LSPV-4",run:495,status:"PROVED/RESTRICTED arithmetic, COMPUTATIONAL finite controls, OPEN Route A",
    date_pacific:"2026-11-08 06:36 PST",
    source:"original signed cubic K4 Tseitin 3-CNF; growing cubic expanders are separate published Resolution-hard control",
    theorem:"for q=n^(gamma+o(1)), M=n^(lambda+o(1)), local=n^(rho+o(1)), per-guest-step native interpreter overhead n^(theta+o(1)) and peak=n^(sigma+o(1)), t*=max(rho,(gamma+theta)/(1-lambda)); FLMV strict contradiction if sigma<beta(t*)",
    beta_root_half_space:root,
    base:baseParameters,
    margins:{time_at_theta0:base,theta_max_at_space_half:thetaCrit,lambda_max_at_space_half:lambdaCrit,gamma_max_at_space_half:gammaCrit,space_max_at_theta0:sigmaCrit},
    cases,finite_controls:{sources:sourceCount,sat:satCount,unsat:unsatCount,assignment_evaluations:modelChecks,clauses_essential_witnessed:essentialClauses,malformed_rejected:parseControls},
    tests
  };
  ok(tests.failed===0,"all checks before finalization");
  raw.tests={...tests};
  return raw;
}
if(typeof module!=="undefined" && require.main===module)console.log(JSON.stringify(audit(),null,2));
