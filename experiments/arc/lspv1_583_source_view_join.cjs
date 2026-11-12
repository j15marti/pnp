"use strict";
// LSPV-1/583: self-contained, deterministic exact source-view joining verifier.
// Run: node experiments/arc/lspv1_583_source_view_join.cjs
const audit=function audit(){
  const ok=(b,m)=>{if(!b)throw new Error(m)};
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const sort=(v)=>{ok(Array.isArray(v),"clause must be array");ok(v.every(x=>Number.isSafeInteger(x)&&x!==0),"literal integers");ok(new Set(v).size===v.length,"duplicate literals");ok(!v.some(x=>v.includes(-x)),"tautological clause");return [...v].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)};
  const rsl=(left,right,p)=>{ok(Number.isSafeInteger(p)&&p!==0,"pivot");ok(left.includes(p)&&right.includes(-p),"strict oriented pivot");return sort([...left.filter(x=>x!==p),...right.filter(x=>x!==-p)])};
  const evaluate=(source,n)=>{let models=0;for(let a=0;a<2**n;a++){let good=source.every(s=>s.clause.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)));if(good)models++}return models};
  const verify=(pkt)=>{
    const seenSource=new Map();for(const s of pkt.external){ok(typeof s.id==="string"&&!seenSource.has(s.id),"root source identity");ok(eq(sort(s.clause),s.clause),"root source normal form");seenSource.set(s.id,s.clause)}
    const all=new Map();const paid=new Set();let boundSources=0,components=0;
    for(const c of pkt.components){
      components++;ok(Array.isArray(c.source_view)&&new Set(c.source_view).size===c.source_view.length,"local view IDs");
      for(const id of c.source_view)ok(seenSource.has(id),"unbound local view");
      for(const r of c.records){
        ok(!all.has(r.id),"duplicate node ID");ok(!r.ctx||r.ctx.length===0,"undischarged assumptions");
        if(r.kind==="SOURCE"){
          ok(c.source_view.includes(r.source_id),"source outside component view");
          ok(eq(seenSource.get(r.source_id),r.clause),"forged original source");
          boundSources++;
        }else if(r.kind==="RES"){
          ok(r.parents.length===2&&r.parents.every(x=>all.has(x)),"parent chronology");
          const parents=r.parents.map(x=>all.get(x));ok(eq(rsl(parents[0],parents[1],r.pivot),r.clause),"inference mismatch");
          paid.add(r.id);
        }else throw new Error("unverified component opcode");
        all.set(r.id,r.clause);
      }
    }
    for(const r of pkt.joins){
      ok(!all.has(r.id),"duplicate join ID");ok(!r.ctx||r.ctx.length===0,"undischarged join");
      ok(r.kind==="RES"&&r.parents.length===2&&r.parents.every(x=>all.has(x)),"unsupported join/parent");
      ok(eq(rsl(all.get(r.parents[0]),all.get(r.parents[1]),r.pivot),r.clause),"bad join resolvent");
      all.set(r.id,r.clause);paid.add(r.id);
    }
    ok(pkt.joins.length>0&&eq(all.get(pkt.joins.at(-1).id),[]),"missing empty-clause sink");
    return {accepted:true,paid_count:paid.size,used_sources:boundSources,root_sources:pkt.external.length,component_views:pkt.components.map(x=>x.source_view.length),same_sources_across_components:eq(pkt.components[0].source_view,pkt.components[1].source_view)};
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
  const basePacket=base();const main=verify(basePacket);ok(evaluate(basePacket.external,2)===0,"base UNSAT");
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
    const x=verify(p);ok(x.paid_count===2&&evaluate(p.external,2)===0,"extension");
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
  for(const [name,change] of malicious){let p=base(),rejected=false,error="";change(p);try{verify(p)}catch(e){rejected=true;error=e.message}ok(rejected,"FAILED hostile "+name);controls.push({name,rejected,error})}
  const sat=p=>evaluate(p.external,2);
  const satPerturb=base();satPerturb.external[2].clause=[1];ok(sat(satPerturb)===1,"false-source SAT witness");
  return {id:"LSPV1-583",status:"PROVED/RESTRICTED symbolic source-view join; COMPUTATIONAL exhaustive controls",meaning:"distinct subset source views joined by explicit source-anchored RES; not a historical R_mix341 checker",base:main,original_external_model_count:0,forged_external_model_count:1,exhaustive_clause_universe:8,exhaustive_multiplicative_source_extensions:variants.length,total_source_extensions_checked:variants.length,extension_min_clause_count:Math.min(...variants.map(x=>x.clauses)),extension_max_clause_count:Math.max(...variants.map(x=>x.clauses)),negative_controls:controls,all_passed:true};
};
console.log(JSON.stringify(audit(),null,2));
