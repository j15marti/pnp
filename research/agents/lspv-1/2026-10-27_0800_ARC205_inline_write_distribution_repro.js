"use strict";
/* ARC205 standalone deterministic finite controls.
   Run with: node 2026-10-27_0800_ARC205_inline_write_distribution_repro.js
   No external packages, no randomness.  This checks selector algebra and
   event-label bookkeeping, not the asymptotic crossing-sequence proof. */
function runARC205() {
  let assertions = 0, crossedPairs = 0, acceptedRuns = 0,
      distinctCodes = 0, positiveCodeCollisionsWithoutState = 0,
      capacityRows = 0, extraHeadReads = 0;
  const expect = (v, label) => { assertions++; if (!v) throw Error("ARC205 FAIL: " + label); };
  const popcount = x => { let n=0; for (;x;x&=x-1) n++; return n; };
  function eventCode(m, a, p, omitState=false, omitWrites=false) {
    const mask=(1<<m)-1, stored=(a^(p?mask:0));
    const changes = Array.from({length:m}, (_,i) => ["W",0,i,(stored>>i)&1]);
    const crossing = ["C",1,omitState?0:p,m];
    return JSON.stringify([...(omitWrites?[]:changes),crossing]);
  }
  for (let m=1;m<=9;m++) {
    const n=1<<m, mask=n-1, observed=new Set();
    for (let a=0;a<n;a++) {
      const b=(~a)&mask;
      expect((a&b)===0, "diagonal YES");
      const p=popcount(a)&1;
      // The physical buffer holds an encoded a; finite control holds the
      // decoding mode. The mode is needed in crossing-event labels.
      const code=eventCode(m,a,p);
      expect(!observed.has(code), "all-program injectivity");
      observed.add(code);
      distinctCodes++;
      for(let a2=a+1;a2<n;a2++){
        const ab=(a&((~a2)&mask))!==0;
        const ba=(a2&b)!==0;
        expect(ab||ba, "one crossed UNSAT");
        crossedPairs++;
      }
    }
    expect(observed.size===n, "size of injective YES code set");
  }
  // A concrete globally promise-sound comparator for BOTH modes p=0,1.
  // It checks a AND b = 0, and its code stores a XOR p with p in finite state.
  for(let m=1;m<=7;m++){
    const n=1<<m, mask=n-1;
    for(let p=0;p<2;p++){
      for(let a=0;a<n;a++)for(let b=0;b<n;b++){
        const buffer=a^(p?mask:0), decoded=buffer^(p?mask:0);
        expect(((decoded&b)===0)===((a&b)===0),"sound comparator");
        acceptedRuns+=Number((a&b)===0);
      }
    }
  }
  // Without the finite control state, different programs collide
  // (a=all-0,p=0) versus (a=all-1,p=1).
  for(let m=1;m<=9;m++){
    const mask=(1<<m)-1;
    expect(eventCode(m,0,0,true)===eventCode(m,mask,1,true),
      "omitting program-dependent control destroys injectivity");
    expect(eventCode(m,0,0)!==eventCode(m,mask,1),
      "full event code distinguishes crossed inputs");
    positiveCodeCollisionsWithoutState++;
  }
  // Omitting all changes also collapses distinct YES inputs on the same p.
  for(let m=2;m<=9;m++) {
    expect(eventCode(m,0,0,false,true)===eventCode(m,1,0,false,true),
      "change chronicle is necessary");
  }
  // Direct finite codebook accounting. At most 2^(B+1)-1 binary
  // strings of lengths <=B, independent of the number of programs.
  for (let m=4;m<=20;m++) for(let B=0;B<=m-3;B++)
    for(let G of [1,2,8,64,100]) {
      const cap=G*(2**(B+1)-1), total=2**m;
      const fractionUpper=Math.min(total,cap)/total;
      expect(fractionUpper>=0&&fractionUpper<=1,"finite capacity");
      if(cap<=total/4) expect(1-fractionUpper>=.75,"75 percent deficit");
      capacityRows++;
    }
  // Two independent source heads have an O(m) promise comparator with
  // no work cells/changes; that is a DIFFERENT machine model.
  for(let m=1;m<=8;m++)for(let a=0;a<(1<<m);a++)
    for(let b=0;b<(1<<m);b++){
      let intersect=false;
      for(let i=0;i<m;i++){
        if(((a>>i)&1)&&((b>>i)&1)) intersect=true;
        extraHeadReads+=2;
      }
      expect(intersect===((a&b)!==0),"two-head escape");
    }
  return {
    title:"ARC205 inline WRITE-chronicle distribution finite audit",
    revision:"standalone source embedded in repository report",
    deterministic:true,seed:null,
    m_diagonal_max:9,m_sound_comparator_max:7,
    crossed_fooling_pairs:crossedPairs,
    accepting_promise_comparator_runs:acceptedRuns,
    distinct_crossing_codes:distinctCodes,
    deliberately_colliding_codes_when_state_omitted:positiveCodeCollisionsWithoutState,
    codebook_capacity_rows:capacityRows,
    two_head_source_reads:extraHeadReads,
    assertions,failures:0,
    limits:"Selector-level and combinatorial finite controls only. They do not certify a full 3CNF source encoder, a TM microprogram, or the asymptotic theorem."
  };
}
if (typeof process!=="undefined" && process.stdout) process.stdout.write(JSON.stringify(runARC205(),null,2)+"\n");
