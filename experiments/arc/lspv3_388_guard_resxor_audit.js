/* LSPV-3/388 Res(oplus) guarded restriction and lift finite audit.
 * No external dependencies. Run: node lspv3_388_guard_resxor_audit.js
 * Symbolic theorem is in report; this finite exhaustive audit is a control.
 */
"use strict";
function parity(n){let p=0;while(n){p^=1;n&=n-1;}return p}
function eq(a,b){return {a,b}}
function validEq(q,n){return q&&Number.isInteger(q.a)&&q.a>=0&&q.a<(1<<n)&&(q.b===0||q.b===1)}
function validClause(C,n){return Array.isArray(C)&&C.every(q=>validEq(q,n))}
function value(C,z){return C.some(q=>parity(q.a&z)===q.b)}
function holds(C,D,n){for(let z=0;z<(1<<n);z++)if(value(C,z)&&!value(D,z))return false;return true}
function twoHold(A,B,C,n){for(let z=0;z<(1<<n);z++)if(value(A,z)&&value(B,z)&&!value(C,z))return false;return true}
function restrict(C){return C.map(q=>eq(q.a&3,q.b^((q.a&4)?1:0)))}
function guard(C){return [eq(4,0),...C]}
function allClauses(n){const atoms=[];for(let a=0;a<(1<<n);a++)for(let b=0;b<2;b++)atoms.push(eq(a,b));
 const out=[[]];for(let i=0;i<atoms.length;i++)out.push([atoms[i]]);
 for(let i=0;i<atoms.length;i++)for(let j=i+1;j<atoms.length;j++)out.push([atoms[i],atoms[j]]);
 return out}
function audit(){
 let checks=0; const claim=(b,msg)=>{checks++;if(!b)throw Error(msg)};
 const C2=allClauses(2),C3=allClauses(3);
 let sourceWeak=0, cofactorWeak=0, resolution=0, active=0, constPivot=0, mixed=0;
 // All one-premise semantic inferences over at most two affine literals.
 for(const A of C2)for(const B of C2)if(holds(A,B,2)){
   sourceWeak++;claim(holds(guard(A),guard(B),3),"guarded semantic weakening fails");
 }
 // Every semantic weakening over the guard and data remains sound on t=1.
 for(const A of C3)for(const B of C3)if(holds(A,B,3)){
   cofactorWeak++;claim(holds(restrict(A),restrict(B),2),"cofactor semantic weakening fails");
 }
 // All complementary affine pivots, including pivots involving the guard.
 for(let a=1;a<8;a++)for(const A of C2)for(const B of C2){
   const P=[...A,eq(a,0)],Q=[...B,eq(a,1)],R=[...A,...B];
   resolution++;claim(twoHold(P,Q,R,3),"general Res(oplus) pivot unsound");
   claim(twoHold(restrict(P),restrict(Q),restrict(R),2),"cofactor pivot unsound");
   if((a&3)===0){
     const PS=restrict(P),QS=restrict(Q),RS=restrict(R);
     const legal=holds(PS,RS,2)||holds(QS,RS,2);
     constPivot++;claim(legal,"constant pivot lacks one-premise weakening");
   } else active++;
   if(a&4)mixed++;
 }
 // Forward guard lift of every data-variable affine pivot.
 let lifted=0;
 for(let a=1;a<4;a++)for(const A of C2)for(const B of C2){
   const P=[...A,eq(a,0)],Q=[...B,eq(a,1)],R=[...A,...B];
   lifted++;claim(twoHold(guard(P),guard(Q),guard(R),3),"guarded resolution pivot fails");
 }
 // Both-label controls from same signed source: contradictory/compatible.
 const Fbad=[[eq(1,0)],[eq(1,1)]], Fgood=[[eq(1,0)]];
 function models(F,n){let count=0;for(let z=0;z<(1<<n);z++)if(F.every(C=>value(C,z)))count++;return count}
 claim(models(Fbad,2)===0,"bad SAT label");
 claim(models(Fgood,2)===2,"good SAT label");
 claim(models(Fbad.map(guard),3)===4,"guarded UNSAT has 4 satisfying models");
 claim(models(Fgood.map(guard),3)===6,"guarded SAT has 6 satisfying models");
 claim(!Array.from({length:8},(_,z)=>z).some(z=>(z&4)&&Fbad.map(guard).every(C=>value(C,z))),"bad guarded entailment");
 claim(Array.from({length:8},(_,z)=>z).some(z=>(z&4)&&Fgood.map(guard).every(C=>value(C,z))),"good guarded non-entailment");
 // Malformed and deliberately corrupted certificates.
 const invalid=[eq(-1,0),eq(8,0),eq(1,2),{a:1,b:"0"},null,{a:1.5,b:0}];
 for(const x of invalid)claim(!validEq(x,3),"malformed affine atom accepted");
 claim(!validClause("x",3),"malformed clause accepted");
 claim(!validClause([{a:1,b:0},{a:7,b:-1}],3),"corrupted clause accepted");
 claim(!holds([eq(1,0)],[eq(1,1)],2),"corrupted semantic step accepted");
 return {schema:"LSPV3_388_RESOPlus_GUARD_AUDIT",status:"COMPUTATIONAL",seed:null,
  exhaustive:true,base_affine_clauses:C2.length,guard_affine_clauses:C3.length,
  semweak_guard_checks:sourceWeak,semweak_cofactor_checks:cofactorWeak,
  resolution_steps:resolution,constant_pivot_cases:constPivot,nonconstant_pivot_cases:active,
  pivots_using_guard:mixed,forward_lifted_resolution_steps:lifted,
  tested_source_labels:{original_unsat_models:0,original_sat_models:2,guard_unsat_source_models:4,guard_sat_source_models:6},
  malformed_and_corruption_rejections:9,assertions:checks,
  limitation:"Only bounded finite local-rule validation; no minimum proof-size or R_mix341 theorem."};
}
console.log(JSON.stringify(audit(),null,2));