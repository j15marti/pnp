#!/usr/bin/env node
"use strict";
// TMR2_FUTURESIGNATURE_E2E055_v3, deterministic seed 20261115.
// Exact #CNF on valid DIMACS (clauses of width <=3), INVALID otherwise.
// Canonical c split A B / seven-pin gadget recognized, other formulas exhaustive.
function pop(x){let c=0;while(x){x&=x-1n;c++}return c}
function fmt(a,b,edges){
 let p=a+b+1,q=p+1,r=q+1,lines=["c split "+a+" "+b,"p cnf "+(a+b+3)+" "+(edges.length+7)];
 for(let z=1;z<8;z++)lines.push([p,q,r].map((v,i)=>(z&(1<<i))?-v:v).join(" ")+" 0");
 for(let [i,j] of edges)lines.push(-(i+1)+" "+(-(a+j+1))+" "+p+" 0");
 return lines.join("\n")+"\n";
}
function parse(s){
 let n=null,m=null,a=null,b=null,c=[];
 for(let line of s.trim().split(/\r?\n/)){let w=line.trim().split(/\s+/);if(!w[0])continue;
 if(w[0]==="c"){if(w[1]==="split"){if(w.length!==4||a!==null)throw Error("split");a=+w[2];b=+w[3]}continue}
 if(w[0]==="p"){if(n!==null||w.length!==4||w[1]!=="cnf")throw Error("header");n=+w[2];m=+w[3];continue}
 if(n===null||w.length>4||w[w.length-1]!=="0")throw Error("clause syntax");
 let row=w.slice(0,-1).map(Number);
 if(row.some(x=>!Number.isSafeInteger(x)||x===0||Math.abs(x)>n))throw Error("literal");
 c.push(row)
 }
 if(!Number.isSafeInteger(n)||n<0||!Number.isSafeInteger(m)||m!==c.length)throw Error("metadata");
 if(a!==null&&(!Number.isSafeInteger(a)||!Number.isSafeInteger(b)||a<0||b<0))throw Error("partition");
 return {n,m,a,b,c}
}
function gadget(P){
 let {n,m,a,b,c}=P;if(a===null||a+b+3!==n||m<7)return null;
 let pins=[a+b+1,a+b+2,a+b+3];
 for(let z=1;z<8;z++)if(c[z-1].length!==3||!pins.every((v,i)=>c[z-1][i]===((z&(1<<i))?-v:v)))return null;
 let N=Array(a).fill(0n),A=Array(a).fill(0),B=Array(b).fill(0),seen=new Set();
 for(let j=7;j<m;j++){let t=c[j];if(t.length!==3||t[2]!==pins[0]||t[0]>=0||t[1]>=0)return null;
 let u=-t[0]-1,v=-t[1]-1-a,key=u+","+v;
 if(u<0||u>=a||v<0||v>=b||seen.has(key))return null;
 seen.add(key);N[u]|=1n<<BigInt(v);A[u]++;B[v]++
 }
 return {a,b,N,k:m-7,match:A.every(v=>v<=1)&&B.every(v=>v<=1)}
}
function fullDP(F){
 let {a,b,N}=F, M=new Map([["0",{u:0n,w:1n}]]),width=[1],arcs=0;
 for(let i=0;i<a;i++){let next=new Map();
 for(let {u,w} of M.values())for(let v of [u,u|N[i]]){arcs++;
 let key=v.toString(),old=next.get(key);if(old)old.w+=w;else next.set(key,{u:v,w})}
 M=next;width.push(M.size)}
 let count=0n;for(let {u,w} of M.values())count+=w*(1n<<BigInt(b-pop(u)));
 return {count,width,arcs}
}
function sig(u,remain){
 let res=[];for(let s=0;s<2**remain.length;s++){let v=u;for(let j=0;j<remain.length;j++)if(s&(1<<j))v|=remain[j];res.push(pop(v))}
 return res.join(",")
}
function quotientDP(F){
 let {a,b,N}=F; if(a>20)throw Error("audit-only exponential signature cap");
 let M=new Map([[sig(0n,N),{u:0n,w:1n}]]),width=[1],visits=2**a;
 for(let t=0;t<a;t++){let next=new Map(),R=N.slice(t+1);
 for(let {u,w} of M.values())for(let v of [u,u|N[t]]){
 let key=sig(v,R);visits+=2**R.length;
 let old=next.get(key);if(old)old.w+=w;else next.set(key,{u:v,w})}
 M=next;width.push(M.size)}
 let count=0n;for(let {u,w} of M.values())count+=w*(1n<<BigInt(b-pop(u)));
 return {count,width,signature_subset_visits:visits}
}
function brute(P){let ans=0n;for(let v=0n;v<(1n<<BigInt(P.n));v++){
 if(P.c.every(row=>row.some(x=>x>0?((v>>BigInt(x-1))&1n)===1n:((v>>BigInt(-x-1))&1n)===0n)))ans++;
 }return ans}
