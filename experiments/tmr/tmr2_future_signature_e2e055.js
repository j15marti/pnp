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
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 if(process.argv.includes("--audit"))console.log(JSON.stringify(audit(),null,2));
 else{try{console.log(solve(require("fs").readFileSync(0,"utf8")).count.toString())}
 catch(e){console.error("INVALID: "+e.message);process.exitCode=2}}
}
