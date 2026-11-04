// LSPV-3/384. Exact signed-source Hall-to-PHP extraction with charged RES.
// Run: node lspv3_384_hall_php_extraction.js
'use strict';
function run(){
 let tests=0,examples=[],counts={};
 const ok=(v)=>{tests++;if(!v)throw Error('invalid source/resolution witness')};
 for(let n=2;n<=3;n++){
  let sat=0,unsat=0,extracts=0;
  const x=(i,j)=>1+i*n+j,p=(i,j)=>1+n*n+i*n+j;
  for(let mask=0;mask<2**(n*n);mask++){
   let bits=Array.from({length:n*n},(_,i)=>(mask>>i)&1);
   const adj=(i,j)=>bits[i*n+j]===0;
   const hasMatch=(i,used)=>i===n||Array.from({length:n},(_,j)=>j).some(j=>adj(i,j)&&!(used&(1<<j))&&hasMatch(i+1,used|(1<<j)));
   const isSat=hasMatch(0,0);
   let S=null,H=null;
   for(let subset=1;subset<(1<<n);subset++){
    let ss=Array.from({length:n},(_,i)=>i).filter(i=>subset&(1<<i));
    let hh=Array.from({length:n},(_,j)=>j).filter(j=>ss.some(i=>adj(i,j)));
    if(hh.length<ss.length){S=ss;H=hh;break;}
   }
   ok(isSat===(S===null));
   if(isSat){sat++;continue}
   unsat++;ok(S.length>H.length);
   let source=[];
   for(let i=0;i<n;i++)source.push(Array.from({length:n},(_,j)=>x(i,j)));
   for(let j=0;j<n;j++)source.push(Array.from({length:n},(_,i)=>x(i,j)));
   for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let k=j+1;k<n;k++)source.push([-x(i,j),-x(i,k)]);
   for(let j=0;j<n;j++)for(let i=0;i<n;i++)for(let k=i+1;k<n;k++)source.push([-x(i,j),-x(k,j)]);
   for(let i=0;i<n;i++)for(let j=0;j<n;j++)source.push([p(i,j),-x(i,j)]);
   for(let i=0;i<n;i++)for(let j=0;j<n;j++)source.push([bits[i*n+j]?-p(i,j):p(i,j)]);
   const ids=new Map(source.map((z,k)=>[JSON.stringify(z.slice().sort((a,b)=>a-b)),k])),proof=[];
   const leaf=(z)=>{let k=ids.get(JSON.stringify(z.slice().sort((a,b)=>a-b)));ok(k!==undefined);return {src:k}};
   const get=(r)=>r.src!==undefined?source[r.src]:proof[r.node].c;
   const res=(a,b,t)=>{let A=get(a),B=get(b);
    ok(A.includes(t)&&B.includes(-t));
    let c=[...new Set([...A.filter(z=>z!==t),...B.filter(z=>z!==-t)])].sort((a,b)=>a-b);
    ok(c.every(z=>!c.includes(-z)));
    proof.push({a,b,t,c});return {node:proof.length-1}};
   let P=S.slice(0,H.length+1),rows=[];
   for(let i of P){let r=leaf(Array.from({length:n},(_,j)=>x(i,j)));
    for(let j=0;j<n;j++)if(!H.includes(j)){
     ok(bits[i*n+j]===1);
     let negx=res(leaf([-p(i,j)]),leaf([p(i,j),-x(i,j)]),-p(i,j));
     r=res(r,negx,x(i,j));
    }
    ok(JSON.stringify(get(r).slice().sort((a,b)=>a-b))===JSON.stringify(H.map(j=>x(i,j)).sort((a,b)=>a-b)));
    rows.push(r);
   }
   for(let u=0;u<P.length;u++)for(let v=u+1;v<P.length;v++)for(let j of H)
    leaf([-x(P[u],j),-x(P[v],j)]);
   ok(proof.length===2*(n-H.length)*(H.length+1));extracts++;
   if(examples.length<12||mask%101===0)examples.push({n,mask:bits.join(''),S,H,P,nodes:proof.length,
      sample_last_clause:get(rows[rows.length-1]),php_holes:H.length});
  }
  counts[n]={sat,unsat,extractions:extracts};
 }
 return {run_id:'LSPV3-384',status:'COMPUTATIONAL',counts,assertions:tests,examples,
   note:'Verifies paid strict RES extraction of canonical PHP axioms; Cook polynomial ER proof is a separate published theorem.'};
}
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run()));
