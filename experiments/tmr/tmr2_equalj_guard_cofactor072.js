#!/usr/bin/env node
"use strict";
function run() {
  let checks=0, failures=0; const samples=[];
  const ok=(cond,msg)=>{checks++;if(!cond){failures++;throw Error("FAIL "+msg)}};
  const parity=(x)=>{let p=0;while(x){p^=x&1;x>>>=1}return p};
  const val=(lit,values)=>{let b=values[Math.abs(lit)]===1;return lit>0?b:!b};
  const sat=(cnf,values)=>cnf.every(c=>c.some(l=>val(l,values)));
  function build(k) {
    const X=Array.from({length:k},(_,i)=>1+i),Y=Array.from({length:k},(_,i)=>1+k+i),Z=[2*k+1,2*k+2,2*k+3],P=[2*k+4,2*k+5,2*k+6];
    const D=[];
    for(let i=0;i<k;i++){D.push([-X[i],Y[i]]);D.push([X[i],-Y[i]])}
    D.push(Z.slice());for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)D.push([-Z[i],-Z[j]]);
    const F=[];
    for(let b=0;b<=1;b++)for(let t=0;t<8;t++)if(parity(t)!==b){F.push(P.map((v,i)=>((t>>i)&1)?-v:v))}
    let next=P[2]+1;const gates=[],B=[];
    function gate(op,a,b) {const out=next++;gates.push({op,a,b,out});if(op==="and")B.push([-out,a],[-out,b],[out,-a,-b]);else B.push([out,-a],[out,-b],[-out,a,b]);return out}
    const viol=D.map(d=>{let t=-d[0];for(let i=1;i<d.length;i++)t=gate("and",t,-d[i]);return t});
    let root=viol[0];for(let i=1;i<viol.length;i++)root=gate("or",root,viol[i]);B.push([root]);
    const A=D.flatMap(d=>F.map(c=>d.concat(c)));
    function extension(shared) {
      const a={...shared};for(const g of gates){const u=val(g.a,a),v=val(g.b,a);a[g.out]=(g.op==="and"?(u&&v):(u||v))?1:0}return a
    }
    return {X,Y,Z,P,D,F,A,B,gates,root,extension,totalVars:next-1};
  }
  for (let k=2;k<=6;k++) {
    const v=build(k), n=2*k+3, tests=1<<n; let trueI=0, trueB=0;
    ok(v.D.length===2*k+4,`D cardinal ${k}`);
    ok(v.F.length===8,`F cardinal ${k}`);
    ok(v.A.length===8*(2*k+4),`A cardinal ${k}`);
    ok(v.B.every(c=>c.length<=3),`B 3CNF ${k}`);
    ok(v.gates.length<=8*k+20,`gate linear ${k}`);
    for(let a=0;a<tests;a++) {
      const shared={};for(let i=1;i<=n;i++)shared[i]=(a>>(i-1))&1;
      const I=sat(v.D,shared), extended=v.extension(shared);
      const b=sat(v.B,extended);
      ok(b===!I,`B projection ${k}/${a}`);
      if(I)trueI++;if(b)trueB++;
      if(k<=4){for(let p=0;p<8;p++){
        const full={...shared};for(let i=0;i<3;i++)full[v.P[i]]=(p>>i)&1;
        ok(sat(v.A,full)===I,`A projection ${k}/${a}/${p}`);
        ok(!(sat(v.A,full)&&sat(v.B,{...full,...extended})),`G unsat ${k}/${a}/${p}`);
      }}
      if(k<=3 && v.gates.length) {
        const corrupt={...extended};const g=v.gates[0];corrupt[g.out]^=1;
        ok(!sat(v.B.filter(c=>c.includes(g.out)||c.includes(-g.out)),corrupt),`corrupted gate ${k}/${a}`);
      }
    }
    ok(trueI===3*(1<<k),`I satisfying assignments ${k}`); ok(trueB===tests-trueI,`B assignments ${k}`);
    for(let x=0;x<(1<<k);x++)for(let xp=0;xp<(1<<k);xp++){
      const shared={};for(let i=0;i<k;i++)shared[v.X[i]]=(xp>>i)&1;
      for(let i=0;i<k;i++)shared[v.Y[i]]=(x>>i)&1;
      for(let j=0;j<3;j++)shared[v.Z[j]]=j===0?1:0;
      ok(sat(v.D,shared)===(x===xp),`distinct cofactor witness ${k}/${x}/${xp}`);
    }
    const restrict={};for(const id of v.X)restrict[id]=0;for(let i=0;i<k;i++)restrict[v.Y[i]]=i===0?1:0;
    for(let j=0;j<3;j++)restrict[v.Z[j]]=j===0?1:0;
    let active=0;const kept=[];
    for(const c of v.A){const smaller=c.filter(l=>!(Math.abs(l) in restrict)); if(c.some(l=>(Math.abs(l) in restrict)&&val(l,restrict)))continue; kept.push(smaller);active++}
    ok(active===8,`restriction F count ${k}`);
    ok(JSON.stringify(kept)===JSON.stringify(v.F),`restriction exactly F ${k}`);
    const ext=v.extension(restrict);ok(sat(v.B,ext),`restricted B trivially true ${k}`);
    const remainingB=v.B.filter(c=>!c.some(l=>val(l,ext)));
    ok(remainingB.length===0,`B disappeared on restriction ${k}`);
    samples.push({k,distinctCofactors:1<<k,Aclauses:v.A.length,Bclauses:v.B.length,gateCount:v.gates.length,sharedAssignments:tests,restrictedClauses:active,totalVariables:v.totalVars});
  }
  return {claim:"EQUALJ guardlift source-interface countercontrol, finite small-core tests",status:"COMPUTATIONAL",checks,failures,samples};
}
console.log(JSON.stringify(run(),null,2));
