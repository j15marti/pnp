'use strict';
// TMR-5/008 independent V8 reproducer, identical function executed for raw result.
const runAudit=function runAudit(){
  let seed=0x5A7E008; const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
  const bitList=(mask,L)=>Array.from({length:L},(_,i)=>i).filter(i=>(mask&(1<<i))!==0);
  const potential=(heads,seen,sets)=>{let best=0;for(const D of sets){if(D.some(p=>seen&(1<<p)))continue;let dist=1e9;for(const h of heads)for(const p of D)dist=Math.min(dist,Math.abs(p-h));best=Math.max(best,1+dist);}return best;};
  function moveVectors(heads,L){let x=[[]];for(const h of heads){const nxt=[];for(let p=Math.max(0,h-1);p<=Math.min(L,h+1);p++)for(const a of x)nxt.push([...a,p]);x=nxt;}return x;}
  function bfs(L,heads0,sets){const Q=[{h:heads0,v:0,t:0}],seen=new Set([heads0.join(",")+":0"]);let ptr=0;while(ptr<Q.length){const x=Q[ptr++];if(sets.every(D=>D.some(p=>x.v&(1<<p))))return [x.t,ptr];let v=x.v;for(const p of x.h)if(p<L)v|=(1<<p);for(const h of moveVectors(x.h,L)){const key=h.join(",")+":"+v;if(!seen.has(key)){seen.add(key);Q.push({h,v,t:x.t+1});}}}throw Error("Unreachable");}
  let stats={hypergraphs:0,initial_exact_BFS:0,abstract_states:0,paid_edges:0,terminal_states:0,failures:0},cases=[];
  function edgeAudit(L,nh,sets){
    let hs=[[]];for(let i=0;i<nh;i++){const a=[];for(const q of hs)for(let p=0;p<=L;p++)a.push([...q,p]);hs=a;}
    for(const h of hs)for(let v=0;v<(1<<L);v++){
      stats.abstract_states++; const old=potential(h,v,sets);
      const available=[...new Set(h.filter(p=>p<L))];
      const moves=moveVectors(h,L);
      for(let sub=0;sub<(1<<available.length);sub++){let nv=v;for(let j=0;j<available.length;j++)if(sub&(1<<j))nv|=1<<available[j];
        for(const hh of moves){if(old>1+potential(hh,nv,sets))throw Error("Potential violation");stats.paid_edges++;}
      }
      if(sets.every(D=>D.some(p=>v&(1<<p)))){if(old!==0)throw Error("Goal violation");stats.terminal_states++;}
    }
  }
  for(let L=2;L<=5;L++){
    const universe=Array.from({length:(1<<L)-1},(_,i)=>bitList(i+1,L));
    let collection=universe.map(D=>({sets:[D],kind:"single"}));
    if(L<=3)for(let a=0;a<universe.length;a++)for(let b=a+1;b<universe.length;b++)collection.push({sets:[universe[a],universe[b]],kind:"pair"});
    for(let k=0;k<18;k++){let n=1+(rnd()%Math.min(5,universe.length)),inds=new Set();while(inds.size<n)inds.add(rnd()%universe.length);collection.push({sets:[...inds].map(i=>universe[i]),kind:"seeded"});}
    for(let h=1;h<=2;h++)for(const {sets,kind} of collection){
      const initial=potential(Array(h).fill(0),0,sets),exact=1+Math.max(...sets.map(D=>Math.min(...D))),[dist,expanded]=bfs(L,Array(h).fill(0),sets);
      if(initial!==exact||dist!==exact||exact>L)throw Error("Distance disagreement");
      stats.hypergraphs++;stats.initial_exact_BFS++;
      if(L<=3||(L===4&&kind==="seeded"&&h===1)||(L===5&&kind==="seeded"&&h===2&&stats.hypergraphs%3===0))edgeAudit(L,h,sets);
      if(cases.length<16||(L===5&&kind==="seeded"&&h===2&&cases.length<28))cases.push({L,heads:h,supports:sets,initial,bfs:dist,explored:expanded});
    }
  }
  let pdisp=potential([5],0,[[0],[10]]),[ddisp,vdisp]=bfs(11,[5],[[0],[10]]);
  if(pdisp!==6||ddisp!==16)throw Error("Dispersion control");
  let before=potential([0],0,[[10]]),after=potential([10],1<<10,[[10]]);
  if(before!==11||after!==0||before<=1+after)throw Error("INDEX control");
  return {tag:"TMR5-SPATIAL-CEILING008",time_PST:"2026-11-13 20:46 PST",
    implementation:"independent hosted V8 JavaScript, no imported project source",seed:"0x5A7E008",model:"h=1 or 2 left-aligned local pre-read heads, finite MAY graph",
    statistics:stats,cases_sample:cases,hostile_dispersion:{L:11,start:[5],supports:[[0],[10]],Phi:pdisp,BFS_shortest:ddisp,expanded:vdisp},
    hostile_free_index:{L:11,supports:[[10]],Phi_before:before,Phi_after:after,putative_jump_cost:1,violates_edge_inequality:before>1+after},
    scope:"COMPUTATIONAL: abstract state/edge enumeration and BFS, no physical SAT TM simulator"};
};
console.log(JSON.stringify(runAudit(),null,2));
