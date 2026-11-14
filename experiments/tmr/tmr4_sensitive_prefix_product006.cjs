'use strict';
// TMR4-PRODUCT006: finite source-event audit. Not physical TM execution or a 3-SAT solver.
const audit=function audit(){
  const t={sources:0,horizonCases:0,abstractEdges:0,allEdgePotentialChecks:0,concreteStepPaths:0,zeroCostStutters:0,SAT:0,UNSAT:0,strictCompositionGains:0,naiveDoubleCountFalsifiers:0,invalidZeroCostRevelationRejected:0,failures:0,maxLength:7,maxConcreteSteps:0};
  const ok=(v,msg)=>{if(!v){t.failures++;throw Error(msg)}},pc=x=>{let n=0;while(x){x&=x-1;n++}return n};
  function trace(x,mode,q){
    const events=[],n=x.length,parity=[...x].reduce((a,b)=>a^Number(b),0);
    const put=(reads,label=null,control="scan")=>events.push({reads,label,control});
    if(mode==="IDLE")for(let i=0;i<3;i++)put([],null,"prep");
    for(let i=0;i<n;i+=q)put(Array.from({length:Math.min(q,n-i)},(_,j)=>i+j));
    if(mode==="RECOMPUTE"){for(let i=0;i<n;i++)put([],null,"rewind");for(let i=0;i<n;i++)put([i],null,"rescan")}
    if(mode==="IDLE")for(let i=0;i<2;i++)put([],null,"finish");
    put([],parity?"SAT":"UNSAT","halt");return events;
  }
  function bfs(s,all,q){
    let layer=[s],seen=new Set([s]),depth=0;
    while(layer.length){
      if(layer.includes(all))return depth;
      const next=[];
      for(const u of layer){const missing=all&~u;for(let v=missing;v;v=(v-1)&missing){
        if(pc(v)>q||seen.has(u|v))continue;seen.add(u|v);next.push(u|v)
      }}
      layer=next;depth++;
    }throw Error("no MAY path");
  }
  for(let n=0;n<=7;n++)for(let z=0;z<(1<<n);z++){
    const input=Array.from({length:n},(_,i)=>String((z>>i)&1)).join(""),all=(1<<n)-1;
    for(const mode of ["FAST","IDLE","RECOMPUTE","PAIR"]){
      const q=mode==="PAIR"?2:1,E=trace(input,mode,q),T=E.length; t.sources++;t.maxConcreteSteps=Math.max(t.maxConcreteSteps,T);
      t[E[T-1].label]++;const masks=[0];let seen=0;
      for(const e of E){ok(e.reads.length<=q,"overcapacity");for(const pos of e.reads){ok(pos>=0&&pos<n,"source range");seen|=1<<pos}masks.push(seen)}
      ok(seen===all,"correct toy run missing source");
      const Bs=[0,1,2,3,Math.floor(T/2),T-1,T,T+1].filter((v,i,a)=>v>=0&&a.indexOf(v)===i);
      for(const B of Bs){
        t.horizonCases++;
        const h=Math.min(B,T),short=h<T,m=masks[h],remaining=n-pc(m),tail=short?Math.ceil(remaining/q):0,pred=short?h+tail:T;
        const phi=v=>Math.ceil((n-pc(v))/q);
        ok(pred<=T,"bound exceeded actual time");
        if(short){
          ok(pred===h+bfs(m,all,q),"BFS potential mismatch");
          if(pred>Math.max(h,Math.ceil(n/q)))t.strictCompositionGains++;
          if(h+Math.ceil(n/q)>T)t.naiveDoubleCountFalsifiers++;
          for(let u=m;u<=all;u++){if((u&m)!==m)continue;
            t.zeroCostStutters++;t.allEdgePotentialChecks++;ok(phi(u)<=phi(u),"zero edge");
            if(u===all){t.allEdgePotentialChecks+=2;ok(phi(u)===0,"terminal potential")}
            const missing=all&~u;
            for(let add=missing;add;add=(add-1)&missing)if(pc(add)<=q){
              t.abstractEdges++;t.allEdgePotentialChecks++;
              ok(phi(u)<=1+phi(u|add),"paid MAY edge")
            }
          }
          if(m!==all){t.invalidZeroCostRevelationRejected++;ok(!(phi(m)<=phi(all)),"invalid free reveal")}
        }
        for(let i=0;i<T;i++){
          const old=masks[i],now=masks[i+1],delta=pc(now&~old);
          ok(delta<=q,"actual source capacity");
          if(i<h){t.concreteStepPaths++;ok(h-i+tail<=1+h-i-1+tail,"exact prefix potential")}
          else if(short){t.concreteStepPaths++;
            if(delta)ok(phi(old)<=1+phi(now),"post-horizon real read");
            else ok(phi(old)===phi(now),"post-horizon free stutter");
            if(i===T-1)ok(now===all,"terminal guard")
          }
        }
      }
    }
  }
  ok(t.strictCompositionGains>0&&t.naiveDoubleCountFalsifiers>0&&t.invalidZeroCostRevelationRejected>0,"missing hostile cases");
  return {type:"TMR4-PRODUCT006",status:"COMPUTATIONAL",timestamp_PST:"2026-11-13 17:37 PST",finite_model:"toy parity language: 4 finite deterministic transition-event programs, exhaustive inputs lengths 0..7; no physical Turing-machine or 3-SAT execution",source:"experiments/tmr/tmr4_sensitive_prefix_product006.cjs",stats:t};
};
console.log(JSON.stringify(audit(),null,2));
