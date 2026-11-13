"use strict";
// TMR-3 / TWO-WAY-CROSSING-TRADEOFF002 independent finite regression.
// No TM simulation: checks exact signed clauses and legal cut-and-paste source locality.
const audit=function audit(){
  const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
  const E=(n,a,b)=>{
    const N=5*n,M=8*n,w=Math.max(1,Math.ceil(Math.log2(N)));
    const f=(s,v)=>String(s)+v.toString(2).padStart(w,"0");
    let z="1".repeat(N)+"0"+"1".repeat(M)+"0";
    for(let side=0;side<2;side++)for(let i=0;i<n;i++){
      const bit=((side?b:a)>>>i)&1, first=1-bit, h=(side?3:1)*n+2*i;
      for(let u=0;u<2;u++)for(let v=0;v<2;v++)z+=f(first,i)+f(u,h)+f(v,h+1);
    }
    return z;
  };
  let r={model:"single sequential two-way read-only input head, constant work tapes; encoded strict-3CNF equality family",seed:null,exhaustive:true,pairs:0,sat:0,unsat:0,localGadgetTruth:0,splices:0,invalidCrossSplices:0,cutsTested:0,casesByN:{},minUpperRatio:100,maxUpperRatio:0};
  for(let sign=0;sign<2;sign++)for(let x=0;x<2;x++)for(let u=0;u<2;u++)for(let v=0;v<2;v++){
    let all=true;
    for(let su=0;su<2;su++)for(let sv=0;sv<2;sv++){
      let lit=(sign===0?x===1:x===0)|| (su===0?u===1:u===0) || (sv===0?v===1:v===0);
      all=all&&lit;
    }
    assert(all===(sign===0?x===1:x===0),"unit forcing gadget");r.localGadgetTruth++;
  }
  for(let n=1;n<=5;n++){
    const w=Math.max(1,Math.ceil(Math.log2(5*n))),g=12*(1+w),h=13*n+2,L=h+2*n*g,N=1<<n,diagonals=[];
    for(let a=0;a<N;a++)diagonals[a]=E(n,a,a);
    for(let a=0;a<N;a++)for(let b=0;b<N;b++){
      let z=E(n,a,b);
      assert(z.length===L,"length for "+n);assert(z.slice(0,h)==="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0","header");
      r.pairs++;if(a===b)r.sat++;else r.unsat++;
    }
    let nx=0;
    for(let j=Math.ceil(n/2);j<n;j++){
      const suffixCount=1<<(n-j),prefixCount=1<<j;
      for(let v=0;v<suffixCount;v++)for(let u1=0;u1<prefixCount;u1++)for(let u2=0;u2<prefixCount;u2++){
        const a1=u1+(v<<j),a2=u2+(v<<j),left=diagonals[a1],right=diagonals[a2],correct=E(n,a1,a2);
        for(let t=0;t<g;t++){
          const cut=h+j*g+t;
          assert(left.slice(0,cut)+right.slice(cut)===correct,"splice failed n="+n+" j="+j+" t="+t);
          r.splices++;nx++;
          if(u1!==u2)r.invalidCrossSplices++;
        }
      }
      r.cutsTested+=g;
    }
    const upper=(L+4*n)*(n+1)/(L*n);
    r.minUpperRatio=Math.min(upper,r.minUpperRatio);r.maxUpperRatio=Math.max(upper,r.maxUpperRatio);
    r.casesByN[n]={encodedLength:L,recordBits:1+w,gadgetBits:g,diagonals:N,cutsWithinFixedSuffixGadgets:(n-Math.ceil(n/2))*g,splices:nx};
  }
  r.minUpperRatio=Number(r.minUpperRatio.toFixed(6));r.maxUpperRatio=Number(r.maxUpperRatio.toFixed(6));
  return r;
};
const result=audit();
console.log(JSON.stringify(result,null,2));
