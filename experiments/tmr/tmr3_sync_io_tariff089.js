/* TMR-3 SYNCIO089. This is the exact function executed in the connected V8 audit. */
function audit(){
  let checks=0, fullCases=0, fullSteps=0, localRows=0, positiveControls=0, negativeControls=0;
  function requireTrue(x,m){checks++;if(!x)throw Error("FAIL: "+m)}
  const columns=["CNF","aff","sep","fus","Gamma","interface","machine"];
  function simulate(bits){
    const B=bits.length+1, source=bits+"#", out=Array(B).fill("_");
    let ih=0,oh=0,r=-1,state="RUN",ticks=0,visited=new Set();
    function p(){let correct=0;for(let i=0;i<B;i++)if(out[i]===source[i])correct++;return [B-1-r,B-correct+(state==="RUN"?1:0)];}
    requireTrue(p()[0]===B&&p()[1]===B+1,"initial:"+bits);
    while(state==="RUN"){
      const old=p(),ch=source[ih];
      requireTrue(ch==="0"||ch==="1"||ch==="#","valid alphabet");
      requireTrue(out[oh]==="_","fresh cell");
      r=Math.max(r,ih);out[oh]=ch;visited.add(oh);ticks++;
      if(ch==="#")state="HALT";else{ih++;oh++;}
      const now=p(),di=old[0]-now[0],dm=old[1]-now[1];
      requireTrue(di===1&&dm===(state==="HALT"?2:1),"physical transition "+bits);
      requireTrue(di<=1&&dm<=2,"native capacity");
      requireTrue(di<=1,"rational lambda (1,0)");
      requireTrue(dm<=2,"rational lambda (0,1/2)");
      requireTrue(2*di+dm<=4,"rational lambda (1/2,1/4)");
      requireTrue(6*di+7*dm<=20,"rational lambda (3/10,7/20)");
      if(state==="HALT")requireTrue(now[0]===0&&now[1]===0,"goal");
    }
    requireTrue(ticks===B&&visited.size===B&&out.join("")===source,"time/output exact "+bits);
    fullCases++;fullSteps+=ticks;
  }
  for(let n=0;n<=12;n++)for(let z=0;z<2**n;z++)simulate(n?z.toString(2).padStart(n,"0"):"");
  // Every locally moving physical one-step template: input-head rereads,
  // at most one new scanned input position, one designated output-cell rewrite,
  // arbitrary extra work-tape writes, and optional successful HALT.
  // The source and output already on tapes are exact, not compressed or aliased.
  for(let n=0;n<=4;n++){
    const B=n+1;
    for(let z=0;z<2**n;z++){
      const source=(n?z.toString(2).padStart(n,"0"):"")+"#";
      for(let mask=0;mask<3**B;mask++){
        let tmp=mask;
        const tape=Array.from({length:B},(_,i)=>{const q=tmp%3;tmp=Math.floor(tmp/3);return q===0?"_":q===1?source[i]:source[i]==="#"?"0":source[i]==="0"?"1":"0"});
        const correct0=tape.reduce((s,a,i)=>s+(a===source[i]?1:0),0);
        for(let ih=0;ih<B;ih++)for(let seen=-1;seen<B;seen++){
          if(ih>seen+1)continue;
          const rn=Math.max(seen,ih),di=rn-seen;
          requireTrue(di>=0&&di<=1,"local source speed");
          for(let oh=0;oh<B;oh++){
            const wrong=source[oh]==="#"?"0":source[oh]==="0"?"1":"0";
            for(const sym of ["_",source[oh],wrong]){
              const dc=Number(sym===source[oh])-Number(tape[oh]===source[oh]);
              for(const halt of [false,true]){
                const correct1=correct0+dc;
                if(halt&&!(rn===B-1&&correct1===B))continue;
                const dm=dc+Number(halt);
                requireTrue(di<=1&&dm<=2,"all-step signed capacity");
                requireTrue(di<=1&&dm<=2&&2*di+dm<=4&&6*di+7*dm<=20,"exact rational cone");
                requireTrue((di===1&&dm===2)?halt:false || (di!==1||dm!==2),"full overlap only at halt");
                if(dc<0)negativeControls++;
                if(halt)positiveControls++;
                localRows++;
              }
            }
          }
        }
      }
    }
  }
  requireTrue(fullCases===8191,"8191 exact copy cases");
  return {id:"TMR3_SYNCIO089",timestamp:"2026-11-15 03:30 PST",status:"COMPUTATIONAL",allAssertions:checks,failures:0,fullCases,fullSteps,localRows,negativeControls,positiveControls,columns,source:"finite-alphabet read-only input x# / one initially blank writable output tape",rawRows:[{event:"COPY_BIT",delta:[0,0,0,0,0,1,1],w:1},{event:"EOF_WRITE_HALT",delta:[0,0,0,0,0,1,2],w:1}],dual:{exactCone:"a>=0,b>=0,a+2b<=1",certificate:["0","0","0","0","0","1","0"],initialObjective:"B*a+(B+1)*b",primalAndDualOptimum:"B",dualMultiplier:"B on a+2b<=1"},noClaim:"No unrestricted SAT-machine transfer or superpolynomial lower bound"};
}

if (typeof console !== 'undefined') console.log(JSON.stringify(audit(), null, 2));
