/* LSPV-4/473 independent V8 check of joint simulator exponent overhead.
   Not an FLMV simulator and not a SAT-complexity lower bound. */
'use strict';
function beta(c) { return (1/c + 2/(c*c) - c)/2; }
const threshold=(function(){let l=1.2,h=1.3; for(let i=0;i<90;i++){let m=(l+h)/2; if(beta(m)>0.5)l=m;else h=m;}return(l+h)/2})();
let count=0;
function check(b,why){if(!b) throw Error('FAIL: '+why); count++;}
check(Math.abs(beta(1.2)-23/45)<1e-13,'beta baseline');
check(Math.abs(beta(1.205)-11642479/23232400)<1e-13,'rational safe point');
check(threshold>1.20556&&threshold<1.20558,'c half');
let seed=473; function rand(){seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;}
let feasible=0,infeasible=0,entry=0;
for(let trial=0;trial<4000;trial++){
 const theta=Math.floor(rand()*8)/10000;
 const omega=(5000+Math.floor(rand()*140))/10000;
 const t0=1.2+Math.floor(rand()*400)/100;
 const s0=0.5+Math.floor(rand()*500)/100;
 const tf=1.2+theta, sf=Math.max(0.5,omega);
 const tm=t=>Math.max(1.1,0.6+(t+theta)/2);
 const sm=s=>Math.max(0.5,(s+omega)/2);
 check(Math.abs(tm(tf)-tf)<1e-12,'t fixed');
 check(Math.abs(sm(sf)-sf)<1e-12,'s fixed');
 const margin=beta(tf)-sf;
 const lip=0.5*(1+1/(tf*tf)+4/(tf*tf*tf));
 const K=lip*Math.max(0,t0-tf)+Math.max(0,s0-sf);
 let t=t0,s=s0;
 for(let depth=0;depth<28;depth++){
   const e=2**(-depth);
   check(t<=tf+Math.max(0,t0-tf)*e+1e-12,'t envelope');
   check(s<=sf+Math.max(0,s0-sf)*e+1e-12,'s envelope');
   if(margin>0&&K*e<margin-1e-12){check(beta(t)>s,'strict entry');entry++;}
   t=tm(t);s=sm(s);
 }
 if(margin>0)feasible++;else infeasible++;
}
check(beta(1.205)>0.501 && beta(1.205)<0.502,'joint threshold');
check(beta(1.206)<0.5,'critical time slowdown');
check(beta(1.2)>0.51,'space allowance');
console.log(JSON.stringify({status:'independent floating-point control; no native FLMV execution',critical_c_approx:threshold,critical_guest_time_overhead_approx:threshold-1.2,checks:count,strict_entry_checks:entry,feasible_trials:feasible,infeasible_trials:infeasible,seed:473},null,2));
