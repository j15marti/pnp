// Independent JS finite audit of the joint FLMV exponent envelope. Node 18+.
'use strict';
const assert = require('assert');
const beta=c=>((c+2)/(c*c)-c)/2;
const poly=d=>1000*d**4+200*d**3+510*d**2-1765*d+2;
const params=d=>{
  const a=.6+d, lambda=.5+d, rho=1.1+d, eta=.5+d;
  return {a,lambda,rho,eta,c:Math.max(rho,a/(1-lambda))};
};
const gap=d=>{const p=params(d);return beta(p.c)-p.eta;};
let count=0;const ok=(x,msg)=>{assert.ok(x,msg);count++};
for(let d of [0,.0001,.001,1/900,1/800,.01]){
  const p=params(d),v=poly(d)/(20*(1-2*d)*(5*d+3)**2);
  ok(Math.abs(gap(d)-v)<2e-12,'quartic identity '+d);
  ok(p.c>=p.rho,'max branch '+d);
}
let lo=0,hi=.01;
for(let i=0;i<120;i++){
 const mid=(lo+hi)/2;
 if(poly(mid)>0)lo=mid;else hi=mid;
}
let root=(lo+hi)/2;
ok(root>.001133515904 && root<.001133515905,'critical joint delta');
const d=.001,p=params(d),g=gap(d),L=433/216;
let maxDepth=0,minMargin=Infinity,cases=0;
let state=482;
const rnd=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state;};
for(let k=0;k<1204;k++){
 let t0=(10+rnd()%2000000)/10, s0=(rnd()%1500000)/10;
 if(k===1200){t0=1;s0=0;}
 if(k===1201){t0=1e6;s0=1e6;}
 if(k===1202){t0=1.2;s0=.5;}
 if(k===1203){t0=1;s0=1e6;}
 let A=L*Math.max(0,t0-p.c)+Math.max(0,s0-p.eta), j=0;
 while(p.lambda**j*A>g/2){j++;ok(j<200,'finite j')}
 let t=t0,s=s0;
 for(let h=0;h<=j;h++){
   ok(t<=p.c+p.lambda**h*Math.max(0,t0-p.c)+1e-8,'time upper envelope');
   ok(s<=p.eta+p.lambda**h*Math.max(0,s0-p.eta)+1e-8,'space upper envelope');
   ok(beta(t)-s>=g-p.lambda**h*A-1e-7,'beta envelope');
   if(h<j){t=Math.max(p.rho,p.a+p.lambda*t);s=Math.max(p.eta,p.lambda*s);}
 }
 ok(beta(t)-s>=g/2-1e-10,'entry gap');
 maxDepth=Math.max(maxDepth,j); minMargin=Math.min(minMargin,beta(t)-s);cases++;
}
let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let cnt={sat:0,unsat:0,checks:0};
for(let mask=0;mask<16;mask++){
 let cl=[];
 for(let v=0;v<4;v++){
   let inc=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
   for(let bits=0;bits<8;bits++){
     let parity=((bits&1)^((bits>>1)&1)^((bits>>2)&1));
     if(parity===((mask>>v)&1)) continue;
     cl.push(inc.map((idx,k)=>((bits>>k)&1)?-(idx+1):idx+1));
   }
 }
 ok(cl.length===16,'16 strict proper source clauses');
 let satCount=0;
 for(let x=0;x<64;x++){
  let clSat=cl.every(c=>c.some(z=>!!((x>>(Math.abs(z)-1))&1)===(z>0)));
  let vertexSat=[0,1,2,3].every(v=>{
    let inc=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
    return inc.reduce((a,i)=>a^((x>>i)&1),0)===((mask>>v)&1);
  });
  ok(clSat===vertexSat,'source clause parity');cnt.checks++;
  if(clSat)satCount++;
 }
 ok(satCount===((mask.toString(2).replace(/0/g,'').length%2===0)?8:0),'model count');
 if(satCount)cnt.sat++;else cnt.unsat++;
}
ok(cnt.sat===8&&cnt.unsat===8,'K4 labels');
console.log(JSON.stringify({independent_js_assertions:count,recurrence_configs:cases,max_depth:maxDepth,minimum_gap:minMargin,delta_critical:root,source_controls:cnt},null,2));
