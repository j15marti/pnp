// LSPV-4/375 independent structural referee. Usage:
// node experiments/arc/lspv4_375_independent_verify.js experiments/arc/lspv4_375_lazy_involution_stream.js
"use strict";
const fs=require("fs");
function verdict(r){
  let n=0;const test=(x,msg)=>{n++;if(!x)throw Error("referee: "+msg);};
  function ownPHP(h){
    const v=h*(h+1),m=(h+1)+(h*h*(h+1))/2,C=[];
    for(let i=0;i<=h;i++)C.push(Array.from({length:h},(_,j)=>i*h+j+1));
    for(let j=0;j<h;j++)for(let i=0;i<=h;i++)for(let k=i+1;k<=h;k++)
      C.push([-(i*h+j+1),-(k*h+j+1)]);
    test(C.length===m,"PHP clause count");return {v,m,clauses:C};
  }
  function ownEasy(h){
    const v=h*(h+1),m=(h+1)+(h*h*(h+1))/2,C=[[1],[-1]];
    for(let i=1;i<=v&&C.length<m;i++)for(let j=i+1;j<=v&&C.length<m;j++)C.push([i,j]);
    test(C.length===m,"easy clause count");return {v,m,clauses:C};
  }
  function ownParse(bytes){
    let v=null,m=null,C=[];
    for(const line of String.fromCharCode(...bytes).split("\n")){
      if(!line.trim()||line.startsWith("c "))continue;
      if(line.startsWith("p cnf ")){const a=line.split(" ");v=+a[2];m=+a[3];}
      else C.push(line.trim().split(/\s+/).slice(0,-1).map(Number));
    }
    test(C.length===m,"parsed clause count");return {v,m,clauses:C};
  }
  function bytes(s){return Uint8Array.from([...s],ch=>ch.charCodeAt(0));}
  function same(a,b){return a.length===b.length && a.every((x,i)=>x===b[i]);}
  let swaps=0,queries=0;
  for(let h=1;h<=8;h++){
    const p=ownPHP(h),q=ownEasy(h);
    const as=r.countBase(r.php(h)),bs=r.countBase(r.easy(h));
    const x=bytes(r.render(r.presented(h,"X",as,bs)));
    const y=bytes(r.render(r.presented(h,"Y",as,bs)));
    test(JSON.stringify(ownParse(x))===JSON.stringify(p),"authenticated PHP");
    test(JSON.stringify(ownParse(y))===JSON.stringify(q),"authenticated Y");
    const f=r.map(x).bytes;
    test(same(f,y),"forward recoding");
    test(same(r.map(y).bytes,x),"reverse recoding");swaps+=2;
    for(const ix of [0,Math.floor(x.length/3),x.length-1]){
      test(r.lazyByte(x,ix)===y[ix],"lazy source X");
      test(r.lazyByte(y,ix)===x[ix],"lazy source Y");queries+=2;
    }
  }
  return {referee_assertions:n,swaps,lazy_queries:queries,status:"PASS"};
}
function start(src){
 const r=new Function(src+"\nreturn {countBase,php,easy,render,presented,map,lazyByte};")();
 return verdict(r);
}
if(typeof require!=="undefined"&&require.main===module){
 const path=process.argv[2]||"experiments/arc/lspv4_375_lazy_involution_stream.js";
 console.log(JSON.stringify(start(fs.readFileSync(path,"utf8")),null,2));
}
