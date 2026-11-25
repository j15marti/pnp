'use strict';
function guardCheck(){
  let assertions=0,charts=0,triangleChecks=0,models=0,words=0;
  const ok=b=>{assertions++;if(!b)throw Error("assertion "+assertions)};
  // Four disjoint NAE triples, 4 separated anchors, 2 relative parity guards.
  // Scale G by 3; G' by 9.
  const n=12, anchors=[0,3,6,9],pairs=[[0,3],[6,9]],orig=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?3:Math.floor(i/3)===Math.floor(j/3)?-1:0));
  const triples=Array.from({length:4},(_,i)=>[3*i,3*i+1,3*i+2]);
  for(let a of [0,1,-1])for(let b of [0,1,-1]){
    const flags=[a,b], G=orig.map(r=>r.map(x=>3*x));
    for(let t=0;t<2;t++)if(flags[t]){const [u,v]=pairs[t],s=flags[t];for(let i=0;i<n;i++)for(let j=0;j<n;j++)G[i][j]+=s*(orig[i][u]*orig[j][v]+orig[i][v]*orig[j][u])}
    charts++;let count=0;
    for(let i=0;i<n;i++){ok(G[i][i]===9);for(let j=0;j<n;j++)ok(G[i][j]===G[j][i])}
    for(let t=0;t<2;t++)if(flags[t]){const [u,v]=pairs[t];ok(G[u][v]===9*flags[t]);for(let j=0;j<n;j++)ok(G[u][j]===flags[t]*G[v][j])}
    for(const c of triples){for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)ok(G[c[i]][c[j]]===-3)}
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)for(let s of [1,-1])for(let t of [1,-1]){ok(9+s*G[i][j]+t*G[i][k]+s*t*G[j][k]>=0);triangleChecks++}
    // Exact PSD check by rational fraction-free Schur updates, positive pivots or zero row.
    let M=G.map(r=>r.map(BigInt));let rank=0;
    function gcd(x,y){x=x<0n?-x:x;y=y<0n?-y:y;while(y){let t=x%y;x=y;y=t}return x}
    for(let i=0;i<n;i++){
      const p=M[i][i];ok(p>=0n);
      if(p===0n){for(let j=i+1;j<n;j++)ok(M[i][j]===0n);continue}
      rank++;
      for(let j=i+1;j<n;j++)for(let k=i+1;k<n;k++)M[j][k]=p*M[j][k]-M[j][i]*M[i][k];
      let g=0n;for(let j=i+1;j<n;j++)for(let k=i+1;k<n;k++)g=gcd(g,M[j][k]);if(g>1n)for(let j=i+1;j<n;j++)for(let k=i+1;k<n;k++)M[j][k]/=g;
    }
    ok(rank===n-flags.filter(Boolean).length);
    for(let x=0;x<(1<<n);x++){words++;const s=i=>1-2*((x>>i)&1);if(!triples.every(c=>!(s(c[0])===s(c[1])&&s(c[1])===s(c[2]))))continue;if(!pairs.every(([u,v],j)=>!flags[j]||s(u)*s(v)===flags[j]))continue;count++}
    ok(count===6**4/2**flags.filter(Boolean).length);models+=count;
  }
  return {scope:"small disjoint NAE triple SAT control; exact PSD and guard fusion only; no high-girth UNSAT instance generated",charts,triangleChecks,reference_words:words,model_count_sum:models,assertions};
}
console.log(JSON.stringify(guardCheck(),null,2));
