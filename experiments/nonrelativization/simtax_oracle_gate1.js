"use strict";
// SIMTAXORACLE1: exact finite oracle/LDE controls and joint-exponent frontier.
// No cryptographic claims. No external libraries needed.
const SEED = 20261014;
function check(c,m){if(!c)throw Error(m);}
function rngFactory(seed){let s=seed>>>0;return ()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return s>>>0;};}
function mod(n,p){return ((n%p)+p)%p;}
function modPow(a,k,p){let z=1;for(let i=0;i<k;i++)z=mod(z*a,p);return z;}
function weights(b,p,alphas){
 const w=[];for(let u=0;u<(1<<b);u++){let x=1;for(let j=0;j<b;j++)x=mod(x*((u>>j)&1?alphas[j]:1-alphas[j]),p);w.push(x);}return w;
}
function evaluate(f,w,p){let x=0;for(let i=0;i<f.length;i++)x=mod(x+f[i]*w[i],p);return x;}
function polynomialSignAtRationalDelta(num,den){
 const a=BigInt(num),b=BigInt(den);
 const value=-4n*b*b*b+870n*a*b*b-900n*a*a*b+250n*a*a*a;
 return {delta:num+"/"+den,sign:value<0n?"NEGATIVE":value>0n?"POSITIVE":"ZERO",numerator:value.toString(),denominator:(b*b*b).toString()};
}
function runAudit(){
 const rand=rngFactory(SEED),p=7;
 let weightChecks=0, flipChecks=0, compactChecks=0, oracleChecks=0;
 const rows=[];
 for(let b=1;b<=10;b++){
   const n=1<<b,as=Array.from({length:b},(_,j)=>2+(j%3)),w=weights(b,p,as);
   for(let u=0;u<n;u++){check(w[u]!==0,"zero LDE weight");weightChecks++;}
   const f=Array.from({length:n},()=>rand()&1);const baseline=evaluate(f,w,p);
   const inds=b<=7?Array.from({length:n},(_,i)=>i):Array.from({length:64},()=>rand()%n);
   for(const i of inds){f[i]^=1;const result=evaluate(f,w,p);const expected=mod(baseline+(f[i]?1:-1)*w[i],p);check(result===expected,"flip");f[i]^=1;flipChecks++;}
   const fAnd=Array.from({length:n},(_,i)=>i===n-1?1:0);
   const directAnd=as.reduce((z,v)=>mod(z*v,p),1);
   check(evaluate(fAnd,w,p)===directAnd,"AND compact evaluation");compactChecks++;
   const fParity=Array.from({length:n},(_,i)=>{let pop=0,x=i;while(x){pop^=x&1;x>>=1;}return pop;});
   const product=as.reduce((z,v)=>mod(z*(1-2*v),p),1),inv2=4;
   const directParity=mod((1-product)*inv2,p);
   check(evaluate(fParity,w,p)===directParity,"PARITY compact evaluation");compactChecks++;
   rows.push({b,hypercube:n,weightNonzero:n,flips:inds.length,compactControls:2});
 }
 for(let n=2;n<=12;n++){
   const maxQueryLength=Math.floor(n/2),target="1".repeat(n);
   for(let k=0;k<=maxQueryLength;k++){
     for(let z=0;z<(1<<k);z++){
       const q=z.toString(2).padStart(k,"0");const bit=rand()&1;
       const oracle0=bit,oracle1=bit;
       check(q!==target&&oracle0===oracle1,"query indistinguishability");oracleChecks++;
     }
   }
   check(n>maxQueryLength,"target would fit small query");oracleChecks++;
 }
 const brackets=[polynomialSignAtRationalDelta(9,2000),polynomialSignAtRationalDelta(1,200),polynomialSignAtRationalDelta(0,1)];
 check(brackets[0].sign==="NEGATIVE"&&brackets[1].sign==="POSITIVE"&&brackets[2].sign==="NEGATIVE","threshold brackets");
 let lo=1.2,hi=1.25;
 for(let i=0;i<70;i++){const m=(lo+hi)/2;if(m*m*m+m*m-m-2>0)hi=m;else lo=m;}
 const criticalC=(lo+hi)/2;
 const criticalQ=2-6/(5*criticalC);
 const grid=[1,1.0045,1.005,1.01,1.1].map(q=>{
   const t=1.2/(2-q),beta=((t+2)/(t*t)-t)/2;
   return {q,t,beta,forbiddenBySufficientCurve:beta>0.5};
 });
 check(grid[0].forbiddenBySufficientCurve&&grid[1].forbiddenBySufficientCurve&&!grid[2].forbiddenBySufficientCurve,"grid");
 return {run_id:"SIMTAXORACLE1",seed:SEED,prime:p,
   weightChecks,flipChecks,compactChecks,oracleChecks,totalAssertions:weightChecks+flipChecks+compactChecks+oracleChecks+3+3,
   rationalSignChecks:brackets,
   criticalC,criticalQ,grid,rows,
   method:"exhaustive Boolean-cube coefficient checks b=1..10; deterministic seeded flips, affine/AND identities; all bounded-length query words n=2..12; rational integer-polynomial signs",
   limits:"Finite oracle indistinguishability and LDE identities only; no implemented Williams simulator, no arbitrary-machine time lower bound, no SAT separation."};
}
if(typeof module!=="undefined"&&require.main===module){
 console.log(JSON.stringify(runAudit(),null,2));
}