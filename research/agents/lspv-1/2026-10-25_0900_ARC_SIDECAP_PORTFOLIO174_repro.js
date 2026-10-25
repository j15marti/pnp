"use strict";
/*
 ARC-SIDECAP-PORTFOLIO174
 Deterministic symbolic SAT/UNSAT two-level tester; NO FLMV physical TM claim.
 Node.js standard library only. Run: node <this-file>
*/
function verify(x, msg) { if (!x) throw Error(msg); }
function serialize(F) {
  return "p cnf " + F.n + " " + F.cs.length + "\n" +
    F.cs.map(c => c.join(" ") + (c.length ? " " : "") + "0\n").join("");
}
function parse(s) {
  const lines=s.trim().split(/\n/);
  verify(/^p cnf \d+ \d+$/.test(lines[0]),"ordinary DIMACS header");
  const h=lines[0].split(" ").map((x,i)=>i<2?x:Number(x)),n=h[2],m=h[3];
  verify(lines.length===m+1, "DIMACS clause count");
  const cs=lines.slice(1).map(line=>{
    const vals=line.trim().split(/\s+/).map(Number);
    verify(vals[vals.length-1]===0 && vals.slice(0,-1).every(v=>v!==0&&Math.abs(v)<=n),"DIMACS literal");
    return vals.slice(0,-1);
  });
  return {n,cs};
}
function satAt(F, mask) {
  return F.cs.every(c=>c.some(l=>{
    const b=(mask>>(Math.abs(l)-1))&1;
    return l>0?b===1:b===0;
  }));
}
function exhaustive(F) {
  for(let mask=0;mask<(1<<F.n);mask++) if(satAt(F,mask)) return true;
  return false;
}
function restrict(F,v,b) {
  return {n:F.n,cs:F.cs.flatMap(c=>{
    if(c.some(l=>(l===v&&b===1)||(l===-v&&b===0))) return [];
    return [c.filter(l=>Math.abs(l)!==v)];
  })};
}
function contradictoryUnits(F) {
  const u=new Set(F.cs.filter(c=>c.length===1).map(c=>c[0]));
  return F.cs.some(c=>c.length===0) || [...u].some(l=>u.has(-l));
}
function positiveWitness(F) {
  return F.cs.every(c=>c.length>0&&c.every(l=>l>0));
}
function* halfMachine(F, kind, cap) {
  // These tests are source-syntactic; no SAT-oracle answer is consulted.
  const losing=(kind==="SAT"&&contradictoryUnits(F))||
               (kind==="UNSAT"&&positiveWitness(F));
  if(losing) {
    yield {op:"remote",position:cap+17};
    while(true) yield {op:"spin"};
  }
  let found=false;
  for(let mask=0;mask<(1<<F.n);mask++) {
    yield {op:"scan",mask};
    if(satAt(F,mask)) {
      found=true;
      if(kind==="SAT") {
        yield {op:"answer",value:"SAT"};
        return;
      }
    }
  }
  if(kind==="UNSAT"&&!found) {
    yield {op:"answer",value:"UNSAT"};
    return;
  }
  while(true) yield {op:"spin"};
}
function race(F, capped=true) {
  const cap=64, limit=(1<<F.n)+8;
  const sim=[{name:"SAT",it:halfMachine(F,"SAT",cap),steps:0,live:true},
             {name:"UNSAT",it:halfMachine(F,"UNSAT",cap),steps:0,live:true}];
  const stats={answer:null,attemptedRemote:0,blockedRemote:0,
    peakTouched:0,sourceBitReads:0,workBitWrites:0,primitiveEvents:0};
  for(let cycle=0;cycle<=limit;cycle++) {
    for(const p of sim) {
      if(!p.live) continue;
      if(p.steps>=limit) {p.live=false;continue;}
      const q=p.it.next();
      if(q.done) {p.live=false;continue;}
      p.steps++;stats.primitiveEvents++;
      if(q.value.op==="remote") {
        stats.attemptedRemote++;
        if(capped&&q.value.position>cap) {
          stats.blockedRemote++;p.live=false;continue;
        }
        stats.peakTouched=Math.max(stats.peakTouched,q.value.position);
      } else if(q.value.op==="scan") {
        // Bit traffic is a CONSERVATIVE SYMBOLIC SOURCE SCAN proxy.
        stats.sourceBitReads+=8*serialize(F).length;
        stats.workBitWrites+=F.n; // includes unchanged assignment-bit writes
        stats.peakTouched=Math.max(stats.peakTouched,F.n+8);
      } else if(q.value.op==="answer") {
        stats.answer=q.value.value;
        return stats;
      }
    }
    if(!sim.some(p=>p.live)) break;
  }
  throw Error("Neither one-sided guest returned in fully enumerated toy cap");
}
function timeoutOneSide(F, kind) {
  // A single sound one-sided algorithm plus clock AND space cap decides both labels.
  const cap=64, limit=(1<<F.n)+8, it=halfMachine(F,kind,cap);
  let remoteAborted=0,steps=0;
  for(let i=0;i<limit;i++) {
    const q=it.next();
    if(q.done) break;
    steps++;
    if(q.value.op==="remote" && q.value.position>cap) {
      remoteAborted++;break;
    }
    if(q.value.op==="answer") {
      return {answer:q.value.value,steps,remoteAborted};
    }
  }
  return {answer:kind==="SAT"?"UNSAT":"SAT",steps,remoteAborted};
}
function run() {
  const roots=[
    {tag:"positive-SAT",n:4,cs:[[1,2],[2,3],[3,4]]},
    {tag:"Horn-SAT",n:4,cs:[[1],[-1,2],[-2,3]]},
    {tag:"XOR-SAT",n:4,cs:[[1,2],[-1,-2],[2,3],[-2,-3]]},
    {tag:"product-SAT",n:6,cs:[[1,2],[-1,3],[4],[5,6]]},
    {tag:"units-SAT",n:3,cs:[[1],[2],[3]]},
    {tag:"empty-SAT",n:3,cs:[]},
    {tag:"unit-UNSAT",n:3,cs:[[1],[-1],[2,3]]},
    {tag:"Horn-UNSAT",n:3,cs:[[1],[-1,2],[-2]]},
    {tag:"XOR-UNSAT",n:3,cs:[[1,2],[-1,-2],[1,-2],[-1,2]]},
    {tag:"binary-UNSAT",n:3,cs:[[1,2],[-1,2],[1,-2],[-1,-2]]},
    {tag:"empty-clause-UNSAT",n:3,cs:[[]]},
    {tag:"mixed-UNSAT",n:4,cs:[[1],[-1],[2,3],[3,4]]}
  ];
  const out={id:"ARC-SIDECAP-PORTFOLIO174",seed:null,execution:"deterministic exhaustive",
    interpretation:"source-level symbolic, not FLMV bit-machine measurements",
    roots:roots.length,rootSAT:0,rootUNSAT:0,firstChildren:0,grandchildren:0,
    firstSAT:0,firstUNSAT:0,grandSAT:0,grandUNSAT:0,
    rootGuestCalls:0,leafGuestCalls:0,oneSideGuestCalls:0,oneSideCappedRemote:0,checks:0,attemptedRemote:0,
    blockedRemote:0,uncappedHighIndex:0,
    sourceBitReads:0,serializedBitWrites:0,workBitWrites:0,
    primitiveEvents:0,maxCappedTouched:0,peakUncappedTouched:0,
    perRoot:[]};
  function check(x,why){verify(x,why);out.checks++;}
  function invoke(F, root=false) {
    const src=serialize(F), decoded=parse(src), gold=exhaustive(decoded);
    check(serialize(decoded)===src,"round-trip");
    const cap=race(decoded,true), bad=race(decoded,false);
    check(cap.answer===(gold?"SAT":"UNSAT"),"capped answer");
    for(const side of ["SAT","UNSAT"]) {
      const one=timeoutOneSide(decoded,side);
      out.oneSideGuestCalls++;
      out.oneSideCappedRemote+=one.remoteAborted;
      check(one.answer===(gold?"SAT":"UNSAT"),"one-sided timeout "+side);
    }
    check(bad.answer===cap.answer,"uncapped answer");
    check(cap.peakTouched<=64,"bounded peak");
    if(bad.peakTouched>64) out.uncappedHighIndex++;
    out.peakUncappedTouched=Math.max(out.peakUncappedTouched,bad.peakTouched);
    out.maxCappedTouched=Math.max(out.maxCappedTouched,cap.peakTouched);
    out.attemptedRemote+=cap.attemptedRemote;
    out.blockedRemote+=cap.blockedRemote;
    out.sourceBitReads+=cap.sourceBitReads;
    out.workBitWrites+=cap.workBitWrites;
    out.primitiveEvents+=cap.primitiveEvents;
    out.serializedBitWrites+=8*src.length;
    if(root)out.rootGuestCalls++;else out.leafGuestCalls++;
    return gold;
  }
  for(const raw of roots) {
    const F=parse(serialize(raw)), gold=exhaustive(F);
    if(gold)out.rootSAT++;else out.rootUNSAT++;
    check(gold===(raw.tag.endsWith("SAT")&&!raw.tag.endsWith("UNSAT")),"source label");
    const rootAnswer=invoke(F,true);
    check(rootAnswer===gold,"paid parent guest");
    const firstResults=[];
    for(let b1=0;b1<=1;b1++) {
      const C=parse(serialize(restrict(F,1,b1)));
      const cGold=exhaustive(C);out.firstChildren++;
      if(cGold)out.firstSAT++;else out.firstUNSAT++;
      const grand=[];
      for(let b2=0;b2<=1;b2++) {
        const G=parse(serialize(restrict(C,2,b2)));
        const gGold=exhaustive(G);out.grandchildren++;
        if(gGold)out.grandSAT++;else out.grandUNSAT++;
        check(invoke(G)===gGold,"actual ordinary grandchild");
        grand.push(gGold);
      }
      check(grand.some(Boolean)===cGold,"second-level OR join");
      firstResults.push(grand.some(Boolean));
    }
    check(firstResults.some(Boolean)===gold,"first-level OR join");
    out.perRoot.push({tag:raw.tag,rootSAT:gold,rootBits:8*serialize(F).length});
  }
  check(out.rootSAT===6&&out.rootUNSAT===6,"both-label roots");
  check(out.rootGuestCalls===12&&out.leafGuestCalls===48,"paid guest calls");
  check(out.oneSideGuestCalls===120,"one-sided timeout guests");
  check(out.blockedRemote>0&&out.uncappedHighIndex>0,"active red-team trap");
  check(out.grandSAT>0&&out.grandUNSAT>0,"both-label descendants");
  return out;
}
if(typeof module!=="undefined"&&require.main===module) {
  console.log(JSON.stringify(run(),null,2));
}
