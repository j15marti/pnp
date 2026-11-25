const check = function check(){
 let assertions=0, sat=0, unsat=0, flowRows=0, jointRows=0, cases=0, selectorCases=0;
 const assert=x=>{assertions++;if(!x)throw Error("assertion "+assertions)};
 const bit=(w,i)=>(w>>i)&1;
 const legal=(c,w)=>{const s=c.reduce((a,[i,b])=>a+(bit(w,i)^b),0);return s===1||s===2};
 const rng=(()=>{let x=20261124;return n=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)%n}})();
 function test(n,F,anchor,base=null){
  let bad=F.map((c,i)=>legal(c,anchor)?-1:i).filter(i=>i>=0);
  assert(bad.length===1);
  let X=F.flat().map(([i])=>bit(anchor,i)),Y=X.slice();X[3*bad[0]]^=1;
  function clauseFlow(c,v){let k=c.reduce((a,[i,b])=>a+b,0),net=k+c.reduce((a,[i,b],j)=>a+(b?-v[j]:v[j]),0);return [1,2].filter(r=>r===net).length;}
  for(let j=0;j<F.length;j++){
   assert(clauseFlow(F[j],X.slice(3*j,3*j+3))===1);
   for(let w=0;w<8;w++){let v=[bit(w,0),bit(w,1),bit(w,2)];let s=v.reduce((a,b,i)=>a+(b^F[j][i][1]),0);assert(clauseFlow(F[j],v)===(s===1||s===2?1:0));flowRows++;}
   for(let i=0;i<3;i++)for(let b=0;b<2;b++)assert(Array.from({length:8},(_,w)=>w).some(w=>bit(w,i)===b&&clauseFlow(F[j],[bit(w,0),bit(w,1),bit(w,2)])===1));
  }
  assert(X.reduce((a,b,i)=>a+(b!==Y[i]),0)===1);
  let found=0;for(let w=0;w<(1<<n);w++){
   let z=F.flat().map(([i])=>bit(w,i));
   let a=F.every(c=>legal(c,w)),b=F.every((c,j)=>clauseFlow(c,z.slice(3*j,3*j+3))===1);
   assert(a===b);jointRows++;if(b)found++;
  }
  if(base){let source=0;for(let w=0;w<(1<<base.n);w++)if(base.F.every(c=>legal(c,w)))source++;assert(found===6*source);selectorCases++;}
  cases++;if(found)sat++;else unsat++;
 }
 // Fano and all 21 single-sign neighbors; choose an all-positive deletion witness, or find near witness.
 const f=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(c=>c.map(i=>[i,0]));
 for(let k=-1;k<21;k++){let F=f.map(c=>c.map(x=>x.slice()));if(k>=0)F[k/3|0][k%3][1]^=1;let a=Array.from({length:128},(_,i)=>i).find(w=>F.filter(c=>!legal(c,w)).length===1);assert(a!==undefined);test(7,F,a);}
 // BH15 selector construction on small random signed NAE sources, including repeated positions.
 for(let q=0;q<80;q++){
   let n=1+rng(4),m=1+rng(8),F=Array.from({length:m},()=>Array.from({length:3},()=>[rng(n),rng(2)]));
   let B=[];for(let i=0;i<n;i++)for(let j=0;j<3;j++)B.push([[2*n+j,1],[2*i,0],[2*i+1,0]]);
   B.push([[2*n,0],[2*n+1,0],[2*n+2,0]]);
   for(let c of F){let [a,b,d]=c.map(([i,s])=>2*i+s);B.push([[a^1,1],[b,0],[d,0]]);}
   test(2*n+3,B,0,{n,F});
 }
 return {seed:20261124,cases,sat,unsat,selectorCases,flowRows,jointRows,assertions,scope:"Local clause balances, marginal closure, one-mismatch anchors, exhaustive common-label comparisons; not a polynomial repair implementation."};
};
console.log(JSON.stringify(check(), null, 2));
