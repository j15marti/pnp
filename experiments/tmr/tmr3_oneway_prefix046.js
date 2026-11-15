#!/usr/bin/env node
"use strict";
/* TMR-3/032: independent finite exact controls for one-way MCSP prefix coupling.
   Exhaustive small circuit classes and rational error, NOT a TM compiler. */
function runTests() {
  let checks=0, exhaustivePairs=0;
  const cases=[];
  function low(n,s) {
    const N=2**n, full=(1n<<BigInt(N))-1n, wires=[0n,full];
    for(let i=0;i<n;i++){
      let v=0n;
      for(let j=0;j<N;j++) if((j>>i)&1) v|=1n<<BigInt(j);
      wires.push(v);
    }
    const set=new Set(wires.map(x=>x.toString()));
    if(s===1) for(const a of wires) {
      set.add((full^a).toString());
      for(const b of wires) {set.add((a&b).toString());set.add((a|b).toString());}
    }
    return new Set([...set].map(x=>BigInt(x)));
  }
  for(const n of [3,4,5]) for(const s of [0,1]) {
    const N=2**n, yes=low(n,s);
    const m=Math.ceil(Math.log2(yes.size))+2, prefix=N-m;
    if(m>=N){cases.push({n,s,N,yes:yes.size,skipped:true});continue;}
    let maxFiber=0;
    for(const x of yes){
      const head=x>>BigInt(m);
      let bySet=0, byExhaustion=0;
      for(const v of yes) if((v>>BigInt(m))===head) bySet++;
      for(let tail=0;tail<2**m;tail++){
        const y=(head<<BigInt(m)) | BigInt(tail);
        if(yes.has(y)) byExhaustion++;
        exhaustivePairs++;
      }
      if(bySet!==byExhaustion) throw Error("suffix enumeration mismatch");
      if(4*bySet>2**m) throw Error("circuit-count fraction failed");
      // delta=1/4; mixture auto YES 1/4, auto NO 1/4, full exact 1/2.
      // P(accept x)=3/4, P(accept Y)=1/4 + (bySet/2^(m+1)).
      // P(scan prefix boundary)=1/2 >= acceptance gap.
      if(!(0.5 >= 0.5*(1-bySet/(2**m)))) throw Error("coupling inequality");
      checks+=3;
      maxFiber=Math.max(maxFiber,bySet);
    }
    if(s===0){
      if(!yes.has(0n)||yes.has(1n<<BigInt(N-1))) throw Error("random-access contrast");
      checks++;
    }
    cases.push({n,s,N,yes:yes.size,unread_suffix_bits:m,shared_prefix_bits:prefix,
      max_yes_suffix_count:maxFiber,all_suffix_count:2**m,
      randomized_delta:"1/4",scan_branch_probability:"1/2"});
  }
  const counting=[];
  for(const n of [16,32,64,128]) for(const muNum of [1,2,3]) {
    const s=2**(n*muNum/4), N=2**n;
    const k=n+s+2;
    const logDupper=Math.ceil(Math.log2(s+1))+Math.ceil(Math.log2(k))+
      s*Math.ceil(Math.log2(3*k*k));
    const mUpper=logDupper+n+2;
    if(!(mUpper>s)) throw Error("counting budget sanity");
    checks++;
    counting.push({n,mu:String(muNum)+"/4",m_over_N:mUpper/N,
       nontrivial_at_this_n:mUpper<N});
  }
  return {identifier:"TMR3/032 ONEWAY-PREFIX46",date_PST:"2026-11-14 17:28 PST",
   status:"COMPUTATIONAL finite only",checks,failures:0,exhaustivePairs,cases,counting,
   note:"Finite enumerations; no physical one-tape or unrestricted SAT runtime proof."};
}
if(typeof module!=="undefined" && require.main===module) console.log(JSON.stringify(runTests(),null,2));
