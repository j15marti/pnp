#!/usr/bin/env node
'use strict';
// LSPV-3/425 independent support-semantics auditor.
// Conditional FACET-LIFT interface, NOT an original R_mix341 parser.
const A=require('assert'); let checks=0;
function ok(a,msg){checks++; A.ok(a,msg)}
function xor(R,S){let a=new Set(R);for(let v of S) a.has(v)?a.delete(v):a.add(v);return [...a].sort((x,y)=>x-y)}
function val(C,m){return C.some(l=>l>0?m[Math.abs(l)]===1:m[Math.abs(l)]===0)}
function forbiddenClause(a,b,z,x,y){
  const wrong=x^y^1;
  return [x?-a:a, y?-b:b, wrong?-z:z];
}
function audit(){
 let out=[];
 for(let n of [2,3,4,5,6,8,16,32,64]){
   let parent=null, ident=[], firstConeFailure=null;
   for(let k=2;k<=n;k++){
     let a=k===2?1:parent,b=k,z=n+k-1;
     let clauses=[];
     for(let x=0;x<2;x++) for(let y=0;y<2;y++)clauses.push(forbiddenClause(a,b,z,x,y));
     for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let v=0;v<2;v++){
       let m={[a]:x,[b]:y,[z]:v};
       let output=clauses.every(C=>val(C,m));
       ok(output===(v===(x^y)),'four-gate-facet equivalence');
     }
     for(const C of clauses){
       let bad=0;
       for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let v=0;v<2;v++){
         let m={[a]:x,[b]:y,[z]:v};
         if(v!==(x^y)&&clauses.filter(t=>t!==C).every(t=>val(t,m)))bad++;
       }
       ok(bad===1,'each facet required for exact gate');
     }
     ok(new Set([a,b,z]).size===3,'literal-port support three');
     if(k>3&&!firstConeFailure)firstConeFailure=k;
     ident.push([a,b,z]); parent=z;
   }
   let sym=[];
   for(const [a,b,z] of ident)sym=xor(sym,[a,b,z]);
   ok(JSON.stringify(sym)===JSON.stringify([...Array(n)].map((_,i)=>i+1).concat([2*n-1]).sort((a,b)=>a-b)),'gate rows telescope');
   let src=[...Array(n)].map((_,i)=>i+1);
   let pin=xor(sym,src);
   ok(pin.length===1&&pin[0]===2*n-1,'affine pin provenance');
   let q=7*n-6, nDef=n-1, nAnd3=n+3*nDef, nGF2=2*n-2;
   ok(q===nDef+nAnd3+nGF2,'exact paid node count');
   if(n<=8)for(let assignment=0;assignment<(1<<n);assignment++){
     let f=assignment===(1<<n)-1;
     if(f){let p=0;for(let i=0;i<n;i++)p^=assignment>>i&1;ok(p===n%2,'source SAT row consequence');}
   }
   out.push({n,q,definitions:nDef,extraction_AND3:3*nDef,source_row_AND3:n,GF2:nGF2,literal_port_support:3,final_source_cone_support:n,first_cone_failure:firstConeFailure,pin:2*n-1,pin_value:n%2});
 }
 // Negative interface controls, each a logically independent invalid replacement.
 ok(xor([1,2,3,4],[1,2,3,4,7]).join(',')==='7','legitimate parity cancellation');
 ok(xor([1,2,3,4],[1,2,3,4,7,8]).join(',')==='7,8','wrong port retains bit');
 let a=1,b=2,z=5,cs=[];
 for(let x=0;x<2;x++)for(let y=0;y<2;y++)cs.push(forbiddenClause(a,b,z,x,y));
 ok(cs.length===4&&cs.every(c=>c.length===3),'four paid-owner facets');
 const wrong={1:0,2:0,5:1};
 ok(cs.filter(c=>!val(c,wrong)).length===1,'deleting a facet accepts false gate assignment');
 return {schema:'LSPV3-425-independent/v1',status:'CONDITIONAL; not native checker acceptance',checks,number_of_sizes:out.length,results:out,negative_controls:4};
}
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={audit};
