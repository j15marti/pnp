"use strict";
function audit(){
  "use strict";
  const check=(v,m)=>{if(!v)throw Error(m)};
  function sketch(x,s,mode){
    if(s===0)return "";
    if(mode==="prefix")return x.slice(0,s);
    const a=Array(s).fill(0);
    for(let i=0;i<x.length;i++){
      const bit=x.charCodeAt(i)-48;
      if(mode==="stripe-xor")a[i%s]^=bit;
      else{
        const j=(7*i*i+3*i+1)%s;
        a[j]^=bit;
        if(i%3===0)a[(j+1)%s]^=bit;
      }
    }
    return a.join("");
  }
  let sourceCases=0,collisionWitnesses=0,physicalPrefixChecks=0,maxWitnessPosition=0;
  const samples=[];
  for(let L=5;L<=14;L++)for(let s=0;s<=Math.min(6,L-2);s++){
    const m=s+1,r=L-m;
    for(const mode of ["prefix","stripe-xor","nonlinear"]){
      const states=new Map();
      let witness=null;
      for(let v=0;v<(1<<m);v++){
        const x="0".repeat(r)+v.toString(2).padStart(m,"0");
        const st=sketch(x,s,mode);
        check(st.length<=s,"oversized sketch");
        if(states.has(st)&&witness===null)witness=[states.get(st),x,st];
        if(!states.has(st))states.set(st,x);
      }
      check(witness!==null,"pigeonhole collision absent");
      const [x,y,st]=witness;
      check(x!==y&&x.length===L&&y.length===L,"bad collision");
      check(sketch(x,s,mode)===sketch(y,s,mode)&&x.slice(0,r)===y.slice(0,r),"incorrect collision");
      const p=[...x].findIndex((z,i)=>z!==y[i])+1;
      check(p>=r+1,"witness outside far suffix");
      let head=0;
      while(head<r+1){
        head++;
        const a=x[head-1],b=y[head-1];
        if(head<=r)check(a===b,"physical prefix disagreement");
        physicalPrefixChecks++;
      }
      check(head>=L-s,"physical lower reach not established");
      sourceCases++;collisionWitnesses++;maxWitnessPosition=Math.max(maxWitnessPosition,p);
      if(samples.length<9)samples.push({L,s,mode,commonPrefix:r,queryIndex:p,sketch:st,witness_x:x,witness_y:y,forcedMovementAtLeast:L-s});
    }
  }
  let fullCacheDistinctChecks=0;
  for(let L=1;L<=10;L++){
    const seen=new Set();
    for(let v=0;v<(1<<L);v++){
      const x=v.toString(2).padStart(L,"0");
      check(!seen.has(x),"full copy collision");
      seen.add(x);fullCacheDistinctChecks++;
    }
    check(seen.size===(1<<L),"full cache not injective");
  }
  function forces(lit,u,v){return [[lit,u,v],[lit,u,-v],[lit,-u,v],[lit,-u,-v]];}
  function sat(clauses){
    for(let mask=0;mask<512;mask++){
      let good=true;
      for(const cl of clauses){
        if(!cl.some(lit=>{const val=Boolean(mask&(1<<(Math.abs(lit)-1)));return lit>0?val:!val;})){good=false;break;}
      }
      if(good)return true;
    }
    return false;
  }
  function encode(clauses){
    return "1".repeat(9)+"0"+"1".repeat(clauses.length)+"0"+clauses.map(cl=>cl.map(lit=>Math.abs(lit).toString(2).padStart(4,"0")+(lit>0?"1":"0")).join("")).join("");
  }
  const prefix=forces(1,4,5).concat(forces(-2,6,7),forces(-3,8,9));
  let validSatControls=0,oppositeValidLabelControls=0,encodingSingleBitControls=0;
  for(const m of [1,2,4,8,16]){
    const base=prefix.concat(Array.from({length:m},()=>[2,3,1]));
    const xb=encode(base);
    check(xb.length===203+16*m,"source length mismatch");
    check(sat(base),"SAT forcing failed");
    validSatControls++;
    for(let j=0;j<m;j++){
      const alt=base.map((c,i)=>i===12+j?[2,3,-1]:c);
      const yb=encode(alt);
      const delta=[...xb].filter((z,i)=>z!==yb[i]).length;
      check(delta===1&&xb.length===yb.length,"not one valid bit flip");
      check(!sat(alt),"UNSAT neighbor failed");
      check(xb[xb.length-1]==="1","final sign missing");
      oppositeValidLabelControls++;encodingSingleBitControls++;
    }
  }
  return {status:"COMPUTATIONAL",experiment:"TMR-3/018 post-preprocessing arbitrary-sketch port collision and exact valid-label controls",model:"finite-state sketch tests and physically tracked prefix reach, NOT a complete arbitrary Turing machine compiler",sourceCases,collisionWitnesses,physicalPrefixChecks,maxWitnessPosition,fullCacheDistinctChecks,validSatControls,oppositeValidLabelControls,encodingSingleBitControls,assertionFailures:0,samples,limitations:"Memory sketches are finite s-bit representations; sketch construction and general SAT solver are not physical TM instructions. The mathematical configuration-count theorem is separate."};
}
console.log(JSON.stringify(audit(),null,2));
