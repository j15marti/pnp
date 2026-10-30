"use strict";
/* Independent Node.js referee: fixed seed original W1 source, source-indexed
   signed targets and inversions, full 4-way matrix, 32768 assignments per
   matched signing, exact source-parent RUP cubes and recursively replayed
   original-source DPLL contradiction trees. Requires ONLY node stdlib. */
const fs=require('fs'),assert=require('assert');
const W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'.split(';').map(c=>c.trim().split(' ').map(Number));
const TWIN=W1.map((c,j)=>c.map(l=>((j===9||j===13)&&Math.abs(l)===6)?-l:l));
const H1=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]];
function countTrue(c,mask){return c.filter(l=>((mask>>(Math.abs(l)-1))&1)===(l>0?1:0)).length;}
function N(f,mask){let out=[0,0,0,0];for(const c of f)out[countTrue(c,mask)]++;return out;}
function incidence(f){return f.map(c=>c.map(Math.abs).sort((a,b)=>a-b).join(','));}
function occurrence(f){const c=new Map();for(const clause of f)for(const l of clause)c.set(l,(c.get(l)||0)+1);return c;}
function modes(a,b){let same=[],opp=[];for(const l of a)for(const k of b){if(Math.abs(l)===Math.abs(k))(Math.sign(l)===Math.sign(k)?same:opp).push(Math.abs(l));}
return {SS:opp.length===0,SU:same.length===0,US:same.length===0,UU:opp.length===0,same:same.length,opposite:opp.length};}
function histogram(f){const h={};for(let j=0;j<f.length;j++)for(let k=j+1;k<f.length;k++){const z=modes(f[j],f[k]);const key=`same_${z.same}_opposite_${z.opposite}`;h[key]=(h[key]||0)+1;}return h;}
function assertRUPCube(f,certificate){const {parents,pivot,non_tautological_resolvent:R,forbidden_partial_cube:cube}=certificate;
const a=f[parents[0]],b=f[parents[1]];assert(a.includes(pivot)&&b.includes(-pivot));
const rhs=new Set([...a.filter(x=>x!==pivot),...b.filter(x=>x!==-pivot)]);assert.deepStrictEqual(new Set(R),rhs);
for(const x of rhs)assert(!rhs.has(-x));
const p={};for(const [v,q] of Object.entries(cube))p[Number(v)]=q;
for(const l of R)assert.strictEqual(p[Math.abs(l)],l>0?0:1);
assert(a.every(l=>l===pivot||p[Math.abs(l)]===(l>0?0:1)));
assert(b.every(l=>l===-pivot||p[Math.abs(l)]===(l>0?0:1)));
}
function checkProof(f,node,state,counts){const s={...state};
for(const u of node.up){assert(s[u.v]===undefined);const C=f[u.j];assert(C.includes(u.value?u.v:-u.v));
 for(const l of C)if(Math.abs(l)!==u.v)assert.strictEqual(s[Math.abs(l)],l>0?0:1);
 s[u.v]=u.value;counts.unit++;}
if(node.conflict_clause!==undefined){const C=f[node.conflict_clause];
 for(const l of C)assert.strictEqual(s[Math.abs(l)],l>0?0:1);
 counts.leaf++;return false;}
if(node.witness!==undefined){assert(f.every(c=>countTrue(c,node.witness)>0));counts.witness++;return true;}
const v=node.branch_var;assert(s[v]===undefined);assert.deepStrictEqual(node.children.map(x=>x.value),[0,1]);
let r=[];for(const c of node.children)r.push(checkProof(f,c.proof,{...s,[v]:c.value},counts));
counts.branch++;assert(r.every(x=>!x));return false;}
function verifyCase(f,caseData){assert.strictEqual(caseData.m,f.length);assert.deepStrictEqual(caseData.original_signed_clauses,f);
assert.strictEqual(caseData.all_signed_original_occurrences_local_S_U_and_inversions.length,f.length);
for(let j=0;j<f.length;j++){
 const got=caseData.all_signed_original_occurrences_local_S_U_and_inversions[j];
 assert.strictEqual(got.original_clause_j,j);
 for(let k=0;k<f[j].length;k++){
  let l=f[j][k],o=got.occurrences[k];let expectS=l>0?1:0,expectU=1-expectS;
  assert.strictEqual(o.original_variable,Math.abs(l));assert.strictEqual(o.signed_literal,l);
  assert.strictEqual(o.S_literal_TRUE_target_x,expectS);
  assert.strictEqual(o.invert_S_literal_FALSE_target_x,expectU);
  assert.strictEqual(o.U_literal_FALSE_target_x,expectU);
  assert.strictEqual(o.invert_U_literal_TRUE_target_x,expectS);
 }}
let k=0;for(let j=0;j<f.length;j++)for(let h=j+1;h<f.length;h++){
 const actual=caseData.source_clause_pair_extreme_matrix[k++];const mm=modes(f[j],f[h]);
 assert.deepStrictEqual(actual.source_clause_pair,[j,h]);
 for(const m of ['SS','SU','US','UU'])assert.strictEqual(actual.all_literal_extreme_compatibility[m],mm[m]);}
assert.deepStrictEqual(N(f,0),caseData.globally_coherent_endpoints.all_zero.N0_N1_N2_N3);
assert.deepStrictEqual(N(f,(1<<caseData.n)-1),caseData.globally_coherent_endpoints.all_one.N0_N1_N2_N3);
for(const R of caseData.sample_proved_forbidden_partial_cubes)assertRUPCube(f,R);
for(const w of caseData.uniform_walks){for(const t of w.trail){assert.deepStrictEqual(N(f,t.global_assignment_mask),t.N0_N1_N2_N3);assert.deepStrictEqual(f.map(c=>countTrue(c,t.global_assignment_mask)),t.clause_t);}}
if(caseData.solver_compare.baseline.SAT===false){let counts={unit:0,leaf:0,branch:0,witness:0};
  assert.strictEqual(checkProof(f,caseData.solver_compare.baseline.source_authenticated_DPLL_certificate,{},counts),false);
  assert(counts.leaf>0);return counts;}return null;}
