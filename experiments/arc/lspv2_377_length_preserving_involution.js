'use strict';
// LSPV-2/377: fixed all-input, length-preserving, SAT-label-preserving involution.
// Pure Node.js, no dependencies. This is NOT an SAT decider or a proof-size optimizer.
function pair(h) {
  if (!Number.isSafeInteger(h) || h<1) throw Error("h");
  const n=h*(h+1),m=h+1+h*h*(h+1)/2,P=[],Q=[[1],[-1]];
  for(let i=0;i<=h;i++){const c=[];for(let j=1;j<=h;j++)c.push(i*h+j);P.push(c);}
  for(let j=1;j<=h;j++)for(let i=0;i<=h;i++)for(let k=i+1;k<=h;k++)P.push([-(i*h+j),-(k*h+j)]);
  for(let a=1;a<=n&&Q.length<m;a++)for(let b=a+1;b<=n&&Q.length<m;b++)Q.push([a,b]);
  if(P.length!==m||Q.length!==m)throw Error("source counts");
  function serialize(rows){return "p cnf "+n+" "+m+"\n"+rows.map(c=>c.join(" ")+" 0\n").join("");}
  const x=serialize(P),y=serialize(Q),N=x.length+y.length+8;
  const X="c X"+"x".repeat(N-x.length-4)+"\n"+x;
  const Y="c Y"+"y".repeat(N-y.length-4)+"\n"+y;
  if(X.length!==N||Y.length!==N||X===Y)throw Error("length match");
  return {h,n,m,N,X,Y,P,Q};
}
function transform(s) {
  if(typeof s!=="string"||/[^\x00-\x7f]/.test(s))return s;
  for(let h=1;h<=s.length;h++){
    const z=pair(h);
    if(z.N===s.length)return s===z.X?z.Y:(s===z.Y?z.X:s);
    if(z.N>s.length)return s;
  }
  return s;
}
function models(n,clauses) {
  if(n>12)return null;
  let count=0;
  for(let mask=0;mask<2**n;mask++){
    if(clauses.every(c=>c.some(l=>((mask>>(Math.abs(l)-1))&1)==(l>0?1:0))))count++;
  }
  return count;
}
function test(){
  let assertions=0,flips=0;const cases=[];
  function ok(b){if(!b)throw Error("verification failure");assertions++;}
  for(let h=1;h<=5;h++){
    const z=pair(h);
    ok(z.X.length===z.Y.length);ok(z.P.length===z.m&&z.Q.length===z.m);
    ok(new Set(z.Q.map(c=>c.join(","))).size===z.m);
    ok(transform(z.X)===z.Y);ok(transform(z.Y)===z.X);
    ok(transform(transform(z.X))===z.X);
    if(h<=3){
      ok(models(z.n,z.P)===0);ok(models(z.n,z.Q)===0);
      for(let a=0;a<z.P.length;a++)for(let b=0;b<z.P[a].length;b++){
        const t=z.P.map(c=>c.slice());t[a][b]*=-1;ok(models(z.n,t)>0);flips++;
      }
    }
    cases.push({h,n:z.n,m:z.m,bytes:z.N,full_model_test:h<=3});
  }
  for(let s of ["","p cnf","nonsense","p cnf 1 1\n1 0\n","p cnf 1 2\n1 0\n-1 0\n"])ok(transform(s)===s);
  return {status:"PASS",assertions,sign_flips:flips,cases,B1:"OPEN for Rmix341",B2:"OPEN",B3:"OPEN"};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(test(),null,2));
if(typeof module!=="undefined")module.exports={pair,transform,models,test};
