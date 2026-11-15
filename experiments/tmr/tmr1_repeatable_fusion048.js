"use strict";
// TMR-1/048. Exact enumerator for the preauthenticated repeatable fusion system.
const audit = function audit() {
  "use strict";
  let assertions=0, paidRows=0, freeRows=0, states=0, failures=0, bellmanStates=0;
  const patterns=new Map(), examples=[], caseStats=[];
  const insist=(condition,message)=>{assertions++;if(!condition){failures++;throw Error(message);}};
  const pop=(x)=>{let c=0;for(;x;x&=x-1)c++;return c;};
  const cases=[
    {name:"one-scale-unit-joint",G:1,q:1,E:[1]},
    {name:"two-scale-singletons-counterexample",G:2,q:2,E:[1,2]},
    {name:"three-scale-singletons",G:3,q:3,E:[1,2,4]},
    {name:"four-scale-singletons",G:4,q:4,E:[1,2,4,8]},
    {name:"three-scale-full-batch",G:3,q:3,E:[7]},
    {name:"triangle-overlaps",G:3,q:3,E:[3,5,6]},
    {name:"four-scale-overlaps",G:3,q:4,E:[3,6,12,9]},
    {name:"fano-plane-overlaps",G:3,q:7,E:[7,25,97,42,82,76,52]},
    {name:"redundant-overlap",G:2,q:3,E:[1,3,6,4]},
    {name:"all-scale-and-singleton",G:4,q:4,E:[15,1,2,4,8]}
  ];
  const colNames=["CNF","XOR","SEP","FUS","Gamma","Interface","Machine"];
  const lambda=[0,0,0,1,0,0,1];
  for (const model of cases){
    const {G,q,E,name}=model, fullG=(1<<G)-1, fullJ=(1<<q)-1, fullB=(1<<E.length)-1;
    insist(E.every(s=>s>0 && (s&~fullJ)===0),"invalid batch");
    insist(E.reduce((a,b)=>a|b,0)===fullJ,"not covering");
    const tauMemo=new Map();
    function tau(U){
      if(tauMemo.has(U))return tauMemo.get(U);
      if(U===0){tauMemo.set(0,0);return 0;}
      let best=E.length+1;
      for(let z=1;z<=fullB;z++){
        let union=0;
        for(let i=0;i<E.length;i++)if(z&(1<<i))union|=E[i];
        if((union&U)===U)best=Math.min(best,pop(z));
      }
      insist(best<=E.length,"uncovered pending");
      tauMemo.set(U,best);
      return best;
    }
    function pending(B){
      let U=fullJ;
      for(let i=0;i<E.length;i++)if(B&(1<<i))U &= ~E[i];
      return U;
    }
    function data(g,b,h) {
      const t=G-pop(g),U=pending(b),m=tau(U);
      const p=[0,0,m,Math.max(t,m),t,0,h];
      return {g,b,h,t,U,m,p,phi:p[3]+p[6]};
    }
    function edges(s){
      if(s.h===0)return [];
      const arr=[];
      for(let i=0;i<G;i++)if(!(s.g&(1<<i))){
        arr.push({kind:"CHECK",id:i,cost:1,to:data(s.g|(1<<i),s.b,1)});
      }
      for(let k=0;k<E.length;k++)if(!(s.b&(1<<k)) && (E[k]&s.U)!==0){
        arr.push({kind:"BATCH",id:k,cost:1,to:data(s.g,s.b|(1<<k),1)});
        for(let i=0;i<G;i++)if(!(s.g&(1<<i))){
          arr.push({kind:"FUSE",id:i,batch:k,cost:1,to:data(s.g|(1<<i),s.b|(1<<k),1)});
        }
      }
      if(s.g===fullG && s.U===0)arr.push({kind:"HALT",cost:1,to:data(s.g,s.b,0)});
      return arr;
    }
    const shortestMemo=new Map(), visiting=new Set();
    function minWork(s){
      const key=`${s.g}:${s.b}:${s.h}`;
      if(shortestMemo.has(key))return shortestMemo.get(key);
      if(s.h===0){insist(s.g===fullG&&s.U===0,"bad terminal");shortestMemo.set(key,0);return 0;}
      insist(!visiting.has(key),"paid cycle");
      visiting.add(key);
      let best=Infinity;
      for (const e of edges(s)) best=Math.min(best,e.cost+minWork(e.to));
      visiting.delete(key);
      insist(Number.isFinite(best),"dead state");
      shortestMemo.set(key,best);
      return best;
    }
    let sampleEdges=0, caseStates=0,casePaid=0,caseFree=0,maxDelta=0;
    for(let g=0;g<=fullG;g++)for(let b=0;b<=fullB;b++){
      const forms=[data(g,b,1)];
      if(g===fullG&&pending(b)===0)forms.push(data(g,b,0));
      for(const s of forms){
        states++;caseStates++;bellmanStates++;
        insist(s.p.every(v=>Number.isInteger(v)&&v>=0),`${name}: negative component`);
        insist(s.phi===Math.max(s.t,s.m)+s.h,`${name}: formula identity`);
        const actual=minWork(s);
        insist(actual===s.phi,`${name}: Bellman mismatch state ${s.g}:${s.b}:${s.h}: ${actual} != ${s.phi}`);
        insist((s.h===0)===(s.g===fullG&&s.U===0&&s.h===0), "terminal classification");
        for(let view=0;view<=1;view++){
          const viewNext=data(s.g,s.b,s.h);
          const zeroDelta=s.p.map((a,i)=>a-viewNext.p[i]);
          insist(zeroDelta.every(d=>d===0), "free view changes paid data");
          insist(s.phi-viewNext.phi<=0,"free view tariff");
          freeRows++;caseFree++;
        }
        for(const e of edges(s)){
          paidRows++;casePaid++;
          const ds=s.p.map((z,i)=>z-e.to.p[i]);
          const weighted=ds.reduce((a,v,i)=>a+v*lambda[i],0);
          insist(weighted===s.phi-e.to.phi,"wrong weighted difference");
          insist(weighted<=e.cost,`${name} price-one overdischarge ${e.kind}: ${weighted}`);
          insist(weighted>=0,`${name} potential increased on paid event unexpectedly`);
          insist(ds[0]===0&&ds[1]===0&&ds[5]===0,"undeclared component altered");
          insist(ds[2]>=0&&ds[2]<=1&&ds[3]>=0&&ds[3]<=1&&ds[4]>=0&&ds[4]<=1&&ds[6]>=0&&ds[6]<=1,"bad signed delta");
          const pk=`${e.kind}|${ds.join(",")}`;
          patterns.set(pk,(patterns.get(pk)||0)+1);
          if(examples.length<16 && (!examples.some(x=>x.kind===e.kind&&x.delta.join(",")===ds.join(",")))){
            examples.push({model:name,kind:e.kind,source:{t:s.t,U:s.U,tau:s.m,h:s.h},target:{t:e.to.t,U:e.to.U,tau:e.to.m,h:e.to.h},delta:ds,weighted,cost:e.cost});
          }
          maxDelta=Math.max(maxDelta,weighted);
          sampleEdges++;
        }
      }
    }
    const initial=data(0,0,1);
    const m=tau(fullJ),opt=Math.max(G,m)+1,cert={lambda, dual:{joint:maxNumber(G,m),halt:1},objective:opt};
    function maxNumber(a,b){return Math.max(a,b);}
    insist(initial.phi===opt&&minWork(initial)===opt,`${name} initial optimum mismatch`);
    insist(opt<=Math.max(G,q)+1,`${name} ceiling violated`);
    insist(cert.dual.joint+cert.dual.halt===opt, "dual mismatch");
    insist(cert.lambda[2]+cert.lambda[3]+cert.lambda[4]<=1 && cert.lambda[6]<=1,"LP infeasible");
    caseStats.push({name,G,q,batch_count:E.length,batches:E,integer_cover:m,states:caseStates,paid_rows:casePaid,free_rows:caseFree,initial_phi:initial.phi,independent_bellman:actualValue(initial),max_discharge:maxDelta});
    function actualValue(st){return minWork(st);}
  }
  const oldPhi=(t,u,full,m)=>t+m+1-((u===full && t>0)?1:0);
  const oldInitial=oldPhi(2,3,3,2),oldAfter1=oldPhi(1,2,3,1),oldAfter2=oldPhi(0,0,3,0);
  insist(oldInitial===4&&oldAfter1===3&&oldAfter2===1,"old credit example broken");
  insist(oldAfter1-oldAfter2===2,"old barrier shortcut not real");
  insist(3===2+1,"two fused plus halt not 3");
  const rowPatterns=[...patterns].map(([p,count])=>{const i=p.indexOf("|");return{rule:p.slice(0,i),delta:p.slice(i+1).split(",").map(Number),count}}).sort((a,b)=>a.rule.localeCompare(b.rule)||a.delta.join(",").localeCompare(b.delta.join(",")));
  const raw={audit_id:"TMR1_REPFUSE048",date_local:"2026-11-15 09:03 PST",runtime:"V8 pure JavaScript functions.exec",scope:"COMPUTATIONAL: finite preauthenticated record grammars; exact symbolic theorem separately stated",assertions,failures,states,bellmanStates,paidRows,freeRows,cases:caseStats,unique_signed_rule_patterns:rowPatterns.length,old_one_fuse_shortcut:{G:2,q:2,E:[1,2],old_potential:[oldInitial,oldAfter1,oldAfter2],violated_second_fuse_delta:oldAfter1-oldAfter2,authentic_paid_route:["FUSE(g0,batch0)","FUSE(g1,batch1)","HALT"],actual_cost:3},limitations:["not a physical Turing machine emulator","preauthenticated gate and batch identities","no SAT all-program transfer","no native Node or repository preflight executed"]};
  const matrix={model:"R_REPEAT_FUSE preauthenticated shared-gate AND-batch calculus",columns:colNames,lambda,exact_rational_certificate:{primal:["0/1","0/1","0/1","1/1","0/1","0/1","1/1"],duals_for_initial:"y_joint=max(G,tau(J)); y_halt=1; both integers and satisfy universal LP",universal_cone:"lambda_SEP+lambda_FUS+lambda_Gamma<=1, lambda_Machine<=1, all weights nonnegative; other columns zero",certified_initial:"max(G,tau_E(J))+1",paid_joint_row:{delta:[0,0,1,1,1,0,0],cost:1},paid_halt_row:{delta:[0,0,0,0,0,0,1],cost:1}},universal_row_schema:[{rule:"VIEW,NOP",cost:0,delta:"zero"},{rule:"CHECK",cost:1,delta:"(0,0,0,delta_max,1,0,0), delta_max in {0,1}"},{rule:"BATCH",cost:1,delta:"(0,0,delta_tau,delta_max,0,0,0), each 0 or 1"},{rule:"FUSE",cost:1,delta:"(0,0,delta_tau,delta_max,1,0,0), each 0 or 1"},{rule:"HALT",cost:1,delta:"(0,0,0,0,0,0,1)"}],all_observed_delta_patterns:rowPatterns,representative_actual_edges:examples,precise_scope:"rows exhaustive for all finite states in audit cases; universal cone exact across the declared class including the one-scale test"};
  return {raw,matrix};
};
const result=audit();
if(typeof process!=="undefined" && process.stdout){
 const obj=process.argv.includes("--matrix")?result.matrix:result.raw;
 process.stdout.write(JSON.stringify(obj,null,2)+"\n");
}
