/* LSPV-3 reproducible deterministic Node.js audit. Run: node <this_file> */
const audit144 = function audit144(){
"use strict";
let assertions=0;
function eq(x,y){return JSON.stringify(x)===JSON.stringify(y)}
function check(x,msg){assertions++;if(!x)throw Error(`${msg} (#${assertions})`)}
function canon(x){return [...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function same(x,y){return eq(canon(x),canon(y))}
function build(r,t){
 const b=r+t;check(r>=1&&t>=2&&b>=3,"params");let v=b,clauses=[],modules=[],pins=[],exceptions=[];
 function module(name,rows,pvt){let ids=[];for(let row of rows){ids.push(clauses.length);clauses.push({id:clauses.length,lits:row,module:name})}const rec={name,ids,private:pvt};modules.push(rec);return rec}
 for(let i=1;i<=r;i++){
  let z=++v,w=++v;let rec=module("PIN"+i,[[-i,z,w],[-i,z,-w],[-i,-z,w],[-i,-z,-w]],[z,w]);pins.push({...rec,y:i,z,w});
 }
 for(let a=0;a<2**t;a++){
  let lits=Array.from({length:r},(_,i)=>i+1);
  for(let j=0;j<t;j++)lits.push((a>>(t-1-j))&1?-(r+j+1):r+j+1);
  let zs=Array.from({length:b-3},()=>++v),rows=[];
  if(b===3)rows.push(lits);
  else{
   rows.push([lits[0],lits[1],zs[0]]);
   for(let k=2;k<=b-3;k++)rows.push([-zs[k-2],lits[k],zs[k-1]]);
   rows.push([-zs[b-4],lits[b-2],lits[b-1]]);
  }
  let rec=module("EX"+a,rows,zs);exceptions.push({...rec,a,lits,zs});
 }
 return {r,t,b,v,clauses,modules,pins,exceptions};
}
function structural(F){
 const V=F.v,C=F.clauses.length,adj=Array.from({length:V+C},()=>[]),seenClauses=new Set(),seenNames=new Set();
 for(let c=0;c<C;c++){
  let row=F.clauses[c].lits;check(row.length===3,"ternary");check(new Set(row.map(Math.abs)).size===3,"proper distinct");
  let key=canon(row).join(",");check(!seenClauses.has(key),"unique clauses");seenClauses.add(key);
  for(let lit of row){let vi=Math.abs(lit)-1;seenNames.add(vi);adj[vi].push(V+c);adj[V+c].push(vi);}
 }
 check(seenNames.size===V,"every variable used");
 let reached=new Set([0]),todo=[0];
 while(todo.length){let u=todo.pop();for(let z of adj[u])if(!reached.has(z)){reached.add(z);todo.push(z)}}
 check(reached.size===V+C,"connected incidence graph");
 for(let m of F.modules)for(let x of m.private){
  check(x>F.b,"private index");
  for(let i=0;i<C;i++)if(F.clauses[i].lits.some(z=>Math.abs(z)===x))check(m.ids.includes(i),"private provenance");
 }
}
function satisfied(row,A){return row.some(z=>A[Math.abs(z)]===(z>0))}
function proj(F,mod,word){
 const A={};for(let i=1;i<=F.b;i++)A[i]=Boolean((word>>(F.b-i))&1);
 for(let mask=0;mask<2**mod.private.length;mask++){
  for(let j=0;j<mod.private.length;j++)A[mod.private[j]]=Boolean((mask>>j)&1);
  if(mod.ids.every(k=>satisfied(F.clauses[k].lits,A)))return true;
 }
 return false;
}
function model(F,deleted=-1){
 for(let w=0;w<2**F.b;w++)if(F.modules.every((mod,i)=>i===deleted||proj(F,mod,w)))return w;
 return null;
}
function refutation(F){
 let lines=F.clauses.map(c=>c.lits.slice()),steps=[];
 function res(p,q,pivot){
  check(p<lines.length&&q<lines.length,"parents chronological");
  let x=lines[p],y=lines[q],sign=x.includes(pivot)&&y.includes(-pivot)?pivot:x.includes(-pivot)&&y.includes(pivot)?-pivot:0;
  check(sign!==0,"source valid opposite pivot");
  let out=canon([...x.filter(z=>z!==sign),...y.filter(z=>z!==-sign)]);
  for(let z of out)check(!out.includes(-z),"non-tautological resolvent");
  let id=lines.length;lines.push(out);steps.push({left:p,right:q,pivot,derived:out});return id;
 }
 const units=[];
 for(let p of F.pins){
  let x=res(p.ids[0],p.ids[1],p.w),y=res(p.ids[2],p.ids[3],p.w),z=res(x,y,p.z);
  check(same(lines[z],[-p.y]),"unit source certificate");units.push(z);
 }
 let current=[];
 for(let ex of F.exceptions){
  let z=ex.ids[0];
  for(let j=1;j<ex.ids.length;j++)z=res(z,ex.ids[j],ex.zs[j-1]);
  check(same(lines[z],ex.lits),"exact original long clause from source");
  for(let j=0;j<units.length;j++)z=res(z,units[j],j+1);
  check(same(lines[z],ex.lits.slice(F.r)),"same-boundary projection");
  current.push(z);
 }
 for(let s=F.t;s>=1;s--){
  let next=[];for(let i=0;i<current.length;i+=2){
   let z=res(current[i],current[i+1],F.r+s);
   check(lines[z].length===s-1,"resolution width decreases");next.push(z);
  }
  current=next;
 }
 check(current.length===1&&lines[current[0]].length===0,"empty refutation");
 const independentlyChecked=F.clauses.map(c=>c.lits.slice());
 for(let step of steps){
  let x=independentlyChecked[step.left],y=independentlyChecked[step.right];
  check(x!==undefined&&y!==undefined,"references existing source/derived line");
  let sign=x.includes(step.pivot)&&y.includes(-step.pivot)?step.pivot:x.includes(-step.pivot)&&y.includes(step.pivot)?-step.pivot:0;
  check(sign!==0,"audit opposition");
  let out=canon([...x.filter(z=>z!==sign),...y.filter(z=>z!==-sign)]);
  check(same(out,step.derived),"audit exact resolvent");
  independentlyChecked.push(out);
 }
 check(independentlyChecked.at(-1).length===0,"source-authenticated empty clause");
 const exact=3*F.r+2**F.t*(F.b+F.r-2)-1;
 check(steps.length===exact,"closed resolution count");
 return {resolutionSteps:steps.length,authenticatedSourceClauses:F.clauses.length,proofLines:independentlyChecked.length};
}
function clonePin(F){
 const o=JSON.parse(JSON.stringify(F)),z=++o.v,w=++o.v,ids=[];
 for(let lits of [[-1,z,w],[-1,z,-w],[-1,-z,w],[-1,-z,-w]]){
  let id=o.clauses.length;ids.push(id);o.clauses.push({id,lits,module:"CHILD"+z});
 }
 o.modules.push({name:"CHILD"+z,private:[z,w],ids});
 return o;
}
function encodeLength(F){
 const width=Math.ceil(Math.log2(F.v+1));
 return `r=${F.r};t=${F.t};n=${F.v};m=${F.clauses.length};w=${width}|`.length+F.clauses.length*3*(width+1);
}
function strict22W1(){
 const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
 let counts={};
 for(let a=0;a<=1;a++)for(let b=0;b<=1;b++){
  const C=W.map(x=>x.slice());if(a===0)for(let [i,j] of [[6,0],[11,0]])C[i][j]*=-1;
  if(b===0)for(let [i,j] of [[17,2],[9,2]])C[i][j]*=-1;
  let hist=Array.from({length:16},()=>[0,0]);
  for(let row of C){check(new Set(row.map(Math.abs)).size===3,"W1 proper");for(let lit of row)hist[Math.abs(lit)][lit>0?0:1]++;}
  for(let i=1;i<=15;i++)check(hist[i][0]===2&&hist[i][1]===2,"W1 exact22 occurrence");
  let sat=0;
  for(let mask=0;mask<2**15;mask++){
   const A={};for(let i=1;i<=15;i++)A[i]=Boolean((mask>>(i-1))&1);
   if(C.every(row=>satisfied(row,A)))sat++;
  }
  check(sat===(a===1&&b===1?0:a===0&&b===0?772:272),"W1 true model count");
  counts[`${a}${b}`]=sat;
 }
 return counts;
}
let examples=[];
for(let [r,t] of [[1,2],[1,3],[2,2],[1,4],[2,3],[2,4]]){
 let F=build(r,t);structural(F);
 check(F.clauses.length===4*r+2**t*(r+t-2),"clause closed count");
 check(F.v===r+t+2*r+2**t*(r+t-3),"variable closed count");
 let occ=Array.from({length:F.v+1},()=>[0,0]);
 for(let c of F.clauses)for(let z of c.lits)occ[Math.abs(z)][z>0?0:1]++;
 let exact22=occ.slice(1).every(([p,n])=>p===2&&n===2);
 check(!exact22,"strict exact22 is NOT claimed");
 for(let w=0;w<2**F.b;w++)for(let j=0;j<F.modules.length;j++){
  let expected=j<r?((w>>(F.b-1-j))&1)===0:w!==(j-r);
  check(proj(F,F.modules[j],w)===expected,"exhaustive source local existential projection");
 }
 check(model(F)===null,"full conjunction UNSAT");
 for(let j=0;j<F.modules.length;j++)check(model(F,j)!==null,"each individual whole-module deletion SAT");
 if(F.modules.length<=8){
  for(let subset=0;subset<2**F.modules.length;subset++){
   let sat=false;
   for(let w=0;w<2**F.b;w++){
    if(F.modules.every((mod,j)=>!(subset&(1<<j))||proj(F,mod,w))){sat=true;break}
   }
   check(sat===(subset!==2**F.modules.length-1),"all module subsets classification");
  }
 }
 let proof=refutation(F),F1=clonePin(F),F2=clonePin(F1);
 structural(F1);structural(F2);
 check(model(F1)===null&&model(F2)===null,"both UNSAT descendants");
 let satParent=JSON.parse(JSON.stringify(F));satParent.modules.splice(r,1);
 check(model(satParent)!==null,"SAT deletion parent");
 check(model(clonePin(satParent))!==null&&model(clonePin(clonePin(satParent)))!==null,"both SAT descendants");
 let lengths=[encodeLength(F),encodeLength(F1),encodeLength(F2)];
 check(lengths[0]<lengths[1]&&lengths[1]<lengths[2],"physical ordinary-3CNF expansion");
 examples.push({r,t,b:F.b,variables:F.v,clauses:F.clauses.length,minimumUnsatModuleSupport:r+2**t,resolutionSteps:proof.resolutionSteps,actualEncodedBits:lengths,incidenceConnected:true,strictSigned22:false});
}
let W1=strict22W1();
const hostiles=[[[1,2],[-1,3]],[[1,2,3],[-1,2,3],[1,-2,3],[1,2,-3]],[[1,2,3],[-1,-2,3]]];
for(let H of hostiles){let F=build(1,2);check(H.length!==F.clauses.length||H.some((c,i)=>!same(c,F.clauses[i].lits)),"malformed/Horn/Tseitin-type source rejected by canonical parser");}
return {study:"SOURCE-RANK-RESOLUTION144",date:"2026-10-27T04:50:00-07:00",auditKind:"exhaustive small existential local projections and full subset masks; independent literal-wise resolution replay; fixed historical W1 strict22 controls",assertions,failures:0,examples,W1modelCounts:W1,status:{theorem:"PROVED/EXACT restricted, independent review pending",experiments:"COMPUTATIONAL",allOrdinaryUNSAT:"OPEN",ARC_EDGE_90:"OPEN",P_vs_NP:"OPEN"}};
};
const result=audit144();
process.stdout.write(JSON.stringify(result,null,2)+'\n');
