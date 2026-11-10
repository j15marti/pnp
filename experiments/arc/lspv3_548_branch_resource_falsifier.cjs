'use strict';
// LSPV-3/548. Independent finite controls. Declared CASE/LEAF test calculus.
// NOT native R_mix341 accepted bytes and NOT native FLMV machine measurement.
const assert=require('node:assert/strict');
const c=6/5, beta=((c+2)/(c*c)-c)/2, L=2*Math.cos(Math.PI/7);
assert(Math.abs(beta-23/45)<1e-12);
assert(Math.abs(beta-1/2-1/90)<1e-12);
assert(beta<11/20 && 11/20<L-c);
function valid(F,n){return Number.isSafeInteger(n)&&n>0&&Array.isArray(F)&&F.length>0&&F.every(cl=>Array.isArray(cl)&&cl.length>0&&cl.every(v=>Number.isSafeInteger(v)&&v!==0&&Math.abs(v)<=n)&&new Set(cl.map(Math.abs)).size===cl.length);}
function evalCNF(F,a){return F.every(cl=>cl.some(v=>v>0?a[v-1]===1:a[-v-1]===0));}
function build(F,n){if(!valid(F,n))throw Error('malformed');
 const rows=[],ctx=Array(n).fill(-1);
 function descend(){const x=ctx.indexOf(-1);
 if(x<0){const j=F.findIndex(cl=>cl.every(l=>l>0?ctx[l-1]===0:ctx[-l-1]===1));if(j<0)throw Error('SAT witness prevents UNSAT tree');const id=String(rows.length);rows.push({id,rule:'LEAF',ctx:[...ctx],source:j});return id;}
 ctx[x]=0;const a=descend();ctx[x]=1;const b=descend();ctx[x]=-1;
 const id=String(rows.length);rows.push({id,rule:'CASE',ctx:[...ctx],variable:x,parents:[a,b]});return id;
 }return{rows,root:descend()};}
function verify(F,n,p){if(!valid(F,n)||!p||!Array.isArray(p.rows))return false;const used=new Map();
 for(const row of p.rows){if(typeof row.id!=='string'||used.has(row.id)||!Array.isArray(row.ctx)||row.ctx.length!==n||!row.ctx.every(v=>[-1,0,1].includes(v)))return false;
 if(row.rule==='LEAF'){if(row.ctx.includes(-1)||!Number.isInteger(row.source)||row.source<0||row.source>=F.length||!F[row.source].every(v=>v>0?row.ctx[v-1]===0:row.ctx[-v-1]===1))return false;}
 else if(row.rule==='CASE'){if(!Number.isInteger(row.variable)||row.variable<0||row.variable>=n||row.ctx[row.variable]!==-1||!Array.isArray(row.parents)||row.parents.length!==2)return false;
 for(let b=0;b<2;b++){const child=used.get(row.parents[b]),expected=[...row.ctx];expected[row.variable]=b;if(!child||JSON.stringify(child.ctx)!==JSON.stringify(expected))return false;}}
 else return false;used.set(row.id,row);}
 return p.rows.length>0&&used.get(p.root)===p.rows[p.rows.length-1]&&p.rows[p.rows.length-1].ctx.every(v=>v===-1);}
const controls={};
for(const [label,F,n] of [['sat',[[1,2]],2],['unsat',[[1],[-1]],1],['other_sat',[[1,2],[-1,2]],2],['malformed',[[0]],1]]){
 if(!valid(F,n)){assert.equal(label,'malformed');controls[label]={malformed:true};continue;}
 let accepted=0;for(let i=0;i<2**n;i++)if(evalCNF(F,Array.from({length:n},(_,j)=>(i>>j)&1)))accepted++;
 controls[label]={acceptingBranches:accepted};
 if(accepted){assert.throws(()=>build(F,n));continue;}
 const p=build(F,n);assert(verify(F,n,p));controls[label].records=p.rows.length;controls[label].paid_CASE=p.rows.filter(r=>r.rule==='CASE').length;
 const wrong=structuredClone(p);wrong.rows[0].source=100;assert(!verify(F,n,wrong));
 const missing=structuredClone(p);missing.rows.at(-1).parents.pop();assert(!verify(F,n,missing));
 const swapped=structuredClone(p);swapped.rows.at(-1).parents.reverse();assert(!verify(F,n,swapped));
 const duplicate=structuredClone(p);duplicate.rows[1].id=duplicate.rows[0].id;assert(!verify(F,n,duplicate));
 const big=structuredClone(p),from=big.rows[0].id,to='987654321012345678909876543210';big.rows[0].id=to;for(const row of big.rows)if(row.parents)row.parents=row.parents.map(s=>s===from?to:s);assert(verify(F,n,big));
}
assert.equal(controls.sat.acceptingBranches,3);
assert.equal(controls.unsat.acceptingBranches,0);
assert.equal(controls.other_sat.acceptingBranches,2);
const out={status:'FINITE CONTROL ONLY',c,beta,threshold_zero_space_L:L,NOT_PROVED_positive_space_bound:L-c,s_between_beta_and_unproved_bound:11/20,controls,ratios:[6,12,24,60].map(k=>({N_power_of_ten:k,ratio:10**(k/90)}))};
console.log(JSON.stringify(out,null,2));
