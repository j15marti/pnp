// ARC-GUEST-PROBE-QUOTIENT117, deterministic finite restricted audit.
// Run with: node 2026-10-25_0836_ARC_GUEST_PROBE_QUOTIENT117_repro.js
// Only elementary logical counters, not measured FLMV machine instruction traces.
"use strict";
let assertions=0;
function check(b,why){assertions++; if(!b)throw Error("Assertion "+assertions+": "+why);}
function bits(x,w){return x.toString(2).padStart(w,"0");}
function makeSource(sat,pad,pivot){
  let clauses=[];
  for(let a=0;a<8;a++){
    if(sat&&a===pivot)clauses.push([[4,true],[5,true],[6,true]]);
    else clauses.push([1,2,3].map((v,j)=>[v,((a>>j)&1)===0]));
  }
  for(let j=0;j<pad;j++){let v=7+3*j;clauses.push([[v,true],[v+1,true],[v+2,true]]);}
  return {n:6+3*pad, clauses, sat, pivot, pad};
}
function encode(C){
  const w=Math.max(1,Math.ceil(Math.log2(Math.max(C.n,C.clauses.length)+1)));
  let b="1".repeat(w)+"0"+bits(C.n,w)+bits(C.clauses.length,w);
  for(const c of C.clauses){check(c.length===3&&new Set(c.map(x=>x[0])).size===3,"proper 3CNF");
    for(const [v,sgn] of c){check(v>0&&v<=C.n,"variable in range");b+=(sgn?"1":"0")+bits(v,w);}
  }
  check(b.length===3*w+1+3*C.clauses.length*(w+1),"exact output length");
  return b;
}
function parse(b){
  let p=0,w=0,reads=0;
  while(p<b.length&&b[p]==="1"){p++;w++;reads++;}
  check(w>0&&b[p]==="0","unary width"); p++;reads++;
  function val(){check(p+w<=b.length,"read field");let z=parseInt(b.slice(p,p+w),2);p+=w;reads+=w;return z;}
  const n=val(),m=val(),clauses=[];
  for(let j=0;j<m;j++){
    let c=[];
    for(let k=0;k<3;k++){
      check(p<b.length,"sign field");let sign=b[p]==="1";p++;reads++;
      let v=val();check(v>0&&v<=n,"valid literal id");c.push([v,sign]);
    }
    check(new Set(c.map(z=>z[0])).size===3,"proper read clauses");clauses.push(c);
  }
  check(p===b.length&&reads===b.length,"parse consumes every bit");
  return {n,clauses,reads};
}
function promiseLabel(P){
  check(P.clauses.length>=8,"fixed core");
  const suffix=P.clauses.slice(8);
  for(let j=0;j<suffix.length;j++){
    const v=7+3*j;
    check(JSON.stringify(suffix[j])===JSON.stringify([[v,true],[v+1,true],[v+2,true]]),"padding grammar");
  }
  let missing=0,which=-1;
  for(let a=0;a<8;a++){
    let expected=[1,2,3].map((v,j)=>[v,((a>>j)&1)===0]);
    let got=P.clauses[a];
    if(JSON.stringify(got)===JSON.stringify(expected))continue;
    check(JSON.stringify(got)===JSON.stringify([[4,true],[5,true],[6,true]]),"SAT replacement clause");
    missing++;which=a;
  }
  check(missing<=1,"only one SAT replacement");
  let satByAssignment=false;
  for(let v=0;v<64;v++){
    let x=Array(7).fill(false);
    for(let j=1;j<=6;j++)x[j]=Boolean((v>>(j-1))&1);
    let good=P.clauses.slice(0,8).every(c=>c.some(([id,s])=>x[id]===s));
    satByAssignment ||=good;
  }
  check(satByAssignment===(missing===1),"64-assignment independent core SAT decision");
  return {sat:satByAssignment,pivot:which,pad:suffix.length};
}
function shrinkCount(N){return Math.max(2,Math.floor(Math.sqrt(N)/Math.log2(N+2)));}
function guest(bitsInput,method){
  let P=parse(bitsInput),answer=promiseLabel(P).sat;
  let L=bitsInput.length,delay=L*L;
  let head=0,checksum=0,logicalSourceReads=P.reads;
  let unchangedWrites=0,changedDummyWrites=0,dummy=0;
  let indexBitWrites=0,erasedIndexBits=0;
  let addressWidth=Math.ceil(Math.log2(L+1));
  for(let j=0;j<delay;j++){
    // Both guests execute the same long delay and rewrite a dummy zero cell.
    unchangedWrites++; // dummy=0 is written as 0, including unchanged writes.
    if(method==="dense"){
      checksum^=(bitsInput[head]==="1"?1:0);
      logicalSourceReads++;
      indexBitWrites+=addressWidth;erasedIndexBits+=addressWidth;
      head=(head+7)%L;
    }
  }
  check(unchangedWrites===delay&&changedDummyWrites===0&&dummy===0,"unchanged writes counted");
  return {answer, L, delaySteps:delay, method, guestInputReads:logicalSourceReads,
    inputReadDuringDelay:method==="dense"?delay:0,
    unchangedWrites, changedDummyWrites, indexBitWrites, erasedIndexBits,
    controlIterations:delay, counterBits:Math.ceil(Math.log2(delay+1)),
    inputAddressBits:addressWidth, checksum};
}
function run(){
  let cases=[],totals={roots:0,sat:0,unsat:0,first:0,second:0,guestExecutions:0,
    sourceBitsParsed:0,emittedBits:0,emittedZeroBits:0,emittedOneBits:0,
    denseGuestReads:0,sparseGuestReads:0,densePaddingReads:0,sparsePaddingReads:0,
    unchangedDummyWrites:0,logicalIndexBitWrites:0,logicalIndexErasures:0};
  for(const m of [64,96,160,256,384]){
    for(const pair of [[false,0],[true,0],[true,3],[true,7]]){
      let [sat,pivot]=pair;let root=makeSource(sat,m,pivot);
      let raw=encode(root);let got=parse(raw),rootResult=promiseLabel(got);
      check(rootResult.sat===sat,"source both-label correctness");
      let m1=shrinkCount(raw.length);let Y=makeSource(sat,m1,pivot);
      let by=encode(Y);let py=parse(by),yres=promiseLabel(py);
      let m2=shrinkCount(by.length);let Z=makeSource(sat,m2,pivot);
      let bz=encode(Z);let pz=parse(bz),zres=promiseLabel(pz);
      check(yres.sat===sat&&zres.sat===sat,"two levels preserve both labels");
      check(bz.length<by.length&&by.length<raw.length,"two strict shorter ordinary encodings");
      // All three are actual serialized proper-3CNF and reparsed.
      let gd=guest(bz,"dense"),gs=guest(bz,"sparse");
      check(gd.answer===sat&&gs.answer===sat&&gd.delaySteps===gs.delaySteps,"two guest labels and equal padded delays");
      check(gd.inputReadDuringDelay===bz.length*bz.length,"dense scan padding");
      check(gs.inputReadDuringDelay===0,"sparse work padding");
      for(let b of [raw,by,bz]){
        totals.emittedBits+=b.length;totals.emittedZeroBits+=(b.match(/0/g)||[]).length;
        totals.emittedOneBits+=(b.match(/1/g)||[]).length;
        totals.sourceBitsParsed+=b.length;
      }
      totals.roots++;totals.sat+=Number(sat);totals.unsat+=Number(!sat);
      totals.first++;totals.second++;totals.guestExecutions+=2;
      totals.denseGuestReads+=gd.guestInputReads;totals.sparseGuestReads+=gs.guestInputReads;
      totals.densePaddingReads+=gd.inputReadDuringDelay;
      totals.sparsePaddingReads+=gs.inputReadDuringDelay;
      totals.unchangedDummyWrites+=gd.unchangedWrites+gs.unchangedWrites;
      totals.logicalIndexBitWrites+=gd.indexBitWrites;
      totals.logicalIndexErasures+=gd.erasedIndexBits;
      cases.push({rootPad:m,sat,pivot,sourceN:raw.length,childL1:by.length,
        grandchildL2:bz.length,denseReads:gd.guestInputReads,
        sparseReads:gs.guestInputReads,paddedSteps:gd.delaySteps,
        firstPad:m1,secondPad:m2,guestCounterBits:gd.counterBits,
        guestIndexBits:gd.inputAddressBits});
    }
  }
  check(totals.roots===20&&totals.guestExecutions===40,"counts");
  check(totals.sat===15&&totals.unsat===5,"balanced labels");
  check(totals.emittedBits===totals.emittedZeroBits+totals.emittedOneBits,"all written bits");
  check(totals.densePaddingReads>0&&totals.sparsePaddingReads===0,"padding contrast");
  return {run_id:"ARC-GUEST-PROBE-QUOTIENT117",date:"2026-10-25",
    audit_model:"deterministic program-level logical read/write counts, NOT physical FLMV work or certified all-input SAT guests",
    seed:null,method:"exhaustive 8 assignments per proper-3CNF core; fixed 20 sources (5 sizes by 4 opposite-label cores), actual two-level encode/parse; two guest delay programs",
    assertions,totals,cases,
    proof_status:{probe_separation:"PROVED/EXACT conditional under P=NP for all-input padded B; finite restricted demonstration COMPUTATIONAL",
      full_ARC_successor:"OPEN",P_versus_NP:"OPEN"},
    missing:["all-input A-dependent exact contractor","image-restricted read-count bound on actual supplied A","simultaneous FLMV work/index peak for one source machine"]};
}
if(typeof module!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
