/* M22-DP-COVER106 peer auditor, Node >= 16, standard library only.
 * Run: node this_file.js [repo_root]. Optional D'oecker U fixture read from checkout.
 * Syntactic theorem is proved in companion LaTeX, tests are finite only.
 */
"use strict";
function ck(x,msg){if(!x)throw Error(msg);}
function build(r){
 ck(r>=5,"r>=5");
 const a=i=>1+(i%r+r)%r,b=i=>1+r+(i%r+r)%r,c=i=>1+2*r+(i%r+r)%r;
 const F=[]; for(let i=0;i<r;i++)
 F.push([a(i),b(i),c(i)],[a(i),b(i+1),c(i+2)],
        [-a(i),-b(i+2),-c(i+1)],[-a(i),-b(i+3),-c(i+3)]);
 return F;
}
function validate(F){
 const names=new Set(),deg=new Map(),clauses=new Set();
 for(const C of F){
  ck(C.length===3&&new Set(C.map(Math.abs)).size===3,"proper");
  ck(C.every(v=>v>0)||C.every(v=>v<0),"monotone");
  const key=[...C].sort((a,b)=>a-b).join(",");
  ck(!clauses.has(key),"unique");clauses.add(key);
  for(const v of C){const p=Math.abs(v);names.add(p);const key=p+":"+(v>0);deg.set(key,(deg.get(key)||0)+1);}
 }
 for(const v of names)ck(deg.get(v+":true")===2&&deg.get(v+":false")===2,"2,2 quota");
 return names.size;
}
function eliminate(F,x){
 const P=F.filter(C=>C.includes(x)),Q=F.filter(C=>C.includes(-x));
 const G=F.filter(C=>!C.includes(x)&&!C.includes(-x)),seen=new Set(G.map(C=>[...C].sort((a,b)=>a-b).join(",")));
 for(const A of P)for(const B of Q){
  const S=new Set([...A,...B].filter(v=>Math.abs(v)!==x));
  if([...S].some(v=>S.has(-v)))continue;
  const C=[...S].sort((a,b)=>a-b),key=C.join(",");
  if(!seen.has(key)){seen.add(key);G.push(C);}
 }
 return G;
}
function sat(F,z){return F.every(C=>C.some(x=>(x>0)===Boolean(z[Math.abs(x)])));}
function project(F,d){
 let G=F;for(let x=1;x<=d;x++)G=eliminate(G,x);
 let checks=0,n=Math.max(...F.flat());
 for(let mask=0;mask<2**(n-d);mask++){
  const z=Array(n+1).fill(false);
  for(let i=d+1;i<=n;i++)z[i]=Boolean((mask>>(i-d-1))&1);
  let expected=false;
  for(let pm=0;pm<(1<<d);pm++){
   for(let j=1;j<=d;j++)z[j]=Boolean((pm>>(j-1))&1);
   if(sat(F,z)){expected=true;break;}
  }
  ck(sat(G,z)===expected,"exact projection");
  checks++;
 }
 return {checks,m:G.length,literals:G.reduce((a,C)=>a+C.length,0)};
}
function greedy(F,count){
 let chosen=new Set(),left=F.slice(),names=new Set(F.flat().map(Math.abs));
 for(let step=0;step<count;step++){
  let best=null,score=-1;
  for(let v of [...names].sort((a,b)=>a-b)){
   if(chosen.has(v))continue;
   let val=left.filter(C=>C.some(t=>Math.abs(t)===v)).length;
   if(val>score){best=v;score=val;}
  }
  chosen.add(best);
  left=left.filter(C=>!C.some(t=>chosen.has(Math.abs(t))));
 }
 return left.length;
}
function audit(uText){
 const controls=[];let exactProjectionChecks=0;
 for(const r of [5,7,66]){
  const F=build(r),n=validate(F),q=F.filter(C=>C[0]>0).length;
  ck(n===3*r&&F.length===4*r&&q===2*r,"dimensions");
  const pos=new Set(F.filter(C=>C[0]>0).map(C=>C.map(Math.abs).join(","))),
    neg=new Set(F.filter(C=>C[0]<0).map(C=>C.map(Math.abs).join(",")));
  ck([...pos].every(x=>!neg.has(x)),"complement pair");
  const witness=Array(3*r+1).fill(false);for(let j=1;j<=r;j++)witness[j]=true;
  ck(sat(F,witness),"SAT witness");
  const stages=[];for(const d of [0,1,2,r]){
   let G=F;for(let i=1;i<=d;i++)G=eliminate(G,i);
   const untouched=F.filter(C=>!C.some(v=>Math.abs(v)<=d)).length;
   ck(untouched===4*(r-d),"original coverage");
   ck(G.length===4*r,"clauses constant");
   const literals=G.reduce((a,C)=>a+C.length,0);
   ck(literals===12*r+4*d,"literal count");
   stages.push({d,untouched,clauses:G.length,literals});
  }
  if(r===5){for(const d of [1,2]){let p=project(F,d);exactProjectionChecks+=p.checks;}}
  controls.push({r,k:n,m:F.length,q:2*r,status:"Cstar SAT",stages,greedy_k_over_3_uncovered:greedy(F,r)});
 }
 if(uText){
  const U=JSON.parse(uText.slice(uText.indexOf("[["))),n=validate(U);
  ck(n===198&&U.length===264,"U source");
  controls.push({name:"Döcker U198",k:n,m:U.length,
    status:"Cstar UNSAT label imported from Döcker; no exhaustive proof in this auditor",
    uncovered_greedy:{33:greedy(U,33),50:greedy(U,50),66:greedy(U,66),80:greedy(U,80),99:greedy(U,99)}});
 }
 return {run:"M22-DP-COVER106",status:"COMPUTATIONAL checks plus restricted symbolic proof in report",
  exactProjectionChecks,controls,limitations:"No FLMV physical steps, bit flips, peak live memory or cumulative bit-time measured."};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const root=process.argv[2]||process.cwd();
 const p=path.join(root,"research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt");
 const s=fs.existsSync(p)?fs.readFileSync(p,"utf8"):null;
 process.stdout.write(JSON.stringify(audit(s),null,2)+"\n");
}
