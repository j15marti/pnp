"use strict";
// TMR-3/012 exact conditional codebook adversary. Run: node experiments/tmr/tmr3_disjoint_conditional012.cjs
const audit = function audit() {
  "use strict";
  const cases = [[3,1,2],[3,1,3],[4,1,2],[4,2,2],[4,2,3],[4,2,4],[5,1,2],[5,2,3],[5,3,2],[6,2,2],[6,3,2],[6,3,3],[7,2,2],[7,3,2],[8,4,2]];
  const outputs = [];
  const totals = {cases:0,completeVectors:0,conditionalFibers:0,conditionalCodewords:0,prefixAdjacencies:0,failures:0,independenceFalseCases:0};
  function assert(ok,msg) {if(!ok) throw new Error(msg);}
  for(const [q,t,K] of cases) {
    const ell=q-t, N=2**q, mask=2**ell-1, nAll=N**K;
    function unpack(index,count) {
      const a=[];
      for(let j=0;j<count;j++){a.push(index%N);index=Math.floor(index/N);}
      return a;
    }
    function commonFlag(xs){
      let hi=0,lo=0;
      for(const x of xs){hi ^= (x >>> ell);lo ^= (x & mask);}
      return hi===0 && lo!==0;
    }
    function encode(x,other) {
      let h=0,l=0;
      for(const y of other){h ^= (y >>> ell);l ^= (y & mask);}
      const myh=x>>>ell,myl=x&mask;
      if(myh===h && myl!==l) {
        const rank=myl-(myl>l?1:0);
        return rank.toString(2).padStart(ell,"0");
      }
      return "1".repeat(ell)+x.toString(2).padStart(q,"0");
    }
    let fibers=0,codewords=0,adjacencies=0,globallyShort=0,tailEvents=0;
    for(let i=0;i<K;i++){
      for(let j=0;j<N**(K-1);j++){
        const others=unpack(j,K-1);
        const words=[];
        let shortCnt=0;
        for(let x=0;x<N;x++){
          const code=encode(x,others);
          words.push(code);
          if(code.length===ell)shortCnt++;
          else assert(code.length===ell+q,"wrong long code length");
        }
        assert(shortCnt===2**ell-1,"wrong short-fiber count");
        words.sort();
        for(let z=1;z<words.length;z++){
          assert(!words[z].startsWith(words[z-1]),"prefix collision");
          adjacencies++;
        }
        const kraft=shortCnt*2**(-ell)+(N-shortCnt)*2**(-(ell+q));
        assert(kraft<=1+1e-12,"Kraft violation");
        fibers++;codewords+=N;
      }
    }
    const delta=2**(-t)*(1+2**(-q));
    const threshold=q+Math.log2(delta);
    for(let j=0;j<nAll;j++){
      const xs=unpack(j,K);
      const common=commonFlag(xs);
      let min=Infinity,max=-Infinity,sum=0;
      for(let i=0;i<K;i++){
        const others=xs.filter((_,v)=>v!==i);
        const length=encode(xs[i],others).length;
        assert((length===ell)===common,"global event not perfectly synchronized");
        min=Math.min(min,length);max=Math.max(max,length);sum+=length;
      }
      assert(min===max,"lengths not perfectly correlated");
      if(common)globallyShort++;
      if(sum/K<threshold)tailEvents++;
    }
    const p=(2**ell-1)/N;
    assert(globallyShort===p*nAll,"incorrect event probability");
    assert(tailEvents===globallyShort,"tail event mismatch");
    assert(p<delta,"aggregate tail false");
    const refutedKProduct= p>delta**K+1e-12;
    if(refutedKProduct)totals.independenceFalseCases++;
    const row={q,t,K,ell,global_vectors:nAll,conditional_fibers:fibers,conditional_codewords:codewords,prefix_adjacencies:adjacencies,tail_events:tailEvents,short_probability:p,delta,ratio_to_delta:p/delta,naive_delta_to_K:delta**K,naive_independence_bound_refuted:refutedKProduct};
    outputs.push(row);
    totals.cases++;totals.completeVectors+=nAll;totals.conditionalFibers+=fibers;totals.conditionalCodewords+=codewords;totals.prefixAdjacencies+=adjacencies;
  }
  return {claim:"disjoint free q-bit blocks with distinct conditional codebooks can have perfectly correlated prefix-code lengths",mode:"exact finite exhaustive, no random sampling",seed:null,totals,cases:outputs,mathematical_status:"CANDIDATE pending peer review",physical_sat_scope:"NO SAT Turing-machine crossing code constructed"};
};
const result = audit();
console.log(JSON.stringify(result,null,2));
