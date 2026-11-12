"use strict";
// LSPV-1/584: externally bound, occurrence-aware SOURCE/RES reference, not historical R_mix341.
// Run: node experiments/arc/lspv1_583_source_view_join.cjs
const audit=function audit(){
  const ok=(b,m)=>{if(!b)throw new Error(m)};
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const sort=(v)=>{ok(Array.isArray(v),"clause must be array");ok(v.every(x=>Number.isSafeInteger(x)&&x!==0),"literal integers");ok(new Set(v).size===v.length,"duplicate literals");ok(!v.some(x=>v.includes(-x)),"tautological clause");return [...v].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)};
  const rsl=(left,right,p)=>{ok(Number.isSafeInteger(p)&&p!==0,"pivot");ok(left.includes(p)&&right.includes(-p),"strict oriented pivot");return sort([...left.filter(x=>x!==p),...right.filter(x=>x!==-p)])};
  const evaluate=(source,n)=>{let models=0;for(let a=0;a<2**n;a++){let good=source.every(s=>s.clause.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)));if(good)models++}return models};
  const rootEncode=root=>{
    ok(Array.isArray(root),"root array");
    const ids=new Set();
    return JSON.stringify(root.map(s=>{
      ok(s&&typeof s.id==="string"&&!ids.has(s.id),"unique root ID");
      ids.add(s.id);ok(eq(sort(s.clause),s.clause),"canonical root clause");
      return [s.id,s.clause];
    }));
  };
  const verify=(pkt,callerRoot)=>{
    ok(rootEncode(pkt.external)===rootEncode(callerRoot),"caller root mismatch");
    const seenSource=new Map();for(const s of pkt.external){ok(typeof s.id==="string"&&!seenSource.has(s.id),"root source identity");ok(eq(sort(s.clause),s.clause),"root source normal form");seenSource.set(s.id,s.clause)}
    const all=new Map();const paid=new Set();const rootUsed=new Set(),leafByID=new Map(),parentsByID=new Map();let boundSources=0,components=0;
    for(const c of pkt.components){
      components++;ok(Array.isArray(c.source_view)&&new Set(c.source_view).size===c.source_view.length,"local view IDs");
      for(const id of c.source_view)ok(seenSource.has(id),"unbound local view");
      for(const r of c.records){
        ok(!all.has(r.id),"duplicate node ID");ok(!r.ctx||r.ctx.length===0,"undischarged assumptions");
        if(r.kind==="SOURCE"){
          ok(c.source_view.includes(r.source_id),"source outside component view");
          ok(eq(seenSource.get(r.source_id),r.clause),"forged original source");
          boundSources++;rootUsed.add(r.source_id);leafByID.set(r.id,r.source_id);
        }else if(r.kind==="RES"){
          ok(r.parents.length===2&&r.parents.every(x=>all.has(x)),"parent chronology");
          const parents=r.parents.map(x=>all.get(x));ok(eq(rsl(parents[0],parents[1],r.pivot),r.clause),"inference mismatch");
          parentsByID.set(r.id,r.parents);paid.add(r.id);
        }else throw new Error("unverified component opcode");
        all.set(r.id,r.clause);
      }
    }
    for(const r of pkt.joins){
      ok(!all.has(r.id),"duplicate join ID");ok(!r.ctx||r.ctx.length===0,"undischarged join");
      ok(r.kind==="RES"&&r.parents.length===2&&r.parents.every(x=>all.has(x)),"unsupported join/parent");
      ok(eq(rsl(all.get(r.parents[0]),all.get(r.parents[1]),r.pivot),r.clause),"bad join resolvent");
      all.set(r.id,r.clause);parentsByID.set(r.id,r.parents);paid.add(r.id);
    }
    ok(pkt.joins.length>0&&eq(all.get(pkt.joins.at(-1).id),[]),"missing empty-clause sink");
    const ancestors=new Set(),stack=[pkt.joins.at(-1).id];
    while(stack.length){const id=stack.pop();if(ancestors.has(id))continue;ancestors.add(id);for(const p of parentsByID.get(id)||[])stack.push(p)}
    const leafAncestors=[...ancestors].filter(id=>leafByID.has(id));
    const rootAncestors=new Set(leafAncestors.map(id=>leafByID.get(id)));
    return {accepted:true,paid_count:paid.size,used_sources:boundSources,source_records:boundSources,unique_root_sources_used:rootUsed.size,terminal_source_records:leafAncestors.length,terminal_root_sources:rootAncestors.size,root_sources:pkt.external.length,component_views:pkt.components.map(x=>x.source_view.length),same_sources_across_components:eq(pkt.components[0].source_view,pkt.components[1].source_view)};
  };
  const base=()=>({
    external:[{id:"s0",clause:[1,2]},{id:"s1",clause:[-2]},{id:"s2",clause:[-1]}],
    components:[
      {name:"A",source_view:["s0","s1"],records:[
        {id:"a0",kind:"SOURCE",source_id:"s0",clause:[1,2]},
        {id:"a1",kind:"SOURCE",source_id:"s1",clause:[-2]},
        {id:"a2",kind:"RES",parents:["a0","a1"],pivot:2,clause:[1]}]},
      {name:"B",source_view:["s2"],records:[
        {id:"b0",kind:"SOURCE",source_id:"s2",clause:[-1]}]}
    ],
    joins:[{id:"j0",kind:"RES",parents:["a2","b0"],pivot:1,clause:[]}]
  });
  const basePacket=base();const main=verify(basePacket,basePacket.external);ok(evaluate(basePacket.external,2)===0,"base UNSAT");
  ok(main.paid_count===2&&!main.same_sources_across_components,"exact source-view counterexample");
  const variants=[];
  const universe=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
  for(let mask=0;mask<256;mask++){
    if(!((mask&(1<<1))&&(mask&(1<<3))&&(mask&(1<<4))))continue;
    const p=base();
    let j=3;
    for(let i=0;i<universe.length;i++)if(mask&(1<<i)){
      const c=universe[i];
      if(eq(c,[-1])||eq(c,[-2])||eq(c,[1,2]))continue;
      p.external.push({id:"extra"+j++,clause:c});
    }
    const x=verify(p,p.external);ok(x.paid_count===2&&evaluate(p.external,2)===0,"extension");
    variants.push({mask,clauses:p.external.length,charge:x.paid_count});
  }
  ok(variants.length===32,"extension count");
  const malicious=[
    ["source_forgery",p=>{p.external[2].clause=[1]}],
    ["missing_source_mapping",p=>{p.components[1].source_view=["absent"]}],
    ["source_view_substitution",p=>{p.components[1].source_view=["s1"]}],
    ["wrong_signed_pivot",p=>{p.components[0].records[2].pivot=-2}],
    ["bad_resolution_conclusion",p=>{p.components[0].records[2].clause=[-1]}],
    ["duplicate_paid_id",p=>{p.joins[0].id="a2"}],
    ["undischarged_assumption",p=>{p.components[0].records[2].ctx=[1]}],
    ["unsupported_uncharged_rule",p=>{p.joins[0].kind="MAGIC"}],
    ["missing_terminal_join",p=>{p.joins=[]}],
    ["new_local_source_without_root",p=>{p.components[1].records[0].source_id="notroot"}],
    ["source_literal_reordering",p=>{p.external[0].clause=[2,1]}]
  ];
  const controls=[];
  for(const [name,change] of malicious){let p=base(),rejected=false,error="";change(p);try{verify(p,p.external)}catch(e){rejected=true;error=e.message}ok(rejected,"FAILED hostile "+name);controls.push({name,rejected,error})}
  const multiplicity=[];
  const trimDeadSource=p=>{
    const cp=JSON.parse(JSON.stringify(p)),used=new Set();
    for(const c of cp.components)for(const r of c.records)for(const id of r.parents||[])used.add(id);
    for(const r of cp.joins)for(const id of r.parents||[])used.add(id);
    for(const c of cp.components)c.records=c.records.filter(r=>r.kind!=="SOURCE"||used.has(r.id));
    return cp;
  };
  for(const k of [0,1,2,4,8,16,64]){
    const p=base();
    for(let j=0;j<k;j++)p.components[0].records.push({id:"duplicate_"+j,kind:"SOURCE",source_id:"s0",clause:[1,2]});
    const m=verify(p,p.external),t=verify(trimDeadSource(p),p.external);
    ok(m.source_records===3+k&&m.unique_root_sources_used===3&&m.terminal_source_records===3&&m.terminal_root_sources===3&&m.paid_count===2,"multiplicity "+k);
    ok(t.paid_count===2&&t.source_records===3,"pruning "+k);
    multiplicity.push({extra_source_copies:k,source_records:m.source_records,unique_root_sources:m.unique_root_sources_used,terminal_source_records:m.terminal_source_records,paid:m.paid_count,after_prune:t.source_records});
  }
  const caller_controls=[];
  const attacks=[
    ["caller_forged_SAT",r=>{r[2].clause=[1]}],
    ["caller_missing_occurrence",r=>{r.pop()}],
    ["caller_occurrence_permutation",r=>{r.reverse()}],
    ["caller_occurrence_ID_changed",r=>{r[1].id="different"}],
    ["caller_noncanonical_clause_order",r=>{r[0].clause=[2,1]}],
    ["caller_duplicate_ID",r=>{r[1].id="s0"}],
    ["caller_literal_change",r=>{r[0].clause=[-1,2]}]
  ];
  for(const [name,modify] of attacks){
    const caller=JSON.parse(JSON.stringify(basePacket.external));modify(caller);
    let rejected=false,reason="";try{verify(basePacket,caller)}catch(e){rejected=true;reason=e.message}
    ok(rejected,"failed caller hostile "+name);caller_controls.push({name,rejected,reason});
  }
  const cross=base();
  cross.components[1].source_view.push("s0");
  cross.components[1].records.push({id:"cross_duplicate",kind:"SOURCE",source_id:"s0",clause:[1,2]});
  const crossResult=verify(cross,cross.external);
  ok(crossResult.source_records===4&&crossResult.unique_root_sources_used===3&&crossResult.paid_count===2,"cross component duplicate");
  const sat=p=>evaluate(p.external,2);
  const satPerturb=base();satPerturb.external[2].clause=[1];ok(sat(satPerturb)===1,"false-source SAT witness");
  return {id:"LSPV1-584",multiplicity,caller_controls,cross_component_duplicate:crossResult,baseline_git_blob:"ecc0157627048fa481123ef1cb4835b9f4b4239e",status:"PROVED/RESTRICTED symbolic source-view join; COMPUTATIONAL exhaustive controls",meaning:"distinct subset source views joined by explicit source-anchored RES; not a historical R_mix341 checker",base:main,original_external_model_count:0,forged_external_model_count:1,exhaustive_clause_universe:8,exhaustive_multiplicative_source_extensions:variants.length,total_source_extensions_checked:variants.length,extension_min_clause_count:Math.min(...variants.map(x=>x.clauses)),extension_max_clause_count:Math.max(...variants.map(x=>x.clauses)),negative_controls:controls,all_passed:true};
};
console.log(JSON.stringify(audit(),null,2));