function main(){const p=process.argv[2];if(!p)throw new Error('Pass raw JSON path');const raw=JSON.parse(fs.readFileSync(p,'utf8'));
const a=raw.cases.find(x=>x.name==='W1_strict22_UNSAT');const b=raw.cases.find(x=>x.name==='SWAP6_strict22_SAT');const h=raw.cases.find(x=>x.name==='H1_plateau_strict22_SAT');
assert.deepStrictEqual(incidence(W1),incidence(TWIN));
for(let v=1;v<=15;v++){assert.strictEqual(occurrence(W1).get(v),2);assert.strictEqual(occurrence(W1).get(-v),2);assert.strictEqual(occurrence(TWIN).get(v),2);assert.strictEqual(occurrence(TWIN).get(-v),2);}
assert.deepStrictEqual(N(W1,0),[1,10,7,2]);assert.deepStrictEqual(N(TWIN,0),[1,10,7,2]);
assert.deepStrictEqual(N(W1,32767),[2,7,10,1]);assert.deepStrictEqual(N(TWIN,32767),[2,7,10,1]);
assert.deepStrictEqual(histogram(W1),histogram(TWIN));
let statuses=[0,0];for(let mask=0;mask<32768;mask++){
  if(W1.every(c=>countTrue(c,mask)>0))statuses[0]++;
  if(TWIN.every(c=>countTrue(c,mask)>0))statuses[1]++;
  if(mask<64){assert(N(H1,mask).reduce((x,y)=>x+y,0)===8);}
  if(mask===19186)assert(TWIN.every(c=>countTrue(c,mask)>0));
}
assert.strictEqual(statuses[0],0);assert(statuses[1]>0);
const checkW1=verifyCase(W1,a),checkTWIN=verifyCase(TWIN,b),checkH1=verifyCase(H1,h);
assert.strictEqual(checkTWIN,null);assert.strictEqual(checkH1,null);
assert.deepStrictEqual(a.pair_mode_signature_histogram,histogram(W1));assert.deepStrictEqual(b.pair_mode_signature_histogram,histogram(TWIN));
let full_modes_different=0;for(let i=0;i<a.source_clause_pair_extreme_matrix.length;i++){
const A=a.source_clause_pair_extreme_matrix[i].all_literal_extreme_compatibility,B=b.source_clause_pair_extreme_matrix[i].all_literal_extreme_compatibility;
if(['SS','SU','US','UU'].some(k=>A[k]!==B[k]))full_modes_different++;}
assert(full_modes_different>0);
console.log(JSON.stringify({result:'PASS',checked_W1_masks:32768,checked_twin_masks:32768,
  W1_SAT_models:statuses[0],twin_SAT_models:statuses[1],original_signed_occurrences_checked:W1.length*3*2+H1.length*3,
  paired_source_mode_entries_checked:(20*19/2)*2+8*7/2,
  source_W1_refutation:checkW1,full_indexed_mode_pairs_differ:full_modes_different,
  matched_aggregate_pair_distribution:histogram(W1),matched_endpoint_zero:N(W1,0),matched_endpoint_one:N(W1,32767)}));}
main();
