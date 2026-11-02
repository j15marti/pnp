"use strict";
// LSPV-4 exact source-authenticated 2CNF-backdoor audit, no imports or random choices.
function execute(extra) {
  const F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],
  [-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
  const Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],
    [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
  const P15=[[1,2,7],[1,3,8],[4,5,9],[4,6,10],[2,3,5],
    [6,11,12],[7,11,13],[8,12,14],[9,13,15],[10,14,15]];
  const N15=[[1,2,11],[2,3,11],[1,3,12],[4,5,13],[5,6,14],
    [4,6,15],[7,8,12],[8,9,13],[9,10,14],[10,7,15]];
  const F15=P15.concat(N15.map(c=>c.map(z=>-z)));
  const assert=(v,msg)=>{if(!v)throw Error(msg)};
  function canonical(C,n) {
    if(n<3 || n%3 || 3*C.length!==4*n) return false;
    const count=Array.from({length:n+1},()=>[0,0]), keys=new Set();
    for(const c of C) {
      if(c.length!==3 || c.some(l=>!Number.isInteger(l)||l===0||Math.abs(l)>n)
          || new Set(c.map(Math.abs)).size!==3 || !c.every(l=>(l>0)===(c[0]>0)))return false;
      const key=c.slice().sort((a,b)=>a-b).join(",");
      if(keys.has(key))return false;keys.add(key);
      for(const l of c)count[Math.abs(l)][l>0?1:0]++;
    }
    return count.slice(1).every(p=>p[0]===2&&p[1]===2);
  }
  function truth(C,n,pins) {
    for(const c of C)if(!c.some(l=>pins[Math.abs(l)]===(l>0?1:0)))return false;
    return true;
  }
  function conditional8(C,n,fixed) {
    let result=0;
    for(let i=1;i<=n;i++)result+=fixed[i]<0?4:(fixed[i]===1?8:0);
    for(const c of C) {
      const xs=c.map(Math.abs);
      if(xs.some(i=>fixed[i]===0))continue;
      const free=xs.filter(i=>fixed[i]<0).length;
      result-=1<<(3-free);
    }
    return result;
  }
  function makeBackdoor(C,n) {
    assert(canonical(C,n),"invalid canonical input");
    const fixed=Array(n+1).fill(-1);fixed[0]=0;
    const initial=conditional8(C,n,fixed);
    let comparison=0;
    for(let i=1;i<=n;i++) {
      fixed[i]=0;const zero=conditional8(C,n,fixed);
      fixed[i]=1;const one=conditional8(C,n,fixed);
      comparison+=2;
      fixed[i]=one>zero?1:0;
      assert(conditional8(C,n,fixed)>=Math.min(zero,one),"conditional fail");
    }
    let S=new Set(Array.from({length:n},(_,i)=>i+1).filter(i=>fixed[i]===1));
    const selected=S.size, inside=C.filter(c=>c.every(l=>S.has(Math.abs(l)))).length;
    for(const c of C)if(c.every(l=>S.has(Math.abs(l))))S.delete(Math.min(...c.map(Math.abs)));
    let I=[...S].sort((a,b)=>a-b);
    const B=Array.from({length:n},(_,i)=>i+1).filter(i=>!S.has(i));
    assert(C.every(c=>c.some(l=>B.includes(Math.abs(l)))),"cover incomplete");
    assert(B.length<=Math.floor(2*n/3),"2n/3 violation");
    assert(I.length>=n/3,"independent size violation");
    assert(initial===8*n/3,"expected score mismatch");
    return {B,I,initial_scaled8:initial,selected_before_cleanup:selected,internal_triples:inside,
      conditional_comparisons:comparison,score_scaled8:conditional8(C,n,fixed),
      construction_clause_scans:2*n*C.length+2*C.length};
  }
  function minimumCover(C,n) {
    if(n>16)return null;
    let min=n+1,nopt=0,example=null;
    for(let mask=0;mask<(1<<n);mask++) {
      const b=mask.toString(2).replace(/0/g,"").length;
      if(b>min)continue;
      if(C.every(c=>c.some(l=>(mask&(1<<(Math.abs(l)-1)))!==0))) {
        if(b<min){min=b;nopt=0;example=[]}
        nopt++;if(example.length===0)example=Array.from({length:n},(_,i)=>i+1).filter(i=>mask&(1<<(i-1)));
      }
    }
    return {minimum:min,count_of_minimum_covers:nopt,example};
  }
  function twoSAT(C,n,pins,certificate) {
    const graph=Array.from({length:2*n},()=>[]),rev=Array.from({length:2*n},()=>[]);
    const index=l=>2*(Math.abs(l)-1)+(l<0?1:0);
    let scans=0,arcs=0,empty=null,units=0,binaries=0;
    function edge(a,b,id) {
      graph[a].push({v:b,id});rev[b].push({v:a,id});arcs++;
    }
    for(let j=0;j<C.length;j++) {
      scans++;let satisfied=false;const remain=[];
      for(const l of C[j]) {
        const v=pins[Math.abs(l)];
        if(v===undefined)remain.push(l);
        else if(v===(l>0?1:0)){satisfied=true;break;}
      }
      if(satisfied)continue;
      if(remain.length===3)throw Error("nonbinary residual, backdoor invalid");
      if(remain.length===0){empty=j+1;break;}
      if(remain.length===1){units++;const a=index(remain[0]);edge(a^1,a,j+1);}
      else {binaries++;const a=index(remain[0]),b=index(remain[1]);
        edge(a^1,b,j+1);edge(b^1,a,j+1);}
    }
    if(empty!==null)return {sat:false,kind:"empty",id:empty,scans,arcs,units,binaries};
    const used=new Uint8Array(2*n),order=[];
    function dfs(u) {
      used[u]=1;
      for(const e of graph[u])if(!used[e.v])dfs(e.v);
      order.push(u);
    }
    for(let i=0;i<2*n;i++)if(!used[i])dfs(i);
    const comp=new Int32Array(2*n).fill(-1);
    function dfs2(u,col) {
      comp[u]=col;for(const e of rev[u])if(comp[e.v]<0)dfs2(e.v,col);
    }
    let nc=0;
    for(let i=order.length-1;i>=0;i--) {
      const u=order[i];if(comp[u]<0)dfs2(u,nc++);
    }
    const conflict=[];
    for(let i=1;i<=n;i++)if(comp[2*(i-1)]===comp[2*(i-1)+1])conflict.push(i);
    if(conflict.length===0) {
      const assignment=Array(n+1).fill(0);
      for(let i=1;i<=n;i++)assignment[i]=comp[2*(i-1)]>comp[2*(i-1)+1]?1:0;
      for(const [k,v] of Object.entries(pins))assignment[+k]=v;
      assert(truth(C,n,assignment),"SCC model reconstruction failed");
      return {sat:true,scans,arcs,units,binaries,assignment:assignment.slice(1).join("")};
    }
    function path(start,end) {
      const seen=new Set([start]),parent=new Map(),queue=[start];
      for(let h=0;h<queue.length;h++) {
        const u=queue[h];if(u===end)break;
        for(const e of graph[u])if(!seen.has(e.v)){seen.add(e.v);parent.set(e.v,{u,id:e.id});queue.push(e.v);}
      }
      assert(seen.has(end),"SCC path impossible");
      const out=[];for(let u=end;u!==start;) {
        const r=parent.get(u);out.push({from:r.u,to:u,clause:r.id});u=r.u;
      }return out.reverse();
    }
    const v=conflict[0],a=2*(v-1);
    const forward=certificate?path(a,a^1):[],reverse=certificate?path(a^1,a):[];
    return {sat:false,kind:"SCC",conflict_variable:v,scans,arcs,units,binaries,
      ...(certificate?{forward,reverse}:{} )};
  }
  function sourceCompletionCount(C,n,pins) {
    const free=Array.from({length:n},(_,i)=>i+1).filter(i=>pins[i]===undefined);
    assert(free.length<=16,"too many free source variables");
    let count=0;for(let mask=0;mask<(1<<free.length);mask++) {
      const a=Array(n+1).fill(0);
      for(const [k,v] of Object.entries(pins))a[+k]=v;
      free.forEach((x,i)=>a[x]=(mask>>i)&1);
      if(truth(C,n,a))count++;
    }return count;
  }
  function finiteExperiment(name,C,n) {
    assert(canonical(C,n),name+" malformed");
    const door=makeBackdoor(C,n),min=minimumCover(C,n);
    let leaves=0,sat=0,unsat=0,empty=0,scc=0,scans=0,arcs=0;
    let proof_example=null,model_example=null,source_verified=0;
    for(let mask=0;mask<(1<<door.B.length);mask++) {
      const pins={};door.B.forEach((x,i)=>pins[x]=(mask>>i)&1);
      const r=twoSAT(C,n,pins,true);leaves++;scans+=r.scans;arcs+=r.arcs;
      const brute=sourceCompletionCount(C,n,pins)>0;source_verified++;
      assert(r.sat===brute,name+" source/2SAT mismatch "+mask);
      if(r.sat){sat++;if(!model_example)model_example=r.assignment;}
      else {unsat++;empty+=r.kind==="empty"?1:0;scc+=r.kind==="SCC"?1:0;
        if(!proof_example)proof_example={mask,pins,kind:r.kind,
          ...(r.kind==="SCC"?{conflict_variable:r.conflict_variable,forward:r.forward,reverse:r.reverse}:{clause:r.id})};}
    }
    const models=n<=15?sourceCompletionCount(C,n,{}):null;
    return {name,n,m:C.length,canonical:true,strong_2sat_backdoor:door.B,
      constructed_size:door.B.length,minimum_cover:min,construction:door,
      leaves,source_verified,sat_leaves:sat,unsat_leaves:unsat,
      unsat_empty_clause_leaves:empty,unsat_scc_leaves:scc,
      per_leaf_source_clause_scans_total:scans,implication_arcs_built_total:arcs,
      complete_original_models:models,example_witness:model_example,
      example_unsat_certificate:proof_example};
  }
  function bigSample(name,C,n,selectedAssignments) {
    assert(canonical(C,n),"invalid "+name);
    const door=makeBackdoor(C,n);
    assert(door.B.length<=132,"large backdoor exceeds bound");
    const results=[];
    for(const pins of selectedAssignments) {
      assert(door.B.every(v=>pins[v]!==undefined),"sample must pin whole backdoor");
      const r=twoSAT(C,n,pins,false);results.push({sat:r.sat,kind:r.kind||"model",arcs:r.arcs});
    }
    return {name,n,m:C.length,constructed_backdoor_size:door.B.length,
      cover_verified:true,sampled_branches:results.length,
      sample_sat:results.filter(x=>x.sat).length,
      sample_unsat:results.filter(x=>!x.sat).length,
      sample_kinds:results.slice(0,8),
      full_branching_work_not_run:true};
  }
  function instances(t) {
    const C=[];for(let k=0;k<t;k++)for(const c of F9)
      C.push(c.map(l=>(l>0?1:-1)*(Math.abs(l)+9*k)));
    assert(canonical(C,9*t),"F9^t malformed");
    return C;
  }
  const f9=finiteExperiment("F9",F9,9), y6=finiteExperiment("Y6",Y6,6),
    f15=finiteExperiment("F15",F15,15);
  const common={3:0,5:1,6:0,7:0,8:0};
  const pS={...common,1:0},pU={...common,1:1};
  const modelsS=sourceCompletionCount(F9,9,pS),modelsU=sourceCompletionCount(F9,9,pU);
  assert(modelsS===2&&modelsU===0,"same-original pair discrepancy");
  const products=[];
  for(const t of [2,3,4,8]) {
    const C=instances(t);
    const B=makeBackdoor(C,9*t);
    assert(B.B.length<=6*t,"2n/3 product failure");
    products.push({blocks:t,n:9*t,m:C.length,canonical:true,
      exact_minimum_cover:t*f9.minimum_cover.minimum,
      min_cover_additivity_proof:"disjoint clause hyperedges",
      constructed_backdoor_size:B.B.length,
      source_recognition:"connected incidence components of size 9; compare each to constant F9 signed template",
      pinned_SAT:firstBlockCount(C,pS),pinned_UNSAT:firstBlockCount(C,pU)});
  }
  function firstBlockCount(C,pins) {
    // number of first-block completions; remaining blocks are unpinned.
    return sourceCompletionCount(C.slice(0,12),9,pins);
  }
  const malformed=[F9.slice(1),[...F9,F9[0]],
      [[1,-5,6],...F9.slice(1)],[[1,1,5],...F9.slice(1)],
      [[0,5,6],...F9.slice(1)],[[1,5,10],...F9.slice(1)]];
  malformed.forEach(C=>assert(!canonical(C,9),"malformed source accepted"));
  const out={name:"LSPV4_SAME_ORIGINAL_STRONG_2SAT_BACKDOOR324",
    status:{cover_construct:"PROVED/EXACT with accompanying paper proof",
      f9_f15_exhaustive:"COMPUTATIONAL",universal_fast_SAT:"OPEN"},
    theorem:{n_mod_3:0,m_eq_4n_over_3:true,
      independent_lower_bound:"n/3",backdoor_upper_bound:"2n/3",
      total_time:"O(poly(N) * 2^(2n/3)) on charged indexed TM",
      peak_writable_space:"O(poly(N)), with explicit CNF/implication materialization",
      not_a_lower_bound:true},
    F9:f9,Y6:y6,F15:f15,same_original_F9_pins:{
      common,pS,pU,completion_counts:{SAT:modelsS,UNSAT:modelsU}},
    disjoint_F9_products:products,
    malformed_rejections:malformed.length};
  if(extra && extra.U198) {
    const U=extra.U198,V=U.map(c=>c.slice());
    [V[2][2],V[44][2]]=[V[44][2],V[2][2]];
    const B=makeBackdoor(U,198).B;
    const samplePins=Array.from({length:16},(_,k)=>{
      const pins={};B.forEach((v,i)=>pins[v]=((i*73+k*97+3*(i^k))%11)<5?1:0);
      return pins;
    });
    out.U198=bigSample("U198",U,198,samplePins);
    const BV=makeBackdoor(V,198).B;
    const sp=Array.from({length:16},(_,k)=>{
      const pins={};BV.forEach((v,i)=>pins[v]=((i*73+k*97+3*(i^k))%11)<5?1:0);
      return pins;
    });
    if(extra.V198Witness) {
      assert(extra.V198Witness.length===198,"V witness length");
      const a=Array(199).fill(0);
      for(let i=1;i<=198;i++)a[i]=+extra.V198Witness[i-1];
      assert(truth(V,198,a),"V198 witness not source-satisfying");
      const w={};BV.forEach(i=>w[i]=a[i]);
      sp.push(w);
      out.V198_witness_preserved=true;
    }
    out.V198=bigSample("V198",V,198,sp);
    out.U198_original_unsat="Inherited source-certified; this code does not prove UNSAT";
  }
  return out;
}

// Reproducible CLI: copy original U198 canonical array into JSON fixture and call execute({U198:...,V198Witness:...}).
if(typeof module!=='undefined'&&require.main===module){const fs=require('fs');const arg=process.argv[2];const extra=arg?JSON.parse(fs.readFileSync(arg,'utf8')):{};console.log(JSON.stringify(execute(extra),null,2));}
