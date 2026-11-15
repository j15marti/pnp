"use strict";
// This is the EXACT executed finite symbolic proxy, not a compiled TM.
function run() {
  const stats={id:"TMR1_LINEARSPARSE049",testedSupports:0,outputBits:0,counterSteps:0,workMoveCharges:0,sourceBitReads:0,assertions:0,failed:0,sizes:[],countingMargins:[],status:"COMPUTATIONAL finite proxy, NOT a compiled Turing machine"};
  function check(cond,msg){stats.assertions++;if(!cond){stats.failed++;throw Error(msg);}}
  function subGap(n, previous, next) {
    const a=Array.from({length:n},(_,i)=> (next>>i)&1);
    const b=Array.from({length:n},(_,i)=>previous<0?1:(previous>>i)&1);
    let borrow=1;const out=[];
    for(let i=0;i<n;i++){let z=a[i]-b[i]-borrow;if(z<0){z+=2;borrow=1;}else borrow=0;out.push(z);}
    return {bits:out,borrow};
  }
  function drain(bits) {
    let top=-1,cost=0,steps=0;
    for(let i=0;i<bits.length;i++) if(bits[i])top=i;
    while(top>=0) {
      let k=0;
      while(bits[k]===0){bits[k]=1;k++;}
      bits[k]=0;
      if(k===top)top=k-1;
      cost+=2*k+5;
      steps++;
      let exact=0;
      for(let i=0;i<bits.length;i++) exact+=bits[i]*2**i;
      check(exact>=0 && (exact===0)===(top<0),"top-marker or counter mismatch");
    }
    return {steps,cost};
  }
  function decode(n,positions) {
    const N=2**n;let prev=-1,output=[],reads=n+1,charges=12*n;
    check(n>=1&&n<=8,"n invalid");
    for(const next of positions) {
      check(next>=0&&next<N&&next>prev,"not strictly sorted");
      const diff=subGap(n,prev,next);
      const gap=next-prev-1;
      let actual=0;
      for(let i=0;i<n;i++)actual+=diff.bits[i]*2**i;
      check(actual===gap,"ripple subtraction");
      const d=drain(diff.bits.slice());
      check(d.steps===gap,"wrong gap decrement count");
      for(let i=0;i<d.steps;i++)output.push(0);
      output.push(1);
      reads+=n;charges+=d.cost+12*n+1;prev=next;
    }
    const tail=prev<0?N:N-1-prev;
    const bits=Array.from({length:n+1},(_,i)=>(tail>>i)&1);
    const last=drain(bits);
    check(last.steps===tail,"tail decrement");
    for(let i=0;i<tail;i++)output.push(0);
    charges+=last.cost+N+4*n;
    check(output.length===N,"output length");
    for(let i=0;i<N;i++)check(output[i]===Number(positions.includes(i)),"wrong bit");
    const chargedBudget=100*(N+(positions.length+1)*(n+1));
    check(charges<=chargedBudget,"charged move proxy too large");
    check(reads===n+1+n*positions.length,"source read mismatch");
    stats.testedSupports++;stats.outputBits+=N;stats.counterSteps+=N-positions.length;stats.workMoveCharges+=charges;stats.sourceBitReads+=reads;
  }
  function combinations(N,r,fn,start=0,acc=[]) {
    if(acc.length===r){fn(acc.slice());return;}
    for(let i=start;i<=N-(r-acc.length);i++){acc.push(i);combinations(N,r,fn,i+1,acc);acc.pop();}
  }
  for(const [n,maxWeight] of [[1,2],[2,4],[3,8],[4,3],[5,2],[6,2],[7,1]]) {
    const N=2**n;const before=stats.testedSupports;
    for(let r=0;r<=Math.min(N,maxWeight);r++)combinations(N,r,x=>decode(n,x));
    decode(n,Array.from({length:N},(_,i)=>i));
    decode(n,Array.from({length:Math.ceil(N/2)},(_,i)=>2*i));
    stats.sizes.push({n,N,checked:stats.testedSupports-before});
  }
  for(const mu of [.25,.5,.75]) {
    const K=Math.floor(2*mu/(1-mu))+2;
    for(const n of [64,128,256]) {
      const N=2**n,s=2**(mu*n),r=Math.ceil(K*s);
      const logDPerS=(Math.log2(s+1)+Math.log2(n+s+2))/s+Math.log2(3)+2*Math.log2(n+s+2);
      const logBPerS=(r/s)*(n-Math.log2(r));
      const gap=logBPerS-logDPerS;
      check(gap>0,"counting gap unexpectedly nonpositive");
      stats.countingMargins.push({mu,K,n,normalizedLog2CountingMargin:Math.round(gap*1e6)/1e6});
    }
  }
  check(stats.failed===0,"failed");
  return stats;
}
console.log(JSON.stringify(run(), null, 2));
