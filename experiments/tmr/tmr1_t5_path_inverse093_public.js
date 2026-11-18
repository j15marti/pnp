#!/usr/bin/env node
'use strict';
// Independent-executable finite certificate for TMR-1/093. Node.js >=18, no dependencies.
const n=5, I=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>BigInt(i===j)));
const R=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>BigInt([1,3].includes((j-i+5)%5))));
const T=R[0].map((_,j)=>R.map(r=>r[j]));
const mul=(A,B)=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>A[i].reduce((s,x,k)=>s+x*B[k][j],0n)));
const eq=(A,B)=>A.every((row,i)=>row.every((v,j)=>v===B[i][j]));
let assertions=0;
const ck=(b,s)=>{assertions++;if(!b)throw Error(s);};
function det(A){
 const a=A.map(r=>r.slice());let sign=1n,prev=1n;
 for(let k=0;k<n-1;k++){
  if(a[k][k]===0n){let t=k+1;while(t<n&&a[t][k]===0n)t++;if(t===n)return 0n;
   [a[k],a[t]]=[a[t],a[k]];sign=-sign;}
  const pivot=a[k][k];
  for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++){
   const x=a[i][j]*pivot-a[i][k]*a[k][j];ck(x%prev===0n,'Bareiss integral division');a[i][j]=x/prev;
  }
  for(let i=k+1;i<n;i++)a[i][k]=0n;
  prev=pivot;
 }
 return sign*a[n-1][n-1];
}
const inv2=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>BigInt([0,1].includes((j-i+5)%5)?-1:1)));
const twiceI=I.map(row=>row.map(x=>2n*x));
ck(eq(mul(R,inv2),twiceI),'2R inverse');ck(det(R)===2n,'det R');
ck(eq(mul(R,T),mul(T,R)),'R and transpose commute');
let cases=0;
for(let len=1;len<=10;len++)for(let mask=0;mask<(1<<len);mask++){
 let M=I;
 for(let k=0;k<len;k++)M=mul(M,(mask&(1<<k))?R:T);
 ck(det(M)===(1n<<BigInt(len)),'det power len='+len+' mask='+mask);
 const rowSum=1n<<BigInt(len);
 for(let i=0;i<n;i++){
  ck(M[i].reduce((a,b)=>a+b,0n)===rowSum,'row sum');
  for(let j=0;j<n;j++)if(len>=4)ck(M[i][j]>0n,'full support');
 }
 cases++;
}
console.log(JSON.stringify({theorem:'C1-T5-FULLRANK-PATH-TRANSFER093',orientation_words:cases,assertions,failures:0,math:'BigInt exact determinants and endpoints, no floating point'},null,2));