function solve(source){
 let P=parse(source),F=gadget(P);
 if(!F)return {count:brute(P),route:"generic-exhaustive"};
 if(F.match)return {count:3n**BigInt(F.k)*2n**BigInt(F.a+F.b-2*F.k),route:"matching-product"};
 let v=fullDP(F);return {count:v.count,route:"neighborhood-union-dp",width:v.width}
}
function rank2(F){
 if(F.a>5||F.b>5)return null;
 let piv=new Map(),lim=2**F.a;
 for(let x=0;x<lim;x++){let u=0n;for(let j=0;j<F.a;j++)if(x&(1<<j))u|=F.N[j];
 let r=0n;for(let y=0;y<(1<<F.b);y++)if((u&BigInt(y))===0n)r|=1n<<BigInt(y);
 while(r){let p=r.toString(2).length-1;if(!piv.has(p)){piv.set(p,r);break}r^=piv.get(p)}
 }return piv.size
}
function audit(){
 let seed=20261115>>>0,checks=0,instances=0,matching=0,generic=0,visits=0,samples=[];
 function ok(z,msg){checks++;if(!z)throw Error(msg)}
 function random(){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed}
 function test(a,b,edges,name){
 instances++;let source=fmt(a,b,edges),P=parse(source),F=gadget(P),z=solve(source),d=fullDP(F),q=quotientDP(F);
 ok(z.count===brute(P),name+" solver");ok(d.count===z.count,name+" full");ok(q.count===z.count,name+" quotient");
 ok(q.width.every((v,t)=>v<=d.width[t]),name+" states");
 ok(P.c.every(v=>v.length===3&&new Set(v.map(Math.abs)).size===3),name+" strict");
 ok(rank2(F)===null||rank2(F)===d.width[a],name+" rank");
 ok(z.route===(F.match?"matching-product":"neighborhood-union-dp"),name+" route");
 visits+=q.signature_subset_visits;if(F.match)matching++;
 if(name.startsWith("MATCH")||name==="COMPLETE4")samples.push({name,count:z.count.toString(),rank:d.width[a],raw:d.width,quotient:q.width,route:z.route})
 }
 for(let k=1;k<=8;k++)test(k,k,Array.from({length:k},(_,i)=>[i,i]),"MATCH"+k);
 for(let k=1;k<=5;k++)test(k,k,Array.from({length:k},(_,i)=>Array.from({length:k},(_,j)=>[i,j])).flat(),"COMPLETE"+k);
 for(let k=1;k<=5;k++)test(k,k,Array.from({length:k},(_,i)=>[0,i]),"STAR"+k);
 for(let a=1;a<=4;a++)for(let b=1;b<=4;b++)for(let j=0;j<7;j++){
 let e=[];for(let i=0;i<a;i++)for(let v=0;v<b;v++)if((random()&3)===0)e.push([i,v]);
 test(a,b,e,"R"+a+"_"+b+"_"+j)
 }
 for(let source of ["p cnf 2 2\n1 0\n-1 2 0\n","p cnf 2 2\n1 2 0\n-1 -2 0\n","p cnf 1 2\n1 0\n-1 0\n"]){
 let P=parse(source),z=solve(source);ok(z.route==="generic-exhaustive"&&z.count===brute(P),"generic");generic++}
 for(let source of ["p cnf 2 1\n1 3 0\n","p cnf 2 1\n1 0\n-1 0\n"]){let fail=false;try{solve(source)}catch(e){fail=true}ok(fail,"invalid")}
 return {revision:"TMR2_FUTURESIGNATURE_E2E055_v3",seed:20261115,instances,checks,matching,generic,signature_subset_visits:visits,failures:0,samples};
}

