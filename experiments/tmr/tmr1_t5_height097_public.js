'use strict';
// TMR-1/097 independent public replay. Node.js; zero dependencies.
const assert=require('node:assert/strict');
const R=(x,y)=>[1,3].includes((y-x+5)%5);
let assertions=0, dags=0, shallow=0, graphs=0;
function ok(b){assertions++;assert.ok(b);}
for(let n=0;n<=6;n++){
 const E0=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)E0.push([u,v]);
 for(let mask=0;mask<2**E0.length;mask++){
  dags++;const h=Array(n).fill(0),E=[];
  for(let j=0;j<E0.length;j++)if(mask&2**j){const [u,v]=E0[j];E.push([u,v]);h[v]=Math.max(h[v],h[u]+1);}
  if(Math.max(0,...h)<=2){shallow++;const a=h.map(i=>[0,3,1][i]);ok(E.every(([u,v])=>R(a[u],a[v])));}
 }
}
const S=Array.from({length:5},(_,x)=>Array.from({length:5},(_,y)=>
 Array.from({length:5},(_,z)=>Number(R(x,z)&&R(y,z))).reduce((a,b)=>a+b)));
for(let x=0;x<5;x++)for(let y=0;y<5;y++){
 const d=(y-x+5)%5;ok(S[x][y]===(d===0?2:([2,3].includes(d)?1:0)));
}
function digits(t,n){const a=[];for(let i=0;i<n;i++){a.push(t%5);t=Math.floor(t/5);}return a;}
const tt4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let tt4Hom=0;for(let t=0;t<625;t++){const a=digits(t,4);if(tt4.every(([u,v])=>R(a[u],a[v])))tt4Hom++;}ok(tt4Hom===0);
for(let n=0;n<=5;n++){
 const all=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)all.push([u,v]);
 for(let mask=0;mask<2**all.length;mask++){
  graphs++;const E=all.filter((_,j)=>mask&2**j),coeff=Array(E.length+1).fill(0n);
  for(let t=0;t<5**n;t++){
   const a=digits(t,n);let j=0,valid=true;
   for(const [u,v] of E){const d=(a[v]-a[u]+5)%5;if(d===0)j++;else if(![2,3].includes(d)){valid=false;break;}}
   if(valid)coeff[j]++;
  }
  const k=Math.max(1,3*n),z=1n<<BigInt(k);
  let y=0n,power=1n;for(const c of coeff){y+=c*power;power*=z;}
  ok(coeff.every(c=>c<z));ok(y%z===coeff[0]);
 }
}
console.log(JSON.stringify({dags,shallow,graphs,tt4Hom,assertions,failures:0,proof:'separate arbitrary-size theorem, this is finite COMPUTATIONAL replay'}));
