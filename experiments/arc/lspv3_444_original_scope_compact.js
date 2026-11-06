/* LSPV-3/444 independent finite analyzer; node lspv3_444_original_scope_compact.js
   Tests one inlined-original-coordinate LOCAL operation, NOT historical R_mix341. */
"use strict";
let assertions=0, rows=0, mutants=0;
function ok(b,msg){assertions++; if(!b) throw Error(msg);}
function relation(x,p,z){return Number(z === Number(x.every((bit,j)=>bit===p[j])));}
function localExistential(x,p,z){
  return Number([0,1].some(t=>z===Number(Boolean(t && x[x.length-1]===p[p.length-1]))));
}
function analytic(ell){
  const n=2**ell,m=n+1,D=m*(2*n-4),B=m*Math.max(0,2*n-16);
  return {ell,n,m,D,B,affected_locals:3*B};
}
for(let ell=2;ell<=6;ell++){
  const z=analytic(ell),expected=[[20,0],[108,0],[476,272],[1980,1584],[8060,7280]][ell-2];
  ok(z.D===expected[0] && z.B===expected[1],"wrong prefix gate counts");
}
for(let d=2;d<=5;d++)for(let mask=0;mask<2**d;mask++){
  const p=Array.from({length:d},(_,j)=>(mask>>j)&1);
  const essential=Array(d).fill(false);let projectedMismatch=false;
  for(let word=0;word<2**d;word++)for(let z=0;z<2;z++){
    const x=Array.from({length:d},(_,j)=>(word>>j)&1),v=relation(x,p,z);rows++;
    for(let j=0;j<d;j++){
      const y=x.slice();y[j]^=1;
      if(relation(y,p,z)!==v)essential[j]=true;
    }
    if(localExistential(x,p,z)!==v) projectedMismatch=true;
  }
  ok(essential.every(Boolean),"a prefix coordinate unexpectedly dispensable");
  ok(projectedMismatch,"ignoring predecessor gives identical relation");
}
const large=2n**32n, M=large+1n;
const dLarge=M*(2n*large-4n),bLarge=M*(2n*large-16n);
ok(dLarge===36893488138829168636n,"large exact D");
ok(bLarge===36893488087289561072n,"large exact B");
ok(3n*bLarge===110680464261868683216n,"large exact LOCAL calls");
function verifySummary(s){
  ok(Array.isArray(s.measurements) && s.measurements.length===5,"missing measurements");
  for(const a of s.measurements){
    const e=analytic(a.ell);
    ok(a.n===e.n && a.m===e.m && a.D===e.D && a.B===e.B &&
       a.affected_locals===e.affected_locals,"bad finite summary");
  }
  const l=s.ell_32_symbolic;
  ok(l.D===dLarge.toString() && l.B===bLarge.toString() &&
     l.affected_locals===(3n*bLarge).toString(),"large values must be exact decimal strings");
}
const summary={
measurements:Array.from({length:5},(_,i)=>analytic(i+2)),
ell_32_symbolic:{D:dLarge.toString(),B:bLarge.toString(),affected_locals:(3n*bLarge).toString()}
};
verifySummary(summary);
for(const mutate of [
 s=>s.measurements[2].n++,s=>s.measurements[1].D++,
 s=>s.measurements[4].B++,s=>s.measurements[0].affected_locals++,
 s=>s.ell_32_symbolic.D="1",s=>s.ell_32_symbolic.B="1",
 s=>s.ell_32_symbolic.affected_locals="1",s=>s.measurements.pop()
]){
  const copy=JSON.parse(JSON.stringify(summary));mutate(copy);
  let failed=false;try{verifySummary(copy);}catch(e){failed=true;}
  ok(failed,"mutated ledger not rejected");mutants++;
}
console.log(JSON.stringify({result:"PASS",assertions,enumerated_truth_rows:rows,mutants_rejected:mutants,
  status:"COMPUTATIONAL; inlined-original support only; native R_mix341 not checked"},null,2));
