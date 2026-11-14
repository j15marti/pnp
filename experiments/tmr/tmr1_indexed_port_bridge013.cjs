/* TMR-1/013. Native Node or hosted V8: node tmr1_indexed_port_bridge013.cjs. */
function audit(){
  const q=11, maxL=9, modes=6;
  let cases=0, queries=0, sat=0, unsat=0, outOfRange=0, repeated=0, mismatches=0, costViolations=0, spaceViolations=0, maxObservedCost=0, maxObservedRatio=0;
  const examples=[];
  const read=(s,j)=>j>=0&&j<s.length?s[j]:"R";
  for(let L=0;L<=maxL;L++) for(let num=0;num<2**L;num++){
    const x=L===0?"":num.toString(2).padStart(L,"0");
    const clone=["L",...x.split(""),"R"], w=Math.ceil(Math.log2(L+2));
    for(let mode=0;mode<modes;mode++){
      let a=0,b=0,p=0,B=2*L+3,prev=null;
      for(let t=0;t<q;t++){
        let j;
        if(mode===0)j=0;
        else if(mode===1)j=L-1;
        else if(mode===2)j=L;
        else if(mode===3)j=(3*t+1)%Math.max(1,L);
        else if(mode===4)j=t%2===0?0:L+3;
        else j=(t*t+mode)%Math.max(1,L+2);
        const actual=read(x,j),target=(j>=0&&j<L)?j+1:L+1;
        const walked=clone[target],seen=walked==="R"?"R":walked;
        if(actual!==seen)mismatches++;
        const steps=1+(Math.abs(target-p)+2)*(w+1)+(w+1);
        B+=steps;p=target;
        const sym=actual==="R"?2:actual==="1"?1:0;
        const sim=seen==="R"?2:seen==="1"?1:0;
        a=(a*5+sym+mode+t)%17;
        b=(b*5+sim+mode+t)%17;
        if(a!==b)mismatches++;
        if(!(j>=0&&j<L))outOfRange++;
        if(j===prev)repeated++;
        prev=j;queries++;
      }
      if(a%2) sat++; else unsat++;
      const bound=16*(L+1)**2*(q+1);
      if(B>bound)costViolations++;
      if(L+2+2*(w+1)>3*(L+3))spaceViolations++;
      maxObservedCost=Math.max(B,maxObservedCost);
      maxObservedRatio=Math.max(maxObservedRatio,B/bound);
      cases++;
      if([0,4,9].includes(L)&&mode===4&&num<2)examples.push({L,x,mode,A_queries:q,B_charged_steps:B,output:(a%2?"ACCEPT":"REJECT"),address_bits:w});
    }
  }
  const result={tag:"TMR1-INDEXED-PORT-BRIDGE013",status:"COMPUTATIONAL",scope:"Deterministic synthetic indexed-read traces, exhaustive binary sources L=0..9, six query patterns, no SAT machine and no instruction-level TM executor",config:{maxL,modes,queriesPerCase:q},cases,queries,accepted:sat,rejected:unsat,outOfRange,repeated,mismatches,costViolations,spaceViolations,maxObservedCost,maxObservedRatio:Number(maxObservedRatio.toFixed(10)),ledger:"B <= 16(L+1)^2 (T+1) for this conservatively charged harness; work copy L+2 plus <=2(w+1) auxiliary cells",examples};
  if(mismatches+costViolations+spaceViolations!==0)throw Error(JSON.stringify(result));
  return result;
}
console.log(JSON.stringify(audit(),null,2));
