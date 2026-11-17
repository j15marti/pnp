'use strict';
// TMR-4/072 independent integer path-transfer audit. Node.js >=18.
const R = (a,b) => +( [1,3].includes((b-a+5)%5) );
const F = [0,1,0,1,0], B = [0,0,1,0,1];
function convol(a,b) {
  return Array.from({length:5},(_,d)=>a.reduce((s,x,i)=>s+x*b[(d-i+5)%5],0));
}
function coeff(bits) {
  return bits.reduce((v,bit)=>convol(v,bit?B:F),[1,0,0,0,0]);
}
function det(M) {
  // Fraction-free Bareiss algorithm, exact BigInt.
  const a = M.map(row=>row.map(BigInt));
  let divisor=1n,sign=1n;
  for(let k=0;k<4;k++) {
    if(a[k][k]===0n) {
      const p=a.findIndex((r,i)=>i>k&&r[k]!==0n);
      if(p<0)return 0n;
      [a[k],a[p]]=[a[p],a[k]];sign=-sign;
    }
    const pivot=a[k][k];
    for(let i=k+1;i<5;i++)for(let j=k+1;j<5;j++)
      a[i][j]=(a[i][j]*pivot-a[i][k]*a[k][j])/divisor;
    for(let i=k+1;i<5;i++)a[i][k]=0n;
    divisor=pivot;
  }
  return sign*a[4][4];
}
function brute(bits,a,b) {
  function rec(i,prev) {
    if(i===bits.length)return +(prev===b);
    let z=0;
    for(let c=0;c<5;c++)
      if(bits[i]?R(c,prev):R(prev,c)) z+=rec(i+1,c);
    return z;
  }
  return rec(0,a);
}
const A=Array.from({length:5},(_,a)=>Array.from({length:5},(_,b)=>R(a,b)));
if(det(A)!==2n)throw Error('det(A)');
let patterns=0,endpointChecks=0,fourDetChecks=0;
for(let len=1;len<=5;len++)for(let b=0;b<(1<<len);b++) {
  const bits=Array.from({length:len},(_,i)=>(b>>i)&1),c=coeff(bits);
  if(c.reduce((s,x)=>s+x,0)!==(2**len))throw Error('row sum');
  if((Math.min(...c)>0)!==(len>=4))throw Error('positivity threshold');
  for(let a=0;a<5;a++)for(let z=0;z<5;z++) {
    if(c[(z-a+5)%5]!==brute(bits,a,z))throw Error('exact pinned path count');
    endpointChecks++;
  }
  if(len===4) {
    const W=Array.from({length:5},(_,a)=>Array.from({length:5},(_,z)=>c[(z-a+5)%5]));
    if(det(W)!==16n)throw Error('det(W)');
    if(bits.reduce((s,x)=>s+x,0)===2)
      for(let a=0;a<5;a++)for(let z=0;z<5;z++)
        if(W[a][z]!==W[z][a])throw Error('balanced symmetry');
    fourDetChecks++;
  }
  patterns++;
}
console.log(JSON.stringify({status:'PASS',patterns,endpointChecks,fourDetChecks,
  detA:'2',detW:'16',universalMinimumPathLength:4}));
