"use strict";
// LSPV-2/485. Independent JS strict-3CNF equality-cofactor control, no packages.
function makeClauses(k) {
  const clauses=[];
  for(let i=0;i<k;i++) {
    const x=4*i+1,y=x+1,u=x+2,v=x+3;
    clauses.push([-x,y,u],[-x,y,-u],[x,-y,v],[x,-y,-v]);
  }
  return clauses;
}
function bits(k,x,y,u=0,v=0) {
  const a=new Uint8Array(4*k);
  for(let i=0;i<k;i++) {
    a[4*i]=(x>>i)&1; a[4*i+1]=(y>>i)&1;
    a[4*i+2]=(u>>i)&1; a[4*i+3]=(v>>i)&1;
  }
  return a;
}
function isSat(clauses,a) {
  for(const c of clauses) {
    let ok=false;
    for(const lit of c) {
      const b=a[Math.abs(lit)-1];
      if((lit>0 && b===1)||(lit<0 && b===0)) {ok=true;break;}
    }
    if(!ok)return false;
  }
  return true;
}
function run485() {
  let assertions=0;
  const rows=[];
  function check(b,m) { assertions++; if(!b)throw Error(m); }
  for(let k=1;k<=6;k++) {
    const F=makeClauses(k);
    check(F.length===4*k,'clauses count');
    check(F.every(c=>c.length===3 && new Set(c.map(Math.abs)).size===3),'proper source');
    for(let x=0;x<(1<<k);x++) {
      for(let y=0;y<(1<<k);y++)
        check(isSat(F,bits(k,x,y))===(x===y),'cofactor truth');
      check(isSat(F,bits(k,x,x)),'witness');
    }
    for(let a=0;a<(1<<k);a++)
      for(let b=0;b<(1<<k);b++)
        if(a!==b)check(isSat(F,bits(k,a,a)) && !isSat(F,bits(k,b,a)),'distinct residuals');
    let counted=0;
    if(k<=4)for(let x=0;x<(1<<k);x++) {
      let n=0;
      for(let y=0;y<(1<<k);y++)
        for(let u=0;u<(1<<k);u++)
          for(let v=0;v<(1<<k);v++)
            if(isSat(F,bits(k,x,y,u,v)))n++;
      check(n===(1<<(2*k)),'model count');counted++;
    }
    rows.push({k,vars:4*k,clauses:4*k,cofactor_count:1<<k,
      projection_labels:1,models_per_cofactor:1<<(2*k),counted});
  }
  return {status:'PASS',assertions,rows,method:'independent evaluator, exact all x/y through k=6, complete auxiliary counts k<=4'};
}
const summary=run485();
if(typeof console!=='undefined')console.log(JSON.stringify(summary,null,2));
