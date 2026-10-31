"use strict";
// LSPV-1 ARC-ADAPTIVE-COFACTOR-MASS269 deterministic reproducibility program.
// Run: node 2026-10-31_0410_LSPV-1_ARC_ADAPTIVE_COFACTOR_MASS269_check.js > raw.json
// No dependencies, seed 2026103104; enumerations are exact for n<=5.
function requireTrue(p,msg){if(!p)throw new Error(msg);}
function parity(i){let k=0;while(i){k^=(i&1);i>>=1;}return k;}
function forbidden3(k){return [1,2,3].map((v,i)=>(k&(1<<i))?-v:v);}
function full3(exclude){const out=[];for(let i=0;i<8;i++)if(i!==exclude)out.push(forbidden3(i));return out;}
function xor3(bit){const out=[];for(let i=0;i<8;i++)if(parity(i)!==bit)out.push(forbidden3(i));return out;}
function rename(clauses){const perm=[3,1,2],flips=[-1,1,-1];return clauses.map(c=>c.map(l=>Math.sign(l)*flips[Math.abs(l)-1]*perm[Math.abs(l)-1]));}
function dense(){let z=2026103104>>>0;const next=()=>{z^=(z<<13);z^=(z>>>17);z^=(z<<5);return z>>>0;};const out=[];for(let j=0;j<12;j++){let vals=[1,2,3,4,5];for(let i=4;i>0;i--){const t=next()%(i+1);[vals[i],vals[t]]=[vals[t],vals[i]];}out.push(vals.slice(0,3).map(v=>(next()&1)?v:-v));}return out;}
function sourceSet(){return [
{id:"H7_SAT",n:3,clauses:full3(2)},
{id:"H8_UNSAT",n:3,clauses:full3(-1)},
{id:"OPPOSING_EXTREMES_SAT",n:3,clauses:[[1,2,3],[1,-2,-3]]},
{id:"XOR_EVEN_SAT",n:3,clauses:xor3(0)},
{id:"XOR_CONFLICT_UNSAT",n:3,clauses:xor3(0).concat(xor3(1))},
{id:"SIGNED_RENAME_SAT",n:3,clauses:rename(full3(2))},
{id:"HORN_SAT",n:4,clauses:[[-1,-2,3],[-3,-4,-2],[-1,-3,-4],[1,-2,-3]]},
{id:"DUAL_HORN_SAT",n:4,clauses:[[1,2,-3],[1,3,4],[-1,2,4],[2,3,-4]]},
{id:"KROM_2SAT",n:3,clauses:[[1,2],[-1,3],[-2,-3],[1,-3]]},
{id:"DENSE_SEEDED",n:5,clauses:dense()}
];}
function evalClause(c,arr){return c.reduce((s,l)=>s+((l>0?arr[Math.abs(l)-1]:1-arr[Math.abs(l)-1])===1?1:0),0);}
function assignment(a,n){return Array.from({length:n},(_,i)=>(a>>i)&1);}
function models(f){const out=[];for(let a=0;a<(1<<f.n);a++){const z=assignment(a,f.n);if(f.clauses.every(c=>evalClause(c,z)>0))out.push(a);}return out;}
function clauseProjection(c,rho){let sat=false,un=0;for(const l of c){const x=rho[Math.abs(l)-1];if(x===null)un++;else if((l>0?x:1-x)===1)sat=true;}return {sat,un};}
function sourceProfile(f,rho,acc){let remain=0,empty=0,unresolved=0;const survive=[];
  for(let j=0;j<f.clauses.length;j++){const c=f.clauses[j];if(acc){acc.source_clause_visits++;acc.source_literal_reads+=c.length;}
    const t=clauseProjection(c,rho);if(!t.sat){remain++;if(t.un===0)empty++;else unresolved++;survive.push({j:j+1,un:t.un});}}
  return {remain,empty,unresolved,survive};
}
function choose(f,rho,policy,acc){
  const u=[];for(let i=0;i<f.n;i++)if(rho[i]===null)u.push(i);
  requireTrue(u.length>0,"pivot impossible");
  if(policy==="fixed")return u[0];
  if(policy==="reverse")return u[u.length-1];
  const score=Array(f.n).fill(0);
  for(const c of f.clauses){const t=clauseProjection(c,rho);acc.policy_clause_visits++;acc.policy_literal_reads+=c.length;
    if(t.sat)continue;for(const l of c)if(rho[Math.abs(l)-1]===null)score[Math.abs(l)-1]++;}
  return u.reduce((p,i)=>score[i]>score[p]?i:p,u[0]);
}
function auditTree(f,policy,depthCap){
  const acc={source_clause_visits:0,source_literal_reads:0,policy_clause_visits:0,policy_literal_reads:0,internal_nodes:0};
  const leaves=[],rho=Array(f.n).fill(null);
  function rec(depth){
    const s=sourceProfile(f,rho,acc);const done=s.empty>0?"UNSAT_TERMINAL":s.remain===0?"SAT_TERMINAL":depth===depthCap?"UNRESOLVED_GUEST":null;
    if(done){let cube={};for(let i=0;i<f.n;i++)if(rho[i]!==null)cube["x"+(i+1)]=rho[i];
      leaves.push({cube,depth,terminal:done,remaining_original_clause_records:s.remain,empty_original_clauses:s.empty,unresolved_original_clauses:s.unresolved,source_surviving:s.survive});return;}
    acc.internal_nodes++;const x=choose(f,rho,policy,acc);
    rho[x]=0;rec(depth+1);rho[x]=1;rec(depth+1);rho[x]=null;
  }
  rec(0);
  const denominator=1<<f.n,originalFalseCount=f.clauses.reduce((a,c)=>a+(1<<(f.n-c.length)),0);
  let survivalNumerator=0,unresolvedSurplusNumerator=0;
  for(const l of leaves){const weight=1<<(f.n-l.depth);survivalNumerator+=weight*l.remaining_original_clause_records;
    for(const s of l.source_surviving)unresolvedSurplusNumerator+=weight-(weight>>s.un);
  }
  requireTrue(survivalNumerator===originalFalseCount+unresolvedSurplusNumerator,f.id+" weighted identity");
  requireTrue(survivalNumerator>=originalFalseCount,f.id+" lower bound");
  return {policy,depthCap,leaves,ledger:acc,weighted:{denominator,survivalNumerator,originalFalseCount,unresolvedSurplusNumerator,
    exact_identity:true,at_least_one_leaf_clause_floor:Math.max(...leaves.map(l=>l.remaining_original_clause_records))>=f.clauses.length/(1<<Math.max(...f.clauses.map(c=>c.length))) }};
}
function exhaustive(f,rho,acc){for(let a=0;a<(1<<f.n);a++){
  let coherent=true;for(let i=0;i<f.n;i++)if(rho[i]!==null&&rho[i]!==((a>>i)&1)){coherent=false;break;}
  if(!coherent)continue;acc.guest_assignment_tests++;
  const z=assignment(a,f.n);let ok=true;for(const c of f.clauses){acc.guest_clause_visits++;acc.guest_literal_reads+=c.length;if(evalClause(c,z)===0){ok=false;break;}}
  if(ok)return true;}return false;
}
function controller(f,policy,depthCap){
  const acc={source_clause_visits:0,source_literal_reads:0,policy_clause_visits:0,policy_literal_reads:0,
    guest_assignment_tests:0,guest_clause_visits:0,guest_literal_reads:0,decision_nodes:0,guests:0,rejected_branches:0};
  const rho=Array(f.n).fill(null);
  function rec(depth){acc.decision_nodes++;const s=sourceProfile(f,rho,acc);if(s.empty){acc.rejected_branches++;return false;}
    if(s.remain===0)return true;if(depth>=depthCap){acc.guests++;return exhaustive(f,rho,acc);}
    const x=choose(f,rho,policy,acc);rho[x]=0;if(rec(depth+1)){rho[x]=null;return true;}
    rho[x]=1;const ans=rec(depth+1);rho[x]=null;return ans;
  }
  const result=rec(0);acc.total_selected_operations=acc.source_literal_reads+acc.policy_literal_reads+acc.guest_literal_reads+acc.decision_nodes;
  return {result,ledger:acc};
}
function upDPLL(f){
  const acc={decision_nodes:0,clause_visits:0,literal_reads:0,unit_assignments:0};
  function rec(rho){acc.decision_nodes++;rho=rho.slice();while(true){
    let changed=false,allSat=true;
    for(const c of f.clauses){acc.clause_visits++;let sat=false,un=0,last=0;for(const l of c){acc.literal_reads++;
       const x=rho[Math.abs(l)-1];if(x===null){un++;last=l;}else if((l>0?x:1-x)===1){sat=true;break;}}
      if(sat)continue;allSat=false;if(un===0)return false;
      if(un===1){const v=Math.abs(last)-1,b=last>0?1:0;
        if(rho[v]!==null&&rho[v]!==b)return false;
        if(rho[v]===null){rho[v]=b;acc.unit_assignments++;changed=true;break;}}
    }
    if(allSat)return true;if(!changed)break;}
    const x=rho.findIndex(a=>a===null);if(x<0)return false;
    const lo=rho.slice();lo[x]=0;if(rec(lo))return true;const hi=rho.slice();hi[x]=1;return rec(hi);
  }
  const result=rec(Array(f.n).fill(null));acc.total_selected_operations=acc.literal_reads+acc.decision_nodes+acc.unit_assignments;
  return {result,ledger:acc};
}
function extremes(f,mods){
  const clauses=f.clauses.map((c,j)=>({clause_index:j+1,signed_occurrences:c.map(l=>{const isPos=l>0;
    return {occurrence:"x_"+Math.abs(l)+","+(j+1),literal:l,S_target:isPos?1:0,S_inverted_U:isPos?0:1,U_target:isPos?0:1,U_inverted_S:isPos?1:0};}),
    global_zero_true_count:evalClause(c,Array(f.n).fill(0)),global_one_true_count:evalClause(c,Array(f.n).fill(1))}));
  const pairs=[],tris=[];
  for(let i=0;i<f.clauses.length;i++)for(let j=i+1;j<f.clauses.length;j++){
    const matrix={},ci=f.clauses[i],cj=f.clauses[j];
    for(const p of ["SS","SU","US","UU"]){
      let targets={},valid=true;
      for(const [c,t] of [[ci,p[0]],[cj,p[1]]])for(const l of c){
        const v=Math.abs(l),want=((l>0)?1:0)^(t==="U"?1:0);if(targets[v]!==undefined&&targets[v]!==want)valid=false;targets[v]=want;}
      let observed=false;
      for(let a=0;a<(1<<f.n);a++){const z=assignment(a,f.n),need1=p[0]==="S"?ci.length:0,need2=p[1]==="S"?cj.length:0;
        if(evalClause(ci,z)===need1&&evalClause(cj,z)===need2){observed=true;break;}}
      requireTrue(valid===observed,f.id+" incompatible pair "+i+","+j+" "+p);matrix[p]=valid;
    }
    pairs.push({source_clause_indices:[i+1,j+1],matrix});
  }
  for(let i=0;i<f.clauses.length;i++)for(let j=i+1;j<f.clauses.length;j++)for(let k=j+1;k<f.clauses.length;k++){
    if(tris.length>=64)break;
    for(let mask=0;mask<8;mask++){const inds=[i,j,k];let targets={},valid=true;
      for(let h=0;h<3;h++)for(const l of f.clauses[inds[h]]){
        const want=((l>0)?1:0)^((mask>>h)&1),v=Math.abs(l);
        if(targets[v]!==undefined&&targets[v]!==want)valid=false;targets[v]=want;
      }
      let observed=false;for(let a=0;a<(1<<f.n);a++){const z=assignment(a,f.n);
        if(inds.every((idx,h)=>evalClause(f.clauses[idx],z)===((mask>>h)&1?0:f.clauses[idx].length))){observed=true;break;}}
      requireTrue(valid===observed,f.id+" triple extreme");tris.push({source_clause_indices:inds.map(v=>v+1),types:[0,1,2].map(h=>(mask>>h)&1?"U":"S").join(""),feasible:valid});
    }
  }
  const banned=[];
  for(let i=0;i<f.clauses.length;i++)for(let j=i+1;j<f.clauses.length;j++){
    for(const l of f.clauses[i])if(f.clauses[j].includes(-l)){
      const tmp=[...f.clauses[i].filter(a=>a!==l),...f.clauses[j].filter(a=>a!==-l)];
      if(tmp.some(a=>tmp.includes(-a)))continue;
      const derived=[...new Set(tmp)],cube=Object.fromEntries(derived.map(a=>["x"+Math.abs(a),a>0?0:1]));
      requireTrue(mods.every(a=>derived.some(l=>((l>0?1:0)===((a>>(Math.abs(l)-1))&1)))||Object.entries(cube).some(([v,x])=>((a>>(Number(v.slice(1))-1))&1)!==x)),f.id+" bad blocker");
      if(banned.length<64)banned.push({source_clause_indices:[i+1,j+1],pivot:Math.abs(l),derived_resolvent:derived,prohibited_cube:cube});
    }
  }
  const endpoints=[];
  for(const a of [0,(1<<f.n)-1]){const z=assignment(a,f.n),count=Array(4).fill(0);
    for(const c of f.clauses){const t=evalClause(c,z);count[t]++;}
    endpoints.push({bits:z,true_literal_histogram_0_to_3:count,formula_satisfied:count[0]===0});
  }
  const flipTrail=[],lim=Math.min(1<<f.n,8);for(let h=0;h<lim;h++){
    const a=h^(h>>1),complement=((1<<f.n)-1)^a,z=assignment(a,f.n),w=assignment(complement,f.n);
    const counts=f.clauses.map(c=>evalClause(c,z)),com=f.clauses.map(c=>evalClause(c,w));
    requireTrue(counts.every((v,i)=>v+com[i]===f.clauses[i].length),f.id+" complement");
    flipTrail.push({flip_step:h,assignment_bits:z,complement_bits:w,source_clause_true_counts:counts,complement_source_clause_true_counts:com});
  }
  // Complete partial/multi-flip identity, with 2^n * 2^n tested masks.
  let flip_checks=0;for(let a=0;a<(1<<f.n);a++)for(let mask=0;mask<(1<<f.n);mask++){
    const z=assignment(a,f.n),r=assignment(a^mask,f.n);
    for(const c of f.clauses){let predicted=evalClause(c,z);
      for(const lit of c)if(mask&(1<<(Math.abs(lit)-1)))predicted+=((lit>0?z[Math.abs(lit)-1]:1-z[Math.abs(lit)-1])===0)?1:-1;
      requireTrue(predicted===evalClause(c,r),f.id+" flip update");flip_checks++;
    }
  }
  return {clauses,pairs,triple_sample:tris,prohibited_cubes:banned,endpoints,flip_trail:flipTrail,checked_flip_clause_updates:flip_checks};
}
function runAll(){
  const rows=[],suite={seed:2026103104,mode:"fully_deterministic_exact_enumeration_n_le_5",source_encoding:"signed integer literal indexed original CNF",status:"COMPUTATIONAL; exact theorem supplied separately",rows:null};
  for(const f of sourceSet()){
    requireTrue(f.clauses.every(c=>new Set(c.map(x=>Math.abs(x))).size===c.length),"nonproper source "+f.id);
    const mod=models(f),expected=mod.length>0;
    const ext=extremes(f,mod),trees=[],d=Math.min(f.n,3);
    for(const policy of ["fixed","reverse","occurrence"])for(const depthCap of [1,d]){
       const tree=auditTree(f,policy,depthCap);
       requireTrue(tree.weighted.at_least_one_leaf_clause_floor,f.id+" bad leaf max");
       trees.push(tree);
    }
    const baseline=upDPLL(f),candidate=controller(f,"occurrence",d);
    requireTrue(baseline.result===expected&&candidate.result===expected,f.id+" SAT/UNSAT mismatch");
    rows.push({id:f.id,n:f.n,m:f.clauses.length,original_clauses:f.clauses,ground_truth_sat:expected,
      model_count:mod.length,satisfying_assignments:mod.map(a=>assignment(a,f.n)),original_clause_controls:ext,
      audit_trees:trees,standard_up_dpll:baseline,charged_adaptive_controller:candidate});
  }
  suite.rows=rows;
  suite.summary={sources:rows.length,sat:rows.filter(r=>r.ground_truth_sat).length,unsat:rows.filter(r=>!r.ground_truth_sat).length,
    tree_policies:rows.reduce((s,r)=>s+r.audit_trees.length,0),
    leaves_audited:rows.reduce((s,r)=>s+r.audit_trees.reduce((a,t)=>a+t.leaves.length,0),0),
    pair_modes_checked:rows.reduce((s,r)=>s+r.original_clause_controls.pairs.length*4,0),
    triple_modes_checked:rows.reduce((s,r)=>s+r.original_clause_controls.triple_sample.length,0),
    exact_flip_clause_updates:rows.reduce((s,r)=>s+r.original_clause_controls.checked_flip_clause_updates,0),
    original_signed_occurrences:rows.reduce((s,r)=>s+r.original_clauses.reduce((a,c)=>a+c.length,0),0),
    standard_nodes:rows.reduce((s,r)=>s+r.standard_up_dpll.ledger.decision_nodes,0),
    candidate_nodes:rows.reduce((s,r)=>s+r.charged_adaptive_controller.ledger.decision_nodes,0),
    standard_selected_work:rows.reduce((s,r)=>s+r.standard_up_dpll.ledger.total_selected_operations,0),
    candidate_selected_work:rows.reduce((s,r)=>s+r.charged_adaptive_controller.ledger.total_selected_operations,0)};
  return suite;
}
if(typeof process!=="undefined" && typeof require!=="undefined" && require.main===module){
  process.stdout.write(JSON.stringify(runAll(),null,2)+"\n");
}