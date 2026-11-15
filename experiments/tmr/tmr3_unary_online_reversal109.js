'use strict';

// Native Node.js and connector V8-compatible deterministic audit. No packages.
function audit(){
  let assertions=0, transitions=0, cases=0, totalFallbacks=0, directOptima=0;
  const check=(v,msg)=>{ assertions++; if(!v) throw Error(msg); };
  const run=(n,k,m=1)=>{
    check(n>=2 && (k===0||k>=2),"parameters");
    const src="1".repeat(n)+"#", W=new Map(), outputs=Array(m).fill(null), visited=new Set([0]), seen=new Set();
    let i=0,w=0,T=0,halted=false, resetAt=0, resetCount=0, readEvents=0;
    const trace=[];
    function step(tag,opts={}){
      const {di=0,dw=0,write=undefined,mark=false,halt=false,expect=undefined}=opts;
      check(!halted && Math.abs(di)<=1&&Math.abs(dw)<=1,"step cost/moves");
      check(i>=0&&i<src.length&&w>=0, "head bounds");
      const sym=src[i], beforeI=i,beforeW=w;
      if(expect!==undefined)check(sym===expect,"read mismatch "+tag);
      seen.add(i);readEvents++;
      if(write!==undefined){
        if(write===null)W.delete(w); else W.set(w,write);
      }
      if(mark)for(let j=0;j<m;j++)outputs[j]="@";
      i+=di;w+=dw;visited.add(w);T++;transitions++;
      check(i>=0&&w>=0, "illegal negative head");
      if(halt)halted=true;
      trace.push({tag,time:T,read:sym,ipos:beforeI,wpos:beforeW,wdelta:dw,write:write===undefined?"-":write,mark,halt});
    }
    function finish(){
      check(halted,"not halted");
      check(seen.size===n+1,"source not fully authenticated");
      check(seen.has(n),"EOF never reached");
      check(i>=0&&w===0,"terminal W head");
      for(let j=0;j<n;j++)check(W.get(j)===(j===0?"1":"g"),"wrong W["+j+"]");
      check(W.size===n,"unexpected W cells");
      for(let j=0;j<m;j++)check(outputs[j]==="@","missing marker");
      const post=trace.filter(x=>x.time>resetAt);
      const staged=post.find(x=>x.write==="0"&&x.wpos===0);
      const activated=post.find(x=>x.write==="1"&&x.wpos===0);
      check(!!staged&&!!activated&&staged.time<activated.time,"header stages");
      const gates=post.filter(x=>x.write==="g"&&x.wpos>=1);
      check(gates.length===n-1,"distinct mandatory gate writes");
      check(new Set(gates.map(x=>x.wpos)).size===n-1,"shared gate identity overcount");
      check(gates.every(x=>x.time<activated.time),"gate after activation");
      check(post.some(x=>x.read==="#"&&x.ipos===n),"original EOF not read in final run");
      check(trace.at(-1).halt && trace.at(-1).time>activated.time,"distinct HALT");
      check(trace.every(x=>Math.abs(x.wdelta)<=1),"W head jump");
      return {n,k,m,T,resetCount,writableCellsVisited:visited.size+m,distinctInputCells:seen.size,readEvents,trace};
    }
    function base(){
      check(i===0&&w===0&&W.size===0&&outputs.every(x=>x===null),"bad clean reset");
      step("BASE_INIT",{expect:"1",write:"0",di:1});
      step("BASE_SEEK",{expect:"1",di:1,dw:1});
      while(src[i]==="1"){
        step("BASE_MID",{expect:"1",write:"g",di:1,dw:1});
      }
      step("BASE_EOF_WRITE",{expect:"#",write:"g",dw:-1});
      while(w>0)step("BASE_BACK",{expect:"#",dw:-1});
      step("BASE_ACT",{expect:"#",write:"1",mark:true});
      step("BASE_HALT",{expect:"#",halt:true});
    }
    function resetAndRun(){
      resetCount++; totalFallbacks++;
      // Explicit finite-control cleanup for this fixed k. Never teleport either head.
      while(w<k)step("RESET_RIGHT",{dw:1,di:i>0?-1:0});
      while(w>0)step("RESET_LEFT",{dw:-1,di:i>0?-1:0,write:null});
      while(i>0)step("RESET_SOURCE",{di:-1});
      step("RESET_HEADER",{write:null});
      check(W.size===0&&w===0&&i===0,"incomplete cleanup");
      resetAt=T;
      base();
    }
    if(k===0)base();else{
      let miss=false;
      for(let j=1;j<=k;j++){
        if(src[i]!=="1"){
          step("MISS_SHORT",{expect:"#"});
          miss=true;break;
        }
        if(j===1)step("FAST_INIT",{expect:"1",write:"0",di:1,dw:1});
        else if(j===k)step("FAST_LAST_GATE",{expect:"1",write:"g",di:1,dw:-1});
        else step("FAST_GATE",{expect:"1",write:"g",di:1,dw:1});
      }
      if(!miss){
        if(src[i]!=="#"){
          step("MISS_LONG",{expect:"1"});miss=true;
        } else if(k===2){
          step("FAST_EOF_ACT",{expect:"#",write:"1",mark:true});
          step("FAST_HALT",{expect:"#",halt:true});
        } else {
          step("FAST_EOF_BACK",{expect:"#",dw:-1});
          while(w>0)step("FAST_BACK",{expect:"#",dw:-1});
          step("FAST_ACT",{expect:"#",write:"1",mark:true});
          step("FAST_HALT",{expect:"#",halt:true});
        }
      }
      if(miss)resetAndRun();
    }
    cases++;
    const result=finish();
    if(k>0&&n===k){check(T===2*n,"fast cost 2n");directOptima++;}
    if(k===0)check(T===2*n+1,"uniform cost 2n+1");
    if(k>0&&n!==k)check(T>2*n,"wrong-length speculative optimum");
    return result;
  };
  const small=[];
  for(let m=1;m<=3;m++){
    for(let k=0;k<=18;k++){
      if(k===1)continue;
      let optimumCount=0;
      for(let n=2;n<=42;n++){
        const o=run(n,k,m);
        if(o.T===2*n)optimumCount++;
        if(n<=4&&[0,2,3,4].includes(k)&&m===1)small.push({n,k,T:o.T,steps:o.trace.map(z=>z.tag)});
      }
      check(optimumCount===(k>0?1:0),"one-optimum property");
    }
  }
  const rowsFor=(n)=>{
    const events=run(n,n,1).trace;
    const deltas={
      FAST_INIT:[1,0,1,0],
      FAST_GATE:[0,1,1,0],
      FAST_LAST_GATE:[0,1,1,0],
      FAST_EOF_BACK:[0,0,1,1],
      FAST_BACK:[0,0,0,1],
      FAST_ACT:[1,0,0,0],
      FAST_EOF_ACT:[1,0,1,0],
      FAST_HALT:[0,0,0,1]
    };
    const sums=[0,0,0,0];
    for(const e of events){
      const d=deltas[e.tag];
      check(!!d,"unknown fast rule");
      const charge=d[0]+d[1]+d[3];
      check(charge<=1, "tariff violation");
      for(let z=0;z<4;z++)sums[z]+=d[z];
    }
    check(sums.join()===[2,n-1,n+1,n-1].join(),"matrix does not telescope");
    check(sums[0]+sums[1]+sums[3]===2*n,"initial LP");
    return {n,initial:{fusion:2,gamma:n-1,interface:n+1,machine:n-1},sumDischarge:sums,primalWeights:{fusion:1,gamma:1,interface:0,machine:1},primalObjective:2*n,dualCost:events.length,rows:Object.entries(deltas).map(([name,d])=>({name,delta:[0,0,0,...d],cost:1,multiplicity:events.filter(e=>e.tag===name).length})).filter(x=>x.multiplicity)};
  };
  const matrices=[2,3,4,7,18].map(rowsFor);
  return {scope:"fixed local multi-tape ordered record service",model:"one original read-only head; one local W head; m fixed marker tapes; one native microstep cost 1",runs:cases,assertions,transitions,fallbackRuns:totalFallbacks,optimalSpecializedRuns:directOptima,failures:0,small,matrices};
}

console.log(JSON.stringify(audit(),null,2));
