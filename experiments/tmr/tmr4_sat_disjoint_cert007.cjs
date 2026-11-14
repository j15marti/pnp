'use strict';
// TMR4/007 independent finite proper 3-CNF controls. NOT native TM.
const auditSAT=function auditSAT(){
 "use strict";
 const ok=(v,msg)=>{if(!v)throw Error(msg)};
 const N=6,M=20,w=3,clauses=[];
 for(let i=1;i<=N;i++)for(let j=i+1;j<=N;j++)for(let k=j+1;k<=N;k++)clauses.push([i,j,k]);
 ok(clauses.length===20,"not 20 unique clauses");
 const y1=clauses.map(c=>c.slice()),y2=clauses.map(c=>c.slice());
 for(let t=0;t<8;t++){
   y1[t]=[1,2,3].map((z,j)=>t&(1<<j)?-z:z);
   y2[12+t]=[4,5,6].map((z,j)=>t&(1<<j)?-z:z);
 }
 const encode=C=>"1".repeat(N)+"0"+"1".repeat(C.length)+"0"+C.flat().map(l=>(l<0?"1":"0")+(Math.abs(l)-1).toString(2).padStart(w,"0")).join("");
 function parse(s){
   const pre="1".repeat(N)+"0"+"1".repeat(M)+"0";
   if(s.length!==268||!s.startsWith(pre))return null;
   const out=[],seen=new Set();
   for(let j=0;j<M;j++){
     const clause=[],used=new Set();
     for(let t=0;t<3;t++){
       const o=pre.length+4*(3*j+t),sgn=s[o],digits=s.slice(o+1,o+4);
       if(!/^[01]$/.test(sgn)||!/^[01]{3}$/.test(digits))return null;
       const k=parseInt(digits,2)+1;
       if(k<1||k>N||used.has(k))return null;
       used.add(k);seen.add(k);clause.push(sgn==="1"?-k:k);
     }
     out.push(clause);
   }
   if(seen.size!==N)return null;
   return out;
 }
 const sat=C=>{for(let a=0;a<(1<<N);a++)if(C.every(cl=>cl.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))return true;return false};
 const x=encode(clauses),p=encode(y1),q=encode(y2);
 ok(x.length===268&&p.length===268&&q.length===268,"source lengths");
 ok(parse(x)!==null&&parse(p)!==null&&parse(q)!==null,"source syntax");
 ok(sat(parse(x))&&!sat(parse(p))&&!sat(parse(q)),"SAT labels");
 let d1=0n,d2=0n,count1=0,count2=0;
 const delta1=[],delta2=[];
 for(let i=0;i<x.length;i++){
   if(x[i]!==p[i]){count1++;delta1.push(i);d1|=1n<<BigInt(i)}
   if(x[i]!==q[i]){count2++;delta2.push(i);d2|=1n<<BigInt(i)}
 }
 ok((d1&d2)===0n&&count1>0&&count2>0,"not disjoint");
 let validSign=0,validId=0,invalidId=0;
 for(let j=0;j<60;j++)for(let k=0;k<4;k++){
   const pos=28+4*j+k;
   const mutant=x.slice(0,pos)+(x[pos]==="0"?"1":"0")+x.slice(pos+1);
   const c=parse(mutant);
   if(c===null){ok(k!==0,"a sign flip may not invalidate proper clause");invalidId++;continue}
   ok(sat(c),"a one-bit literal edit made the all-positive SAT formula UNSAT");
   if(k===0)validSign++;else validId++;
 }
 ok(validSign===60,"sign control count");
 // For two disjoint verified opposite difference sets, minimum hitting set size is 2, though no literal bit is singly opposite.
 const tau=2,phi1=tau,phi2=1;
 return {type:"TMR4-SAT-DISJOINT-WITNESS-007",status:"COMPUTATIONAL",date_PST:"2026-11-13 18:40 PST",
   description:"Independent native-JavaScript exhaustive assignment evaluation for ordinary proper 3-CNF strings, 6 variables 20 clauses, two disjoint opposite-label source difference sets; not TM execution",
   source:{encodedLength:x.length,variables:N,clauses:M,threeDistinctPerClause:true,allSixVariablesOccur:true},
   results:{xSAT:true,y1UNSAT:true,y2UNSAT:true,firstDifferenceBits:count1,secondDifferenceBits:count2,overlap:0,firstMinPosition:delta1[0],secondMinPosition:delta2[0],validSingleSignSAT:validSign,validSingleIdentifierSAT:validId,invalidSingleIdentifier:invalidId,certifiedSingletonOppositesInLiteralFields:0,minHittingSet:tau,phi_q1:phi1,phi_q2:phi2},
   sourceFingerprints:{firstClauseX:clauses[0].join(","),firstClauseY1:y1[0].join(","),lastClauseY2:y2[M-1].join(",")}};
};
console.log(JSON.stringify(auditSAT(),null,2));
