#!/usr/bin/env node
"use strict";
// Independent source-labelled DAG checker for LSPV3-342; no producer imports.
function ck(x,m){if(!x)throw Error(m)}
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const uni=(a,b)=>[...new Set([...a,...b])].sort((x,y)=>x-y);
function xors(a,b){let s=new Set(a);for(let x of b)s.has(x)?s.delete(x):s.add(x);return [...s].sort((x,y)=>x-y)}
function sat(c,x){return c.some(l=>Number((x>>BigInt(Math.abs(l)-1))&1n)===(l>0?1:0))}
function tabcl(c,v){let z=0;for(let a=0;a<8;a++)if(c.some(l=>{let j=v.indexOf(Math.abs(l)-1);ck(j>=0,"external variable");return ((a>>j)&1)===(l>0?1:0)}))z|=1<<a;return z}
function tabrow(mask,rhs,v){let z=0;for(let a=0;a<8;a++){let p=0;for(let e of mask){let j=v.indexOf(e);ck(j>=0,"external edge");p^=(a>>j)&1}if(p===rhs)z|=1<<a}return z}
function len(m){let k=Math.floor(Math.log2(m));return m*k+2*(m-2**k)}
function verify(P){
 let {h,n,edges,charge,clauses:F,nodes,root,deleted,evenClauses}=P;
 ck(Number.isInteger(h)&&h>=4&&h%2===0&&Number.isInteger(n)&&n===3*h/2,"graph header");
 ck(Array.isArray(edges)&&edges.length===n&&Array.isArray(charge)&&charge.length===h,"graph fields");
 ck(Array.isArray(F)&&F.length===4*h&&Array.isArray(nodes)&&nodes.length>=F.length&&Array.isArray(deleted)&&deleted.length===F.length,"certificate fields");
 ck(charge.every(x=>x===0||x===1)&&charge.reduce((x,y)=>x^y,0)===1,"charge");
 let inc=Array.from({length:h},()=>[]);
 edges.forEach((uv,i)=>{ck(Array.isArray(uv)&&uv.length===2,"edge shape");let [u,v]=uv;ck(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v>=0&&u<h&&v<h&&u!==v,"endpoint");inc[u].push(i);inc[v].push(i)});
 ck(inc.every(a=>a.length===3),"degree");
 let forms=F.map((c,i)=>{ck(Array.isArray(c)&&c.length===3&&new Set(c.map(Math.abs)).size===3,"source clause");let v=inc[Math.floor(i/4)];ck(eq(c.map(x=>Math.abs(x)-1),v),"clause edge map");return tabcl(c,v)});
 for(let v=0;v<h;v++){let T=255;for(let i=0;i<4;i++)T&=forms[4*v+i];ck(T===tabrow(inc[v],charge[v],inc[v]),"local source parity")}
 let support=[],statement=[],volume=0;
 nodes.forEach((r,j)=>{
   if(j<F.length){ck(r.kind==="source"&&r.source===j&&eq(r.clause,F[j]),"source record");support.push([j]);statement.push({kind:"factor",v:Math.floor(j/4),table:forms[j]});return}
   ck(Array.isArray(r.parents)&&r.parents.length===2,"binary rule");
   let [a,b]=r.parents;ck(Number.isInteger(a)&&Number.isInteger(b)&&a>=0&&b>=0&&a<j&&b<j,"parent DAG");
   volume+=support[a].length+support[b].length;support.push(uni(support[a],support[b]));
   let A=statement[a],B=statement[b];
   if(r.kind==="factor"||r.kind==="row"){
      ck(A.kind==="factor"&&B.kind==="factor"&&A.v===B.v&&r.v===A.v,"AND scope");
      let T=A.table&B.table;
      if(r.kind==="factor"){ck(r.table===T,"AND rule");statement.push({kind:"factor",v:r.v,table:T})}
      else{ck(eq(r.mask,inc[r.v])&&(r.rhs===0||r.rhs===1),"row syntax");ck(T===tabrow(r.mask,r.rhs,inc[r.v]),"row semantics");statement.push({kind:"row",mask:r.mask,rhs:r.rhs})}
   }else if(r.kind==="xor"){
      ck(A.kind==="row"&&B.kind==="row","XOR parent type");
      ck(eq(r.mask,xors(A.mask,B.mask))&&r.rhs===(A.rhs^B.rhs),"XOR rule");
      statement.push({kind:"row",mask:r.mask,rhs:r.rhs})
   }else throw Error("unsupported rule");
 });
 ck(root===nodes.length-1,"root");
 ck(statement[root].kind==="row"&&statement[root].mask.length===0&&statement[root].rhs===1,"final false");
 ck(support[root].length===F.length&&support[root].every((x,i)=>x===i),"source ancestry");
 ck(nodes.length===2*F.length-1,"m-1 node bound");
 ck(volume===len(F.length),"weighted source bound");
 deleted.forEach((w,j)=>{ck(typeof w==="string"&&/^[0-9a-f]+$/.test(w),"witness hex");let x=BigInt("0x"+w);ck(x>>BigInt(n)===0n,"witness range");ck(!sat(F[j],x),"witness must falsify removed");F.forEach((c,k)=>{if(k!==j)ck(sat(c,x),"deletion witness fails")})});
 ck(Array.isArray(evenClauses)&&evenClauses.length===F.length&&evenClauses.every(c=>sat(c,0n)),"even SAT");
 for(let v=0;v<h;v++){let T=255;for(let k=0;k<4;k++){let c=evenClauses[4*v+k];ck(Array.isArray(c)&&c.length===3&&eq(c.map(l=>Math.abs(l)-1),inc[v]),"even-edge pattern");T&=tabcl(c,inc[v])}ck(T===tabrow(inc[v],0,inc[v]),"even charge source parity")}
 let models=null;
 if(n<=12){let odd=0,even=0;for(let z=0;z<2**n;z++){let x=BigInt(z);if(F.every(c=>sat(c,x)))odd++;if(evenClauses.every(c=>sat(c,x)))even++}ck(odd===0&&even===2**(n-h+1),"exhaustive labels");models={odd,even}}
 return {h,m:F.length,q:nodes.length-F.length,source_reads:volume,L_m:len(F.length),models};
}
function run(R){
 ck(R.id==="LSPV3-PROVENANCE-KRAFT342"&&Array.isArray(R.cases),"archive");
 let out=R.cases.map(z=>{let v=verify(z.proof);ck(z.summary.m===v.m&&z.summary.q===v.q&&z.summary.source_reads===v.source_reads&&z.summary.L_m===v.L_m,"summary");return v});
 let P=R.cases[0].proof,bad=0;
 function negate(f){let q=JSON.parse(JSON.stringify(P));f(q);try{verify(q)}catch(e){bad++;return}throw Error("corruption accepted in test "+bad)}
 negate(q=>q.nodes[q.root].rhs=0);
 negate(q=>q.nodes[q.nodes.length-2].parents=[0,0]);
 negate(q=>q.clauses[0][0]*=-1);
 negate(q=>q.nodes[q.root].mask=[0]);
 negate(q=>q.deleted[0]="zz");
 negate(q=>q.nodes[0].source=999);
 negate(q=>q.h=5);
 negate(q=>q.nodes.push({kind:"oracle",parents:[0,1]}));
 negate(q=>q.evenClauses[0][0]*=-1);
 ck(bad===9,"negative test count");
 return {verified:out,negative_rejects:bad,exhaustive_original_pairs:out.filter(x=>x.models!==null).length};
}
if(require.main===module){let data=JSON.parse(require("fs").readFileSync(process.argv[2],"utf8"));process.stdout.write(JSON.stringify(run(data))+"\n")}
module.exports={verify,run};
