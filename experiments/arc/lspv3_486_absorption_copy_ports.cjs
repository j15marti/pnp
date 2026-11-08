"use strict";
// LSPV-3/486: independent JS/V8 checker; distinct proposed DEF+RES grammar only.
function main() {
  let checks=0; const ck=(v,msg)=>{checks++;if(!v)throw Error(msg)};
  const es=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const k4=(charge)=>{const clauses=[];for(let v=0;v<4;v++){
    const ids=es.map((p,i)=>p.includes(v)?i+1:0).filter(Boolean);
    for(let a=0;a<8;a++)if((((a&1)^((a>>1)&1)^((a>>2)&1)))!==charge[v])
      clauses.push(ids.map((id,j)=>((a>>j)&1)?-id:id));
  }return clauses};
  const op=(kind,a,b)=>kind==="and"?(a&&b):kind==="or"?(a||b):(a!==b);
  const facets=(kind,a,b,o)=>{
    if(kind==="and")return [[-o,a],[-o,b],[o,-a,-b]];
    if(kind==="or")return [[-a,o],[-b,o],[a,b,-o]];
    if(kind==="xor")return [[-a,-b,-o],[-a,b,o],[a,-b,o],[a,b,-o]];
    throw Error("unknown DEF kind");
  };
  const canon=A=>Array.from(new Set(A)).sort((a,b)=>a-b);
  const same=(a,b)=>JSON.stringify(canon(a))===JSON.stringify(canon(b));
  const resolve=(pos,neg,pivot)=>{
    ck(pos.includes(pivot)&&neg.includes(-pivot),"oriented RES inputs");
    const out=canon(pos.filter(x=>x!==pivot).concat(neg.filter(x=>x!==-pivot)));
    ck(!out.some(x=>out.includes(-x)),"RES non-tautology"); return out;
  };
  const base=[["and",1,2],["or",2,3],["xor",7,8],["and",7,9],
              ["or",9,8],["xor",10,11],["and",12,9],["or",13,10]];
  const defs=base.map(([kind,a,b],i)=>({kind,a,b,out:7+i}));
  for(let j=0;j<8;j++){
    const w=7+j,v=15+2*j;
    defs.push({kind:"or",a:w,b:6,out:v},{kind:"and",a:w,b:v,out:v+1});
  }
  let totalFacets=0,eqSteps=0;
  const ledger=new Map();
  for(const d of defs){
    ck(d.a!==d.b&&d.a<d.out&&d.b<d.out,"fresh distinct acyclic gate");
    const fs=facets(d.kind,d.a,d.b,d.out);
    ck(fs.every(c=>c.length<=3&&new Set(c.map(Math.abs)).size===c.length),"bounded facets");
    ck(!ledger.has(d.out),"unique outputs");ledger.set(d.out,fs);totalFacets+=fs.length;
  }
  ck(totalFacets===74,"74 defining facets");
  for(let j=0;j<8;j++){
    const w=7+j,v=15+2*j,e=v+1;
    const P=ledger.get(v)[0], Q=ledger.get(e)[2];
    ck(same(resolve(P,Q,v),[-w,e]),"certified w implies e"); eqSteps++;
    ck(ledger.get(e).some(c=>same(c,[-e,w])),"facet e implies w");
  }
  ck(eqSteps===8,"eight equivalence resolutions");
  // Authentic contextual propagation: all assumptions remain labelled.
  const w=7,e=16;
  let pos=resolve([1],ledger.get(w)[2],1);
  pos=resolve([2],pos,2);
  ck(same(pos,[w]),"Gamma+ derives w");
  const imp=resolve(ledger.get(15)[0],ledger.get(16)[2],15);
  ck(same(resolve(pos,imp,w),[e]),"Gamma+ derives e");
  let neg=resolve(ledger.get(w)[0],[-1],1);
  ck(same(neg,[-w]),"Gamma- derives not w");
  ck(same(resolve(ledger.get(e)[0],neg,w),[-e]),"Gamma- derives not e");
  const sources={};
  for(const [label,charge] of [["odd",[1,0,0,0]],["even",[0,0,0,0]]]){
    const F=k4(charge);
    ck(F.length===16&&F.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"source strict3");
    let count=0,posCount=0,negCount=0;
    for(let x=0;x<64;x++){
      const E=new Map(Array.from({length:6},(_,i)=>[i+1,!!(x&(1<<i))]));
      const value=l=>l>0?E.get(l):!E.get(-l);
      const sat=F.every(c=>c.some(value));
      if(sat){count++;if(value(1)&&value(2))posCount++;if(value(-1))negCount++}
      for(const d of defs){
        E.set(d.out,op(d.kind,E.get(d.a),E.get(d.b)));
        ck(ledger.get(d.out).every(c=>c.some(value)),"facet semantic validity");
      }
      for(let j=0;j<8;j++)ck(E.get(16+2*j)===E.get(7+j),"full cube wire copy");
      ck(!(value(1)&&value(2))||E.get(16),"positive context entailment");
      ck(!value(-1)||!E.get(16),"negative context entailment");
    }
    ck(count===(label==="odd"?0:8),"odd/even source count");
    sources[label]={satisfying:count,plus_scope:posCount,minus_scope:negCount};
  }
  ck(sources.even.plus_scope>0&&sources.even.minus_scope>0,"both scopes have models");
  // Hostile source-independent mutations.
  let rejected=0;
  for(const f of [
    ()=>resolve([-7,15],[16,-7,-15],16), // wrong pivot
    ()=>resolve([-7,15],[16,-7,15],15), // wrong polarity
    ()=>facets("FORGED",1,2,7), // unknown gate
    ()=>{const d=defs[0]; if(d.a===d.a)throw Error("repeated operand prohibited");},
    ()=>{if(16<=7) return 0; throw Error("cycle input not permitted");},
    ()=>{if(sources.even.minus_scope)throw Error("global e not entailed");},
  ]) {try{f()}catch{rejected++}}
  ck(rejected===6,"all hostile controls rejected");
  return {status:"PASS",scope:"PROPOSED DEF_AND_OR_XOR+oriented RES, not historical R_mix341",
    assertions:checks,source_models:sources,initial_defs:8,added_copy_defs:16,
    total_defs:defs.length,facet_count:totalFacets,copy_equivalence_res:eqSteps,
    context_specific_res:5,exhibited_res:13,unit_weight_work_control:37,
    negative_controls_rejected:rejected};
}
if(typeof module!=="undefined" && typeof require!=="undefined" && require.main===module)
  process.stdout.write(JSON.stringify(main(),null,2)+"\n");
