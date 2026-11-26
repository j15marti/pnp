'use strict';
// FP18 independent recursive Laplace determinant and sparse set basis.
function fp18AlgebraAudit(){
  function* match(V,partial=false){
    if(!V.length){yield [];return}
    const [a,...r]=V;if(partial)yield* match(r,true);
    for(const b of r)for(const P of match(r.filter(v=>v!==b),partial))yield [[a,b],...P];
  }
  function path(p,P,C,s,t){
    const adj=Array.from({length:p},()=>[]);for(const [a,b] of [...P,...C]){adj[a].push(b);adj[b].push(a)}
    let u=s,last=-1;while(u!==t){const v=adj[u].find(x=>x!==last);if(v===undefined)return false;last=u;u=v}return true;
  }
  function mul(a,b){let c=0;while(b){if(b&1)c^=a;a<<=1;b>>=1}return c}
  function det(A){
    if(!A.length)return 1;
    let out=0;for(let j=0;j<A.length;j++)if(A[0][j])out^=mul(A[0][j],det(A.slice(1).map(r=>r.filter((_,k)=>k!==j))));
    return out;
  }
  let count=0;
  for(const p of [2,4,6]){
    const V=Array.from({length:p},(_,i)=>i);
    for(const P of match(V)){
      const M=Array.from({length:p},()=>new Int32Array(p));for(const [a,b] of P){M[a][b]=1;M[b][a]=1}
      for(let s=0;s<p;s++)for(let t=s+1;t<p;t++)for(const C of match(V.filter(v=>v!==s&&v!==t),true)){
        const N=M.map(r=>[...r]);for(const [a,b] of C){N[a][b]^=2;N[b][a]^=2}
        const cofactor=det(N.filter((_,i)=>i!==t).map(r=>r.filter((_,i)=>i!==s)));
        if(Boolean(cofactor)!==path(p,P,C,s,t))throw Error("cofactor mismatch");count++;
      }
    }
  }
  function* perms(V){if(!V.length){yield [];return}for(const x of V)for(const w of perms(V.filter(y=>x!==y)))yield [x,...w]}
  function feat(P,p){const m=Array(p);for(const [a,b] of P){m[a]=b;m[b]=a}const v=new Set();for(let s=0;s<2**p;s++){let t=0;for(let i=0;i<p;i++)if(s>>i&1)t|=1<<m[i];v.add((s<<p)|t)}return v}
  function xor(a,b){for(const x of b)if(a.has(x))a.delete(x);else a.add(x)}
  const P=[...perms([0,1,2,3,4])].map(w=>w.map((v,i)=>[i,5+v]));
  const piv=new Map(),total=new Set(),R=[];
  for(const w of P){const v=feat(w,10);xor(total,v);while(v.size){let j=-1;for(const i of v)if(i>j)j=i;if(!piv.has(j)){piv.set(j,v);R.push(w);break}xor(v,piv.get(j))}}
  if(total.size||R.length!==119)throw Error("basis rank");
  let contexts=0;
  const V=Array.from({length:10},(_,i)=>i);
  for(let s=0;s<10;s++)for(let t=s+1;t<10;t++)for(const C of match(V.filter(v=>v!==s&&v!==t),true)){
    if(P.some(w=>path(10,w,C,s,t))!==R.some(w=>path(10,w,C,s,t)))throw Error("representative mismatch");contexts++;
  }
  return {directLaplaceCofactorChecks:count,fullPermutationTable:P.length,minorBasisRank:R.length,allContextChecks:contexts};
}
console.log(JSON.stringify(fp18AlgebraAudit(),null,2));
