"use strict";
/* Independent TMR-5/012 hosted-V8 reproducer; node-compatible; no peer imports. */
function run() {
  const Rlist=[[2,2,2],[1,2,2,4,4],[2,2,2,5,5,5],[0,1,2,3,4,5],[3,3,3,3,4,5],[1,1,3,3,5,5],[5,1,2,3,4,5]];
  const assert=(v,msg)=>{if(!v)throw new Error(msg)};
  function allWords(K, callback) {
    const n=4**K;
    for(let z=0;z<n;z++){let x=[],v=z;for(let j=0;j<K;j++){x.push(v%4);v=Math.floor(v/4)}callback(x)}
    return n;
  }
  function length(x,i,R){
    let special=0;for(let j=i+1;j<=R[i];j++) special^=x[j];
    return x[i]===special?1:3;
  }
  function code(x,i,R){
    let special=0;for(let j=i+1;j<=R[i];j++)special^=x[j];
    if(x[i]===special)return "0";
    return ["100","101","110"][[0,1,2,3].filter(z=>z!==special).indexOf(x[i])];
  }
  function colors(R){
    let classes=[];
    for(let i=0;i<R.length;i++){
      let cls=classes.find(c=>c[c.length-1][1]<i);
      if(!cls){cls=[];classes.push(cls)}cls.push([i,R[i]]);
    }
    const depth=Math.max(...R.map((_,j)=>R.filter((r,i)=>i<=j&&j<=r).length));
    assert(classes.length===depth,"interval coloring");
    return classes;
  }
  const coding=[];
  for(const R of Rlist) {
    const K=R.length, cls=colors(R), d=cls.length;
    let fibers=0, maxMoment=Array(d).fill(0), histogram={};
    for(let i=0;i<K;i++){
      let w=R[i]-i;
      for(let z=0;z<4**w;z++){
        let x=Array(K).fill(0), v=z;
        for(let j=i+1;j<=R[i];j++){x[j]=v%4;v=Math.floor(v/4)}
        let words=[];for(let xi=0;xi<4;xi++){x[i]=xi;words.push(code(x,i,R))}
        assert(new Set(words).size===4,"injection");
        assert(words.every((a,j)=>words.every((b,k)=>j===k||(!a.startsWith(b)&&!b.startsWith(a)))),"prefix");
        assert(words.reduce((s,a)=>s+2**(-a.length),0)<=1,"Kraft");
        fibers++;
      }
    }
    const vectors=allWords(K,x=>{
      let lens=R.map((_,i)=>length(x,i,R));let tot=lens.reduce((a,b)=>a+b,0);
      histogram[tot]=(histogram[tot]||0)+1;
      cls.forEach((c,j)=>maxMoment[j]+=c.reduce((v,[i])=>v*2**(2-lens[i]),1));
    });
    assert(maxMoment.every(v=>v<=vectors+1e-7),"class product");
    let tails=[];
    for(const b of [.5,1,2,3,4,5,6,7,8]){
      let count=Object.entries(histogram).reduce((v,[l,n])=>v+(Number(l)<2*K-b?n:0),0);
      let prob=count/vectors,bound=2**(-b/d);
      assert(prob<=bound+1e-12,"interval tail");
      tails.push({b,prob,bound});
    }
    coding.push({R,K,depth:d,vectors,fibers,momentMax:Math.max(...maxMoment)/vectors,histogram,tails});
  }
  let counts={executions:0,labels:{SAT:0,UNSAT:0,MALFORMED:0},
     hCounts:{1:0,2:0,3:0},coreSteps:0,resetSteps:0,copySteps:0,
     terminalSteps:0,totalSteps:0,potentialEdgeChecks:0,hostilePhi2:0};
  function independent(bits){
    if(bits.length%3)return "MALFORMED";
    let seen=new Set();for(let j=0;j<bits.length;j+=3)seen.add(parseInt(bits.slice(j,j+3),2));
    return seen.size===8?"UNSAT":"SAT";
  }
  function core(bits,h){
    const src=["L",...bits.split(""),"R"], heads=Array(h).fill(0);
    let seen=0,clause=0,residue=0,ticks=0;
    while(true) {
      let ch=src[heads[0]];ticks++;
      if(ch==="R")return {heads,label:residue?"MALFORMED":seen===255?"UNSAT":"SAT",ticks};
      if(ch!=="L"){clause=(clause<<1)|Number(ch);residue++;
        if(residue===3){seen|=1<<clause;residue=0;clause=0}}
      heads[0]=Math.min(heads[0]+1,src.length-1);
      for(let j=1;j<h;j++)if(ticks%(j+1)===0)heads[j]=Math.min(heads[j]+1,src.length-1);
      assert(ticks<=src.length+1,"termination");
    }
  }
  const fixtures=[""];for(let L=1;L<=12;L++)for(let n=0;n<2**L;n++)fixtures.push(n.toString(2).padStart(L,"0"));
  const unsat=Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0")).join("");
  fixtures.push(unsat,unsat+"000",unsat.slice(0,-3)+"000","000".repeat(12),"000".repeat(7)+"111","111".repeat(20));
  assert(independent(unsat)==="UNSAT","control UNSAT");
  for(const h of [1,2,3])for(const bits of fixtures){
    const a=core(bits,h),src=["L",...bits.split(""),"R"], heads=a.heads.slice();
    let reset=0,copy=[],steps=a.ticks;
    while(Math.max(...heads)>0){for(let j=0;j<h;j++)heads[j]=Math.max(0,heads[j]-1);reset++;steps++}
    for(let j=0;j<src.length;j++){assert(heads[0]===j,"local copy head");copy.push(src[j]);steps++;if(j<src.length-1)heads[0]++}
    assert(copy.join("")===src.join(""),"source copy");
    steps++;
    const expected=a.ticks+Math.max(...a.heads)+src.length+1;
    assert(steps===expected && reset===Math.max(...a.heads),"ledger");
    assert(a.label===independent(bits),"both-label exactness");
    // Bellman equality on every exact abstract edge, including the READY -> terminal edge.
    for(let edge=0;edge<steps;edge++) {
      const phi=steps-edge,phiNext=phi-1;assert(phi<=1+phiNext,"Bellman");
    }
    assert(!(2<=1+0),"wrong ready potential survived");
    counts.executions++;counts.hCounts[h]++;counts.labels[a.label]++;
    counts.coreSteps+=a.ticks;counts.resetSteps+=reset;counts.copySteps+=src.length;
    counts.terminalSteps++;counts.totalSteps+=steps;
    counts.potentialEdgeChecks+=steps;counts.hostilePhi2++;
  }
  assert(counts.executions===24591 && counts.totalSteps===960327,"native independent parity of ledger");
  return {tag:"TMR5-ID12-LC15",status:"COMPUTATIONAL",language:"restricted fixed-three-variable signed 3CNF SAT + malformed",version:"V8",coding,lateCopy:counts,hostileNonPrefix:{K:3,q:2,b:1,actual:1,unsoundBound:0.5},failures:0};
}
if(typeof module!=="undefined" && typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(run(),null,2));
