// TMR-4/073, independent exact integer transfer audit; Node.js 18+.
'use strict';
const A=Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>+(new Set([1,3]).has((j-i+5)%5))));
const AT=A.map((r,i)=>r.map((_,j)=>A[j][i]));
const I=A.map((r,i)=>r.map((_,j)=>+(i===j)));
function mul(X,Y){return X.map((r,i)=>r.map((_,j)=>r.reduce((v,a,k)=>v+a*Y[k][j],0)));}
function fac(bits){let P=I;for(const b of bits)P=mul(P,b?A:AT);return P;}
function det(X){ // exact fraction-free Bareiss elimination
 let sign=1,previous=1;
 for(let k=0;k<4;k++){
   let a=k;while(a<5&&X[a][k]===0)a++;if(a===5)return 0;
   if(a!==k){[X[k],X[a]]=[X[a],X[k]];sign=-sign;}
   const pivot=X[k][k];
   for(let i=k+1;i<5;i++)for(let j=k+1;j<5;j++){
     const numerator=X[i][j]*pivot-X[i][k]*X[k][j];
     if(numerator%previous!==0)throw Error('nonexact determinant division');
     X[i][j]=numerator/previous;
   }
   for(let i=k+1;i<5;i++)X[i][k]=0;
   previous=pivot;
 }
 return sign*X[4][4];
}
let patterns=0,brutes=0,cycleChecks=0,allPositive=true;
for(let p=0;p<16;p++){
 let bits=[0,1,2,3].map(i=>(p>>i)&1),W=fac(bits);
 if(W.some(r=>r.some(x=>x<=0)||r.reduce((a,b)=>a+b,0)!==16))throw Error('positive/rows');
 for(let j=0;j<5;j++)if(W.reduce((a,r)=>a+r[j],0)!==16)throw Error('columns');
 if(det(W.map(r=>r.slice()))!==16)throw Error('determinant');
 let count=0;for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)for(let d=0;d<5;d++)for(let e=0;e<5;e++){
   let x=[a,b,c,d,e],ok=true;
   for(let j=0;j<4;j++){let u=bits[j]?x[j]:x[j+1],v=bits[j]?x[j+1]:x[j];
     if(![1,3].includes((v-u+5)%5)){ok=false;break;}}
   if(ok)count++;
 }
 if(count!==W.flat().reduce((a,b)=>a+b,0))throw Error('brute');
 patterns++;brutes++;
}
let q0=2,q1=7;
for(let n=2;n<=40;n++){
 let q=7*q1-q0;[q0,q1]=[q1,q];
 if(n>=3&&n<=10){let P=I,W=fac([1,1,0,0]);for(let j=0;j<n;j++)P=mul(P,W);
 if(P.reduce((s,r,i)=>s+r[i],0)!==16**n+2*q)throw Error('cycle trace');cycleChecks++;}
}
console.log(JSON.stringify({source:'TMR4/073',patterns,brutes,cycleChecks,allPositive,determinant:16,failures:0}));
