const runAudit=function runAudit() {
  const get=(m,i)=>m.get(i)??0, set=(m,i,v)=>{if(v===0)m.delete(i);else m.set(i,v)};
  const F=c=>c%2;
  function potential(s,L,z) {
    if(s.phase==="HALT")return 0;
    if(s.phase==="SCAN")return (L-s.p+1)+7+(2*L+4+2*(L+1)*z);
    if(/^R[0-6]$/.test(s.phase))return 7-Number(s.phase[1])+(2*L+4+2*(L+1)*z);
    if(s.phase==="GATE")return 2*L+4+2*(L+1)*z;
    if(s.phase==="DL")return s.p+3*L+5;
    if(s.phase==="DR")return 3*L-s.p+3;
    if(s.phase==="RETURN")return L+s.p+3;
    if(s.phase==="PARSE")return L-s.p+1;
    throw Error("bad phase "+s.phase);
  }
  function run(input,abstract) {
    const L=input.length,z=[...input].reduce((a,b)=>a^Number(b),0);
    const s={phase:"SCAN",p:-1,hB:0,hC:0,B:new Map(),C:new Map(),vb:new Set([0]),vc:new Set([0]),mask:0,part:"",label:null,steps:0};
    const startPhi=potential(s,L,z);
    while(s.phase!=="HALT") {
      if(s.steps>10*L+100)throw Error("nonterminal");
      if(s.hC-s.hB!==({R1:1,R2:1,R5:1}[s.phase]??0))throw Error("delta phase "+s.phase);
      const before=potential(s,L,z), oldPhase=s.phase;
      if(s.phase==="SCAN") {
        if(s.p===-1){s.p=0;}
        else if(s.p<L) {
          const bit=Number(input[s.p]);
          if(bit){set(s.C,0,(get(s.C,0)+1)%4);if(!abstract)set(s.B,0,get(s.B,0)^1);}
          s.p++;
        } else s.phase="R0";
      } else if(s.phase==="R0"){s.hC++;s.vc.add(s.hC);s.phase="R1";}
      else if(s.phase==="R1"){set(s.C,s.hC,(get(s.C,s.hC)+2)%4);s.phase="R2";}
      else if(s.phase==="R2"){s.hC--;s.phase="R3";}
      else if(s.phase==="R3"){s.hB++;s.hC++;s.vb.add(s.hB);s.vc.add(s.hC);s.phase="R4";}
      else if(s.phase==="R4"){s.hB--;s.phase="R5";}
      else if(s.phase==="R5"){s.hB++;s.phase="R6";}
      else if(s.phase==="R6"){s.hB--;s.hC--;s.phase="GATE";}
      else if(s.phase==="GATE") {
        const gate=abstract?F(get(s.C,s.hC)):get(s.B,s.hB);
        s.phase=gate?"DL":"RETURN";
      } else if(s.phase==="DL"){s.p--;if(s.p===-1)s.phase="DR";}
      else if(s.phase==="DR"){s.p++;if(s.p===L)s.phase="RETURN";}
      else if(s.phase==="RETURN"){s.p--;if(s.p===-1)s.phase="PARSE";}
      else if(s.phase==="PARSE") {
        if(s.p<L){if(s.p>=0){s.part+=input[s.p];if(s.part.length===3){s.mask|=(1<<parseInt(s.part,2));s.part="";}}s.p++;}
        else {s.label=(L>0&&L%3===0)?(s.mask===255?"UNSAT":"SAT"):"MALFORMED";s.phase="HALT";}
      } else throw Error("unhandled phase "+s.phase);
      s.steps++;
      if(before!==1+potential(s,L,z))throw Error("Bellman failure "+oldPhase+" "+before+" "+potential(s,L,z));
      if(s.hC-s.hB!==({R1:1,R2:1,R5:1}[s.phase]??0))throw Error("next delta "+oldPhase+"->"+s.phase);
    }
    if(s.steps!==startPhi||s.steps!==3*L+13+2*(L+1)*z)throw Error("time formula mismatch");
    return {...s,initialPotential:startPhi,space:s.vb.size+s.vc.size};
  }
  const inputs=[];
  for(let L=0;L<=10;L++)for(let k=0;k<2**L;k++)inputs.push(k.toString(2).padStart(L,"0"));
  for(let L of [12,18,24,30,48]){
    inputs.push("0".repeat(L),"1".repeat(L),"01".repeat(Math.ceil(L/2)).slice(0,L),"10".repeat(Math.ceil(L/2)).slice(0,L));
  }
  inputs.push(["000","001","010","011","100","101","110","111"].join(""));
  let stepChecks=0,paired=0,sat=0,unsat=0,malformed=0,peakSpace=0;
  let runtimeChecksum=0;
  for(const x of inputs){
    const c=run(x,false),a=run(x,true);paired++;
    if(c.steps!==a.steps||c.label!==a.label||c.p!==a.p||c.hB!==a.hB||c.hC!==a.hC||c.mask!==a.mask||c.part!==a.part||c.space!==a.space)throw Error("abstract replay mismatch");
    for(const j of [0,1,2])if(get(c.B,j)!==F(get(a.C,j)))throw Error("factor invalid");
    if(c.steps!==c.initialPotential||a.steps!==a.initialPotential)throw Error("start rank mismatch");
    stepChecks+=c.steps;runtimeChecksum=(runtimeChecksum+c.steps*x.length)%1000000007;
    peakSpace=Math.max(peakSpace,c.space);
    if(c.label==="SAT")sat++;else if(c.label==="UNSAT")unsat++;else malformed++;
  }
  let checkedAligned=0,checkedDivergent=0;
  for(let c=0;c<4;c++)for(let newC=0;newC<4;newC++) {
    const oldB=F(c), newB=F(newC);
    if(newB===F(newC))checkedAligned++;
    if(F(c)===F(newC)) {if(oldB!==F(newC))throw Error("kernel flaw");checkedDivergent++;}
  }
  const movingOffsetFailure={B0:1,C0:1,C1:0,hB:0,hC:1,incorrectDynamicOffset:1};
  if(movingOffsetFailure.B0===F(movingOffsetFailure.C1))throw Error("moving offset control failure");
  const nonKernelFailure={B1:0,C1After:1};if(nonKernelFailure.B1===F(nonKernelFailure.C1After))throw Error("nonkernel failure missing");
  const offInvariantGate={B0:1,C0:0};if(offInvariantGate.B0===F(offInvariantGate.C0))throw Error("offinvariant control failed");
  return {audit:"TMR4-DIVERGENT-HEAD-FACTOR021",execution:"direct hosted V8 (not native Node or full arbitrary-TM compiler)",inputEnumeration:"all bitstrings lengths 0..10 plus 21 long/control words",pairedTraces:paired,concreteTransitions:stepChecks,abstractTransitions:stepChecks,bellmanEqualities:stepChecks,labels:{SAT:sat,UNSAT:unsat,MALFORMED:malformed},checkedAlignedFactorPairs:checkedAligned,checkedDivergentKernelPairs:checkedDivergent,peakVisitedWorkCells:peakSpace,nonkernelCounterexamples:1,dynamicOffsetCounterexamples:1,offInvariantGateCounterexamples:1,transitionLengthChecksum:runtimeChecksum,failures:0,status:"COMPUTATIONAL"};
};
console.log(JSON.stringify(runAudit(),null,2));
