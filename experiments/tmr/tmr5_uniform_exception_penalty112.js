'use strict';
// Native Node 18+ or V8, no dependencies, deterministic finite physical trace checks.
function run(n,k,m=2){
  const src="1".repeat(n)+"#", W=new Map(), O=Array(m).fill(null), paid=new Set(), seen=new Set();
  let ip=0,wp=0,T=0,phase=0,halt=false,mode="RAMP",rampIndex=1,actTime=-1,finalGateTime=-1;
  const rows=new Map();let assertions=0,maxStep=8*n+8;
  const check=(yes,msg)=>{assertions++;if(!yes)throw Error(`n=${n} k=${k} t=${T} mode=${mode}: ${msg}`)};
  const pot=()=>{
    const q=phase===0?Math.abs(wp-(n-1))+1:0;
    const r=phase===0?n:phase===1?Math.abs(wp)+2:phase===2?1:0;
    return [q,r];
  };
  function step(tag,di,dw,write=null,mark=false,stop=false){
    check(!halt&&Math.abs(di)<=1&&Math.abs(dw)<=1,"paid head move");
    check(ip>=0&&ip<=n&&wp>=0,"head bounds");
    const sym=src[ip],p0=pot();
    if(write!==null){
      if(write==="0"){check(wp===0&&!W.has(0),"initial header");W.set(0,"0")}
      else if(write==="g"){check(wp>0&&!W.has(wp)&&!paid.has(wp),"new gate identity"); W.set(wp,"g");paid.add(wp);if(wp===n-1){check(phase===0,"first last gate");phase=1;finalGateTime=T+1}}
      else if(write==="1"){check(wp===0&&W.get(0)==="0"&&phase===1,"activation at W0 after last gate"); W.set(0,"1");phase=2;actTime=T+1}
      else throw Error("bad write");
    }
    if(mark){check(write==="1"&&O.every(v=>v===null),"markers with activation"); O.fill("@")}
    if(stop){check(write===null&&phase===2&&!halt,"separate HALT");phase=3;halt=true}
    if(sym==="#")seen.add("EOF");
    else if(sym==="1")seen.add(ip);
    else throw Error("bad source");
    ip+=di; wp+=dw; T++;
    const p1=pot(),dq=p0[0]-p1[0],dr=p0[1]-p1[1];
    check(dq+dr<=1,"cost sound tariff");
    rows.set(`${tag}:${dq},${dr}`,(rows.get(`${tag}:${dq},${dr}`)||0)+1);
  }
  while(!halt){
    check(T<maxStep,"termination guard");
    const sym=src[ip];
    if(mode==="RAMP"){
      if(sym==="#"){step("EARLY_EOF",0,-1);mode="BACK";continue}
      if(rampIndex===1)step("INIT",1,1,"0");
      else if(rampIndex<k)step("GATE",1,1,"g");
      else if(rampIndex===k){step("SPEC_REV",1,-1,"g");mode="SPEC";rampIndex++;continue}
      rampIndex++;continue;
    }
    if(mode==="SPEC"){
      if(sym==="#"){
        if(wp===0){step("SPEC_EOF_ACT",0,0,"1",true);mode="HALT"}
        else {step("SPEC_EOF_BACK",0,-1);mode="BACK"}
      }else{step("SPEC_MISMATCH",1,1);mode="ALIGN"}
      continue;
    }
    if(mode==="ALIGN"){
      if(sym==="#"){step("ALIGN_EOF",0,1);mode="LAST"}
      else{step("ALIGN_ONE",1,1);mode="LAG"}
      continue;
    }
    if(mode==="LAG"){
      if(sym==="#"){step("LAG_EOF",0,1,"g");mode="LAST"}
      else{step("LAG_GATE",1,1,"g")}
      continue;
    }
    if(mode==="LAST"){check(sym==="#","final gate after EOF");step("LAST_GATE",0,-1,"g");mode="BACK";continue}
    if(mode==="BACK"){
      if(wp>0)step("BACK",0,-1);
      else{step("ACTIVATE",0,0,"1",true);mode="HALT"}
      continue;
    }
    if(mode==="HALT"){step("HALT",0,0,null,false,true);continue}
    throw Error("unknown mode");
  }
  check(seen.has("EOF")&&[...Array(n).keys()].every(j=>seen.has(j)),"all original input observed");
  check(W.size===n&&paid.size===n-1&&[...Array(n).keys()].every(j=>W.get(j)===(j?"g":"1")),"all distinct gate records");
  check(O.every(v=>v==="@")&&actTime>finalGateTime&&wp===0,"ordered service");
  check(T===(n===k?2*n:2*n+2),"exact off-length runtime");
  check(pot()[0]+pot()[1]===0,"terminal potential");
  return {n,k,m,T,checks:assertions,rows:Object.fromEntries([...rows.entries()].sort())};
}
function audit(){
  let checks=0,traces=0,paid=0;const totals={},examples=[];
  for(let k=2;k<=60;k++)for(let n=2;n<=90;n++)for(let m of [1,2,4]){
    const o=run(n,k,m);checks+=o.checks;traces++;paid+=o.T;
    for(const [row,count] of Object.entries(o.rows))totals[row]=(totals[row]||0)+count;
    if([2,3,5,9,20].includes(k)&&[2,3,5,9,20].includes(n)&&m===1)examples.push({n,k,steps:o.T,expected:n===k?2*n:2*n+2});
  }
  return {role:"TMR-5",run:"042",time:"2026-11-15 06:54 PST",scope:"one fixed finite-control program A_k for each fixed k, all promised unary n>=2",experiment:"deterministic exhaustive n=2..90,k=2..60,m in {1,2,4}; finite checks do not establish unbounded result",traces,paidTransitions:paid,assertions:checks,failures:0,examples,tariffRowCounts:totals,exactFormula:"T_Ak(n)=2k if n=k; 2n+2 otherwise",lambda:[0,0,0,0,1,0,1],zeroCostSCC:"singleton",unrestrictedSATTransfer:"OPEN"};
}
if(typeof require !== 'undefined' && require.main === module) console.log(JSON.stringify(audit(),null,2));
