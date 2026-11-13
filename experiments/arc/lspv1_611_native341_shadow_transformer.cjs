#!/usr/bin/env node
"use strict";
/* LSPV-1/611. A pin-by-source recreation of the /341 AND3 local block, and
   an independently expressed Array/String shadow-coordinate semantics.
   No historical full-R_mix341 claims. Run: node <this-file>. */
function gate(s,S) {
  try {return s?.length===S.length && new Set(s).size===S.length && S.every(x=>s.includes(x));}
  catch {return false;}
}
function originalFactor(a,b,s,E) {
  const sup=[...new Set([...a.support,...b.support])];
  if(sup.length>3||!gate(s,sup))return null;
  const ev=(tab,support,bits)=>{
    let p=0;for(let i=0;i<support.length;i++)p|=Number(bits[support[i]])<<i;
    return (tab>>p)&1;
  };
  let table=0; const shadows=[];
  for(let m=0;m<(1<<sup.length);m++){
    let bits=Array(E).fill(0);
    for(let j=0;j<s.length;j++)bits[s[j]]=(m>>j)&1;
    shadows.push(bits.slice());
    if(ev(a.table,a.support,bits)&&ev(b.table,b.support,bits))table|=1<<m;
  }
  return {table,shadows,sup};
}
function specFactor(a,b,s,E) {
  const sup=[...new Set([...a.support,...b.support])];
  if(!gate(s,sup))return null;
  let table=0,shadow10max=0;
  for(let m=0;m<(1<<sup.length);m++){
    const bitAt=e=>{
      if(Array.isArray(s)){let j=s.indexOf(e);return j<0?0:(m>>j)&1;}
      for(let j=0;j<s.length;j++)if(s.charCodeAt(j)===48+e&&e<=9)return (m>>j)&1;
      return 0;
    };
    const truth=v=>{
      let p=0;v.support.forEach((e,j)=>p|=bitAt(e)<<j);
      return (v.table>>p)&1;
    };
    if(truth(a)&&truth(b))table|=1<<m;
    if(E>10)shadow10max=Math.max(shadow10max,bitAt(10));
  }
  return {table,shadow10max};
}
function originalAlias(tab,s,E,mask,rhs) {
  const M=BigInt(mask);
  for(let e=0;e<E;e++)if(((M>>BigInt(e))&1n)!==0n&&!s.includes(e))return false;
  for(let m=0;m<(1<<s.length);m++){
    let bits=Array(E).fill(0);
    for(let j=0;j<s.length;j++)bits[s[j]]=(m>>j)&1;
    let lhs=0;for(let e=0;e<E;e++)if((M>>BigInt(e))&1n)lhs^=bits[e];
    if(((tab>>m)&1)!==(lhs===rhs?1:0))return false;
  }
  return true;
}
function specAlias(tab,s,E,mask,rhs) {
  const M=BigInt(mask);
  const allowed=e=>Array.isArray(s)?s.includes(e):typeof s==="string"&&s.includes(String(e));
  for(let e=0;e<E;e++)if(((M>>BigInt(e))&1n)!==0n&&!allowed(e))return false;
  for(let m=0;m<(1<<s.length);m++){
    let lhs=0;
    for(let e=0;e<E;e++)if(((M>>BigInt(e))&1n)!==0n){
      let bit=0;
      if(Array.isArray(s)){let j=s.indexOf(e);if(j>=0)bit=(m>>j)&1;}
      else if(e<10)for(let j=0;j<s.length;j++)if(s.charCodeAt(j)===48+e)bit=(m>>j)&1;
      lhs^=bit;
    }
    if(((tab>>m)&1)!==(lhs===rhs?1:0))return false;
  }
  return true;
}
function run() {
  const alpha=[..."0123456789AZ","\ud800","\udc00"];
  const strings=["😀0","0😀","10A","A10","10\ud800","\ud80010"];
  for(const a of alpha)for(const b of alpha)for(const c of alpha)strings.push(a+b+c);
  const indices=[0,1,2,9,10,11,12],masks=[0n,1n,2n,3n,512n,1024n,1025n,2048n,-1n,(1n<<40n)];
  let inspected=0,eligible=0,tableChecks=0,aliasChecks=0,arrChecks=0,typeControls=0,stringShadowChecks=0;
  const per=[];let witness=null;
  for(let i=0;i<indices.length;i++)for(let j=i+1;j<indices.length;j++)for(let k=j+1;k<indices.length;k++){
    const sup=[indices[i],indices[j],indices[k]],E=13;
    const a={support:sup,table:0x96},b={support:sup,table:0xe7};
    let count=0;
    for(const s of strings){
      inspected++;
      const x=originalFactor(a,b,s,E),y=specFactor(a,b,s,E);
      if((x===null)!==(y===null))throw Error("gate mismatch");
      if(x!==null){
        eligible++;count++;tableChecks++;
        if(x.table!==y.table)throw Error("table mismatch");
        const allHighZero=x.shadows.every(bits=>bits.slice(10).every(z=>z===0));
        if(!allHighZero||y.shadow10max!==0)throw Error("high-coordinate shadow violated");
        stringShadowChecks++;
        for(const mask of masks)for(const rhs of [0,1]){
          aliasChecks++;
          if(originalAlias(x.table,s,E,mask,rhs)!==specAlias(x.table,s,E,mask,rhs))
            throw Error("alias mismatch");
        }
        if(s==="10A"&&sup.join(",")==="0,1,10")
          witness={support:s,source_support:sup,table:x.table,mask10_allowed:s.includes(10),bit10_always_zero:allHighZero};
      }
    }
    const perm=[
      [sup[0],sup[1],sup[2]],[sup[0],sup[2],sup[1]],
      [sup[1],sup[0],sup[2]],[sup[1],sup[2],sup[0]],
      [sup[2],sup[0],sup[1]],[sup[2],sup[1],sup[0]]
    ];
    for(const s of perm){
      const x=originalFactor(a,b,s,E),y=specFactor(a,b,s,E);
      arrChecks++;if(!x||x.table!==y.table)throw Error("array mismatch");
    }
    per.push({sup,count});
  }
  const objects=[null,true,23,{},{"length":3},{"length":3,"includes":true},{"length":3,"includes":"012"}];
  for(const s of objects){typeControls++;if(gate(s,[0,1,2]))throw Error("nonarray nonstring accepted");}
  const sup=[0,1,10],s="10A",E=13,a={support:sup,table:0},b={support:sup,table:0};
  for(let t=0;t<65536;t++){
    a.table=t>>8;b.table=t&255;
    const x=originalFactor(a,b,s,E),y=specFactor(a,b,s,E);
    tableChecks++;if(x.table!==y.table)throw Error("exhaustive parent table mismatch");
  }
  if(!witness)throw Error("missing witness");
  return {result:"PASS",checker_fragment:"experiments/arc/lspv2_341_independent_verify.js",
    checker_blob:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0",
    alphabet_code_units:alpha.length,inspected,eligible,tableChecks,aliasChecks,
    arrChecks,typeControls,stringShadowChecks,witness,
    nonzero_supports:per.filter(v=>v.count>0),
    surrogate_pair_control:{codepoint_set_size:new Set("😀0").size,code_units:"😀0".length},
    scope:"Exact recovered AND3 local Array/String semantics only; no full native calculus authentication."};
}
if(require.main===module) console.log(JSON.stringify(run(),null,2));
module.exports={run,gate,originalFactor,specFactor,originalAlias,specAlias};
