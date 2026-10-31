// Independent replay of the published ORIGINAL signed-clause raw artifact.
// Separate implementation; no calls to the producer's solver or arithmetic.
"use strict";
const assert=require("node:assert/strict");
const raw=require("../../../results/raw/arc/2026-10-30_1836_LSPV4_ARC_COUPLED_CHILD_BUDGET260_raw.json");
let tested=0;
const truthful=(lit,m)=>(Boolean(m&(1<<(Math.abs(lit)-1)))===(lit>0));
function signs(c,z){const m=new Map();for(let l of c){const v=z==="S"?(l>0):(l<0);if(m.has(Math.abs(l))&&m.get(Math.abs(l))!==v)return null;m.set(Math.abs(l),v)}return m}
for(const r of raw.formulas){
 let models=0,comp=0,pairs=0;
 for(let m=0;m<2**r.n;m++){let sat=true;for(const c of r.original_clauses){let a=0,b=0;for(let l of c){a+=Number(truthful(l,m));b+=Number(truthful(l,((1<<r.n)-1)^m))}assert.equal(a+b,c.length);if(a===0)sat=false;comp++}if(sat)models++}
 assert.equal(models,r.models);assert.equal(comp,r.complement_checks);
 for(const p of r.nontrivial_pair_compatibility)for(const mod of ["SS","SU","US","UU"]){let A=signs(r.original_clauses[p.j],mod[0]),B=signs(r.original_clauses[p.k],mod[1]);let compatible=A!==null&&B!==null;if(compatible)for(let [v,x] of A)if(B.has(v)&&B.get(v)!==x)compatible=false;assert.equal(compatible,p.modes[mod]);pairs++}
 // Also check all non-overlapping pairs produce no conflicts.
 let full=0;for(let i=0;i<r.m;i++)for(let j=i+1;j<r.m;j++)for(let mod of ["SS","SU","US","UU"]){const A=signs(r.original_clauses[i],mod[0]),B=signs(r.original_clauses[j],mod[1]);let compatible=A!==null&&B!==null;if(compatible)for(let [v,x] of A)if(B.has(v)&&B.get(v)!==x)compatible=false;const stored=r.nontrivial_pair_compatibility.find(p=>p.j===i&&p.k===j);if(stored)assert.equal(compatible,stored.modes[mod]);else assert.equal(compatible,true);full++}
 assert.equal(full,r.pair_mode_checks);
 for(const step of r.global_endpoints_and_partial_flip_trail){const cnt=r.original_clauses.map(c=>c.reduce((s,l)=>s+Number(truthful(l,step.assignment_bitmask)),0));assert.deepEqual(cnt,step.true_literal_counts);assert.deepEqual([0,1,2,3].map(k=>cnt.filter(x=>x===k).length),step.category_0_1_2_3)}
 assert.equal(r.baseline_DPLL.SAT,models>0);assert.equal(r.charged_two_child_DPLL.SAT,models>0);tested+=comp+full+1;
}
assert.equal(raw.flmv[0].best,"23/45");assert.equal(raw.flmv[1].best,"11642479/23232400");assert.equal(raw.flmv[0].k,2);assert.equal(raw.flmv[1].k,2);
assert.equal(raw.formulas[0].models,0);assert.equal(raw.formulas[1].models,168);
const H=raw.formulas.find(x=>x.name==="H1_SAT").original_clauses;assert.deepEqual(H[0],[1,3,5]);assert.deepEqual(H[1],[1,-3,6]);
for(let m=0;m<64;m++)if(!truthful(1,m)&&!truthful(5,m)&&!truthful(6,m))assert.equal(H.every(c=>c.some(l=>truthful(l,m))),false);
console.log(JSON.stringify({pass:true,checked_events:tested,sources:raw.formulas.length,models:raw.formulas.map(f=>[f.name,f.models])}));
