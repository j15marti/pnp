const pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
function parts(n){const a=[];function visit(p){if(p.length===n){a.push(p);return}for(let j=0;j<=Math.max(-1,...p)+1;j++)visit([...p,j])}visit([]);return a}
function pairSet(n,p){let x=0,i=0;for(let a=0;a<n;a++)for(let b=a+1;b<n;b++,i++)if(p[a]!==p[b])x|=1<<i;return x}
function audit(){
 const P=parts(6),E=P.map(p=>pairSet(6,p)), target=pairSet(6,[0,0,0,0,0,0]);let mask=0,z=0;
 for(let a=0;a<6;a++)for(let b=a+1;b<6;b++,z++)if((a===0&&b===5)||(a===1&&b===4)||(a===2&&b===3))mask|=1<<z;
 let checks=0;for(const a of E)for(const b of E){if((a&b)===mask)throw Error("three disjoint pairs representable");checks++}
 const S=parts(5),F=S.map(p=>pairSet(5,p));let seed=26112619;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};let progress=0,none=0,partial=0;
 for(let t=0;t<3000;t++){
  const p=S[rnd(S.length)],a=pairSet(5,p);if(!a)continue;
  const possible=a&rnd(1024),T=possible&rnd(1024),bad=possible&~T;if(!T||!bad)continue;
  const admissible=F.some(b=>(b&~a)===0&&(b&T)===T&&(bad&~b)!==0);
  let single=false;
  for(let i=0;i<=Math.max(...p);i++)for(let j=i+1;j<=Math.max(...p);j++){
    const b=pairSet(5,p.map(x=>x===j?i:x));
    if((b&T)===T&&(bad&~b)!==0)single=true;
  }
  if(single!==admissible)throw Error("safe merge completeness");
  if(single){progress++;if(!F.some(b=>(b&~a)===0&&(b&T)===T&&!(bad&b)))partial++;}else none++;
 }
 return {rankTwoPartitions6:P.length,threeDisjointPairIntersections:checks,threeDisjointPairRepresentations:0,safeMergeChecks:progress+none,progress,none,progressWithoutFullCompletion:partial,seed:26112619}
}
console.log(JSON.stringify(audit(),null,2));
