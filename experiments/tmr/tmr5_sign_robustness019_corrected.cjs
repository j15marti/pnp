/* Independent TMR-5/019 CORRECTED polarity sensitivity and Hamming robustness audit. Run: node experiments/tmr/tmr5_sign_robustness019_corrected.cjs */
const audit=function audit() {
  "use strict";
  let assertions = 0;
  function check(ok,msg) { assertions++; if(!ok) throw Error(msg); }
  function sat3types(sigs) {
    let m=0; for (const v of sigs) m|=(1<<v);
    return m!==255;
  }
  function fullMulti(r) { const a=[];for(let v=0;v<8;v++)for(let i=0;i<r;i++)a.push(v);return a; }
  function flipIndex(a,ix) { a[Math.floor(ix/3)]^=1<<(ix%3); }
  const multi=[];
  let neighborhoodEvaluations=0;
  for(let r=1;r<=3;r++){
    const a=fullMulti(r),N=a.length*3;
    check(!sat3types(a),"base must UNSAT r="+r);
    let firstSat=-1, firstCount=0;
    const layerCounts=[];
    function search(d,start,remain) {
      if(remain===0) {
        neighborhoodEvaluations++;
        if(sat3types(a)){firstCount++; if(firstSat<0)firstSat=d;}
        return;
      }
      for(let ix=start;ix<=N-remain;ix++){
        flipIndex(a,ix);search(d,ix+1,remain-1);flipIndex(a,ix);
      }
    }
    for(let d=0;d<=r;d++){
      firstCount=0;search(d,0,d);layerCounts.push({distance:d,satisfiable:firstCount});
      if(d<r)check(firstCount===0,"unexpected SAT below radius r");
      else check(firstCount===8*Math.pow(3,r),"wrong boundary count at d=r");
    }
    let sensitiveBlocks=0;
    for(let typ=0;typ<8;typ++){
      let changed=fullMulti(r);
      for(let c=typ*r;c<(typ+1)*r;c++)changed[c]^=1;
      check(sat3types(changed),"type block not SAT");
      sensitiveBlocks++;
    }
    check(sensitiveBlocks===8,"expected eight disjoint blocks");
    let signSensitivity=0;
    for(let ix=0;ix<N;ix++){
      flipIndex(a,ix);if(sat3types(a))signSensitivity++;flipIndex(a,ix);
    }
    check(signSensitivity===(r===1?24:0),"bad sign sensitivity");
    multi.push({multiplicity:r,sign_bits:N,distance_to_sat:r,sign_sensitivity:signSensitivity,block_sensitivity:8,layerCounts,unsat_certificate_sign_bits:24});
  }
  let seed=170141183;
  function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
  function modelSatisfies(cs,n,assignment,omit=-1){
    for(let i=0;i<cs.length;i++){
      if(i===omit)continue;
      let truth=false;
      for(let j=0;j<3;j++){
        const l=cs[i][j];
        if(((assignment>>l[0])&1)!==l[1]){truth=true;break;}
      }
      if(!truth)return false;
    }
    return true;
  }
  function isSat(cs,n,omit=-1){
    for(let a=0;a<(1<<n);a++)if(modelSatisfies(cs,n,a,omit))return true;
    return false;
  }
  let tested=0,mutations=0,unsatCl=0,satPivots=0,unsatPivots=0,zeroS=0;
  const controls={horn:0,duplicate:0,xor:0,renaming:0,product:0};
  for(const n of [3,4,5,6]){
    for(let m=1;m<=18;m++){
      for(let k=0;k<31;k++){
        let cs=[];
        const mode=k%8;
        for(let i=0;i<m;i++){
          if(mode===4 && m>=8){const sig=i%8;cs.push([[0,sig&1],[1,(sig>>1)&1],[2,(sig>>2)&1]]);continue;}
          if(mode===5 && m>=8){const sig=(i<7?i+1:1);cs.push([[0,sig&1],[1,(sig>>1)&1],[2,(sig>>2)&1]]);continue;}
          if(mode===6 && n===6){const sig=Math.floor(i/2)%8; const off=i%2?3:0;cs.push([[off,sig&1],[off+1,(sig>>1)&1],[off+2,(sig>>2)&1]]);controls.product++;continue;}
          if(mode===2 && i>0 && i%3===0){cs.push(cs[i-1].map(z=>z.slice()));continue;}
          const vars=[];
          while(vars.length<3){const v=(rand()>>>10)%n;if(!vars.includes(v))vars.push(v);}
          let signs=[(rand()>>>17)&1,(rand()>>>17)&1,(rand()>>>17)&1];
          if(mode===1){signs=[1,1,1];signs[(rand()>>>16)%3]=0;controls.horn++;}
          if(mode===3){const sig=(i%4);signs=[sig&1,(sig>>1)&1,((sig>>1)&1)^1];controls.xor++;}
          cs.push(vars.map((v,j)=>[v,signs[j]]));
        }
        const base=isSat(cs,n);
        let sumPivot=0,e=0,clauseMax=0;
        for(let i=0;i<m;i++){
          const hSat=isSat(cs,n,i);
          if(!base && hSat)e++;
          let localPiv=0;
          for(let j=0;j<3;j++){
            cs[i][j][1]^=1;
            const newSat=isSat(cs,n);
            cs[i][j][1]^=1;mutations++;
            const actual=(newSat!==base);
            let predicted=false;
            if(!base)predicted=hSat;
            else {
              predicted=hSat;
              for(let a=0;a<(1<<n)&&predicted;a++) {
                if(!modelSatisfies(cs,n,a,i))continue;
                for(let b=0;b<3;b++){
                  const l=cs[i][b],val=(a>>l[0])&1;
                  const originalTruth=val!==l[1];
                  if(originalTruth!==(b===j)){predicted=false;break;}
                }
              }
            }
            check(actual===predicted,"exact sign dichotomy failed n="+n+",m="+m);
            if(actual){localPiv++;sumPivot++;}
          }
          if(base)check(localPiv<=1,"SAT clause had two pivotal signs");
          else check(localPiv===0||localPiv===3,"UNSAT clause had mixed pivot");
          if(localPiv>clauseMax)clauseMax=localPiv;
        }
        if(!base){unsatCl++;check(sumPivot===3*e,"UNSAT 3*essential failed");unsatPivots+=sumPivot;}
        else {satPivots+=sumPivot;check(sumPivot<=m,"SAT sensitivity >m");}
        if(sumPivot===0)zeroS++;
        if(mode===2)controls.duplicate++;
        if(m>0 && k===0){ // independent variable renaming automorphism
          const bij=[...Array(n).keys()].reverse();
          let renamed=cs.map(c=>c.map(([v,s])=>[bij[v],s]));
          check(isSat(renamed,n)===base,"rename changed label");
          controls.renaming++;
        }
        tested++;
      }
    }
  }
  const y={tag:"TMR5-ROBUST-SIGN-REDTEAM019",engine:"hosted V8 ECMAScript",seed:170141183,configuration:"n=3..6,m=1..14,k=0..30; complete assignment truth-table; exhaustive Hamming spheres for r<=3",multi,neighborhoodEvaluations,formulaChecks:tested,individualSignMutations:mutations,unsatFormulas:unsatCl,satFormulas:tested-unsatCl,unsatPivots,satPivots,zeroSensitivityFormulas:zeroS,controls,assertions,failedAssertions:0,limits:"finite computations corroborate symbolic proofs but do not establish unrestricted 3SAT time bound"};
  return y;
};
console.log(JSON.stringify(audit(),null,2));
