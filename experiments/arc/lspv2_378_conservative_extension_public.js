#!/usr/bin/env node
"use strict";
// LSPV-2/378 standalone signed-PHP + Cook conservative extension verifier.
// Reproduce: node experiments/arc/lspv2_378_conservative_extension_public.js
// This is a source/witness check, NOT a Cook-proof size checker.
const assert = require("node:assert/strict");
let checks = 0;
function ok(cond,msg) {assert.ok(cond,msg);checks++;}
function source(h) {
  const f=[], ids=[], varid=(i,j)=>(i-1)*h+j;
  for(let i=1;i<=h+1;i++) {f.push(Array.from({length:h},(_,j)=>varid(i,j+1)));ids.push(["O",i]);}
  for(let j=1;j<=h;j++)for(let i=1;i<=h+1;i++)for(let k=i+1;k<=h+1;k++) {
    f.push([-varid(i,j),-varid(k,j)]);ids.push(["C",i,k,j]);
  }
  return {f,ids};
}
function definitions(h) {
  let rows=Array.from({length:h+1},(_,i)=>Array.from({length:h},(_,j)=>i*h+j+1));
  const gates=[],clauses=[];let next=h*(h+1)+1;
  for(let k=h;k>=2;k--){
    const reduced=[];
    for(let i=0;i<k;i++) {
      const row=[];
      for(let j=0;j<k-1;j++) {
        let y=next++,a=rows[i][j],b=rows[i][k-1],c=rows[k][j];
        gates.push([y,a,b,c]);
        clauses.push([y,-a],[y,-b,-c],[-y,a,b],[-y,a,c]);
        row.push(y);
      }
      reduced.push(row);
    }
    rows=reduced;
  }
  return {gates,clauses,vars:next-1};
}
function witness(h,tag) {
  const holes=new Map();
  if(tag[0]==="O") {
    let j=1;for(let p=1;p<=h+1;p++)if(p!==tag[1])holes.set(p,j++);
  } else {
    const [,a,b,j]=tag;holes.set(a,j);holes.set(b,j);
    let next=1;for(let p=1;p<=h+1;p++)if(p!==a&&p!==b) {
      while(next===j)next++;holes.set(p,next++);
    }
  }
  const out=new Map();
  for(let p=1;p<=h+1;p++)for(let j=1;j<=h;j++)out.set((p-1)*h+j,holes.get(p)===j);
  return out;
}
function extend(gates,input) {
  const v=new Map(input);
  for(const [y,a,b,c] of gates){ok(!v.has(y));v.set(y,v.get(a)||(v.get(b)&&v.get(c)));}
  return v;
}
function holds(c,v) {return c.some(x=>x>0?v.get(x):!v.get(-x));}
function parse(s) {
  let head=null,all=[],cur=[];
  for(const raw of s.split(/\r?\n/)){
    const line=raw.trim();if(!line||line.startsWith("c "))continue;
    if(line.startsWith("p ")){
      if(head!==null)throw Error("double header");
      const p=line.split(/\s+/);
      if(p.length!==4||p[1]!=="cnf")throw Error("bad header");
      head=p.slice(2).map(Number);
      if(head.some(x=>!Number.isSafeInteger(x)||x<0))throw Error("bad integers");
      continue;
    }
    if(head===null)throw Error("missing header");
    for(const s of line.split(/\s+/)){
      if(!/^-?\d+$/.test(s))throw Error("bad literal");
      const x=Number(s);
      if(!Number.isSafeInteger(x))throw Error("overflow");
      if(x===0){all.push(cur);cur=[];}
      else {if(Math.abs(x)>head[0])throw Error("out of range");cur.push(x);}
    }
  }
  if(!head||cur.length||all.length!==head[1])throw Error("wrong count");
  return all;
}
function k4(odd) {
  const e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j]);
  let n=0;
  for(let x=0;x<64;x++){
    let good=true;
    for(let v=0;v<4;v++){
      let parity=0;
      for(let i=0;i<6;i++)if(e[i].includes(v))parity^=(x>>i)&1;
      if(parity!==((odd&&v===0)?1:0))good=false;
    }
    if(good)n++;
  }
  return n;
}
const out=[];
for(let h=1;h<=6;h++){
  const {f,ids}=source(h),{gates,clauses,vars}=definitions(h);
  ok(f.length===h+1+h*h*(h+1)/2);
  ok(gates.length===h*(h+1)*(h-1)/3);
  ok(clauses.length===4*gates.length);
  let text="p cnf "+vars+" "+(f.length+clauses.length)+"\n";
  text+=[...f,...clauses].map(c=>c.join(" ")+" 0\n").join("");
  ok(parse(text).length===f.length+clauses.length);
  for(let index=0;index<ids.length;index++){
    const v=extend(gates,witness(h,ids[index]));
    let bad=[];
    for(let i=0;i<f.length;i++)if(!holds(f[i],v))bad.push(i);
    ok(bad.length===1&&bad[0]===index,"bad deletion witness "+h+"/"+index);
    for(const c of clauses)ok(holds(c,v),"gate failed");
    for(let g=0;g<gates.length;g++){
      let corrupt=new Map(v);const y=gates[g][0];
      corrupt.set(y,!corrupt.get(y));
      ok(!clauses.slice(4*g,4*g+4).every(c=>holds(c,corrupt)),"not unique");
    }
  }
  if(h<=3)for(let mask=0;mask<2**(h*(h+1));mask++){
    const v=new Map();for(let i=1;i<=h*(h+1);i++)v.set(i,Boolean((mask>>(i-1))&1));
    const ext=extend(gates,v);
    ok(clauses.every(c=>holds(c,ext)));
    ok(!f.every(c=>holds(c,ext)));
  }
  out.push({holes:h,original_clauses:f.length,auxiliary_gates:gates.length,
    total_clauses:f.length+clauses.length,source_deletion_witnesses:ids.length,
    dimacs_bytes:Buffer.byteLength(text)});
}
const malformed=[
  "p cnf 1 1\n1 0\n1 0\n","p cnf 1 1\n2 0\n",
  "p cnf 1 1\n1\n","1 0\n","p cnf x 1\n1 0\n",
  "p cnf 1 1\n1 0\np cnf 1 0\n"
];
for(const s of malformed){let rejected=false;try{parse(s);}catch(e){rejected=true;}ok(rejected);}
ok(k4(true)===0);ok(k4(false)===8);
console.log(JSON.stringify({status:"COMPUTATIONAL",checks,model:out,
  malformed_rejected:malformed.length,k4_odd_even:[0,8],
  scope:"functional conservativity and all original source-deletion witnesses; not Cook proof validity"},null,2));
