"use strict";
// Exact TMR-3/015 hosted-V8 executable. For each fixed h, the host recursion
// has fixed maximum depth and can be unrolled into finite control.
// The Set and BigInt inverse are audit apparatus, not machine resources.
const audit = function audit() {
  "use strict";
  function assert(c, msg) { if (!c) throw Error(msg); }
  function labelOracle(x) {
    if (x.length % 3) return "MALFORMED";
    const seen = new Set();
    for (let i=0;i<x.length;i+=3) seen.add(parseInt(x.slice(i,i+3),2));
    for (let a=0;a<8;a++) if (!seen.has(a)) return "SAT";
    return "UNSAT";
  }
  function execute(x,h) {
    const L=x.length,q=L+1,p=Array(h).fill(0), seen=new Set();
    let steps=0,first=true,mod=0,partial=0,mask=0,answer=null,reads=0;
    function move(k,dir) {
      const key=p.join(",")+":"+k+":"+dir;
      assert(!seen.has(key),"repeated movement state h="+h+" L="+L+" "+key);
      seen.add(key);
      if(k===0 && dir===1 && first && p[0]>=1 && p[0]<=L) {
        const bit=Number(x[p[0]-1]); // current physical cell
        reads++;partial=(partial<<1)|bit;mod++;
        if(mod===3){mask|=1<<partial;partial=0;mod=0;}
      }
      assert(p[k]+dir>=0&&p[k]+dir<=q,"head escaped");
      p[k]+=dir;steps++;
      if(k===0&&dir===1&&p[0]===q&&first){
        answer=mod!==0?"MALFORMED":mask===255?"UNSAT":"SAT";
        first=false;
      }
    }
    function sweep(k) {
      if(k===0){
        while(p[0]<q)move(0,1);
        while(p[0]>0)move(0,-1);
      }else{
        while(p[k]<q){sweep(k-1);move(k,1);}
        while(p[k]>0)move(k,-1);
      }
    }
    sweep(h-1);steps++;
    assert(p.every(z=>z===0),"not restored");
    const exact=2*Array.from({length:h},(_,j)=>q**(j+1)).reduce((a,b)=>a+b,0)+1;
    assert(steps===exact,"bad exact transitions");
    assert(seen.size===steps-1,"duplicate movement state");
    assert(steps-1<=2*h*(L+2)**h,"finite-state bound");
    assert(reads===L,"data not read once");
    assert(answer===labelOracle(x),"wrong label");
    return {steps,reads,label:answer,states:seen.size};
  }
  let cases=0,transitions=0,reads=0,states=0;
  const counts={SAT:0,UNSAT:0,MALFORMED:0};
  let worst={steps:0,length:0,heads:0};
  const byHeads=[];
  const extras=[
    "000001010011100101110111",
    "000001010011100101110110",
    "000001010011100101110111001",
    "000001010011100101110111000",
    "111".repeat(22),
    "000".repeat(22),
    "010110011100101001000111".repeat(2),
    "10".repeat(25),
    "000001010011100101",
    "000001010011100101110"
  ];
  for(let h=1;h<=4;h++){
    let local=0,localSteps=0;
    for(let L=0;L<=8;L++){
      for(let v=0;v<2**L;v++){
        const x=v.toString(2).padStart(L,"0");
        const y=execute(x,h);
        local++;cases++;localSteps+=y.steps;transitions+=y.steps;reads+=y.reads;states+=y.states;counts[y.label]++;
        if(y.steps>worst.steps)worst={steps:y.steps,length:L,heads:h};
      }
    }
    for(const x of extras){
      if((h===3&&x.length>27)||(h===4&&x.length>18))continue;
      const y=execute(x,h);
      local++;cases++;localSteps+=y.steps;transitions+=y.steps;reads+=y.reads;states+=y.states;counts[y.label]++;
      if(y.steps>worst.steps)worst={steps:y.steps,length:x.length,heads:h};
    }
    byHeads.push({h,cases:local,transitions:localSteps});
  }
  function minCells({h,b,gamma,logL,extra,Q}){
    const L=2n**BigInt(logL),q=L+1n,target=2n*q**BigInt(h+extra),G=BigInt(gamma);
    const bound=s=>BigInt(Q)*(L+2n)**BigInt(h)*BigInt(s+1)**BigInt(b)*G**BigInt(b*s);
    let s=0;while(bound(s)<target){s++;assert(s<5000,"inverse out of range");}
    assert(bound(s)>=target&&(s===0||bound(s-1)<target),"bad inverse");
    return s;
  }
  const inversion=[];
  for(const h of [1,2])for(const b of [1,2])for(const extra of [1,2,3])for(const logL of [8,16,32])
    inversion.push({h,b,extra,logL,minCells:minCells({h,b,extra,logL,gamma:2,Q:256})});
  return {
    name:"TMR3-MCF15",
    mode:"exhaustive current-cell finite-state multihead odometer plus exact integer configuration-envelope inversions",
    source:"one fixed controller per h=1,2,3,4; proper three-variable 3CNF sign stream",
    lengths:"all binary words length 0..8, plus controls limited by head count",
    cases,transitions,reads,distinctMovementStates:states,
    labels:counts,worst,byHeads,
    inversionModel:{fixedControlStateCap:256,workAlphabetSize:2,formula:"Q*(L+2)^h*(S+1)^b*Gamma^(b*S)",target:"2*(L+1)^(h+extra)",status:"exact integer inequality, not a physical TM run"},
    inversions:inversion,failures:0,
    limitations:"finite-depth recursive host implementation unrolls to finite-state control for each fixed h; Set is an audit only; no unrestricted 3-SAT compiler"
  };
};
const result = audit();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
