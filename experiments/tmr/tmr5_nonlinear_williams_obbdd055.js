#!/usr/bin/env node
"use strict";
// Independent exhaustive nonaffine, canonical-source and prefix-rank verifier.
const verify = function verify() {
  let assertions=0,cases=0,edges=0,malformed=0,ranks=0;
  const ck=(v,s)=>{if(!v)throw new Error(s);assertions++};
  const F=(p,a,x)=>(p&a)^x;
  const bits=(n,k)=>Array.from({length:k},(_,j)=>(n>>(k-j-1))&1);
  const src=(xs,b)=>"1".repeat(b-1)+"0"+xs.map(x=>x+"1".repeat(b-2)+"0").join("");
  function parse(s){
    if(!/^[01]+$/.test(s))return null;
    let z=s.indexOf("0");if(z<2)return null;let b=z+1;
    if(s.length<2*b||s.length%b)return null;
    let out=[];
    for(let i=b;i<s.length;i+=b){let r=s.slice(i,i+b);if(r.slice(1)!=="1".repeat(b-2)+"0")return null;out.push(+r[0]);}
    return [b,out];
  }
  function physical(xs,b){
    let work=new Map(),last=new Map(),p=0,pos=b-1,d=1,moves=b-1,trace=[];
    for(let j=1;j<=xs.length;j++){
      let v=F(p,work.get(pos)||0,xs[j-1]);
      trace.push([j,last.get(pos)||0,pos]);
      work.set(pos,v);last.set(pos,j);p=v;pos+=d;moves++;d=-d;
    }return {p,trace,moves};
  }
  function obdd(xs){let p=0,a=0;for(let x of xs){let z=F(p,a,x);a=p;p=z;}return p;}
  function count(B){let S=new Map([["0,0",1n]]);for(let j=0;j<B;j++){
    let T=new Map();for(let [s,c] of S){let [p,a]=s.split(",").map(Number);
      for(let x of [0,1]){let k=F(p,a,x)+","+p;T.set(k,(T.get(k)||0n)+c);}
    }S=T;
  }let ans=0n;for(let [s,c] of S)if(s[0]==="1")ans+=c;return [ans,S];}
  function rank(A,prime){
    A=A.map(row=>row.map(x=>x%prime));let m=A.length,n=A[0].length,r=0;
    function inv(x){for(let v=1;v<prime;v++)if(x*v%prime===1)return v;throw Error("non-field")}
    for(let j=0;j<n&&r<m;j++){
      let i=r;while(i<m&&!A[i][j])i++;if(i===m)continue;
      [A[i],A[r]]=[A[r],A[i]];let z=inv(A[r][j]);
      for(let h=j;h<n;h++)A[r][h]=A[r][h]*z%prime;
      for(let k=r+1;k<m;k++){z=A[k][j];if(z)for(let h=j;h<n;h++)A[k][h]=((A[k][h]-z*A[r][h])%prime+prime)%prime;}
      r++;
    }return r;
  }
  for(let b=3;b<=6;b++)for(let B=1;B<=9;B++){
    for(let code=0;code<2**B;code++){
      let xs=bits(code,B),word=src(xs,b),parsed=parse(word);
      ck(parsed&&parsed[0]===b&&parsed[1].join("")===xs.join(""),"auth");
      let v=physical(xs,b);ck(v.p===obdd(xs),"same terminal");
      ck(v.moves===b-1+B,"head movements");
      for(let [j,last,pos] of v.trace){
        ck(pos===b-1+(j-1)%2,"head position");
        ck(last===(j<=2?0:j-2),"authentic revisit");
        if(j>=3)edges++;
      }
      cases++;
    }
    let s=src(Array(B).fill(0),b);
    for(let bad of [s.slice(0,-1),s+"0",s.slice(0,b+1)+"0"+s.slice(b+2),"0"+s,s+"x"]){
      ck(parse(bad)===null,"malformed");malformed++;
    }
  }
  for(let B=1;B<=9;B++){
    let [num,S]=count(B);ck(num===2n**BigInt(B-1),"balanced count");
    ck(S.size<=4,"4 states");
    ck(Array.from(S.values()).reduce((a,b)=>a+b,0n)===2n**BigInt(B),"state multiplicities");
    for(let k=0;k<=B;k++)for(let prime of [2,101]){
      let M=Array.from({length:2**k},(_,i)=>Array.from({length:2**(B-k)},(_,j)=>obdd([...bits(i,k),...bits(j,B-k)])));
      ck(rank(M,prime)<=4,"rank <=4");ranks++;
    }
  }
  ck(F(0,0,0)^F(1,0,0)^F(0,1,0)^F(1,1,0),"degree two");
  for(let j=3;j<=9;j++){
    let seen=new Set();for(let z=0;z<2**(j-1);z++){
      let p=0,a=0;for(let x of bits(z,j-1)){let v=F(p,a,x);a=p;p=v;}
      seen.add(p+","+a);
    }ck(seen.size===4,"all prior states attainable");
  }
  function fib(n){let a=0n,b=1n;for(let i=0;i<n;i++)[a,b]=[b,a+b];return a;}
  let Q=fib(66)-1n;ck(Q===27777890035287n,"B64 exact Q");
  return {revision:"tmr5-nonlinear-fibonacci055.v2-js",status:"COMPUTATIONAL",seed:null,assertions,failures:0,authentic_source_runs:cases,genuine_revisit_edges:edges,malformed_rejections:malformed,prefix_rank_checks:ranks,B64:{naive_no_cache_Q:String(Q),OBDD_nodes_upper:256,exact_accepting_inputs:String(2n**63n)}};
};
if (typeof module!=="undefined"&&require.main===module) console.log(JSON.stringify(verify(),null,2));
