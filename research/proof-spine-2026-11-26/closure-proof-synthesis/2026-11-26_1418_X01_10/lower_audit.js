function extraAudit(){
 let checks=0;const ok=(v,m)=>{checks++;if(!v)throw Error(m||"check "+checks)};
 const pc=n=>{let k=0;while(n){n&=n-1;k++}return k},bits=(n,S)=>Array.from({length:n},(_,i)=>i).filter(i=>S>>i&1),mask=a=>a.reduce((v,i)=>v|(1<<i),0);
 const sign=a=>{let p=0;for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)if(a[i]>a[j])p^=1;return p};
 let cutCases=0,cycleWitnesses=0,detChecks=0;
 for(let n=2;n<=7;n++)for(let S=1;S<(1<<n)-1;S++){cutCases++;const V=(1<<n)-1,A=bits(n,S),E=bits(n,V^S);let ct=0;
  for(let T=0;T<=V;T++)if(pc(T)===A.length){let L=bits(n,T),R=bits(n,V^T);
    // Laplace block sign, all canonical image subsets are independent and nonzero.
    let w=Array(n);A.forEach((v,i)=>w[v]=L[i]);E.forEach((v,i)=>w[v]=R[i]);let eps=sign(w);
    for(let rev of [false,true]){let p=rev?L.slice().reverse():L,q=rev?R.slice().reverse():R;let u=Array(n);A.forEach((v,i)=>u[v]=p[i]);E.forEach((v,i)=>u[v]=q[i]);ok(sign(u)===(eps^sign(p)^sign(q)));detChecks++}
    if(T!==S){let B=bits(n,S&~T),C=bits(n,T&~S),I=bits(n,S&T),J=bits(n,V&~(S|T)),tour=[B[0],...I,C[0],...J];for(let j=1;j<B.length;j++)tour.push(B[j],C[j]);ok(new Set(tour).size===n);let succ=Array(n);tour.forEach((u,i)=>succ[u]=tour[(i+1)%n]);ok(mask(A.map(v=>succ[v]))===T);let cur=0,seen=new Set();while(!seen.has(cur)){seen.add(cur);cur=succ[cur]}ok(cur===0&&seen.size===n);ct++;cycleWitnesses++}
   }
  let bin=1;for(let j=1;j<=A.length;j++)bin=bin*(n-j+1)/j;ok(ct===bin-1)
 }
 const S=[0,1,2];let stab=R=>R.filter(d=>R.every(x=>R.includes(x^d)));ok(stab(S).length===1);let sum=[...new Set(S.flatMap(x=>S.map(y=>x^y)))];ok(sum.length===4&&stab(sum).length===4);for(let z=0;z<4;z++)ok(S.some(x=>S.includes(x^z)));
 return {checks,cutCases,cycleWitnesses,detChecks,pairMerge:{local:[0,1,2],localStabilizerRank:0,sumSupport:sum,mergedStabilizerRank:2},limits:"determinant sign factorization checked on sorted and reversed assignments, not full symbolic circuit execution; all S,T through n7, constructive cycle checks; pair merge finite relation check"}
}
console.log(JSON.stringify(extraAudit(),null,2));
