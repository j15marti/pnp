"use strict";
// LSPV-4/491: independent native source-grammar and guarded normalization controls.
// Run: node lspv4_491_two_mode_guard.cjs
const assert = require("node:assert/strict");
function clean(cl) {
  const d = new Map();
  for (const x of cl) {
    if (!Number.isSafeInteger(x) || x===0) throw Error("bad literal");
    const k=Math.abs(x), s=x>0;
    if (d.has(k)&&d.get(k)!==s) return null;
    d.set(k,s);
  }
  return [...d].map(([k,s])=>s?k:-k);
}
function normalize8(cl,base) {
  const v=clean(cl), [a,b,c]=[base,base+1,base+2]; let p=[];
  const signs=[1,-1];
  if (v===null) p=[[a,b,c]];
  else if (!v.length) for (const s of signs) for(const t of signs) for(const u of signs) p.push([s*a,t*b,u*c]);
  else if (v.length===1) for(const s of signs) for(const t of signs) p.push([v[0],s*a,t*b]);
  else if (v.length===2) p=[[v[0],v[1],a],[v[0],v[1],-a]];
  else p=[v];
  return Array.from({length:8},(_,i)=>p[i%p.length].slice());
}
function transform(F,n) {
  const m=F.length;
  const fast=F.every(cl=>cl.length===3 && new Set(cl.map(Math.abs)).size===3);
  const Q=fast?F.map(c=>c.slice()):F.flatMap((cl,j)=>normalize8(cl,n+3*j+1));
  const base=fast?n:n+3*m;
  const q=Q.length,z=base+q+1,u=z+1,v=z+2;
  const out=[];
  for (let i=0;i<q;i++) {
    const [a,b,c]=Q[i], h=base+i+1;
    out.push([a,b,h],[-h,c,z]);
  }
  for (const s of [1,-1]) for(const t of [1,-1]) out.push([-z,s*u,t*v]);
  assert.equal(out.length, (fast?2:16)*m+4);
  assert.ok(v<=3*out.length+3);
  assert.ok(out.every(cl=>cl.length===3 && new Set(cl.map(Math.abs)).size===3 && cl.every(x=>Math.abs(x)<=v)));
  return {out,n:v,fast,q};
}
function enc(F,n){
  const m=F.length;
  assert.ok(n<=3*m+3 && F.every(c=>c.length<=3&&c.every(x=>Math.abs(x)<=n&&x!==0)));
  const b=Math.ceil(Math.log2(128*(n+m+3)));
  const bits=(x,w)=>x.toString(2).padStart(w,"0");
  return "1".repeat(b)+"0"+bits(n,b)+bits(m,b)+
    F.map(cl=>Array.from({length:3},(_,j)=>j<cl.length?"1"+(cl[j]>0?"1":"0")+bits(Math.abs(cl[j]),b):"0".repeat(b+2)).join("")).join("");
}
function dec(raw){
  const b=raw.indexOf("0"); if(b<=0||!/^[01]+$/.test(raw))throw Error("bad prefix");
  const n=parseInt(raw.slice(b+1,2*b+1),2),m=parseInt(raw.slice(2*b+1,3*b+1),2);
  if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m)||n>3*m+3||b!==Math.ceil(Math.log2(128*(n+m+3)))||raw.length!==3*b+1+3*m*(b+2))throw Error("bad header");
  const F=[]; let p=3*b+1;
  for(let i=0;i<m;i++) {
    const c=[];let absent=false;
    for(let j=0;j<3;j++){
      const present=raw[p++],sign=raw[p++],v=parseInt(raw.slice(p,p+b),2);p+=b;
      if(present==="0"){if(sign!=="0"||v!==0)throw Error("bad absent");absent=true}
      else {if(absent||v<1||v>n)throw Error("bad slot");c.push(sign==="1"?v:-v)}
    } F.push(c)
  }
  return {F,n};
}
function ev(c,a){return c.some(x=>a[Math.abs(x)]===(x>0))}
function sat(F){
  const vs=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
  function dfs(a){
    while(true){
      let changed=false;
      for(const c of F){
        if(ev(c,a))continue;
        const rem=c.filter(x=>a[Math.abs(x)]===undefined);
        if(!rem.length)return false;
        if(rem.length===1){const x=rem[0],k=Math.abs(x),v=x>0;
          if(a[k]!==undefined&&a[k]!==v)return false;
          if(a[k]===undefined){a[k]=v;changed=true}
        }
      }
      if(!changed)break;
    }
    if(F.every(c=>ev(c,a)))return true;
    const k=vs.find(x=>a[x]===undefined);if(k===undefined)return false;
    return dfs({...a,[k]:false})||dfs({...a,[k]:true});
  }
  return dfs({});
}
const pool=[[],[1],[-1],[1,1],[1,-1],[1,2],[-1,-2],[1,2,3],[-1,2,3],[1,1,2]];
let cases=0,assertions=0,rounds=0,modeFast=0,modeSlow=0,localChecks=0;
for(let m=0;m<=2;m++){
  const total=pool.length**m;
  for(let index=0;index<total;index++){
    let p=index;const F=[];for(let j=0;j<m;j++){F.push(pool[p%pool.length].slice());p=Math.floor(p/pool.length)}
    const raw=enc(F,3),parsed=dec(raw);assert.deepEqual(parsed.F,F);assertions++;
    const obj=transform(F,3);obj.fast?modeFast++:modeSlow++;
    const output=enc(obj.out,obj.n),parsedOut=dec(output);
    assert.deepEqual(parsedOut.F,obj.out);assertions++;
    assert.equal(parsedOut.n,obj.n);assertions++;
    for(let j=0;j<m;j++)for(let mask=0;mask<8;mask++){
      const a={1:!!(mask&1),2:!!(mask&2),3:!!(mask&4)};
      const expected=ev(F[j],a), local=normalize8(F[j],4+3*j);
      let exists=false;
      for(let bits=0;bits<8;bits++){
        const va={...a};for(let h=0;h<3;h++)va[4+3*j+h]=!!(bits&(1<<h));
        if(local.every(c=>ev(c,va))){exists=true;break}
      }
      assert.equal(exists,expected);assertions++;localChecks++;
    }
    if(m<=1){assert.equal(sat(F),sat(obj.out));assertions++}
    if(cases<35){
      const next=transform(obj.out,obj.n);
      assert.equal(next.fast,true);assertions++;
      assert.equal(next.out.length,2*obj.out.length+4);assertions++;
      assert.deepEqual(dec(enc(next.out,next.n)).F,next.out);assertions++;
      rounds++;
    }
    cases++;
  }
}
let malformed=0;
for(const bad of ["","0","101010","1110001010","xyz"]){assert.throws(()=>dec(bad));assertions++;malformed++}
for(let m=0;m<=8;m++){
  const slow=16*m+4,slowIter=[slow];for(let j=1;j<7;j++)slowIter.push(2*slowIter.at(-1)+4);
  for(let j=1;j<=7;j++){
    const formula=(2**(j-1))*(slow+4)-4;
    assert.equal(slowIter[j-1],formula);assertions++;
  }
}
const result={status:"COMPUTATIONAL finite controls",run:"LSPV-4/491",cases,modeFast,modeSlow,assertions,localChecks,secondLevelRoundtrips:rounds,malformedRejected:malformed,errors:0,nativeFLMVExecuted:false,fullMixedCheckerExecuted:false};
if(require.main===module) process.stdout.write(JSON.stringify(result,null,2)+"\n");
module.exports={transform,normalize8,enc,dec,result};
