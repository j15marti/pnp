#!/usr/bin/env node
"use strict";
/* Independent standard-Node exact checker. Reads the published raw JSON,
   recomputes S/U modes by coherent truth assignments, complement identities,
   true SAT model counts, the bounded-middle property, and full DPLL UNSAT leaves.
   No code from the Python producer is imported. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const filename=process.argv[2]||'LSPV4_NEAR_FULL_TRUE_FPT249_raw.json';
const raw=JSON.parse(fs.readFileSync(filename,'utf8'));
const counted={pair_modes:0,assignment_complements:0,certificate_checks:0,parameter_cases:0,source_occurrences:0};
function isTrue(l,a){return Boolean((a>>>(Math.abs(l)-1))&1)===(l>0)}
function truth(c,a){return c.filter(l=>isTrue(l,a)).length}
function matrix(c,d){
  let vs=[...new Set([...c,...d].map(Math.abs))], M={SS:false,SU:false,US:false,UU:false};
  for(let b=0;b<(1<<vs.length);b++){
    let a=0;for(let i=0;i<vs.length;i++)if((b>>>i)&1)a|=(1<<(vs[i]-1));
    const x=truth(c,a), y=truth(d,a);
    if((x===0||x===3)&&(y===0||y===3))M[(x===3?'S':'U')+(y===3?'S':'U')]=true;
  }
  return M;
}
function upContradiction(F,pins){
 const a={...pins};
 while(true){
  let changed=false;
  for(const c of F){
   if(c.some(l=>Object.hasOwn(a,Math.abs(l))&&a[Math.abs(l)]===(l>0?1:0)))continue;
   let free=c.filter(l=>!Object.hasOwn(a,Math.abs(l)));
   if(free.length===0)return true;
   if(free.length===1){let l=free[0],v=Math.abs(l),z=l>0?1:0;
     if(Object.hasOwn(a,v)&&a[v]!==z)return true;
     if(!Object.hasOwn(a,v)){a[v]=z;changed=true;}}
  }
  if(!changed)return false;
 }
}
for(const [label,c] of Object.entries(raw.cases)){
 const F=c.original_source,n=c.n,m=F.length;
 assert.equal(m,c.m);
 for(let j=0;j<m;j++){
  assert.equal(c.signed_occurrence_targets[j].clause,j);
  assert.equal(c.signed_occurrence_targets[j].occurrences.length,3);
  for(let z=0;z<3;z++){
   let l=F[j][z],r=c.signed_occurrence_targets[j].occurrences[z];
   assert.equal(r.literal,l);assert.equal(r.var,Math.abs(l));
   assert.equal(r.S_target,Number(l>0));assert.equal(r.U_target,Number(l<0));
   assert.equal(r.S_inverted_to_U,r.U_target);assert.equal(r.U_inverted_to_S,r.S_target);
   counted.source_occurrences++;
  }
 }
 const edges=[];
 for(const p of c.original_clause_pair_compatibility){
  let [j,k]=p.source_clause_pair;
  let same=F[j].filter(x=>F[k].includes(x)).map(Math.abs).sort((a,b)=>a-b);
  let opp=F[j].filter(x=>F[k].includes(-x)).map(Math.abs).sort((a,b)=>a-b);
  assert.deepEqual(p.same_sign_vars,same);assert.deepEqual(p.opposite_sign_vars,opp);
  assert.deepEqual(p.modes,matrix(F[j],F[k]));
  if(opp.length)edges.push([j,k]);counted.pair_modes+=4;
 }
 assert.deepEqual(edges,c.source_opposite_sign_conflict_graph_edges);
 let modelCount=0,minMiddle=null;
 for(let a=0;a<(1<<n);a++){
  const cnt=[0,0,0,0];for(const clause of F)cnt[truth(clause,a)]++;
  const bc=[0,0,0,0];let comp=((1<<n)-1)^a;
  for(const clause of F)bc[truth(clause,comp)]++;
  assert.deepEqual(cnt,bc.toReversed());counted.assignment_complements++;
  if(cnt[0]===0){modelCount++;const middle=cnt[1]+cnt[2];
   if(minMiddle===null||middle<minMiddle)minMiddle=middle;
   // For EVERY SAT witness, all S clauses must be an independent set in H.
   for(const [u,v] of edges){assert(!(truth(F[u],a)===3&&truth(F[v],a)===3));}
  }
 }
 assert.equal(modelCount,c.independent_exact_models);
 assert.equal(minMiddle,c.exact_min_middle_in_any_SAT_model);
 if(c.strict22&&modelCount)assert(4*minMiddle>=3*m);
 for(const q of c.bounded_middle_controllers){
  assert.equal(q.within_budget_SAT,(minMiddle!==null && minMiddle<=q.budget));
  if(q.within_budget_SAT){const z=q.SAT_witness;
   assert(F.every(x=>truth(x,z)>0));
   assert(F.filter(x=>{let t=truth(x,z);return t===1||t===2}).length<=q.budget);}
  counted.parameter_cases++;
 }
 if(c.parent_resolvent_forbidden_cube){const r=c.parent_resolvent_forbidden_cube;
  const [p,q]=r.source_parent_clause_indices;
  const v=r.pivot_original_var;
  assert(F[p].some(x=>Math.abs(x)===v)&&F[q].some(x=>Math.abs(x)===v));
  for(let a=0;a<(1<<n);a++){
    if(Object.entries(r.forbidden_original_variable_cube).every(([v,z])=>((a>>>(Number(v)-1))&1)===z)){
      assert(!(truth(F[p],a)>0&&truth(F[q],a)>0));
    }
  }
  counted.certificate_checks++;
 }
 if(c.dpll.answer==='UNSAT'){
   const paths=c.dpll.proof_leaves.map(x=>x.branch_decisions);
   assert.equal(paths.length,c.dpll.complete_leaf_count);
   const keys=new Set(paths.map(x=>JSON.stringify(x)));assert.equal(keys.size,paths.length);
   for(const path of paths){
    let pins={};path.forEach(([v,z])=>pins[v]=z);
    assert(upContradiction(F,pins));
    for(let i=0;i<path.length;i++){
      const other=path.slice(0,i);other.push([path[i][0],1-path[i][1]]);
      assert(paths.some(x=>other.every((y,t)=>JSON.stringify(x[t])===JSON.stringify(y))));
    }
   }
   counted.certificate_checks+=paths.length;
 }else assert(F.every(x=>truth(x,c.dpll.model)>0));
 console.log(label,'SAT_models',modelCount,'min_middle',minMiddle,'source_pairs',m*(m-1)/2);
}
assert.equal(counted.pair_modes,raw.assertions.source_pair_modes_checked);
assert.equal(counted.assignment_complements,raw.assertions.complement_complete_states_checked);
console.log(JSON.stringify({result:'PASS',cases:Object.keys(raw.cases).length,assertions:counted,scope:'finite exact controls; no unrestricted SAT complexity claim'}));