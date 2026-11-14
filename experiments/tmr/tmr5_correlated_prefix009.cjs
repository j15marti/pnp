"use strict";
/* TMR-5/009: independent constructive sharpness audit for the
   TMR-3/010 aggregate Kraft/Markov probability tail.
   Native Node: node experiments/tmr/tmr5_correlated_prefix009.cjs
   FINITE combinatorial codebook tests, NOT a Turing machine simulation.
*/
function audit() {
  const out={id:"TMR5-CORRELATED-PREFIX009",status:"COMPUTATIONAL",
    prefix_codebooks:0,per_K_tail_checks:0,codeword_comparisons:0,
    failures:0,seed:"none/exhaustive",samples:[]};
  function assert(c,msg){if(!c){out.failures++;throw Error(msg)}}
  for(let q=4;q<=14;q++)for(let t=1;t<=Math.min(q-1,6);t++){
    const ell=q-t, count=2**q, short=2**ell-1, reserve="1".repeat(ell);
    const words=[];
    for(let x=0;x<count;x++){
      words.push(x<short
        ? x.toString(2).padStart(ell,"0")
        : reserve+(x-short).toString(2).padStart(q,"0"));
    }
    assert(new Set(words).size===count,"not injective");
    const sorted=words.slice().sort();
    for(let j=1;j<sorted.length;j++){
      assert(!sorted[j].startsWith(sorted[j-1]),"not prefix-free");
      out.codeword_comparisons++;
    }
    const kraft=words.reduce((a,w)=>a+2**(-w.length),0);
    assert(kraft<=1+1e-11,"Kraft violation");
    const delta=2**(-t)*(1+2**(-q));
    const threshold=q-Math.log2(1/delta);
    const failure=words.filter(w=>w.length<threshold).length;
    assert(failure===short,"wrong tail count");
    assert(failure/count<=delta,"aggregate Markov tail failure");
    for(const K of [1,4,64,4096]){
      // Every cut uses the SAME prefix-free codebook. Thus the K-cut
      // mean code length equals the one-cut length for every input.
      const event=words.filter(w=>K*w.length<K*threshold).length;
      assert(event===failure,"spurious K-dependent concentration");
      out.per_K_tail_checks++;
    }
    out.prefix_codebooks++;
    if(q===14&&[2,3,5].includes(t)){
      out.samples.push({q,t,K:4096,short_length:ell,
        long_length:ell+q,delta,observed_failure_probability:failure/count,
        ratio_to_Markov_bound:(failure/count)/delta,
        kraft_sum:kraft});
    }
  }
  assert(out.prefix_codebooks===60,"missing cases");
  assert(out.per_K_tail_checks===240,"missing K comparisons");
  return out;
}
if(typeof require!=="undefined"&&require.main===module)
  console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined")module.exports={audit};
