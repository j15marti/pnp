"use strict";
// The runAudit function below is the EXACT evaluated V8 source function.
function runAudit(){
 "use strict";
 let checks=0;const ok=(b,m)=>{checks++;if(!b)throw Error("FAIL: "+m)};
 const n=3,all=255,sourceA=[],sourceB=[];
 for(let i=0;i<n;i++){const ay=n+2*i+1,az=ay+1,by=n+2*n+2*i+1,bz=by+1;
  for(const sy of [1,-1])for(const sz of [1,-1]){sourceA.push([-(i+1),sy*ay,sz*az]);sourceB.push([i+1,sy*by,sz*bz]);}}
 const sat=(cnf,x)=>cnf.every(cl=>cl.some(l=>l>0?((x>>(l-1))&1)===1:((x>>(-l-1))&1)===0));
 for(const c of sourceA.concat(sourceB))ok(c.length===3&&new Set(c.map(Math.abs)).size===3,"strict 3clause");
 let U=0,V=0,sourceTrials=0;
 for(let x=0;x<8;x++){let a=false,b=false;for(let y=0;y<64;y++){
  const aa=sat(sourceA,x|(y<<3)),bb=sat(sourceB,x|(y<<9));
  ok(!aa||x===0,"bad A projection");ok(!bb||x===7,"bad B projection");
  sourceTrials+=2;a ||= aa;b ||= bb;
 }if(a)U|=1<<x;if(b)V|=1<<x;}
 ok(U===1&&V===128&&!(U&V),"complete 3CNF projections");
 let damaged=false;for(let x=1;x<8;x++)for(let y=0;y<64;y++)damaged ||= sat(sourceA.slice(1),x|(y<<3));
 ok(damaged,"deleted source clause must broaden projection");
 const allowed=[];for(let f=0;f<256;f++)if((f&1)===1 && !(f&128))allowed.push(f);
 ok(allowed.length===64,"interpolant lattice");
 const input=[0,1,2].map(j=>{let r=0;for(let x=0;x<8;x++)r|=((x>>j)&1)<<x;return r;});
 const base=Array.from(new Set([0,255,...input])).sort((a,b)=>a-b),reached=new Map(base.map(f=>[f,0]));
 let frontier=new Map([[base.join(","),base]]),stateCounts=[1],functionCounts=[reached.size];
 for(let depth=1;depth<=6;depth++){const nxt=new Map();for(const wires of frontier.values()){const prev=new Set(wires);
  function record(t){if(prev.has(t))return;if(!reached.has(t))reached.set(t,depth);const more=[...wires,t].sort((a,b)=>a-b);nxt.set(more.join(","),more);}
  for(let i=0;i<wires.length;i++){record(255^wires[i]);for(let j=i;j<wires.length;j++)record(wires[i]&wires[j]);}
 }frontier=nxt;stateCounts.push(nxt.size);functionCounts.push(reached.size);}
 ok(stateCounts.join(",")==="1,6,27,113,469,1942,8027","complete DAG frontiers");
 ok(functionCounts.join(",")==="5,11,21,37,58,83,102","reachable-functions inventory");
 const validReachable=allowed.filter(f=>reached.has(f)).length;
 ok(validReachable===35&&allowed.length-validReachable===29,"29 valid interpolants need >6 gates");
 const easy=255^input[0];ok(easy===85&&allowed.includes(easy)&&reached.get(easy)===1,"NOT x1");
 ok(allowed.every(f=>!base.includes(f)),"minimum separator has nonzero gate cost");
 let asymptoticChecks=0;for(let k=8;k<=24;k++){const s=Math.floor(2**k/(4*k));ok(2*k+s*(1+2*k)<2**k-2,"counting inequality n="+k);asymptoticChecks++;}
 const triples=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)for(let c=b+1;c<5;c++)triples.push([a,b,c]);
 const leaves=(mask)=>{const deg=[0,0,0,0,0];for(let i=0;i<10;i++)if(mask&(1<<i))for(const v of triples[i])deg[v]++;
  const e=[];for(let i=0;i<10;i++)if(mask&(1<<i)&&triples[i].some(v=>deg[v]===1))e.push(i);return e;};
 function viaStable(mask){let union=0;for(let sub=mask;;sub=(sub-1)&mask){if(!leaves(sub).length)union|=sub;if(sub===0)break;}return union;}
 function viaParallel(mask){for(;;){const els=leaves(mask);if(!els.length)return mask;for(const i of els)mask &= ~(1<<i);}}
 const memo=new Map();function terminals(mask){if(memo.has(mask))return memo.get(mask);const e=leaves(mask),r=new Set();if(!e.length)r.add(mask);else for(const i of e)for(const t of terminals(mask^(1<<i)))r.add(t);memo.set(mask,r);return r;}
 const pop=x=>{let k=0;while(x){x&=x-1;k++;}return k;};
 const cols=["CNF","XOR","SEP","FUS","GAMMA","INT","MACHINE"],weights=["0","0","1/2","3/4","1","0","1"],w4=[0,0,2,3,4,0,4];
 const rows=[{name:"ZERO_NOP_SWITCH",cost:0,delta:[0,0,0,0,0,0,0]},{name:"PAID_PEEL",cost:1,delta:[0,0,1,2,-1,0,0]},{name:"PAID_RESTORE",cost:1,delta:[0,0,0,0,1,0,0]},{name:"PAID_HALT",cost:1,delta:[0,0,0,0,0,0,1]}];
 const dot=xs=>xs.reduce((v,x,i)=>v+x*w4[i],0);
 for(const r of rows)ok(dot(r.delta)<=4*r.cost,"signed rational tariff "+r.name);
 let edges=0,peelable=0;for(let m=0;m<1024;m++){
  const core=viaStable(m);ok(core===viaParallel(m),"stable union vs parallel "+m);
  const targets=terminals(m);ok(targets.size===1&&targets.has(core),"all orders agree "+m);
  if(core===0)peelable++;
  const burden=pop(m)-pop(core);
  for(const i of leaves(m)){const child=m^(1<<i),childcore=viaStable(child);edges++;
   ok(core===childcore&&burden===1+pop(child)-pop(childcore),"single paid PEEL "+m+","+i);
   ok(dot(rows[1].delta)===4,"one charged discharge");}
 }
 ok(edges===430&&peelable===156,"complete 5-vertex hypergraph inventory");
 const addedFree={name:"ADDED_FREE_PEEL",cost:0,delta:rows[1].delta};
 const addedBatch={name:"ADDED_PRICE_ONE_TWO_EDGE_BATCH",cost:1,delta:[0,0,2,4,-2,0,0]};
 ok(dot(addedFree.delta)===4&&dot(addedFree.delta)>0,"free shortcut falsifier");
 ok(dot(addedBatch.delta)===8&&dot(addedBatch.delta)>4,"batch shortcut falsifier");
 return {experiment:"TMR5_SELCORE086",timestamp:"2026-11-15 02:48 PST",status:"COMPUTATIONAL",assertions:checks,failures:0,
  proper3CNF:{AClauses:12,BClauses:12,authenticatedClauseChecks:24,assignmentChecks:sourceTrials,U,V,deletedClauseBroadensProjection:damaged},
  separatorCircuit:{validInterpolants:64,minimumSeparatorGates:1,easyNotX1Mask:85,allCircuitStatesAtBudgets0To6:stateCounts,allFunctionsAtBudgets0To6:functionCounts,validInterpolantsWithin6:validReachable,validInterpolantsAtLeast7:29},
  countingProof:{nRangeChecked:[8,24],instancesChecked:asymptoticChecks,hardSelectedInterpolantLowerBound:"floor(2^n/(4n))+1 AND/NOT gates, existential and nonconstructive"},
  leafCore:{allThreeUniformFiveVertexHypergraphs:1024,eligiblePaidPeelRows:edges,fullyPeelable:peelable,canonicalStableUnionEqualsAllOrderTerminal:true},
  tariff:{columns:cols,lambda:weights,lambdaTimesFour:w4,rows,originalRowDischargesTimesFour:rows.map(r=>dot(r.delta)),addedFreePeelTimesFour:dot(addedFree.delta),addedBatchTimesFour:dot(addedBatch.delta),dualForPeelableM:"y=(m,m,1), cost=2m+1"},
  limitations:["not an actual physical SAT-machine simulation","chosen hard interpolant only nonconstructive","added zero/batch operations are counterfactual controls, not original R_leaf legal rules","physical source verification and every other SAT algorithm remain MAY"]};
}
if(typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(runAudit(),null,2));
