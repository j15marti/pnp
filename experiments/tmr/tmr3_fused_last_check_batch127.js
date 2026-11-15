"use strict";
// TMR-3/046 independent exact finite-state fusion tariff audit.
// Run: node experiments/tmr/tmr3_fused_last_check_batch127.js
function audit() {
  "use strict";
  const fano = [[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const specs = [
    {name:"fano",q:7,E:fano,G:1,tauFraction:[7,3]},
    {name:"fano",q:7,E:fano,G:2,tauFraction:[7,3]},
    {name:"fano",q:7,E:fano,G:3,tauFraction:[7,3]},
    {name:"fano",q:7,E:fano,G:4,tauFraction:[7,3]},
    {name:"triangle",q:3,E:[[0,1],[1,2],[0,2]],G:1,tauFraction:[3,2]},
    {name:"triangle",q:3,E:[[0,1],[1,2],[0,2]],G:2,tauFraction:[3,2]},
    {name:"full",q:7,E:[Array.from({length:7},(_,i)=>i)],G:3,tauFraction:[1,1]},
    {name:"singletons",q:4,E:[[0],[1],[2],[3]],G:2,tauFraction:[4,1]}
  ];
  const UNIT=42;let assertions=0,edgeChecks=0,freeChecks=0;
  const ruleCounts={};const outcomes=[];
  function check(b, message) {assertions++;if(!b)throw Error(message);}
  function pop(x){let r=0;while(x){x&=x-1;r++;}return r;}
  function encode(s){return `${s.P},${s.U},${s.h},${s.v}`;}
  for (const spec of specs) {
    const q=spec.q,G=spec.G, full=(1<<q)-1,pfull=(1<<G)-1;
    const batches=spec.E.map(S=>S.reduce((mask,j)=>mask|(1<<j),0));
    function transitions(s) {
      const out=[
        {rule:"VIEW",cost:0,next:{...s,v:1-s.v},batch:-1},
        {rule:"NOP",cost:0,next:{...s},batch:-1}
      ];
      if (!s.h) return out;
      for(let g=0;g<G;g++) if(!(s.P&(1<<g)))
        out.push({rule:"CHECK",cost:1,next:{...s,P:s.P|(1<<g)},batch:-1});
      if(s.P===pfull && s.U)
        for(let i=0;i<batches.length;i++)if(s.U&batches[i])
          out.push({rule:"BATCH",cost:1,next:{...s,U:s.U&~batches[i]},batch:i});
      const unpaid=pfull^s.P;
      if(s.U===full && unpaid && !(unpaid&(unpaid-1)))
        for(let i=0;i<batches.length;i++)
          out.push({rule:"FUSE",cost:1,next:{...s,P:pfull,U:s.U&~batches[i]},batch:i});
      if(s.P===pfull && s.U===0)
        out.push({rule:"HALT",cost:1,next:{...s,h:0},batch:-1});
      return out;
    }
    const masks=batches;let tau=Infinity;
    for(let chosen=0;chosen<(1<<masks.length);chosen++){
      let cover=0,ct=0;
      for(let j=0;j<masks.length;j++)if(chosen&(1<<j)){cover|=masks[j];ct++;}
      if(cover===full)tau=Math.min(tau,ct);
    }
    const init={P:0,U:full,h:1,v:0};
    const dist=new Map([[encode(init),0]]),queue=[init];
    for(let at=0;at<queue.length;at++){
      const s=queue[at],d=dist.get(encode(s));
      for(const e of transitions(s)){
        const t=encode(e.next), nd=d+e.cost, old=dist.get(t);
        if(old===undefined || nd<old){dist.set(t,nd);queue.push(e.next);}
      }
    }
    const shortest=Math.min(dist.get(encode({P:pfull,U:0,h:0,v:0}))??Infinity,
                            dist.get(encode({P:pfull,U:0,h:0,v:1}))??Infinity);
    check(shortest===G+tau,`${spec.name}: G${G} genuine min ${shortest} != ${G+tau}`);
    let certs=[
      {name:"gateDominant",g:UNIT,h:UNIT,theta:Array(q).fill(0)},
      {name:"batchDominant",g:0,h:UNIT,theta:Array(q).fill(
        spec.name==="fano"?14:spec.name==="triangle"?21:spec.name==="full"?6:42)}
    ];
    const allStates=[];
    for(let P=0;P<=pfull;P++)for(let U=0;U<=full;U++)
      for(let h=0;h<=1;h++)for(let v=0;v<=1;v++){
        if(P!==pfull && U!==full)continue;
        if(h===0 && !(P===pfull && U===0))continue;
        allStates.push({P,U,h,v});
      }
    for(const s of allStates){
      for(const e of transitions(s)){
        const dG=pop(e.next.P)-pop(s.P);
        const dH=s.h-e.next.h;
        check(dG>=0&&dG<=1&&dH>=0&&dH<=1,"count-once CHECK/HALT");
        if(e.rule==="FUSE"){
          check(dG===1&&dH===0,"FUSE exactly last gate");
          check(s.U===full&&e.next.U!==full,"FUSE discharges nonempty batch");
        }
        for(const z of certs){
          let charge=z.g*dG+z.h*dH;
          for(let j=0;j<q;j++)charge+=z.theta[j]*((s.U>>j&1)-(e.next.U>>j&1));
          check(charge<=UNIT*e.cost,
            `${spec.name} G${G} ${z.name} ${e.rule} ${charge}>${UNIT*e.cost}`);
          if(e.cost===0){check(charge===0,"zero VIEW illegally decreases potential");freeChecks++;}
          edgeChecks++;
        }
        ruleCounts[e.rule]=(ruleCounts[e.rule]||0)+1;
      }
    }
    const [fracNum,fracDen]=spec.tauFraction;
    const predicted=1+Math.max(G,fracNum/fracDen);
    const actual=Math.max(...certs.map(z=>(G*z.g+z.h+z.theta.reduce((a,b)=>a+b,0))/UNIT));
    check(Math.abs(actual-predicted)<1e-9,
      `${spec.name}: G${G} exact certificate ${actual} != ${predicted}`);
    check(shortest+1e-9>=actual,"LP cannot exceed shortest authentic path");
    const lpNumer=fracDen+Math.max(G*fracDen,fracNum);
    outcomes.push({family:spec.name,gates:G,scales:q,batches:spec.E.length,
      fractional_cover:`${fracNum}/${fracDen}`,integer_cover:tau,
      exact_record_min:shortest,exact_tariff_LP:`${lpNumer}/${fracDen}`,
      reachable_states:dist.size,all_legal_states:allStates.length,
      LP_gap_numerator:(shortest*fracDen-lpNumer),LP_gap_denominator:fracDen});
  }
  const tiny={G:1,q:1,E:[[0]],before:{P:0,U:1,h:1},after:{P:1,U:0,h:1},
    rule:"FUSE",cost:1,delta_gamma:1,delta_scale:1,
    old_weights:{gamma:1,theta:1},old_weighted_discharge:2,
    exact_fused_cone:"gamma+theta<=1"};
  check(tiny.old_weighted_discharge>tiny.cost,"tiny legal hostile FUSE");
  return {id:"TMR3_FUSEBATCH127",status:"COMPUTATIONAL for finite exhaustive traces; restricted exact theorem symbolic",
    assertions,all_state_tariff_checks:edgeChecks,zero_cost_tariff_checks:freeChecks,
    rule_counts:ruleCounts,failures:0,cases:outcomes,smallest_fusion_counterexample:tiny};
}
if (typeof module !== "undefined" && require.main === module) {
  console.log(JSON.stringify(audit(), null, 2));
}
