#!/usr/bin/env node
"use strict";
function audit() {
  const fail=[], results=[];
  let assertions=0, edgesChecked=0, zeroEdges=0;
  function ok(condition,msg) { assertions++; if(!condition) fail.push(msg); }
  function pop(x) { let n=0; while(x){n+=x&1; x>>>=1;} return n; }
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const cases=[
    {name:"fano",n:7,edges:fano,den:3,dual:1,tau:3},
    {name:"triangle",n:3,edges:[[0,1],[1,2],[0,2]],den:2,dual:1,tau:2},
    {name:"full",n:7,edges:[[0,1,2,3,4,5,6]],den:7,dual:7,tau:1},
    {name:"singleton",n:7,edges:Array.from({length:7},(_,i)=>[i]),den:1,dual:1,tau:7}
  ];
  for (const c of cases) {
    const n=c.n, den=c.den, G=3, full=(1<<n)-1, allG=(1<<G)-1;
    const masks=c.edges.map(e=>e.reduce((z,i)=>z|(1<<i),0));
    const ranks=Array.from({length:n},(_,i)=>4n**BigInt(i+5)-1n);
    for(const d of ranks) ok(d>0n,"rank invalid "+c.name);
    for(const mask of masks) ok(pop(mask)<=den,"primal activation inequality "+c.name);
    for(let j=0;j<n;j++) ok(masks.filter(m=>(m&(1<<j))!==0).length*c.dual>=den,"dual covering inequality "+c.name);
    ok(n===masks.length*c.dual,"fractional primal/dual mismatch "+c.name);
    const dp=Array(1<<n).fill(100000); dp[0]=0;
    for(let u=1;u<=full;u++)for(const m of masks) if(u&m) dp[u]=Math.min(dp[u],dp[u&~m]+1);
    ok(dp[full]===c.tau,"integer covering mismatch "+c.name);
    const phi=(u,p,h)=>pop(u)+den*(G-pop(p)+h);
    for(let p=0;p<=allG;p++)for(let u=0;u<=full;u++)for(let h=0;h<=1;h++){
      if(h===0&&(p!==allG||u!==0))continue;
      for(let view=0;view<2;view++){
        const before=phi(u,p,h);
        function edge(name,u2,p2,h2,cost,expected) {
          const delta=before-phi(u2,p2,h2);
          assertions++;edgesChecked++;
          if(delta>den*cost)fail.push(c.name+" "+name+" excessive discharge "+delta);
          if(cost===0){zeroEdges++;ok(delta===0,"zero closure discharge");}
          if(expected!==null)ok(delta===expected,c.name+" "+name+" wrong delta "+delta);
        }
        edge("VIEW",u,p,h,0,0);edge("NOP",u,p,h,0,0);
        if(h===0){ok(before===0,"goal nonzero");continue;}
        for(let g=0;g<G;g++)if(!(p&(1<<g)))edge("CHECK",u,p|(1<<g),h,1,den);
        if(p===allG){
          for(const mask of masks)if(u&mask)edge("ACTIVATE_BATCH",u&~mask,p,h,1,pop(u&mask));
          if(u===0)edge("HALT",0,p,0,1,den);
        }
      }
    }
    results.push({case:c.name,scales:n,ranks:ranks.map(String),activationEdges:c.edges,
      primalScaleWeights:Array.from({length:n},(_,i)=>"1/("+den+"*(4^"+(i+5)+"-1))"),
      dualBatchWeights:c.edges.map(()=>c.dual+"/"+den),
      fractionalCost:n+"/"+den,minimumBatches:dp[full],
      dynamicPotentialInitialWithG3:(4*den+n)+"/"+den,
      trueRecordCostWithG3:G+dp[full]+1});
  }
  const raw={status:fail.length?"FAIL":"PASS",assertions,edgesChecked,zeroEdges,failures:fail,results,
    theorem:"Exact tariff optimum G+1+fractional hyperedge cover; authentic minimum G+1+integer hyperedge cover",
    scope:"Explicit authenticated record calculus only, not an unrestricted SAT or Turing-machine lower bound"};
  if(fail.length)throw Error(JSON.stringify(raw));
  return raw;
}
if(typeof module!=="undefined"&&module.exports){module.exports={audit}; if(require.main===module)console.log(JSON.stringify(audit(),null,2));}
