/* TMR-1/012 finite replication audit. Run: node tmr1_input_head_copy012.cjs. */
function runHarness() {
  const cfg={maxL:8,modes:12,headChoices:[1,2,3],steps:23};
  const symbolCode={L:1,"0":2,"1":3,R:4};
  function source(x){return ["L",...x.split(""),"R"];}
  function newState(h) {
    return {q:0,acc:0,t:0,heads:Array(h).fill(0),
      workHeads:[0,0],work:[Object.create(null),Object.create(null)],
      touched:[new Set([0]),new Set([0])]};
  }
  function step(s,read,mode,len) {
    const seen=s.heads.map((p,j)=>read(j,p)),v=seen.reduce((a,c)=>a+symbolCode[c],0);
    const oldW=s.workHeads.map((p,j)=>s.work[j][p]??0);
    const q=(s.q*3+v+oldW[0]*5+oldW[1]*7+mode+s.t)%17;
    for(let j=0;j<2;j++){
      const p=s.workHeads[j];
      s.work[j][p]=(q+v+oldW[j]+j)%4;
      const delta=(q+mode+j+s.t)%3-1;
      s.workHeads[j]=Math.max(0,p+delta);
      s.touched[j].add(s.workHeads[j]);
    }
    const nextHeads=s.heads.map((p,j)=>{
      const d=(q+2*j+symbolCode[seen[j]]+s.t+mode)%3-1;
      return Math.max(0,Math.min(len+1,p+d));
    });
    s.acc=(s.acc+q+v+oldW[0]+oldW[1])%2;
    s.q=q;s.heads=nextHeads;s.t++;
    return {seen:seen.join(""),q:s.q,acc:s.acc,heads:s.heads.join(","),workHeads:s.workHeads.join(",")};
  }
  function execute(x,mode,h,clone) {
    const original=source(x),len=x.length,s=newState(h),trace=[];
    const copies=clone?Array.from({length:h},()=>original.slice()):null;
    for(let i=0;i<cfg.steps;i++)
      trace.push(step(s,(j,p)=>clone?copies[j][p]:original[p],mode,len));
    return {answer:s.acc,t:s.t,trace,workVisits:s.touched.reduce((a,set)=>a+set.size,0)};
  }
  let tests=0,steps=0,mismatch=0,accounting=0,maxStartup=0,ones=0,zeros=0;
  const examples=[];
  for(let L=0;L<=cfg.maxL;L++){
    for(let m=0;m<(1<<L);m++){
      const x=L===0?"":m.toString(2).padStart(L,"0");
      for(const h of cfg.headChoices){
        for(let mode=0;mode<cfg.modes;mode++){
          const a=execute(x,mode,h,false),b=execute(x,mode,h,true);
          const startup=2*L+3,totalB=startup+b.t;
          tests++;steps+=a.t;
          if(a.answer)ones++;else zeros++;
          if(JSON.stringify(a.trace)!==JSON.stringify(b.trace)||a.answer!==b.answer||a.t!==b.t||a.workVisits!==b.workVisits)mismatch++;
          if(totalB!==a.t+2*L+3||b.workVisits+h*(L+2)<a.workVisits)accounting++;
          maxStartup=Math.max(maxStartup,startup);
          if([0,3,8].includes(L)&&[0,1,3].includes(mode)&&h===3&&m<2)
            examples.push({x,mode,h,A:a.t,B:totalB,accepted:!!a.answer});
        }
      }
    }
  }
  if(mismatch||accounting)throw new Error(JSON.stringify({mismatch,accounting}));
  return {tag:"TMR1-INPUT-HEAD-COPY012",status:"COMPUTATIONAL",model:"Synthetic fixed bounded finite-control deterministic machines; h independent read-only heads start on left marker; two writable tapes; original-work traces matched step for step; bounded heads; not SAT solvers",cfg,tests,simulatedSteps:steps,accepted:ones,rejected:zeros,traceMismatches:mismatch,chargeMismatches:accounting,maxStartup,formula:"T_B=T_A+2L+3; S_B<=S_A+h(L+2)+O(1)",examples};
}
console.log(JSON.stringify(runHarness(),null,2));
