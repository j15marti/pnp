"use strict";
// TMR-3/063 finite abstract block-word/liveness test, not a native TM microtrace.
// Run with: node tmr3_frontier_guard063.js
const REV="tmr3-frontier-guard063-v1";
let assertions=0;
function check(cond,why){assertions++;if(!cond)throw Error(why+" at "+assertions)}
function readSource(word){
  if(!/^[01]+$/.test(word))return null;
  let k=0;while(k<word.length && word[k]==="1")k++;
  if(k<4 || k+1+k!==word.length || word[k]!=="0")return null;
  return [...word.slice(k+1)].map(Number);
}
const p=2;
function candidate(B,id){
  const out=Array.from({length:p},()=>[]);
  for(let j=0;j<B;j++)for(let h=0;h<p;h++){
    let z;
    if(id===0)z=0;
    else if(id===1)z=(j>=(h===0?2:4)?1:0);
    else if(id===2)z=[0,1,2,3,2,1,0,1][j];
    else z=[0,1,0,1,2,1,2,3][j];
    out[h].push(z);
  }
  return out;
}
function frontierBrute(g){
  let w=0;
  for(let j=0;j<g[0].length;j++){
    const live=new Set();
    for(let h=0;h<p;h++)for(let i=0;i<=j;i++)
      if(g[h].slice(j+1).includes(g[h][i]))live.add(h+":"+g[h][i]);
    w=Math.max(w,live.size);
  }
  return w;
}
function frontierGuard(g,W){
  const B=g[0].length;
  for(let j=0;j<B;j++){
    let count=0;
    for(let h=0;h<p;h++)for(let i=0;i<=j;i++){
      let first=true;
      for(let r=0;r<i;r++)if(g[h][r]===g[h][i]){first=false;break}
      if(!first)continue;
      let later=false;
      for(let r=j+1;r<B;r++)if(g[h][r]===g[h][i]){later=true;break}
      if(later && ++count>W)return false;
    }
  }
  return true;
}
function direct(x,g){
  const cells=new Map();let out=0;
  for(let j=0;j<x.length;j++){
    const a="0:"+g[0][j],b="1:"+g[1][j];
    const old0=cells.get(a)||0,old1=cells.get(b)||0;
    const v0=old0^x[j],v1=old1^v0;
    cells.set(a,v0);cells.set(b,v1);out^=v1;
  }
  return out;
}
function trial(x,g,W){
  if(!frontierGuard(g,W))return "SKIP";
  const authentic=candidate(x.length,x[0]^x[1]);
  const cells=new Map();let out=0;
  for(let j=0;j<x.length;j++){
    for(let h=0;h<p;h++)if(g[h][j]!==authentic[h][j])return "FAIL";
    const a="0:"+g[0][j],b="1:"+g[1][j];
    const old0=cells.get(a)||0,old1=cells.get(b)||0;
    const v0=old0^x[j],v1=old1^v0;
    out^=v1;
    for(const [h,key,value] of [[0,a,v0],[1,b,v1]]){
      let future=false;
      for(let r=j+1;r<x.length;r++)if(g[h][r]===g[h][j]){future=true;break}
      if(future)cells.set(key,value);else cells.delete(key);
    }
    check(cells.size<=W,"live cache violates prechecked width");
  }
  return out;
}
let cases=0,attempts=0,skips=0,fails=0,accepts=0,malformed=0,maxWidth=0;
for(let B=4;B<=8;B++)for(let bits=0;bits<(1<<B);bits++){
  const x=Array.from({length:B},(_,j)=>(bits>>(B-j-1))&1);
  const source="1".repeat(B)+"0"+x.join("");
  check(JSON.stringify(readSource(source))===JSON.stringify(x),"source roundtrip");
  for(const bad of [source+"0",source.slice(1),source+"x"]){
    check(readSource(bad)===null,"malformed source accepted");malformed++;
  }
  cases++;
  const gTrue=candidate(B,x[0]^x[1]),wTrue=frontierBrute(gTrue);
  maxWidth=Math.max(maxWidth,wTrue);
  for(let W=0;W<=4;W++){
    let outputs=[];
    for(let id=0;id<4;id++){
      const g=candidate(B,id),w=frontierBrute(g);
      for(let h=0;h<p;h++)for(let j=1;j<B;j++)check(Math.abs(g[h][j]-g[h][j-1])<=1,"nonadjacent block control");
      check(frontierGuard(g,W)===(w<=W),"guard/brute mismatch");
      const r=trial(x,g,W);attempts++;
      if(r==="SKIP")skips++;
      else if(r==="FAIL")fails++;
      else {check(r===direct(x,gTrue),"bad accepted result");outputs.push(r);accepts++}
    }
    check((outputs.length>0)===(wTrue<=W),"completeness vs width");
    check(outputs.every(a=>a===outputs[0]),"nonunique accepting output");
  }
}
const raw={revision:REV,seed:null,model:"finite abstract block stage interface, no native local-head TM",cases,malformed,attempts,guard_skips:skips,failed_candidates:fails,accepted_candidates:accepts,max_authentic_width:maxWidth,assertions,failures:0,limitations:["No physical b-step local-head microcode","Candidate family is a special 4-word control, not a general compiler","Test uses materialized arrays and maps; low-space guard bound is symbolic","No generic nonassociative TreeEval evaluator executed"]};
console.log(JSON.stringify(raw));
