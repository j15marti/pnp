'use strict';
// TMR-1/077 independent connected V8 arithmetic certificate; no source parser (full parser audit is separate).
const colors=[0,2,3], representatives=[[0,2,3],[2,0,3],[2,3,0]];
const p=x=>x===0?2n:1n;
const q=(a,b)=>a===b?0n:(a!==0&&b!==0?3n:1n);
function W(a,b,c){
  let s=0n;
  for(const x of colors)for(const y of colors)for(const z of colors){
    if(x===y||y===z||x===z)continue;
    s+=p(x)*p(y)*p(z)*q(x,y)*q(x,z)*q(y,z)*q(x,a)*q(y,b)*q(z,c);
  }
  return s;
}

function palette(T,F,B){
  const alpha=p(T)*p(F)*q(T,F)*q(T,B)*q(F,B);
  const L=[];
  for(let code=0;code<8;code++){
    const a=(code&4)?T:F,b=(code&2)?T:F,c=(code&1)?T:F;
    let v=0n;
    for(const s of [T,F])v+=W(a,b,s)*W(s===T?F:T,c,F);
    L.push(alpha*v);
  }
  return {alpha,L};
}

function denseDP(n,alpha,L){
  let dp=Array(n+1).fill(0n);dp[0]=1n;
  const M=[[L[0],L[3]],[L[4],L[7]]];
  for(let j=0;j<n;j++){
    const next=Array(n+1).fill(0n);
    for(let t=0;t<=j;t++)if(dp[t]!==0n)
      for(let b=0;b<2;b++)next[t+b]+=dp[t]*M[0][b]**BigInt(j-t)*M[1][b]**BigInt(t);
    dp=next;
  }
  return alpha**BigInt(n)*dp.reduce((a,b)=>a+b,0n);
}

function denseDirect(n,alpha,L){
  let sum=0n;
  for(let mask=0;mask<2**n;mask++){
    let v=1n;
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
      const a=(mask>>i)&1,b=(mask>>j)&1;
      v*=L[4*a+3*b];
    }
    sum+=v;
  }
  return alpha**BigInt(n)*sum;
}

function run(){
  let checks=0;
  const expected=[
    [0,7776,7776,5184,7776,5184,2592,864],
    [0,864,864,5184,864,5184,2592,7776],
    [0,34992,34992,69984,34992,69984,34992,34992]
  ];
  const rows=representatives.map(pal=>palette(...pal));
  for(let i=0;i<3;i++){
    if(rows[i].L.some((x,j)=>x!==BigInt(expected[i][j])))throw Error('table mismatch');
    checks+=8;
  }
  let family=[];
  for(let n=2;n<=9;n++){
    let dp=0n,direct=0n;
    for(const row of rows){
      dp+=denseDP(n,row.alpha,row.L);
      direct+=denseDirect(n,row.alpha,row.L);
      checks++;
    }
    if(dp!==direct)throw Error('DP vs full 2^n assignment sum');
    family.push({n,satSolutions:n+1,t5Count:(120n*dp).toString()});
  }
  return {revision:'tmr1-t5-weighted077-published-certificate-v1',checks,failures:0,
    palettes:rows.map((r,i)=>({source:representatives[i],alpha:r.alpha.toString(),L:r.L.map(String)})),
    families:family,scope:'arithmetic/DP certificate; signed source parser and NAE local checks are in separate executed full audit'};
}
console.log(JSON.stringify(run(),null,2));
