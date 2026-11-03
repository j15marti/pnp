'use strict';
// Independently authored deterministic brute-force verifier for LSPV1-358.
// Regenerates signed clauses; does not import the producer.
function verify(){
 let asserts=0,points=[];
 function yes(b,msg){asserts++;if(!b)throw Error(msg);}
 function holds(cl,x){for(const a of cl)if(x[Math.abs(a)]===(a>0?1:0))return true;return false;}
 function cs(n,g,satCase){
   const b=[[1]];
   for(let t=1;t<n;t++)b.push([t+1,-t]);
   b.push([satCase?n:-n]);
   const all=b.map(t=>t.slice()),defs=[];
   for(let j=0;j<g;j++){
     const out=n+j+1,first=j?n+j:1,second=j?(j%n)+1:2;
     defs.push([out,first,second]);
     all.push([first,-out],[second,-out],[-first,-second,out]);
   }
   return {b,all,defs};
 }
 for(let n of [2,3,4,6,8])for(let g of [1,2,4]){
   const u=cs(n,g,false),s=cs(n,g,true);
   let solutions=[0,0];
   for(let k=0;k<(1<<(n+g));k++){
     const v=Array(n+g+1).fill(0);
     for(let j=1;j<=n+g;j++)v[j]=(k>>(j-1))&1;
     if(u.all.every(cl=>holds(cl,v)))solutions[0]++;
     if(s.all.every(cl=>holds(cl,v)))solutions[1]++;
     let gateValid=u.defs.every(([q,a,b])=>v[q]===(v[a]&v[b]));
     let gateClauses=u.all.slice(n+1).every(cl=>holds(cl,v));
     yes(gateValid===gateClauses,'complete gate equivalence');
   }
   yes(solutions[0]===0,'UNSAT label');
   yes(solutions[1]===1,'SAT label');
   // Direct signed RES proof of the original core, ignoring all fresh sources.
   let active=u.all[0];
   for(let i=1;i<=n;i++){
     yes(active.includes(i)&&u.all[i].includes(-i),'signed pivot');
     let out=[...new Set([...active.filter(z=>z!==i),...u.all[i].filter(z=>z!==-i)])];
     yes(!out.some(z=>out.includes(-z)),'no tautology');
     active=out;
   }
   yes(active.length===0,'root is empty');
   // Each original source can be deleted without destroying satisfiability.
   for(let j=0;j<=n;j++){
     const v=Array(n+g+1).fill(0);
     if(j===0){/* all zero */}
     else if(j===n){for(let a=1;a<=n;a++)v[a]=1;}
     else for(let a=1;a<=j;a++)v[a]=1;
     for(const [q,a,b] of u.defs)v[q]=v[a]&v[b];
     yes(!holds(u.all[j],v),'designated clause false');
     yes(u.all.every((cl,i)=>i===j||holds(cl,v)),'other clauses true');
     for(let k=0;k<u.b[j].length;k++){
       let changed=u.b[j].slice();changed[k]=-changed[k];
       yes(holds(changed,v),'literal flip repair');
     }
   }
   points.push({n,g,m:u.all.length,variables:n+g,mixedExactMinimum:n,pairedModels:solutions});
 }
 // Authenticated gate source cannot be replaced by a free answer axiom.
 const v=[0,1,1,0];yes(![[1],[-1,2],[-2]].every(x=>holds(x,v)),'hostile UNSAT source');
 const wrong=[[-3,1],[-3,2],[-3,-1,-2]];yes(wrong.every(x=>holds(x,v)),
 'malformed sign change can alter extension relation (not a valid gate)');
 const genuine=[[-3,1],[-3,2],[3,-1,-2]];yes(!genuine.every(x=>holds(x,v)),
 'genuine gate forces q=1');
 // Authenticated padding-consuming RES proof, 5 nodes with 1 paid gate.
 const input=[[1],[-1,2],[-2],[-3,1],[-3,2],[3,-1,-2]];
 const rules=[[0,1,1],[5,6,-2],[0,7,1],[8,4,3],[9,2,2]];
 let lines=input.slice();
 for(const [a,b,p] of rules){
   yes(lines[a].includes(p)&&lines[b].includes(-p),'strict pivot source');
   const out=[...new Set([...lines[a].filter(z=>z!==p),...lines[b].filter(z=>z!==-p)])].sort((x,y)=>x-y);
   yes(!out.some(z=>out.includes(-z)),'no tautological output');
   lines.push(out);
 }
 yes(lines.at(-1).length===0,'DEF-consuming proof ends in empty');
 return {assertions:asserts,points,defConsumingRESNodes:rules.length,
    defConsumingPaidReplayNodes:rules.length+1,
    corruptedGateDetected:true,typeFirewall:'AND3 original-support mismatch remains OPEN for full mixed source replay'};
}
if(typeof module!=='undefined'&&module.exports)module.exports={verify};
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(verify(),null,2));
