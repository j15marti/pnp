"use strict";
// TMR-3/029. Finite semantic and explicit input-head accounting proxy.
// This is not a compiled finite-state Turing machine.
(function () {
  let tests=0, bad=0, streamComparisons=0, sourceMoves=0, counterBitCost=0;
  let malformed=0, networkControls=0, networkSteps=0;
  const classCounts={};
  function check(ok,msg) { tests++; if(!ok) throw Error("CHECK "+msg); }
  function gates(n,s) {
    const N=2**n, full=2**N-1, bases=[0,full];
    for(let j=0;j<n;j++){
      let mask=0;
      for(let i=0;i<N;i++) if((i>>j)&1) mask |= 2**i;
      bases.push(mask);
    }
    let states=[bases], out=new Set(bases);
    for(let depth=0;depth<s;depth++){
      const next=[];
      for(const wires of states){
        const choices=new Set();
        for(const a of wires){
          choices.add(full^a);
          for(const b of wires) { choices.add(a&b); choices.add(a|b); }
        }
        for(const v of choices){ out.add(v); next.push(wires.concat([v])); }
      }
      states=next;
    }
    return Array.from(out).sort((a,b)=>a-b);
  }
  function gamma(m) {
    const b=m.toString(2);
    return "0".repeat(b.length-1)+b;
  }
  function gammaDecode(h) {
    let z=0; while(z<h.length && h[z]==="0") z++;
    const w=z+1;
    if(z+w!==h.length) return -1;
    const v=parseInt(h.slice(z),2);
    return v-1;
  }
  function annotatedStream(h,bits,candidates){
    const n=gammaDecode(h);
    if(n<1 || 2**n!==bits.length) return false;
    const live=candidates.map(()=>true);
    for(let i=0;i<bits.length;i++) {
      for(let j=0;j<candidates.length;j++){
        const b=(candidates[j]>>i)&1;
        live[j]=live[j] && b===bits[i];
        streamComparisons++;
      }
    }
    return live.some(Boolean);
  }
  // The source head is first moved right to EOF, then left to the
  // left endmarker, then right again while consuming the virtual table.
  function bareWithTwoWayInput(bits,candidates) {
    let head=0,count=0,moves=0;
    while(head<bits.length) {
      head++; moves++; count++;
      counterBitCost+=Math.ceil(Math.log2(count+1))+1;
    }
    if(count<2 || (count & (count-1))!==0) {
      sourceMoves+=moves; return {accept:false,moves,valid:false};
    }
    const n=Math.log2(count);
    while(head>0){head--;moves++;}
    check(head===0,"rewind head");
    // Gamma header is synthesized on the work tape, not read from source.
    const h=gamma(n+1);
    check(gammaDecode(h)===n,"gamma header");
    const ans=annotatedStream(h,bits,candidates);
    while(head<count){head++;moves++;}
    check(head===bits.length && moves===3*count,"two-way source charges");
    sourceMoves+=moves;
    return {accept:ans,moves,valid:true};
  }
  for(let n=1;n<=3;n++){
    const N=2**n;
    for(let s=0;s<=2;s++){
      const candidates=gates(n,s);
      const expect={ "1:0":3,"1:1":4,"1:2":4,
                     "2:0":4,"2:1":8,"2:2":14,
                     "3:0":5,"3:1":14,"3:2":40 }[n+":"+s];
      check(candidates.length===expect,"gate count n="+n+" s="+s);
      classCounts[n+":"+s]=candidates.length;
      const candidateSet=new Set(candidates);
      for(let truth=0;truth<2**N;truth++){
        const bits=Array.from({length:N},(_,i)=>(truth>>i)&1);
        const ann=annotatedStream(gamma(n+1),bits,candidates);
        const bare=bareWithTwoWayInput(bits,candidates);
        const direct=candidateSet.has(truth);
        check(ann===direct,"annotated classification");
        check(bare.accept===direct && bare.valid,"two-way classification");
        // This independent label check uses literal candidate truth masks.
      }
    }
  }
  for(const size of [0,1,3,5,6,7,9,10,11,12,17]){
    for(const bit of [0,1]){
      const b=Array(size).fill(bit);
      const v=bareWithTwoWayInput(b,[]);
      check(!v.valid && !v.accept,"malformed must reject");
      malformed++;
    }
  }
  function networkParity(bits) {
    // Three fixed nodes: two stream readers + one parity combiner.
    // A read and a one-symbol message each count as a local action.
    let a=0,b=0,steps=0;
    for(let i=0;i<bits.length;i++) { if((i&1)===0) a^=bits[i]; steps++; }
    for(let i=0;i<bits.length;i++) { if((i&1)===1) b^=bits[i]; steps++; }
    steps+=3; // two message writes and one combining operation
    return {value:a^b,steps};
  }
  for(const n of [2,3]){
    const N=2**n;
    for(let truth=0;truth<2**N;truth++){
      const bits=Array.from({length:N},(_,i)=>(truth>>i)&1);
      const got=networkParity(bits);
      const direct=bits.reduce((a,b)=>a^b,0);
      check(got.value===direct,"network parity");
      check(got.steps===2*N+3,"network charged events");
      networkControls++; networkSteps+=got.steps;
    }
  }
  return JSON.stringify({
    label:"TMR3_TWOWAY_NETWORK032",
    status:"COMPUTATIONAL finite proxy, not compiled TM",
    exhaustive_mcsp_classification_cases:828,
    exact_gate_class_counts:classCounts,
    gamma_header_and_two_way_head_charges:"two source scans plus rewind, exactly 3N moves per valid case",
    assertions_passed:tests,
    failures:bad,
    malformed_controls:malformed,
    source_head_moves:sourceMoves,
    charged_binary_counter_proxy:counterBitCost,
    candidate_record_comparisons:streamComparisons,
    network_parity_cases:networkControls,
    network_charged_local_events:networkSteps,
    limitations:"native hosted V8 semantic mask comparison and explicit head counters; no compiled finite-control one-work-tape executor, no lower-bound experiment"
  },null,2);
})()