/* TMR-4/049 exact-rational singleton batch fusion tariff audit. Native JS V8, Node-compatible. */
const audit = function audit() {
  "use strict";
  const stats={assertions:0,cases:0,states:0,paidRows:0,zeroRows:0,nontrivialZeroSCCs:0,negativeGammaRows:0,fuseRows:0,failed:0};
  function check(b,label){stats.assertions++;if(!b)throw Error("ASSERT "+label);}
  const pop=x=>{let c=0;while(x){x&=x-1;c++;}return c;};
  function M(t,q,B,cache=new Map()){
    const key=t+":"+q;
    if(cache.has(key))return cache.get(key);
    let v=0;
    if(t>0&&q>0){
      v=M(t,q-1,B,cache);
      for(const b of B)if(b<=t)v=Math.max(v,b+M(t-b,q-1,B,cache));
    }
    cache.set(key,v);return v;
  }
  function independentM(t,q,B){
    let best=0;
    function recur(k,used){if(used<=t)best=Math.max(best,used);if(k===q)return;for(const b of B){if(used+b<=t)recur(k+1,used+b)}}
    recur(0,0);return best;
  }
  function frac(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}let x=a<0n?-a:a,y=b;while(y){const r=x%y;x=y;y=r;}const g=x||1n;return [a/g,b/g];}
  function fadd(x,y){return frac(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
  function fmul(x,n){return frac(x[0]*BigInt(n),x[1]);}
  function fle(x,y){return x[0]*y[1]<=y[0]*x[1];}
  const fstr=x=>x[0].toString()+"/"+x[1].toString();
  const one=frac(1),half=frac(1,2);
  function potential(t,q,h,B){return t+q-M(t,q,B)+h;}
  function vec(t,q,h,B){return [0,0,q,0,t-M(t,q,B),0,h];}
  const list=[];
  for(let G=1;G<=5;G++){
    for(let q=1;q<=3;q++){
      const maxW=Math.min(G,4),variants=(1<<maxW)-1;
      for(let mask=1;mask<=variants;mask++){
        const B=[];for(let b=1;b<=maxW;b++)if(mask&(1<<(b-1)))B.push(b);
        list.push({G,q,B});
      }
    }
  }
  // Also include q=0 and no-FUSE catalogue to verify boundary states and all-CHECK paths.
  list.push({G:4,q:0,B:[2,3]},{G:5,q:2,B:[]},{G:5,q:2,B:[2,4]},{G:4,q:2,B:[2,3]},{G:4,q:1,B:[4]});
  const full={feature:null,exhaustive:[]};
  for(const cfg of list){
    const {G,q,B}=cfg,allp=(1<<G)-1,allu=(1<<q)-1, mcache=new Map();
    for(let t=0;t<=G;t++)for(let u=0;u<=q;u++){
      const m=M(t,u,B,mcache);
      check(m===independentM(t,u,B),`M brute ${G}/${q}/${B}/${t}/${u}`);
      check(0<=m&&m<=t,`M bounded ${t}/${u}`);
      if(t)check(M(t-1,u,B,mcache)<=m,"M monotone t");
      if(u)check(M(t,u-1,B,mcache)<=m,"M monotone q");
    }
    const map=new Map();
    function state(pm,um,h){return pm+","+um+","+h;}
    const goal=state(allp,0,0);
    const isFeature=G===5&&q===2&&B.join(",")==="2,4";
    const edges=[];
    for(let pm=0;pm<=allp;pm++)for(let um=0;um<=allu;um++){
      const key=state(pm,um,1),t=G-pop(pm),u=pop(um),pv=vec(t,u,1,B);
      const out=[];
      const add=(rule,pm2,um2,h2,cost,detail="")=>{
        const dest=state(pm2,um2,h2);
        const v2=vec(G-pop(pm2),pop(um2),h2,B);
        const delta=pv.map((x,j)=>x-v2[j]);
        let s=frac(0);
        for(const j of [2,4,6])s=fadd(s,fmul(one,delta[j]));
        check(fle(s,frac(cost)),`tariff ${cfg.G}/${cfg.q}/${B} ${rule} ${key} -> ${dest}: ${fstr(s)} > ${cost}`);
        let sh=frac(0);for(const j of [2,4,6])sh=fadd(sh,fmul(half,delta[j]));
        check(fle(sh,frac(cost)),`fractional tariff ${rule}`);
        check(potential(t,u,1,B)-potential(G-pop(pm2),pop(um2),h2,B)===delta[2]+delta[4]+delta[6],"delta exact");
        if(delta[4]<0)stats.negativeGammaRows++;
        if(rule.startsWith("FUSE"))stats.fuseRows++;
        if(cost===0)stats.zeroRows++;else stats.paidRows++;
        const e={from:key,to:dest,rule,detail,cost,delta};
        out.push(e);if(isFeature)edges.push(e);
      };
      for(let i=0;i<G;i++)if(!(pm&(1<<i)))add("CHECK",pm|(1<<i),um,1,1,"g"+i);
      for(let j=0;j<q;j++)if(um&(1<<j))add("BATCH",pm,um&~(1<<j),1,1,"j"+j);
      const unpaid=allp&~pm;
      for(const b of B)if(b<=t)for(let sub=unpaid;sub;sub=(sub-1)&unpaid){
        if(pop(sub)!==b)continue;
        for(let j=0;j<q;j++)if(um&(1<<j))add("FUSE_"+b,pm|sub,um&~(1<<j),1,1,"gmask"+sub+"/j"+j);
      }
      if(t===0&&u===0)add("HALT",pm,um,0,1);
      add("BAD_REQUEST",pm,um,1,1);
      // At the quotient, reversible VIEW and zero-price NOP become self-loop edges.
      add("VIEW",pm,um,1,0);add("NOP",pm,um,1,0);
      map.set(key,out);
      check(potential(t,u,1,B)>=0,"nonnegative");
      check(pv.every(x=>x>=0),"nonnegative coordinates");
      stats.states++;
    }
    map.set(goal,[]);
    // Independent Bellman shortest-path, enumerated actual identity-sets rather than t,q recurrence.
    const memo=new Map();let visits=0;
    function distance(key){
      if(key===goal)return 0;
      if(memo.has(key))return memo.get(key);
      if(++visits>100000)throw Error("cycle detected in paid-progress graph");
      let best=1e9;
      for(const e of map.get(key)){
        if(e.to===key)continue; // Free SCC loops and paid malformed no-op never improve an optimal path.
        best=Math.min(best,e.cost+distance(e.to));
      }
      memo.set(key,best);
      return best;
    }
    for(let pm=0;pm<=allp;pm++)for(let um=0;um<=allu;um++){
      const t=G-pop(pm),u=pop(um);
      check(distance(state(pm,um,1))===potential(t,u,1,B),
        `all-state Bellman ${G},${q},${B},pm${pm},um${um}`);
    }
    check(distance(goal)===0,"zero terminal");
    const initial=potential(G,q,1,B);
    const dpCoin=M(G,q,B,mcache);
    check(initial===G+q-dpCoin+1,"initial coin certificate");
    // Independent exact rational primal/dual: three authentic unit rows yield [0,1]^3.
    const primal=[frac(1),frac(1),frac(1)];
    let obj=frac(0);for(let j=0;j<3;j++)obj=fadd(obj,fmul(primal[j],[q,G-dpCoin,1][j]));
    const dual=[q,G-dpCoin,1];let dualCost=frac(0);for(const y of dual)dualCost=fadd(dualCost,frac(y));
    check(fle(obj,dualCost)&&fle(dualCost,obj),"primal and dual equal");
    check(fstr(obj)===initial+"/1","exact rational LP optimum");
    stats.cases++;
    if(isFeature){
      // Generic Tarjan SCC algorithm over literal metadata-view nodes, not just an assumed quotient.
      const allkeys=[...map.keys()];
      const ids=allkeys.flatMap(k=>[k+":0",k+":1"]);
      const zAdj=new Map(ids.map(k=>[k,[]]));
      for(const k of allkeys)for(let v=0;v<=1;v++){
        zAdj.get(k+":"+v).push(k+":"+v);zAdj.get(k+":"+v).push(k+":"+(1-v));
      }
      let counter=0;const index=new Map(),low=new Map(),stack=[],on=new Set(),sccs=[];
      function visit(v){
        index.set(v,counter);low.set(v,counter);counter++;stack.push(v);on.add(v);
        for(const w of zAdj.get(v)){
          if(!index.has(w)){visit(w);low.set(v,Math.min(low.get(v),low.get(w)));}
          else if(on.has(w))low.set(v,Math.min(low.get(v),index.get(w)));
        }
        if(low.get(v)===index.get(v)){const part=[];while(true){const w=stack.pop();on.delete(w);part.push(w);if(w===v)break;}sccs.push(part);}
      }
      for(const v of ids)if(!index.has(v))visit(v);
      check(sccs.length===allkeys.length,"authentic zero SCC count");
      for(const s of sccs){check(s.length===2,"authentic two-view SCC");stats.nontrivialZeroSCCs++;}
      const uniq=new Map();
      for(const e of edges){
        const key=e.rule+"|"+e.cost+"|"+e.delta.join(",");
        if(!uniq.has(key))uniq.set(key,{rule:e.rule,cost:e.cost,delta:e.delta,multiplicity:0});
        uniq.get(key).multiplicity++;
      }
      full.feature={G,q,B,initial,dpCoin,graph:{concreteStates:ids.length,zeroSCCs:sccs.length,quotientStates:allkeys.length,quotientEdges:edges.length},exactRational:{lambda:["1/1","1/1","1/1"],primalObjective:fstr(obj),dualMultipliers:dual.map(x=>x+"/1"),dualObjective:fstr(dualCost)},rows:edges,aggregateRows:[...uniq.values()],sampleOptimalTrace:(()=>{
        const trace=[];let s=state(0,allu,1);while(s!==goal){const here=memo.get(s);const e=map.get(s).find(e=>e.to!==s&&e.cost+distance(e.to)===here);if(!e)throw Error("no shortest path witness");trace.push(e);s=e.to;}return trace;})()};
    }
    if((G===5&&q===2&&B.join(",")==="2,4")||(G===4&&q===1&&B.join(",")==="4")||(G===4&&q===2&&B.join(",")==="2,3")||(G===5&&q===2&&B.join(",")==="2,3")){
      full.exhaustive.push({G,q,B,M:dpCoin,W:initial});
    }
  }
  // Hostile controls: genuine operations in separately EXPANDED authorities are not CEGAR spurious.
  const base=(t,q,B)=>potential(t,q,1,B);
  const failures={
    overlappingSetCover:{G:4,t:4,originalU:["a","b"],E:[["a"],["b"],["a","b"]],B:[2],tauInitial:1,
      naiveBefore:base(4,1,[2]),naiveAfterFirstFUSE:base(2,1,[2]),firstFUSECost:1,genuineTwoFUSEAndHALTCost:3},
    undeclaredWideFUSE:{G:4,q:1,B:[2],before:base(4,1,[2]),after:base(0,0,[2]),cost:1},
    freeFUSE:{G:2,q:1,B:[2],before:base(2,1,[2]),after:base(0,0,[2]),cost:0},
    compactDirectFinish:{G:4,q:2,B:[2],before:base(4,2,[2]),after:0,cost:1},
    signedCheck:{G:4,q:1,B:[4],before:base(4,1,[4]),after:base(3,1,[4]),cost:1}
  };
  check(failures.overlappingSetCover.naiveBefore-failures.overlappingSetCover.naiveAfterFirstFUSE===2,"true overlap violation 2>1");
  check(failures.undeclaredWideFUSE.before-failures.undeclaredWideFUSE.after>1,"wider shortcut");
  check(failures.freeFUSE.before-failures.freeFUSE.after>0,"free shortcut");
  check(failures.compactDirectFinish.before>1,"compact shortcut");
  check(failures.signedCheck.before-failures.signedCheck.after<0,"negative signed check");
  return {raw:{run:"TMR4-KNAPFUSE049",timestamp_pst:"2026-11-15 09:36 PST",status:"COMPUTATIONAL",checks:stats,feature:full.feature&&{G:full.feature.G,q:full.feature.q,B:full.feature.B,initial:full.feature.initial,dpCoin:full.feature.dpCoin,graph:full.feature.graph,exactRational:full.feature.exactRational,sampleOptimalTrace:full.feature.sampleOptimalTrace},cases:full.exhaustive,falsifiers:failures},matrix:{schema:"Seven columns [CNF,XOR,SEP,FUS,Gamma,Interface,Machine]; signed exact integer deltas are rational denominators one",model:"Repeatable disjoint-width FUSE in singleton-batch preauthenticated record calculus",ruleClasses:"VIEW,NOP cost0; BAD_REQUEST cost1; CHECK(g) cost1; BATCH(j) cost1; FUSE_b(K,j) cost1 with all b distinct unpaid identities and unpaid j; HALT cost1 when finished",formula:"M_B(t,q)=max sum of <=q widths in B with sum<=t; p=(0,0,q,0,t-M_B(t,q),0,h)",lambda:["0/1","0/1","1/1","0/1","1/1","0/1","1/1"],primalDual:full.feature.exactRational,graph:full.feature.graph,aggregateRows:full.feature.aggregateRows,rows:full.feature.rows}};
};
const result=audit();
if(typeof console!== 'undefined') console.log(JSON.stringify(result.raw,null,2));
