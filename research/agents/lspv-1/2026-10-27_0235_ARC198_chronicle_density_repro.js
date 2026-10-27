'use strict';
// ARC198 deterministic finite controls. Run: node 2026-10-27_0235_ARC198_chronicle_density_repro.js
// No external packages, no random source; not a simulation of all TMs.
const W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
let assertions=0;
function check(z,msg){assertions++;if(!z)throw Error(msg);}
function module22(a,b){const C=W1.map(x=>x.slice());if(a===0){for(const [i,j] of [[6,0],[11,0]])C[i][j]*=-1;}if(b===0){for(const [i,j] of [[17,2],[9,2]])C[i][j]*=-1;}return C;}
function modelCount(C){let cnt=0;for(let v=0;v<32768;v++){let ok=true;for(const c of C){if(!c.some(l=>Number(Boolean(v&(1<<(Math.abs(l)-1))))===Number(l>0))){ok=false;break;}}if(ok)cnt++;}return cnt;}
function physN(m){const w=Math.floor(Math.log2(20*m))+1;return 32+3*w+60*m*(w+1);}
function gapG(m){const w=Math.floor(Math.log2(20*m))+1;return 48*m*(w+1);}
function hist(C,h){let p=1n,s=0n;for(let j=0;j<=h;j++){s+=p;p*=BigInt(C);}return s;}
function main(){const modes=[];
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){const F=module22(a,b),pos=Array(16).fill(0),neg=Array(16).fill(0);for(const cl of F){check(cl.length===3&&new Set(cl.map(Math.abs)).size===3,'distinct');for(const l of cl){if(l>0)pos[l]++;else neg[-l]++;}}for(let v=1;v<=15;v++)check(pos[v]===2&&neg[v]===2,'exact22');modes.push(modelCount(F));}
 check(JSON.stringify(modes)==='[772,272,272,0]','source counts');
 let crossed=0,yes=0,no=0,queried=0;
 for(let m=1;m<=8;m++){const mask=(1<<m)-1;for(let a=0;a<=mask;a++){const b=mask^a;check((a&b)===0,'diagonal SAT');yes++;for(let ap=a+1;ap<=mask;ap++){const bp=mask^ap;check(((a&bp)!==0)||((ap&b)!==0),'mixed UNSAT');crossed++;}for(let i=0;i<m;i++){if((a&(1<<i))!==0){const badB=b|(1<<i);check((a&badB)!==0,'UNSAT hostile flip');no++;}else {check((a&b)===0,'SAT zero module');queried++;}}}}
 let capacity=0;
 for(let C=2;C<=5;C++)for(let D=0;D<=2;D++)for(let L=0;L<=3;L++)for(let G=1;G<=4;G++){
   const words=[];for(let len=0;len<=D+L;len++){if(len===0)words.push('');else {const count=C**len;for(let i=0;i<count;i++){let x=i,s='';for(let j=0;j<len;j++){s=String(x%C)+s;x=Math.floor(x/C);}words.push(s);}}}
   check(BigInt(words.length)===hist(C,D+L),'enumerated words');check(new Set(words).size===words.length,'unique codes');check(BigInt(G*words.length)===BigInt(G)*hist(C,D+L),'union capacity');capacity++;
 }
 const asymptotic=[];for(const m of [10000,100000,1000000]){const N=physN(m),G=gapG(m),k=1,q=4,g=2;const S=Math.ceil(N**.10),D=Math.ceil(N**.10),R=Math.ceil(N**.25),T=Math.ceil(N**1.4);
   const h=2*S+3,V=2*q*h**k,C=1+V+k*h*g;const Lepoch=(D+1)*V+D;
   const Lstar=Math.min(R+1,Lepoch,Math.floor(T/G));const Lfixed=Math.min(R+1,Lepoch);
   const fixedLog=(D+Lfixed+1)*Math.log2(C);const timeLog=Math.log2(G)+(D+Lstar+1)*Math.log2(C);
   check(N>G&&Lstar<=Lfixed,'simultaneous cap');asymptotic.push({m,N,G,S,D,R,T,C,Lepoch,Lstar,log2_density_fixed_upper:Math.round((fixedLog-m)*100)/100,log2_density_time_upper:Math.round((timeLog-m)*100)/100,strict_density_certified:fixedLog<m&&timeLog<m});
 }
 check(asymptotic.every(x=>x.strict_density_certified),'tail examples');
 return {run:'ARC198_EDIT_CHRONICLE_DENSITY',status:'Symbolic restricted theorem; computational controls only, independent review pending',assertions,failures:0,mode_models:modes,crossed_yes_pairs:crossed,diagonal_yes:yes,local_unsat_flips:no,sat_zero_controls:queried,capacity_exhaustive_rows:capacity,asymptotic,random_seed:null,scope:'One fixed globally sound inline-prefix one-input-head U; canonical signed exact22 DISJ promise only. No FLMV or arbitrary SAT claim.'};
}
if(typeof module!=='undefined' && require.main===module){console.log(JSON.stringify(main(),null,2));}
