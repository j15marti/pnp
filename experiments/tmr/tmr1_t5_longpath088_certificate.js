'use strict';
// Exact dependency-free T5 long-subdivision certificate. Node.js.
let assertions=0;
function test(ok,msg){if(!ok)throw Error(msg);assertions++;}
const mod=x=>(x%5+5)%5;
const pow=(x,k)=>BigInt(x)**BigInt(k);
function choose(n,k){let z=1n;for(let i=1;i<=k;i++)z=z*BigInt(n-i+1)/BigInt(i);return z;}
function formula(s){const l=s.length,p=s.filter(t=>t===1).length,q=l-p;const v=Array(5).fill(0n);for(let k=0;k<=l;k++)v[mod(p-3*q+2*k)]+=choose(l,k);return v;}
function independent(s){let v=[1n,0n,0n,0n,0n];for(const a of s){const w=Array(5).fill(0n);for(let j=0;j<5;j++){w[mod(j+a)]+=v[j];w[mod(j+3*a)]+=v[j];}v=w;}return v;}
let words=0;
for(let l=1;l<=10;l++)for(let mask=0;mask<2**l;mask++){
 const s=Array.from({length:l},(_,i)=>mask&(1<<i)?1:-1);
 const v=formula(s),w=independent(s);
 for(let d=0;d<5;d++){
  test(v[d]===w[d],'transfer mismatch l='+l+' mask='+mask+' residue='+d);
  let diff=5n*v[d]-pow(2,l);if(diff<0n)diff=-diff;
  test(diff*pow(16,l)<=4n*pow(13,l)*pow(2,l),'spectral bound');
 }
 words++;
}
const paths=[];
for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
 const l=32+((i*4+j)%5),s=Array.from({length:l},(_,k)=>(k*7+i+j)%4===0?-1:1);
 paths.push({i,j,l,v:formula(s)});
}
let z=0n;
for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)for(let d=0;d<5;d++){
 const labels=[a,b,c,d];let t=1n;
 for(const p of paths)t*=p.v[mod(labels[p.j]-labels[p.i])];
 z+=t;
}
const edges=paths.reduce((s,p)=>s+p.l,0),m=paths.length;
const baseNum=pow(2,edges),baseDen=pow(5,m-4);
let error=z*baseDen-baseNum;if(error<0n)error=-error;
const minLen=Math.min(...paths.map(p=>p.l));
test(8n*BigInt(m)*pow(13,minLen)*10n<=pow(16,minLen),'epsilon certificate for 1/10');
test(error*10n<=baseNum,'relative error <=1/10');
const result={version:'TMR1-088-public-certificate',words,assertions,failures:0,
 longGraph:{branchVertices:4,paths:m,arcs:edges,minLength:minLen,
 count:z.toString(),estimateNumerator:baseNum.toString(),estimateDenominator:baseDen.toString()},
 scope:'Finite computational checks only; full arbitrary-size theorem separately proved'};
console.log(JSON.stringify(result,null,2));
