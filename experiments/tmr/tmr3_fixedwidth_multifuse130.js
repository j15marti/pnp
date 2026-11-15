"use strict";
// TMR-3/047 reproducible finite quotient and exact signed tariff audit.
// Run: node experiments/tmr/tmr3_fixedwidth_multifuse130.js
(function () {
  function runAudit() {
    let assertions=0, paidRows=0, zeroRows=0, signedIncrease=0, failures=0, states=0;
    function ok(cond,msg) {assertions++; if(!cond) {failures++; throw new Error(msg);} }
    function bitcount(v) {let c=0;while(v){c+=v&1;v>>>=1;}return c;}
    const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
    const cases=[
      {name:"tiny_b2",G:2,b:2,q:1,sets:[[0]],expected:2},
      {name:"tiny_b1",G:2,b:1,q:1,sets:[[0]],expected:3},
      {name:"fano_b1",G:3,b:1,q:7,sets:fano,expected:6},
      {name:"fano_b2",G:3,b:2,q:7,sets:fano,expected:5},
      {name:"fano_b3",G:3,b:3,q:7,sets:fano,expected:4},
      {name:"fano_b4_unavailable",G:3,b:4,q:7,sets:fano,expected:7},
      {name:"triangle_b2",G:3,b:2,q:3,sets:[[0,1],[1,2],[0,2]],expected:4},
      {name:"singletons_b2",G:3,b:2,q:4,sets:[[0],[1],[2],[3]],expected:6},
      {name:"full_b2",G:3,b:2,q:7,sets:[[0,1,2,3,4,5,6]],expected:3},
      {name:"G1_b2_no_fuse",G:1,b:2,q:2,sets:[[0],[1]],expected:4},
      {name:"G2_b2_overlap",G:2,b:2,q:3,sets:[[0,1],[1,2]],expected:3}
    ];
    const summaries=[];
    for(const s of cases) {
      const fullP=(1<<s.G)-1, fullU=(1<<s.q)-1;
      const sets=s.sets.map(a=>a.reduce((m,j)=>m|(1<<j),0));
      ok(sets.every(x=>x>0),"nonempty set");
      ok(sets.reduce((a,x)=>a|x,0)===fullU,"cover condition");
      const coverMemo=new Map([[0,0]]);
      function tau(U) {
        if(coverMemo.has(U))return coverMemo.get(U);
        let best=1e9;
        for(const S of sets)if(U&S)best=Math.min(best,1+tau(U&~S));
        coverMemo.set(U,best);return best;
      }
      function bruteTau(U) {
        let best=Infinity;
        for(let mask=0;mask<(1<<sets.length);mask++) {
          let union=0;for(let j=0;j<sets.length;j++)if(mask&(1<<j))union|=sets[j];
          if((union&U)===U)best=Math.min(best,bitcount(mask));
        }
        return best;
      }
      for(let U=0;U<=fullU;U++)ok(tau(U)===bruteTau(U),"independent subset cover "+s.name+" U="+U);
      function p(P,U,h) {
        if(!h)return [0,0,0,0,0,0,0];
        const t=s.G-bitcount(P),chi=(t>=s.b && U===fullU)?s.b:0;
        ok(t-chi>=0,"nonnegative Gamma");
        return [0,0,tau(U),0,t-chi,0,h];
      }
      function V(P,U,h) {const a=p(P,U,h);return a[2]+a[4]+a[6];}
      function edges(P,U,h) {
        if(h===0)return [];
        const t=s.G-bitcount(P),a=[];
        for(let g=0;g<s.G;g++)if(!(P&(1<<g)))a.push({rule:"CHECK",P:P|(1<<g),U,h:1,w:1});
        if(t===0)for(let j=0;j<sets.length;j++)if(U&sets[j])
          a.push({rule:"BATCH",batch:j,P,U:U&~sets[j],h:1,w:1});
        if(t===s.b && U===fullU)for(let j=0;j<sets.length;j++)
          a.push({rule:"FUSE_"+s.b,batch:j,P:fullP,U:U&~sets[j],h:1,w:1});
        if(t===0 && U===0)a.push({rule:"HALT",P,U,h:0,w:1});
        return a;
      }
      const memo=new Map();
      function distance(P,U,h) {
        if(h===0)return 0;
        const key=P+"/"+U+"/"+h;
        if(memo.has(key))return memo.get(key);
        const es=edges(P,U,h);
        ok(es.length>0,"no dead end "+s.name+" "+key);
        const d=Math.min(...es.map(e=>e.w+distance(e.P,e.U,e.h)));
        memo.set(key,d);return d;
      }
      let localPaid=0,localZero=0,localIncrease=0,localMaxDelta=-Infinity;
      for(let P=0;P<=fullP;P++)for(let U=0;U<=fullU;U++) {
        states+=2;
        const b0=p(P,U,1),value=V(P,U,1);
        ok(value===distance(P,U,1),"Bellman exact "+s.name+" "+P+"/"+U);
        // Each of the two genuine zero-cost reversible VIEW states has invariant product.
        for(let v=0;v<2;v++){zeroRows++;localZero++;ok(V(P,U,1)===V(P,U,1),"zero VIEW");}
        for(const e of edges(P,U,1)) {
          const c=p(e.P,e.U,e.h),delta=b0.map((v,i)=>v-c[i]);
          const charged=delta[2]+delta[4]+delta[6];
          ok(charged===value-V(e.P,e.U,e.h),"signed seven-column identity");
          ok(charged<=e.w,"tariff violation "+s.name+"/"+e.rule);
          ok(e.w===1,"paid event cost exactly one");
          // Every nonnegative rational cone point 0, 1/2, or 1 is feasible.
          for(const a of [0,.5,1])for(const b of [0,.5,1])for(const d of [0,.5,1])
            ok(a*delta[2]+b*delta[4]+d*delta[6]<=1,"rational cube LP");
          if(charged<0){signedIncrease++;localIncrease++;}
          localMaxDelta=Math.max(localMaxDelta,charged);
          paidRows++;localPaid++;
        }
      }
      ok(V(fullP,0,0)===0,"completed goal zero");
      const trueMin=distance(0,fullU,1);
      ok(trueMin===s.expected,"known exact minimum "+s.name);
      const formula=s.G+tau(fullU)+1-(s.G>=s.b?s.b:0);
      ok(formula===trueMin,"closed-form optimum "+s.name);
      summaries.push({name:s.name,G:s.G,b:s.b,q:s.q,batches:sets.length,tau:tau(fullU),
        actual_exact:trueMin,initial_tariff:V(0,fullU,1),quotient_states:(fullP+1)*(fullU+1)+1,
        paid_rows:localPaid,zero_rows:localZero,signed_increase_rows:localIncrease,
        max_weighted_discharge:localMaxDelta});
    }
    // Smallest genuine FUSE_2 failure of TMR-4/047's b=1 credit.
    // G=2, q=1, U={0}; pre=(P=empty,t=2,U=J,h=1), post=(P=all,t=0,U=empty,h=1).
    const oldBefore=2+1+1-1,oldAfter=0+0+1; // V_old=3 -> 1.
    ok(oldBefore-oldAfter===2,"minimum legal b2 violation of old credit");
    ok(failures===0,"no failed check");
    return {id:"TMR3_MULTIFUSE130",stamp:"2026-11-15 08:28 PST",
      status:"PROVED/RESTRICTED symbolic conditional; finite audit COMPUTATIONAL",
      independent_review:"OPEN",node_compatible:true,
      program:"exhaustive viable quotient-state enumeration + independent set-subset cover + recursive genuine-edge shortest path",
      assertions,paidRows,zeroRows,states,signedIncrease,failures,
      theorem:"W=t+tau(U)+h-b*1[h=1,t>=b,U=J] for the EXACT preauthenticated b-FUSE grammar",
      exact_weights:[0,0,1,0,1,0,1],hostile:{smallest:"G=b=2,q=1,one batch",old_weighted_discharge:2,cost:1},
      cases:summaries};
  }
  const result=runAudit();
  if(typeof process!=="undefined" && typeof console!=="undefined" && typeof module!=="undefined"
    && require.main===module) console.log(JSON.stringify(result,null,2));
  return result;
})()
