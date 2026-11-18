'use strict';
// TMR-1/064 source-verified vector-junta batching finite control.
// Reproducible: node experiments/tmr/tmr1_batched_junta064.js
const run = () => {
  "use strict";
  const seed=20261116; let state=seed>>>0;
  const next=()=>{state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0};
  const pop=x=>{let z=0;while(x){z+=x&1;x>>>=1}return z};
  const stats={revision:"tmr1-vector-batched-junta064-v1",seed,cases:0,vector_queries:0,baseline_per_bit_bound:0,full_input_checks:0,assertions:0,failures:0,constant_output_controls:0,parity_controls:0};
  const check=(ok,msg)=>{stats.assertions++;if(!ok){stats.failures++;throw Error(msg)}};
  for(let ell=1;ell<=9;ell++) for(let w=0;w<=Math.min(3,ell);w++) for(let rep=0;rep<12;rep++){
    const outputs=1+(next()%11);
    const funcs=[];
    for(let j=0;j<outputs;j++){
      const positions=Array.from({length:ell},(_,i)=>i);
      for(let i=ell-1;i>0;i--){let k=next()%(i+1);[positions[i],positions[k]]=[positions[k],positions[i]]}
      const k=(rep%4===0)?0:(w===0?0:next()%(w+1));
      const relevant=positions.slice(0,k);
      const table=Array.from({length:1<<k},(_,t)=>rep%7===0?(pop(t)&1):(next()&1));
      funcs.push({relevant,table});
      if(!k)stats.constant_output_controls++;
      if(rep%7===0 && k>=2)stats.parity_controls++;
    }
    const evalVector=m=>funcs.map(f=>{let t=0;for(let j=0;j<f.relevant.length;j++)t|=((m>>>f.relevant[j])&1)<<j;return f.table[t]});
    const lowMasks=[];for(let m=0;m<(1<<ell);m++) if(pop(m)<=w)lowMasks.push(m);
    const cached=new Map();for(const mask of lowMasks) cached.set(mask,evalVector(mask));
    stats.vector_queries+=cached.size;
    let qExpected=0;for(let j=0;j<=w;j++){let c=1;for(let i=0;i<j;i++)c=c*(ell-i)/(i+1);qExpected+=Math.round(c)}
    check(cached.size===qExpected,"low-weight query count");
    const recovered=[];
    for(let j=0;j<outputs;j++){
      const supp=[];
      for(let i=0;i<ell;i++){
        let relevant=false;
        for(const mask of lowMasks){
          if((mask&(1<<i))===0 && pop(mask)<=w-1 && cached.get(mask)[j]!==cached.get(mask|(1<<i))[j]){
            relevant=true;break
          }
        }
        if(relevant)supp.push(i);
      }
      check(supp.length<=w,"support exceeds promise");
      const tab=[];
      for(let t=0;t<(1<<supp.length);t++){
        let mask=0;for(let h=0;h<supp.length;h++)mask|=((t>>>h)&1)<<supp[h];
        check(cached.has(mask),"truth table query missing");
        tab.push(cached.get(mask)[j]);
      }
      recovered.push({supp,tab});
    }
    let oldQ=Math.pow(2,w);for(let t=0;t<w;t++){let c=1;for(let k=0;k<t;k++)c=c*(ell-1-k)/(k+1);oldQ+=2*ell*Math.round(c)}stats.baseline_per_bit_bound+=outputs*oldQ;
    for(let m=0;m<(1<<ell);m++){
      const truth=evalVector(m);
      for(let j=0;j<outputs;j++){
        const f=recovered[j];let ix=0;for(let h=0;h<f.supp.length;h++) ix|=((m>>>f.supp[h])&1)<<h;
        check(f.tab[ix]===truth[j],"reconstructed output mismatch");
        stats.full_input_checks++;
      }
    }
    stats.cases++;
  }
  check(stats.vector_queries<stats.baseline_per_bit_bound,"nontrivial batching");
  return stats;
};
process.stdout.write(JSON.stringify(run(),null,2)+'\n');
