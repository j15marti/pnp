#!/usr/bin/env node
/* LSPV-3/445: executable strict-3-CNF private-chain consequence reproducer.
 * Standalone no-package executable, tests actual signed bit-PHP collision clauses.
 * Verifies one native RES-only proof per case, projection and deletion witnesses.
 * NOT an authoritative checker for the entire historical R_mix341 grammar.
 */
'use strict';
const crypto=require('crypto');
let checks=0, rejected=0;
function chk(b,msg){checks++;if(!b)throw Error(msg)}
function sat(C,v){return C.some(l=>v[Math.abs(l)-1]===(l>0?1:0))}
function sort(C){return [...new Set(C)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function res(A,B,p){
  chk(A.includes(p)&&B.includes(-p),'bad oriented RES pivot');
  const c=sort([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
  chk(c.every(x=>!c.includes(-x)),'tautological resolvent');
  return c;
}
function run(ell){
  const k=2*ell,h=Array.from({length:ell},(_,i)=>(Math.floor(ell/2)>>i)&1);
  const L=Array.from({length:k},(_,i)=>(h[i%ell]?-1:1)*(i+1));
  const y=j=>k+j;
  const g=[sort([L[0],L[1],y(1)])];
  for(let j=2;j<=k-3;j++)g.push(sort([-y(j-1),L[j],y(j)]));
  g.push(sort([-y(k-3),L[k-2],L[k-1]]));
  chk(g.length===k-2&&g.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'not strict3');
  const dimacs='p cnf '+(2*k-3)+' '+g.length+'\n'+g.map(c=>c.join(' ')+' 0\n').join('');
  const digest=crypto.createHash('sha256').update(dimacs).digest('hex');
  let C=g[0],proof=[];
  for(let i=1;i<g.length;i++){
    C=res(C,g[i],y(i));
    proof.push({pivot:y(i),out:C});
  }
  chk(eq(C,sort(L))&&proof.length===k-3,'reconstruction failed');
  const ff=Array.from({length:k},(_,i)=>L[i]<0?1:0);
  for(let missing=1;missing<=g.length;missing++){
    const ys=Array.from({length:k-3},(_,i)=>i+1<missing?1:0);
    const vals=ff.concat(ys);
    chk(!sat(L,vals)&&!sat(g[missing-1],vals),'wrong deletion');
    for(let j=0;j<g.length;j++)if(j!==missing-1)chk(sat(g[j],vals),'deleted source needed');
  }
  let yes=0,no=0;
  for(let mask=0;mask<(1<<k);mask++){
    const v=Array.from({length:k},(_,i)=>(mask>>i)&1);
    const truth=sat(L,v);let all=false;
    const ys=[];
    for(let j=1;j<=k-3;j++){
      all=!L.slice(0,j+1).some(l=>sat([l],v));
      ys.push(Number(all));
    }
    chk(g.every(c=>sat(c,v.concat(ys)))===truth,'projection forward/backward');
    if(truth)yes++;else{
      no++;
      for(let j=0;j<(1<<(k-3));j++){
        const a=v.concat(Array.from({length:k-3},(_,t)=>(j>>t)&1));
        chk(!g.every(c=>sat(c,a)),'false original has extension');
      }
    }
  }
  chk(yes===(1<<k)-1&&no===1,'assignment controls');
  return {ell,k,original_clause:L,source_clauses:g.length,paid_RES:proof.length,original_models:yes,non_models:no,
          source_sha256:digest,dimacs_bytes:Buffer.byteLength(dimacs)};
}
const cases=[2,3,4,5].map(run);
function reject(fn){let ok=false;try{fn()}catch(e){ok=true}chk(ok,'corruption accepted');rejected++}
reject(()=>res([1,2],[-1,3],-1));
reject(()=>res([1,-2],[-1,2],1));
reject(()=>{const z=cases[0];chk(z.paid_RES===2,'tampered cost')});
reject(()=>{const z=cases[1];chk(z.source_clauses===3,'missing original')});
chk(rejected===4,'hostile control tally');
console.log(JSON.stringify({status:'finite independent strict RES replay only',checks,rejected,cases},null,2));
