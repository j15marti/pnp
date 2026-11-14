"use strict";
// Self-contained hosted V8/Node-compatible instrumented window-cache source emulator.
// All source reads are performed at the current physically tracked original input-head cell.
// Cache and source work-head movements are charged separately. Binary arithmetic is
// charged symbolically by a conservative O(log L) ledger per reload, not compiled microcode.
function audit(){
  "use strict";
  const ok=(v,s)=>{if(!v)throw Error(s)};
  const val=(x,p)=>p===0?"<":p===x.length+1?">":x[p-1];
  let runs=0,virtualSteps=0,virtualSymbolChecks=0,physicalSourceReads=0,physicalSourceMoves=0,cacheReloads=0,cacheHeadMoves=0,chargedOps=0,maxSpace=0,maxBoundRatio=0,failures=0;
  const samples=[];
  function simulate(x,requestedR,steps,mode){
    const q=x.length+1, n=q+1, R=Math.max(1,Math.min(n,requestedR)), h=3, w=Math.max(1,Math.ceil(Math.log2(n)));
    let bill=0,reads=0,moves=0,reloads=0,cmoves=0, sourcePos=0;
    function sourceMoveTo(p){
      ok(p>=0&&p<=q,"source target");
      while(sourcePos!==p){sourcePos+=sourcePos<p?1:-1;bill++;moves++;}
    }
    function sourceRead(){
      reads++;bill++;
      return val(x,sourcePos);
    }
    // Charged input-length discovery and return; charged O(log L) counters.
    sourceMoveTo(q);ok(sourceRead()===">","right marker");sourceMoveTo(0);
    bill+=8*w+8;
    const c=Array.from({length:h},(_,i)=>({p:i===0?0:i===1?Math.floor(q/2):q,base:-1,head:0,data:[],reloads:0}));
    function cacheMoveTo(z,d){
      while(z.head!==d){z.head+=z.head<d?1:-1;bill++;cmoves++;}
    }
    function refresh(z){
      const base=Math.max(0,Math.min(q-R+1,z.p-Math.floor((R-1)/2)));
      // Charge fixed-width address calculations and preservation of counters.
      bill+=12*w+12;
      sourceMoveTo(base);
      if(z.base!==-1)cacheMoveTo(z,0);
      else z.head=0;
      const data=new Array(R);
      for(let j=0;j<R;j++){
        ok(sourcePos===base+j&&z.head===j,"current head read/write alignment");
        data[j]=sourceRead();
        bill++; // physically writable cache cell write
        if(j+1<R){sourceMoveTo(sourcePos+1);cacheMoveTo(z,j+1);}
      }
      z.data=data;z.base=base;
      cacheMoveTo(z,z.p-base);
      z.reloads++;reloads++;
      ok(z.p>=z.base&&z.p<z.base+R,"cache covers virtual position");
    }
    for(const z of c)refresh(z);
    let phase=0;
    const direction=[1,-1,1];
    for(let t=0;t<steps;t++){
      const values=c.map(z=>{
        ok(z.head===z.p-z.base,"virtual/work-head correspondence");
        return z.data[z.head];
      });
      for(let i=0;i<h;i++)ok(values[i]===val(x,c[i].p),"cached vs original current-cell mismatch");
      virtualSymbolChecks+=h;
      const v=values.map(z=>z==="<"?0:z==="0"?1:z==="1"?2:3);
      for(let i=0;i<h;i++){
        const z=c[i];
        if((direction[i]<0&&z.p===0)||(direction[i]>0&&z.p===q))direction[i]*=-1;
        if(mode===1&&(phase+v[i]+i)%13===0)direction[i]*=-1;
        if(mode===2&&(phase+v[(i+1)%h]+2*i)%7===0)direction[i]*=-1;
        let d=direction[i];
        if(mode===3)d=((phase+3*i+v[i])%3)-1;
        const target=Math.max(0,Math.min(q,z.p+d));
        if(target>=z.base&&target<z.base+R){
          cacheMoveTo(z,target-z.base);z.p=target;
        } else {
          z.p=target;refresh(z);
        }
      }
      phase=(phase+v[0]+3*v[1]+5*v[2]+1)%17;
      bill+=4*h+4; // fixed instruction dispatch and finite-state bookkeeping
    }
    const auxVisited=h*R+6*h*w+10*w+12;
    const comparison=600*((x.length+2)+steps*(1+(x.length+2)/R));
    ok(bill<=comparison,"violated conservative charged asymptotic envelope");
    ok(reloads<=h*(2+3*steps/Math.max(1,Math.floor(R/2))),"refresh locality bound");
    runs++;virtualSteps+=steps;physicalSourceReads+=reads;physicalSourceMoves+=moves;cacheReloads+=reloads;cacheHeadMoves+=cmoves;chargedOps+=bill;
    maxSpace=Math.max(maxSpace,auxVisited);
    maxBoundRatio=Math.max(maxBoundRatio,bill/((x.length+2)+steps*(1+(x.length+2)/R)));
    if(samples.length<12&&x.length>=7&&mode===0)samples.push({L:x.length,R,steps,cost:bill,sourceMoves:moves,refresh:reloads,symbolChecks:h*steps,auxVisited});
  }
  for(let L=0;L<=8;L++)for(let mask=0;mask<2**L;mask++){
    const x=L?mask.toString(2).padStart(L,"0"):"";
    const n=L+2, choices=[1,2,3,Math.ceil(Math.sqrt(n)),Math.ceil(n/2),n];
    for(const R of new Set(choices))for(let mode=0;mode<4;mode++)simulate(x,R,5*n+8,mode);
  }
  for(const L of [15,31,32,63,64,127,255,511,1023]){
    for(let seed=0;seed<3;seed++){
      const x=Array.from({length:L},(_,j)=>((17*j*j+19*j+seed*11)%23<11?"1":"0")).join("");
      for(const R of new Set([1,2,Math.ceil(Math.sqrt(L+2)),Math.ceil((L+2)/4),L+2]))for(let mode=0;mode<4;mode++)simulate(x,R,2*(L+2)+35,mode);
    }
  }
  return {status:"COMPUTATIONAL",model:"physical one-input-head plus locally moving writable cache-tape head per virtual source head; finite fixed h=3",sourceAccess:"every new cache symbol comes ONLY from the physically current read-only input-head position",runs,virtualSteps,virtualSymbolChecks,physicalSourceReads,physicalSourceMoves,cacheReloads,cacheHeadMoves,chargedOps,maxExtraVisitedWorkCellBound:maxSpace,maxObservedCostRatio:maxBoundRatio,assertionFailures:failures,samples,note:"The code verifies a charged source-port/cache emulator, not compiled complete arbitrary-TM instructions or a SAT complexity bound."};
}
console.log(JSON.stringify(audit(),null,2));
