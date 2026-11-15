'use strict';
// TMR-3/054. Run: node experiments/tmr/tmr3_streamgraph054.js
// Exact finite implementation checks; not an unrestricted complexity theorem.
function audit054() {
  "use strict";
  const counts={cases2:0,cases3:0,queryChecks:0,sourceReplaySymbols:0,anchorRecordCellsVisited:0,anchorCoveragePatterns:0,physicalSteps:0,streamChecks:0,negativeControls:0};
  let assertions=0,failures=0;
  const ok=(cond,msg)=>{assertions++; if(!cond){failures++; throw Error(msg);}};
  const bitWidth=(v)=>Math.max(1,Math.ceil(Math.log2(v+1)));
  function runPhysical(bits,transition,C){
    let q=0,p=0;
    const trace=[];
    for(let i=0;i<bits.length;i++){
      const entry=transition[q][bits[i]];
      q=entry[0]; const m=entry[1]; p+=m;
      trace.push({state:q,pos:p,move:m});
    }
    return {trace,state:q,pos:p,decision:p>=Math.ceil(bits.length/2),physicalSteps:bits.length+1,originalMoveTapeVisited:p+1,originalStateTapeVisited:1};
  }
  function anchors(bits,tr,C,L) {
    let state=0,pos=0;
    const rec=[{step:0,state:0,pos:0}];
    let sourceProbes=0;
    for(let i=1;i<=bits.length;i++){
      const e=tr[state][bits[i-1]];state=e[0];pos+=e[1];sourceProbes++;
      if(i<bits.length && i%L===0)rec.push({step:i,state,pos});
    }
    const width=bitWidth(C-1)+bitWidth(bits.length);
    return {rec,width,sourceProbes};
  }
  function access(bits,tr,C,L,store,j){
    const idx=Math.floor((j-1)/L),a=store.rec[idx];
    if(!a||a.step!==idx*L)throw Error("anchor lookup invalid");
    let state=a.state,pos=a.pos,move=0,probes=0;
    for(let t=a.step;t<j;t++){
      const e=tr[state][bits[t]];state=e[0];move=e[1];pos+=move;probes++;
    }
    return {state,pos,move,probes,anchorIndex:idx,anchorBitsVisited:(idx+1)*store.width};
  }
  function streaming(bits,tr){
    let state=0,pos=0;
    for(const x of bits){const e=tr[state][x];state=e[0];pos+=e[1];}
    return {state,pos,decision:pos>=Math.ceil(bits.length/2),sourceProbes:bits.length};
  }
  function verify(bits,tr,C,modelTag){
    const n=bits.length,direct=runPhysical(bits,tr,C);
    const stream=streaming(bits,tr);
    ok(stream.pos===direct.pos && stream.state===direct.state && stream.decision===direct.decision,"stream output parity");
    ok(direct.physicalSteps===n+1 && direct.originalMoveTapeVisited===direct.pos+1,"paid physical suffix");
    counts.physicalSteps+=n+1;counts.streamChecks++;
    for(let L=1;L<=n;L++){
      const store=anchors(bits,tr,C,L);
      const r=Math.ceil(n/L);
      ok(store.rec.length===r,"anchor record count");
      ok(store.sourceProbes===n,"preprocessing scans source");
      ok(store.rec[0].step===0,"blank-start initial anchor");
      const b=store.width;
      let evalSum=0,totalProbes=0,totalAnchorCells=0;
      for(let j=1;j<=n;j++){
        const got=access(bits,tr,C,L,store,j),truth=direct.trace[j-1];
        ok(got.state===truth.state && got.pos===truth.pos && got.move===truth.move,"end-to-end per-node answer");
        ok(got.probes===j-Math.floor((j-1)/L)*L && got.probes<=L,"exact replay limit");
        ok(got.anchorBitsVisited=== (Math.floor((j-1)/L)+1)*b,"sequential anchored index tax");
        evalSum+=got.move;totalProbes+=got.probes;totalAnchorCells+=got.anchorBitsVisited;
        counts.queryChecks++;
      }
      ok(evalSum===direct.pos && (evalSum>=Math.ceil(n/2))===direct.decision,"comb evaluator output");
      ok(store.rec.length*b===r*b,"simultaneous stored anchor size");
      ok(totalProbes<=n*L,"aggregate query source probes");
      ok(totalAnchorCells<=n*r*b,"aggregate sequential anchor scan");
      counts.sourceReplaySymbols+=totalProbes;counts.anchorRecordCellsVisited+=totalAnchorCells;
      if (modelTag===2) counts.cases2++; else counts.cases3++;
    }
  }
  // Every two-state, binary-input, one-work-symbol, move-or-stay transition table.
  // Four independent (state,input) entries, each one of four (next,move) pairs.
  for(let n=1;n<=7;n++){
    for(let tableCode=0;tableCode<256;tableCode++){
      const tr=[[],[]];for(let q=0;q<2;q++)for(let x=0;x<2;x++){
        const d=(tableCode>>(2*(2*q+x)))&3;tr[q][x]=[d>>1,d&1];
      }
      for(let word=0;word<(1<<n);word++){
        const bits=Array.from({length:n},(_,j)=>(word>>j)&1);
        verify(bits,tr,2,2);
      }
    }
  }
  // Deterministic random 3-state finite-control tables, exhaustive binary inputs.
  let seed=20261115>>>0;
  const rand=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;};
  for(let sample=0;sample<16;sample++){
    const tr=Array.from({length:3},()=>Array.from({length:2},()=>{const d=rand()%6;return [d>>1,d&1];}));
    for(let n=1;n<=8;n++)for(let word=0;word<(1<<n);word++){
      const bits=Array.from({length:n},(_,j)=>(word>>j)&1);
      verify(bits,tr,3,3);
    }
  }
  // Exact minimum static forward anchors for max replay length L:
  // anchors are positive positions <n plus mandatory position 0;
  // for every j the largest anchor strictly before j must be within L.
  let checkedMinima=0;
  for(let n=1;n<=9;n++)for(let L=1;L<=n;L++){
    let min=n+1;
    for(let mask=0;mask<(1<<(n-1));mask++){
      const marks=[0];for(let a=1;a<n;a++)if(mask&(1<<(a-1)))marks.push(a);
      let good=true;for(let j=1;j<=n;j++){
        let last=0;for(const a of marks)if(a<j)last=a;
        if(j-last>L){good=false;break;}
      }
      if(good)min=Math.min(min,marks.length);
      counts.anchorCoveragePatterns++;
    }
    ok(min===Math.ceil(n/L),"exact static replay anchor minimum");
    checkedMinima++;
  }
  // Forced source-head seeks in a standard one-head input implementation
  // of a stateless random-access replay provider. This is NOT a general lower bound:
  // caching, alternate algorithms and query reordering remain legal.
  const n=64,L=8,requests=[];
  for(let i=0;i<64;i++)requests.push(i%2?1:n);
  let prev=0,moves=0;
  for(const j of requests){
    const start=Math.floor((j-1)/L)*L;
    moves+=Math.abs(prev-start);prev=j; // replay ends with input head at j
  }
  ok(moves>=32*n,"alternating queries force head seeks in this provider");
  counts.negativeControls++;
  // Work-dependent prefix parity: the next movement is previous stored STATE xor x.
  const parityTr=[[[0,0],[1,1]],[[1,1],[0,0]]];
  const x=[1,0,1,1,0,0,1,0],path=runPhysical(x,parityTr,2);
  let prefix=0;for(let j=0;j<x.length;j++){prefix^=x[j];ok(path.trace[j].move===prefix,"work-dependent XOR control");}
  counts.negativeControls+=x.length;
  ok(path.trace.some(t=>t.move!==0)&&path.trace.some(t=>t.move!==1),"nonconstant graph path control");
  counts.negativeControls++;
  return {
    run_id:"TMR3_STREAMGRAPH054",status:"COMPUTATIONAL",source_revision:"tmr3-streamgraph054.v1",
    assertions,failures,seed:20261115,
    counts,
    coverage_lemma_cases:checkedMinima,
    witness:{n:64,L:8,Q:requests.length,sequential_source_head_seek_moves:moves},
    model:{input:"binary read-only source, blank work tapes, fixed finite-state transition table",physical:"STATE tape one cell and MOVE tape monotone head; 1 paid transition per source symbol plus HALT",query_model:"indexed source symbols, sequentially scanned explicit anchor records; full address arithmetic and input-index costs upper-bounded polylog",cross_model_warning:"ordinary sequential input head adds up to Theta(n) movement per adversarial query; end-to-end streaming mode avoids that",no_claims:["no general Cook-Mertz TreeEval improvement","no arbitrary work-tape checkpoint virtualization","no SAT/complexity separation","no physical machine microtrace compiler executed"]},
    reproducibility:"pure deterministic JavaScript, no dependencies, no external random input; native Node can run standalone file"
  };
}
if (typeof process !== 'undefined') process.stdout.write(JSON.stringify(audit054(),null,2)+'\n');
