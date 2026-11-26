// Standalone exact integer-scaled Fourier and recurrence audit. Node.js.
function audit(){
 const Z=Array.from({length:16},(_,m)=>Array.from({length:4},(_,j)=>m>>j&1?1n:-1n));
 const pairs=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)pairs.push([i,j]);
 const abs=x=>x<0n?-x:x, prod=z=>z.reduce((a,b)=>a*b,1n);
 let seed=26112621n;const rng=()=>{seed=(1664525n*seed+1013904223n)%4294967296n;return seed%1001n-500n;};
 let checked=0,nonzero=0,recurrences=0,chainChecks=0;
 for(let t=0;t<1000;t++){
  const F=Array(16);for(let m=0;m<8;m++)F[m]=F[m^15]=rng();
  let c=F.reduce((a,b)=>a+b,0n),p=pairs.map(([i,j])=>Z.reduce((a,z,m)=>a+F[m]*z[i]*z[j],0n)),q=Z.reduce((a,z,m)=>a+F[m]*prod(z),0n);
  let a=2n*abs(q),eta=[q>0n?-1n:1n,1n,1n,1n]; if(q)nonzero++;
  c-=3n*a/2n;p=p.map((w,i)=>w-a*eta[pairs[i][0]]*eta[pairs[i][1]]/2n);
  for(let m=0;m<16;m++){let z=Z[m],v=c+p.reduce((s,w,i)=>s+w*z[pairs[i][0]]*z[pairs[i][1]],0n)+abs(a*z.reduce((s,b,i)=>s+b*eta[i],0n));if(v!==16n*F[m])throw Error("Fourier response mismatch");checked++;}
 }
 for(let n=8n;n<=400n;n++)for(let a=2n;2n*a+4n<=n;a++){if(8n*(a+1n)**6n+(n-a+1n)**6n>n**6n-1n)throw Error("recurrence");recurrences++;}
 // Each subset of x<=y has exact unit/implication representation after deleting chain words.
 const chain=[[0,0],[0,1],[1,1]];
 for(let mask=0;mask<8;mask++)for(let x=0;x<2;x++)for(let y=0;y<2;y++){
  const truth=x<=y&&((x===0&&y===0)?!!(mask&1):x===0?!!(mask&2):!!(mask&4));
  const formula=x<=y&&((mask&1)||y===1)&&((mask&2)||x>=y)&&((mask&4)||x===0);
  if(truth!==!!formula)throw Error("chain pin mismatch");chainChecks++;
 }
 return {checked,nonzero,recurrences,chainChecks,seed:26112621};
}
console.log(JSON.stringify(audit(),null,2));
