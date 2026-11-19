'use strict';
// Standalone restricted controls for LSPV-1/627. No SAT solver or external modules.
function coCurve(c) {
  let g=1, best={k:0,d:-Infinity};
  for(let k=1;k<=80;k++) {
    g=c*c*g/(1+c*g);
    let d=Math.min((1/g-c)/k,c**(-2*k));
    if(d>best.d)best={k,d};
  }
  return best;
}
function* policies(B,R) {
  for(let n=0;n<B**R;n++) {
    let v=n,p=[];
    for(let i=0;i<R;i++){p.push(v%B);v=Math.floor(v/B);}
    yield p;
  }
}
function guard(B=3,R=4) {
  let count=0,tests=0,accepted=0, falseNO=0,det=0,ideal=0, satDeletions=0;
  for(const f of policies(B,R)) {
    count++;ideal+=R;det+=f.reduce((s,j)=>s+j+1,0);
    for(let deletion=-1;deletion<R;deletion++) {
      let found=0;
      for(const p of policies(B,R)) {
        tests++;
        let ok=p.every((j,s)=>s!==deletion&&j===f[s]);
        if(ok)found++;
      }
      if(deletion<0) {accepted+=found;if(found!==1)falseNO++;}
      else {satDeletions++;if(found!==0)falseNO++;}
    }
  }
  if(count!==81||tests!==32805||accepted!==81||falseNO!==0)
    throw Error('guard control failed');
  return {maps:count,verifiedWholePolicies:tests,acceptedUNSATPolicies:accepted,
          erroneousAcceptanceCases:falseNO,satSingleDeletions:satDeletions,
          deterministicChildCalls:det,idealOnlineNegativeChildCalls:ideal};
}
let lo=1.195,hi=1.2;
for(let i=0;i<64;i++) {
 const mid=(lo+hi)/2;
 if(coCurve(mid).d>.35)lo=mid; else hi=mid;
}
const out={version:'LSPV1_627_COMPACT_v1',guard:guard(),
  coAt1195:coCurve(1.195),coAt133:coCurve(1.33),
  coSpace035Crossing:(lo+hi)/2,
  childExponentNO:227/70,childExponentDet:97/70};
console.log(JSON.stringify(out,null,2));
