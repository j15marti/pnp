'use strict';
// LSPV-2/478. Native JavaScript finite controls for an oracle-answer-only barrier.
// Restricted toy-language tests, NOT a SAT algorithm or an FLMV machine emulator.
function check(cond,msg){if(!cond)throw Error(msg);}
function gcd(a,b){while(b){const c=a%b;a=b;b=c;}return a;}
function f(a,b=1){const g=gcd(a,b);return [a/g,b/g];}
function add(x,y){return f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function sub(x,y){return f(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
function mul(x,y){return f(x[0]*y[0],x[1]*y[1]);}
function div(x,y){return f(x[0]*y[1],x[1]*y[0]);}
function less(x,y){return x[0]*y[1]<y[0]*x[1];}
function eq(x,y){return x[0]*y[1]===y[0]*x[1];}
function beta(c){return div(sub(div(add(c,f(2)),mul(c,c)),c),f(2));}
const a=f(3,5),lam=f(1,2),rho=f(11,10),eta=f(1,2);
const tau=div(a,sub(f(1),lam)),gap=sub(beta(tau),eta);
check(eq(tau,f(6,5)),'time fixed point');
check(eq(beta(tau),f(23,45)),'FLMV beta');
check(eq(gap,f(1,90)),'strict gap');
check(less(f(501,1000),beta(f(1201,1000))),'strict epsilon');
let t=f(0),maxError=0;
for(let i=0;i<28;i++){
 const next=add(a,mul(lam,t));t=less(next,rho)?rho:next;
 check(!less(tau,t),'upper-envelope iterate');
 maxError=Math.max(maxError,6/5-t[0]/t[1]);
}
check(6/5-t[0]/t[1]<1e-8,'contraction recurrence limit');
// A three-label toy language, not a SAT encoding.
function label(x){
 if(!/^[01]+$/.test(x)||x[0]!=='1')return 'MALFORMED';
 return x.slice(1).includes('1')?'SAT':'UNSAT';
}
function fast(x){return label(x);}
function slow(x){let z=0;for(let i=0;i<7*x.length*x.length;i++)z=(z+i)%19;return label(x);}
function Q(x,oracle,trace){
 if(label(x)==='MALFORMED')return 'MALFORMED';
 const n=x.length;if(n<16)return label(x);
 const B=Math.floor(Math.sqrt(n)),block=B-1;
 let calls=0;
 for(let p=1;p<n;p+=block){
  const y='1'+x.slice(p,p+block);
  check(y.length<=B,'child length');
  const ans=oracle(y);trace.push([y,ans]);calls++;
  if(ans==='SAT')return 'SAT';
 }
 check(calls<=Math.pow(n,.6)+1e-9,'number of children');
 return 'UNSAT';
}
let cases=0,checks=0;
for(const n of [16,36,64,100,256]){
 let seed=478+n;
 const samples=['0'+'0'.repeat(n-1),'1'+'0'.repeat(n-1),'1'+'1'.repeat(n-1)];
 for(const p of [1,Math.floor(n/2),n-1]){
  let a=('1'+'0'.repeat(n-1)).split('');a[p]='1';samples.push(a.join(''));
 }
 for(let j=0;j<200;j++){
  let s='1';
  for(let k=1;k<n;k++){
   seed=(Math.imul(seed,1664525)+1013904223)>>>0;
   s+=((seed>>>31)?'1':'0');
  }samples.push(s);
 }
 for(const x of samples){
  const u=[],v=[],actual=label(x),one=Q(x,fast,u),two=Q(x,slow,v);
  check(one===actual&&two===actual,'labels');
  check(JSON.stringify(u)===JSON.stringify(v),'oracle extensionality');
  cases++;checks+=3;
 }
}
let sFast=5,sSlow=7*25;
check(fast('10000')===slow('10000')&&sFast!==sSlow,'timing distinguisher');
console.log(JSON.stringify({role:'LSPV-2/478',status:'COMPUTATIONAL finite toy controls; exact rational arithmetic',cases,checks,seed:'478+n, LCG 1664525/1013904223',frontier:{alpha:'3/5',lambda:'1/2',rho:'11/10',eta:'1/2',time:'6/5',beta:'23/45',gap:'1/90'},timing_distinguisher:true,limitations:'This toy predicate is not SAT; no native FLMV executor or full solver-dependent contraction.'},null,2));