// TMR2_FRONTIER_CYCLE_E2E056_v1. Base includes actual DIMACS parser, strict pin checker, fullDP and exhaustive fallback.
function frontierForOrder(F,order){
 let a=F.a,future=Array(a+1).fill(0n),past=0n,bound=Array(a+1).fill(0n);
 for(let t=a-1;t>=0;t--)future[t]=future[t+1]|F.N[order[t]];
 for(let t=0;t<=a;t++){bound[t]=past&future[t];if(t<a)past|=F.N[order[t]]}
 return bound
}
function compressedFrontierDP(F,order){
 let {a,b,N}=F;if(order.length!==a||new Set(order).size!==a||order.some(x=>x<0||x>=a))throw Error("bad order");
 let bound=frontierForOrder(F,order),maxFront=Math.max(...bound.map(pop));
 let states=new Map([["0/0",{h:0,x:0n,w:1n}]]),width=[1],arcs=0,merged=0;
 for(let t=0;t<a;t++){
  let next=new Map(),nbr=N[order[t]],B=bound[t+1];
  for(let {h,x,w} of states.values()){
   let successors=[{h:h,x:x&B},{h:h+pop(nbr)-pop(x&nbr),x:(x|nbr)&B}];
   for(let v of successors){arcs++;let key=v.h+"/"+v.x.toString(16),old=next.get(key);
    if(old){old.w+=w;merged++}else next.set(key,{h:v.h,x:v.x,w})}
  }
  states=next;width.push(states.size);
  if(states.size>(b+1)*(2**maxFront))throw Error("frontier bound violated");
 }
 let count=0n;for(let {h,w} of states.values())count+=w*(1n<<BigInt(b-h));
 return {count,width,arcs,merged,maxFront,frontierSizes:bound.map(pop)}
}
function cycleOrder(F){
 let {a,b,N,k}=F;if(a!==b||a<3||k!==2*a)return null;
 let A=Array.from({length:a},()=>[]),B=Array.from({length:b},()=>[]);
 for(let u=0;u<a;u++)for(let v=0;v<b;v++)if((N[u]>>BigInt(v))&1n){A[u].push(v);B[v].push(u)}
 if(!A.every(v=>v.length===2)||!B.every(v=>v.length===2))return null;
 let seen=new Set(),curA=0,prevB=-1,order=[];
 for(let i=0;i<a;i++){
  if(seen.has(curA))return null;seen.add(curA);order.push(curA);
  let targetB=A[curA].find(v=>v!==prevB);
  if(targetB===undefined)return null;
  let nextA=B[targetB].find(v=>v!==curA);
  if(nextA===undefined)return null;
  prevB=targetB;curA=nextA;
 }
 if(curA!==0||seen.size!==a)return null;
 return order
}
function solveCycleSource(s){
 let P=parse(s),F=gadget(P);
 if(!F)return {count:brute(P),route:"generic-exhaustive"};
 if(F.match)return {count:3n**BigInt(F.k)*2n**BigInt(F.a+F.b-2*F.k),route:"matching-product"};
 let order=cycleOrder(F);
 if(order!==null){let d=compressedFrontierDP(F,order);
  if(d.maxFront>2)throw Error("cycle frontier unexpectedly >2");
  return {...d,route:"authenticated-cycle-frontier",order}
 }
 return {...fullDP(F),route:"neighborhood-union-dp"}
}
function lucas(n){let u=2n,v=1n;if(n===0)return u;for(let i=1;i<=n;i++){let z=u+v;u=v;v=z}return u}
function cycleEdges(k,perA,perB){
 return Array.from({length:k},(_,i)=>[i,i]).concat(Array.from({length:k},(_,i)=>[i,(i+1)%k]))
  .map(([u,v])=>[perA[u],perB[v]]).sort((x,y)=>x[0]-y[0]||x[1]-y[1])
}
function cycleAudit(){
 let seed=20261115>>>0,checks=0,instances=0,brutes=0,fulls=0,malformed=0,controls=0,examples=[];
 function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 function ok(v,msg){checks++;if(!v)throw Error(msg)}
 for(let k=3;k<=22;k++){
  let perA=Array.from({length:k},(_,i)=>i),perB=perA.slice();
  for(let i=k-1;i>0;i--){let j=rand()%(i+1);[perA[i],perA[j]]=[perA[j],perA[i]]}
  for(let i=k-1;i>0;i--){let j=rand()%(i+1);[perB[i],perB[j]]=[perB[j],perB[i]]}
  let source=fmt(k,k,cycleEdges(k,perA,perB)),P=parse(source),F=gadget(P);
  let derived=cycleOrder(F),result=solveCycleSource(source),independent=lucas(2*k);
  ok(derived!==null&&derived.length===k,"cycle recognize "+k);
  ok(result.route==="authenticated-cycle-frontier","route "+k);
  ok(result.count===independent,"count vs Lucas "+k);
  ok(result.maxFront===2,"frontier 2 "+k);
  ok(result.width.every(z=>z<=4*(k+1)),"width bound "+k);
  ok(result.arcs===2*result.width.slice(0,-1).reduce((x,y)=>x+y,0),"genuine arcs "+k);
  ok(result.frontierSizes[0]===0&&result.frontierSizes[k]===0,"terminal boundaries "+k);
  ok(P.c.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"strict CNF "+k);
  instances++;
  if(k<=5){ok(result.count===brute(P),"full original assignments "+k);brutes++}
  if(k<=12){let d=fullDP(F);ok(d.count===result.count,"uncompressed DP "+k);fulls++;
   if(k<=7){let q=quotientDP(F);ok(q.count===result.count,"full future signature "+k)}
  }
  if([3,4,5,8,12,16,22].includes(k))examples.push({
   k,sourceBits:source.length*8,count:result.count.toString(),rankLowerBound:2**Math.floor(k/2),
   frontierMax:result.maxFront,width:result.width,arcs:result.arcs})
 }
 let tests=[
  [4,4,Array.from({length:4},(_,i)=>[i,i]),"matching-product"],
  [3,3,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j])).flat(),"neighborhood-union-dp"],
  [3,4,Array.from({length:4},(_,i)=>[0,i]),"neighborhood-union-dp"],
  [4,4,[[0,0],[1,0],[1,1],[2,1],[2,2],[3,3]],"neighborhood-union-dp"],
  [3,4,[],"matching-product"]
 ];
 for(let [a,b,edges,route] of tests){
  let src=fmt(a,b,edges),P=parse(src),F=gadget(P),ans=solveCycleSource(src);
  ok(ans.route===route,"hostile route "+route);
  ok(ans.count===fullDP(F).count,"hostile exact count "+route);
  ok(ans.count===brute(P),"hostile complete CNF "+route);controls++;
 }
 for(let src of ["p cnf 2 1\n1 3 0\n","p cnf 2 1\n1 0\n-1 0\n"]){
  let rejected=false;try{solveCycleSource(src)}catch(e){rejected=true}ok(rejected,"malformed rejects");malformed++
 }
 return {revision:"TMR2_FRONTIER_CYCLE_E2E056_v1",seed:20261115,cycleInstances:instances,
  bruteCNFInstances:brutes,genericDPComparisons:fulls,hostileControls:controls,malformedControls:malformed,
  checks,failures:0,examples}
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 if(process.argv.includes("--audit"))console.log(JSON.stringify(cycleAudit(),null,2));
 else{try{console.log(solveCycleSource(require("fs").readFileSync(0,"utf8")).count.toString())}
 catch(e){console.error("INVALID: "+e.message);process.exitCode=2}}
}
