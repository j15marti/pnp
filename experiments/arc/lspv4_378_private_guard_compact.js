'use strict';
// LSPV4/378: finite controls for clause-private selectors and MUS projection.
// Deterministic, standalone: node experiments/arc/lspv4_378_private_guard_compact.js
let checks=0;
function ok(x,m){checks++;if(!x)throw Error(m)}
function isSAT(F,n){for(let a=0;a<2**n;a++)if(F.every(C=>C.some(l=>(((a>>(Math.abs(l)-1))&1)===+(l>0)))))return true;return false}
function php(h){let F=[],id=(i,j)=>i*h+j+1;for(let i=0;i<=h;i++)F.push(Array.from({length:h},(_,j)=>id(i,j)));for(let j=0;j<h;j++)for(let i=0;i<=h;i++)for(let k=i+1;k<=h;k++)F.push([-id(i,j),-id(k,j)]);return F}
function boundary(F,t){return isSAT(F.filter((_,i)=>t>>i&1),Math.max(0,...F.flat().map(Math.abs)))}
function guarded(F,t){const n=Math.max(0,...F.flat().map(Math.abs)),m=F.length;
 const G=F.map((C,i)=>[-n-i-1,...C]);
 const units=Array.from({length:m},(_,i)=>[(t>>i&1)?n+i+1:-(n+i+1)]);
 return isSAT([...G,...units],n+m);
}
const U=[];for(let a of [0,1,-1])for(let b of [0,2,-2])U.push([a,b].filter(Boolean));
let sat=0,unsat=0,mus=0,projections=0;
for(let mask=0;mask<512;mask++){const F=U.filter((_,i)=>mask>>i&1),m=F.length;
 const s=isSAT(F,2);s?sat++:unsat++;
 const minimal=!s&&F.every((_,i)=>isSAT(F.filter((__,j)=>j!==i),2));if(minimal)mus++;
 for(let t=0;t<2**m;t++){const a=boundary(F,t),b=guarded(F,t);ok(a===b,'guard projection');if(minimal)ok(a===(t!==2**m-1),'MUS exact one-clause boundary');projections++;}
}
const lengths=[];
for(let h=1;h<=3;h++){const F=php(h),m=F.length,n=h*(h+1),L=F.reduce((x,C)=>x+C.length,0),b=Math.ceil(Math.log2(n+m+2));
 ok(!isSAT(F,n),'PHP UNSAT');for(let i=0;i<m;i++)ok(isSAT(F.filter((_,j)=>j!==i),n),'PHP deletion SAT');
 for(let i=0;i<18;i++)ok(boundary(F,(2**m-1)^(1<<(i%m))),'all proper activated subsets SAT');
 lengths.push({h,m,n,sourceBits:L*(b+1)+m+2*b,guardedBits:(L+m)*(b+1)+m+2*b,boundaryClauseBits:m*(b+1)+1});}
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function chargeModels(target){let k=0;for(let a=0;a<64;a++){const c=Array.from({length:4},(_,v)=>E.reduce((z,p,i)=>z^(p.includes(v)?a>>i&1:0),0));if(c.every((x,i)=>x===target[i]))k++;}return k}
ok(chargeModels([1,0,0,0])===0&&chargeModels([0,0,0,0])===8,'K4 parity control');
function guardedGrammar(G,F){const n=Math.max(0,...F.flat().map(Math.abs));return G.length===F.length&&G.every((r,i)=>JSON.stringify(r)===JSON.stringify([-(n+i+1),...F[i]]))}
let malformed=0;for(const bad of [[[-3,1],[-3,-1]],[[-4,1],[-3,-1]],[[3,1],[-4,-1]],[[-3,1]],[[-3,-1],[-4,1]],[[-3,1],[-4,-1,1]]]){ok(!guardedGrammar(bad,[[1],[-1]]),'malformed guard');malformed++}
console.log(JSON.stringify({cnf:512,sat,unsat,mus,projections,php:lengths,malformed,k4:{odd:0,even:8},checks}));
