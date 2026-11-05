#!/usr/bin/env node
/* LSPV3/413 independent strict-RES verifier.
 * Usage: node lspv3_413_independent_alias_verify.js lspv3_413_alias_raw.json
 * Full raw is in reproducibility archive; do not mistake this conditional
 * addressable-DEF-facet fragment for a native R_mix341 verifier. */
'use strict';
const fs=require('fs'),assert=require('assert');
const file=process.argv[2];if(!file)throw Error('requires full raw JSON path');
const raw=JSON.parse(fs.readFileSync(file,'utf8'));let checks=0,rejected=0;
function ok(v,m){assert.ok(v,m);checks++}
function equal(a,b,m){assert.deepStrictEqual(a,b,m);checks++}
function canon(xs){const s=new Set(xs);for(const x of s)if(s.has(-x))return null;return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||Number(b<0)-Number(a<0))}
function bit(op,a,b){return(op>>(2*a+b))&1}
function L(i,v){return v?i:-i}
function facets(g){let out=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++){const c=canon([-L(g.in1,a),-L(g.in2,b),L(g.out,bit(g.op,a,b))]);if(c&&!out.some(x=>JSON.stringify(x)===JSON.stringify(c)))out.push(c)}return out}
function test(c,mutate=true){
const {k,t,gates,steps,source_facets:src}=c;
ok(gates.length===t&&steps.length===c.strict_res_count,'counts');
const used=new Set(Array.from({length:k},(_,i)=>i+1));
for(const g of gates){
ok(Number.isInteger(g.out)&&g.out>k&&!used.has(g.out),'fresh output');
ok(used.has(g.in1)&&used.has(g.in2),'topological inputs');
ok(Number.isInteger(g.op)&&g.op>=0&&g.op<16,'gate truth table');used.add(g.out)}
const available=new Set(gates.flatMap(g=>facets(g).map(x=>JSON.stringify(x))));
for(const c0 of src){equal(c0,canon(c0),'normal source');ok(available.has(JSON.stringify(c0)),'genuine defining facet')}
function deref(r,n){ok(Array.isArray(r)&&r.length===2&&['s','r'].includes(r[0]),'reference syntax');ok(Number.isInteger(r[1])&&r[1]>=0&&r[1]<(r[0]==='s'?src.length:n),'reference ancestry');return r[0]==='s'?src[r[1]]:steps[r[1]].clause}
for(let j=0;j<steps.length;j++){
const st=steps[j],a=deref(st.a,j),b=deref(st.b,j),pivot=st.pivot;
ok(Number.isInteger(pivot)&&pivot>0,'pivot integer');
ok((a.includes(pivot)&&b.includes(-pivot))||(a.includes(-pivot)&&b.includes(pivot)),'complementary pivot');
const r=canon([...a.filter(x=>Math.abs(x)!==pivot),...b.filter(x=>Math.abs(x)!==pivot)]);
ok(r!==null,'no tautological resolvent');equal(st.clause,r,'strict resolvent')}
for(let mask=0;mask<(1<<k);mask++){
const val=new Map(Array.from({length:k},(_,j)=>[j+1,(mask>>j)&1]));
for(const g of gates)val.set(g.out,bit(g.op,val.get(g.in1),val.get(g.in2)));
ok(val.get(c.p)===val.get(c.q),'semantic equality');
for(const clause of src)ok(clause.some(x=>val.get(Math.abs(x))===(x>0?1:0)),'definition entailed');
for(const st of steps)ok(st.clause.some(x=>val.get(Math.abs(x))===(x>0?1:0)),'derived consequence entailed')}
for(const f of c.finals){const proof=deref(f.ref,steps.length);equal(proof,f.result,'root evidence');ok(proof.every(x=>f.goal.includes(x)),'target subclause')}
const bound=2*t*(1<<k)+2*((1<<k)-1);
ok(steps.length<=bound&&bound===c.additional_res_bound,'conditional upper bound');
if(mutate){const bad=JSON.parse(JSON.stringify(c));bad.steps[0].pivot=999;try{test(bad,false);throw Error('BAD accepted')}catch(e){ok(e instanceof assert.AssertionError,'bad pivot rejected');rejected++}}
}
for(const c of raw.cases)test(c);
equal(raw.cases.map(c=>c.strict_res_count),[10,22,54,126,286,638],'baseline exact trace sizes');
ok(raw.stats.negative_controls.changed_xor_rejected===true,'inequivalent function rejected');
ok(raw.stats.negative_controls.SAT_models===8&&raw.stats.negative_controls.UNSAT_models===0,'both labels');
process.stdout.write(JSON.stringify({status:'COMPUTATIONAL',fixtures:raw.cases.length,assertions:checks,corrupted_pivots_rejected:rejected,passed:true,full_native_R_mix341_verified:false})+'\n');
