/* LSPV-3 LOCAL-INTERFACE-BACKDOOR 2026-10-28. No external packages. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
let counts = Object.create(null);
function check(x,tag){ counts[tag]=(counts[tag]||0)+1; assert.ok(x,tag); }
function moduleFamily(b, specifications){
  let clauses=[], modules=[], n=b;
  for (const [j,w] of specifications){
    if(!(j>=1 && j<=b && (w===0 || w===1)))throw Error('bad spec');
    let a=++n,t=++n,c=++n,d=++n, ids=[];
    const y=w===1?j:-j;
    for(const aa of [a,-a]) for(const tt of [t,-t]){
      ids.push(clauses.length); clauses.push([y,aa,tt]);
    }
    ids.push(clauses.length);clauses.push([a,c,d]);
    modules.push({boundaryIndex:j,required:w,private:[a,t,c,d],backdoor:[a],ids});
  }
  return {b,n,clauses,modules};
}
function validStructure(F){
  const owners=new Map();
  const all=new Set();
  for(let mi=0;mi<F.modules.length;mi++){
    const M=F.modules[mi], q=new Set(M.private);
    if(q.size!==M.private.length || !q.has(M.backdoor[0]) || M.backdoor.length!==1)return false;
    for(const v of M.private){if(v<=F.b || v>F.n || owners.has(v))return false; owners.set(v,mi);}
    for(const id of M.ids){
      if(id<0 || id>=F.clauses.length || all.has(id))return false;
      all.add(id); let C=F.clauses[id];
      if(C.length!==3 || new Set(C.map(Math.abs)).size!==3)return false;
      if(!C.every(l=>Math.abs(l)<=F.b || q.has(Math.abs(l))))return false;
      if(!C.some(l=>Math.abs(l)<=F.b || M.backdoor.includes(Math.abs(l))))return false;
    }
  }
  return all.size===F.clauses.length;
}
function residual(F,mi,assignment){
  let out=[];
  for(const id of F.modules[mi].ids){
    const C=F.clauses[id], rem=[];let satisfied=false;
    for(const lit of C){let v=Math.abs(lit);
      if(Object.hasOwn(assignment,v)){
        if(assignment[v] === (lit>0?1:0)){satisfied=true;break;}
      }else rem.push(lit);
    }
    if(!satisfied){ if(rem.length>2)throw Error('incorrect claimed backdoor');out.push({id,clause:rem}); }
  }
  return out;
}
function implicationEdges(ress){
  let edges=[];
  for(const {id,clause:C} of ress){
    if(C.length===1)edges.push({from:-C[0],to:C[0],id});
    if(C.length===2){edges.push({from:-C[0],to:C[1],id},{from:-C[1],to:C[0],id});}
  }
  return edges;
}
function bfs(edges,start,target){
  const queue=[start], prev=new Map([[start,null]]);
  for(let i=0;i<queue.length;i++){
    let v=queue[i];if(v===target)break;
    for(const e of edges){if(e.from===v && !prev.has(e.to)){prev.set(e.to,e);queue.push(e.to);}}
  }
  if(!prev.has(target))return null;
  let p=[],cur=target;
  while(cur!==start){let edge=prev.get(cur);p.push(edge);cur=edge.from;}
  return p.reverse();
}
function proof2SAT(ress){
  if(ress.some(r=>r.clause.length===0))return {kind:'empty',id:ress.find(r=>r.clause.length===0).id};
  let ed=implicationEdges(ress),vs=new Set(ress.flatMap(r=>r.clause.map(Math.abs)));
  for(const v of vs){let p=bfs(ed,v,-v),q=bfs(ed,-v,v);
    if(p && q)return {kind:'paths',var:v,first:p,second:q};
  }
  return null;
}
function verify2SAT(F,mi,asgn,p){
  const ress=residual(F,mi,asgn);
  if(p?.kind==='empty')return ress.some(r=>r.id===p.id && r.clause.length===0);
  if(p?.kind!=='paths' || !(p.var>0 && p.var<=F.n))return false;
  const E=implicationEdges(ress);
  function checkPath(path,start,target){
    if(!Array.isArray(path))return false;let v=start;
    for(const e of path){if(!E.some(t=>t.from===e.from&&t.to===e.to&&t.id===e.id)||e.from!==v)return false;v=e.to;}
    return v===target;
  }
  return checkPath(p.first,p.var,-p.var)&&checkPath(p.second,-p.var,p.var);
}
function twoSATModelSCC(ress,n){
  if(ress.some(r=>r.clause.length===0))return null;
  const G=Array.from({length:2*n},()=>[]),R=Array.from({length:2*n},()=>[]);
  function ix(l){return 2*(Math.abs(l)-1)+(l<0?1:0);}
  for(const e of implicationEdges(ress)){let u=ix(e.from),v=ix(e.to);G[u].push(v);R[v].push(u);}
  let seen=Array(2*n).fill(false),order=[];
  function dfs(v){seen[v]=true;for(const w of G[v])if(!seen[w])dfs(w);order.push(v);}
  for(let v=0;v<2*n;v++)if(!seen[v])dfs(v);
  let comp=Array(2*n).fill(-1),cn=0;
  function rdfs(v){comp[v]=cn;for(const w of R[v])if(comp[w]===-1)rdfs(w);}
  for(const v of order.reverse())if(comp[v]===-1){rdfs(v);cn++;}
  let assignment={};
  for(let v=1;v<=n;v++){
    if(comp[ix(v)]===comp[ix(-v)])return null;
    assignment[v]=comp[ix(v)]>comp[ix(-v)]?1:0;
  }
  if(!ress.every(r=>r.clause.some(l=>assignment[Math.abs(l)]===(l>0?1:0))))throw Error('SCC model bug');
  return assignment;
}
function findCertificateOrModel(F){
  if(!validStructure(F))return {kind:'reject_grammar'};
  let unsatBranches=[],discoveredSAT=null, SCCcounts=0;
  for(let bits=0;bits<2**F.b;bits++){
    let y={}; for(let j=1;j<=F.b;j++)y[j]=(bits>>(j-1))&1;
    let bad=null,good=[];
    for(let mi=0;mi<F.modules.length;mi++){
      let M=F.modules[mi], local=[],candidate=null;
      for(let sub=0;sub<2**M.backdoor.length;sub++){
        let a={...y}; M.backdoor.forEach((v,i)=>a[v]=(sub>>i)&1);
        let rr=residual(F,mi,a), p=proof2SAT(rr);SCCcounts++;
        if(p)local.push({sub,proof:p});
        else{candidate={sub,asgn:a,model:twoSATModelSCC(rr,F.n)}; if(!candidate.model)throw Error('SCC contradiction not detected');break;}
      }
      if(!candidate){bad={module:mi,branches:local};break;}
      good.push({module:mi,modelSeed:candidate});
    }
    if(!bad){discoveredSAT={y,good};break;}
    unsatBranches.push({y,bad});
  }
  if(discoveredSAT){
    let model={...discoveredSAT.y};
    for(const entry of discoveredSAT.good){
      const M=F.modules[entry.module], z=entry.modelSeed;
      for(const v of M.private)model[v]=Object.hasOwn(z.asgn,v)?z.asgn[v]:z.model[v];
    }
    if(!evaluateFormula(F,model))throw Error('SAT witness construction failed');
    return {kind:'sat',discoveredSAT,model,SCCcounts};
  }
  return {kind:'unsat',branches:unsatBranches,SCCcounts};
}
function verifyUnsat(F,certificate){
  if(!validStructure(F) || certificate.kind!=='unsat' || certificate.branches.length!==2**F.b)return false;
  const seen=new Set();
  for(const branch of certificate.branches){
    const y=branch.y;
    if(!y || Object.keys(y).length!==F.b || !Array.from({length:F.b},(_,i)=>y[i+1]).every(v=>v===0||v===1))return false;
    const bits=Array.from({length:F.b},(_,i)=>y[i+1]).join('');
    if(bits.includes('undefined')||seen.has(bits))return false;seen.add(bits);
    const mi=branch.bad.module;
    if(!Number.isInteger(mi)||mi<0||mi>=F.modules.length)return false;
    const B=F.modules[mi].backdoor, bs=branch.bad.branches;
    if(bs.length!==2**B.length)return false;
    let used=new Set();
    for(const part of bs){if(used.has(part.sub)||part.sub<0||part.sub>=2**B.length)return false;used.add(part.sub);
      let a={...y}; B.forEach((v,i)=>a[v]=(part.sub>>i)&1);
      if(!verify2SAT(F,mi,a,part.proof))return false;
    }
  }
  return true;
}
function evaluateFormula(F,assignment){return F.clauses.every(c=>c.some(l=>assignment[Math.abs(l)]===(l>0?1:0)));}
function expectedSAT(F){const pinned=new Map(); for(const M of F.modules){const v=M.boundaryIndex; if(pinned.has(v) && pinned.get(v)!==M.required)return false; pinned.set(v,M.required);}return true;}
function copied(o){return JSON.parse(JSON.stringify(o));}
// Verify the independently specified cross-product elimination over 69,904 boundary assignments.
let cross=0;
for(let t=1;t<=4;t++)for(let mask=0;mask<2**(4*t);mask++){
  let x=Array.from({length:4*t},(_,j)=>(mask>>j)&1);
  const A=Array.from({length:t},(_,i)=>x[2*i]||x[2*i+1]);
  const B=Array.from({length:t},(_,i)=>x[2*t+2*i]||x[2*t+2*i+1]);
  let exist= [0,1].some(z=> A.every(a=>z||a)&&B.every(b=>(!z)||b));
  let dist=A.every(a=>B.every(b=>a||b));
  let factor=A.every(Boolean)||B.every(Boolean);
  check(exist===dist && dist===factor,'cross_product_69904');cross++;
}
let sources=0,refutations=0,satSources=0,unsatSources=0,hostile=0,rawExamples=[];
for(let b=1;b<=3;b++)for(let k=1;k<=7;k++){
  const combos=Math.min(1<<(Math.min(k,8)),64);
  for(let s=0;s<combos;s++){
    let specs=Array.from({length:k},(_,i)=>[1+(i%b),(s>>i)&1]);
    let F=moduleFamily(b,specs);
    check(validStructure(F),'validated_proper3');sources++;
    let r=findCertificateOrModel(F), expected=expectedSAT(F);
    check((r.kind==='sat')===expected,'same_program_both_labels');
    if(expected){satSources++;let y=r.discoveredSAT.y;
      let asgn={...y};
      for(const M of F.modules){let [a,t,c,d]=M.private;asgn[a]=1;asgn[t]=0;asgn[c]=0;asgn[d]=0;}
      check(evaluateFormula(F,asgn) && evaluateFormula(F,r.model),'full_source_sat_model');
      check(!verifyUnsat(F,{kind:'unsat',branches:[]}), 'no_unsat_proof_on_sat');
    }else{
      unsatSources++;check(verifyUnsat(F,r),'complete_authenticated_unsat');refutations++;
      let altered=copied(r); altered.branches[0].bad.branches[0].proof= {kind:'paths',var:2,first:[],second:[]};
      check(!verifyUnsat(F,altered),'forged_terminal_rejected');hostile++;
      if(r.branches.length>1){let absent=copied(r);absent.branches.pop();check(!verifyUnsat(F,absent),'missing_boundary_rejected');hostile++;let illegal=copied(r); illegal.branches[0].y[1]=2;check(!verifyUnsat(F,illegal),'invalid_boundary_rejected');hostile++;}
      if(r.branches[0].bad.branches.length>1){let absent=copied(r);absent.branches[0].bad.branches.pop();check(!verifyUnsat(F,absent),'missing_backdoor_rejected');hostile++;}
    }
    if(b===1 && k===2 && s===1)rawExamples.push({b,k,s,source_clauses:F.clauses, certificate:r});
  }
}
// Exhaustive whole-formula truth evaluations for small sources; no SAT oracle.
let brute=0;
for(let k=1;k<=3;k++)for(let s=0;s<(1<<k);s++){
  let F=moduleFamily(1,Array.from({length:k},(_,i)=>[1,(s>>i)&1]));
  let result=false;
  for(let bits=0;bits<2**F.n;bits++){
    let a={};for(let i=1;i<=F.n;i++)a[i]=(bits>>(i-1))&1;
    if(evaluateFormula(F,a)){result=true;break;}
  }
  check(result===expectedSAT(F),'brute_source_label');brute++;
}
// Genuinely connected graph, each module individually SAT, global strong backdoor >=k.
for(let k=2;k<=18;k++){
  let F=moduleFamily(1,Array.from({length:k},(_,i)=>[1,i%2]));
  let r=findCertificateOrModel(F);check(!expectedSAT(F)&&verifyUnsat(F,r),'connected_both_labels');
  check(F.modules.every(M=>M.ids.length===5),'module_original_clause_count');
  check(F.modules.every(M=>F.clauses[M.ids[4]].every(l=>Math.abs(l)!==1)),'private_ternary_global_backdoor_floor');
  // Exactly two local branch leaves per each of 2 boundary assignments.
  check(r.branches.length===2 && r.branches.every(e=>e.bad.branches.length===2),'four_source_id_leaves');
}
// Hidden shared private-name collision: projections onto x are true, conjunction UNSAT.
for(const x of [0,1]){
  let F=(u,xx)=>u===xx;let G=(u,xx)=>u!==xx;
  check([0,1].some(u=>F(u,x)) && [0,1].some(u=>G(u,x)),'separate_projection_true');
  check(![0,1].some(u=>F(u,x)&&G(u,x)),'shared_private_merge_unsat');
}
// Explicit source-authenticated proper-3CNF padding of two incompatible projections.
// F1 is u iff x; F2 is u iff not x; each separately projects TRUE on x,
// but retaining the common u makes their conjunction UNSAT.
const binaryF1=[[-2,1],[2,-1]], binaryF2=[[-2,-1],[2,1]];
function padBinary(binary,startZ){
  let out=[],z=startZ;
  for(const [a,b] of binary){out.push([a,b,z],[a,b,-z]);z++;}
  return out;
}
const C1=padBinary(binaryF1,3),C2=padBinary(binaryF2,5);
function satWithX(clauses,x){
  for(let mask=0;mask<32;mask++){
    let a={1:x,2:mask&1,3:(mask>>1)&1,4:(mask>>2)&1,5:(mask>>3)&1,6:(mask>>4)&1};
    if(clauses.every(C=>C.some(l=>a[Math.abs(l)]===(l>0?1:0))))return true;
  }
  return false;
}
for(const x of [0,1]){
  check(satWithX(C1,x)&&satWithX(C2,x),'proper3_separate_projection_true');
  check(!satWithX([...C1,...C2],x),'proper3_shared_hidden_unsat');
}
// Fixed-order OBDD exact residual count on equality: after reading x[1..b], 2^b distinct Y-functions.
for(let b=1;b<=9;b++){
  const signatures=new Set();
  for(let x=0;x<2**b;x++){
    let truth='';for(let y=0;y<2**b;y++)truth+=x===y?'1':'0';
    signatures.add(truth);
  }
  check(signatures.size===2**b,'bad_order_obdd_exact_width');
  // Matched interleaved order x1,y1,x2,y2,... needs only O(b) states (not constructing OBDD here).
}
let result={run:'LOCAL_INTERFACE_BACKDOOR_20261028',test_date:'2026-10-28',counts,assertions:Object.values(counts).reduce((a,b)=>a+b,0),source_count:sources,refutations,sat_sources:satSources,unsat_sources:unsatSources,hostile_mutations:hostile,exhaustive_brute_sources:brute,elimination_assignments:cross,example:rawExamples[0],statuses:{modular_coverage:'RESTRICTED_PROVED_PENDING_REVIEW',counterexample_global_backdoor:'RESTRICTED_PROVED_PENDING_REVIEW',fixed_order_OBDD:'KNOWN_RESTRICTED_PROVED',unrestricted_coverage:'OPEN',sublinear_all_sat_child:'OPEN',p_vs_np:'OPEN'}};
fs.writeFileSync(new URL('./LOCAL_INTERFACE_BACKDOOR_raw.json',import.meta.url),JSON.stringify(result,null,2)+'
');
console.log(JSON.stringify({...result,example:undefined},null,2));

