#!/usr/bin/env node
// Independent JavaScript replay of the local literal-substitution lemma.

import crypto from "node:crypto";

const TOP = null;
let checks = 0;
function ok(x, m="assertion") { checks++; if (!x) throw new Error(m); }
function key(c) { return c === TOP ? "TOP" : c.join(","); }
function norm(xs) {
  const s = new Set(xs);
  for (const x of s) if (s.has(-x)) return TOP;
  return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b) || (a<0)-(b<0));
}
function subset(a,b) { return a!==TOP && b!==TOP && a.every(x=>b.includes(x)); }
function res(a,b,p) {
  if (a===TOP || b===TOP || !a.includes(p) || !b.includes(-p)) throw new Error("pivot");
  return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
}
function project(c,sigma) {
  if (c===TOP) return TOP;
  return norm(c.map(l=>l>0?sigma[Math.abs(l)]:-sigma[Math.abs(l)]));
}
function subs(c) {
  if (c===TOP) return [TOP];
  const out=[];
  for(let m=0;m<(1<<c.length);m++) out.push(c.filter((_,i)=>m&(1<<i)));
  return out;
}
function compile(a,b,p,sigma,wa,wb) {
  const child=res(a,b,p), pa=project(a,sigma), pb=project(b,sigma), pc=project(child,sigma);
  if(pc===TOP) return ["skip-top",TOP];
  if(pa!==TOP && (wa===TOP || !subset(wa,pa))) throw new Error("left invariant");
  if(pb!==TOP && (wb===TOP || !subset(wb,pb))) throw new Error("right invariant");
  if(pa===TOP && wa!==TOP) throw new Error("taut left");
  if(pb===TOP && wb!==TOP) throw new Error("taut right");
  if(wa!==TOP && subset(wa,pc)) return ["left-survivor",wa];
  if(wb!==TOP && subset(wb,pc)) return ["right-survivor",wb];
  const image=p>0?sigma[Math.abs(p)]:-sigma[Math.abs(p)];
  if(wa!==TOP && wb!==TOP && wa.includes(image) && wb.includes(-image)) {
    const w=res(wa,wb,image);
    if(w!==TOP && subset(w,pc)) return ["one-res",w];
  }
  throw new Error("uncompiled transition");
}
function clauses(vars) {
  const out=[];
  function go(i,xs){
    if(i===vars.length){out.push(norm(xs));return;}
    go(i+1,xs); go(i+1,[...xs,vars[i]]); go(i+1,[...xs,-vars[i]]);
  }
  go(0,[]); return out;
}

const outcomes={"skip-top":0,"left-survivor":0,"right-survivor":0,"one-res":0};
let transitions=0,pairs=0;
const tails=clauses([2,3]);
const images=[-3,-2,-1,1,2,3];
for(const a0 of tails) for(const b0 of tails) {
  const a=norm([1,...a0]), b=norm([-1,...b0]);
  for(const i1 of images) for(const i2 of images) for(const i3 of images) {
    const sigma={1:i1,2:i2,3:i3}; transitions++;
    const pa=project(a,sigma),pb=project(b,sigma);
    for(const wa of pa===TOP?[TOP]:subs(pa)) for(const wb of pb===TOP?[TOP]:subs(pb)) {
      const [kind,w]=compile(a,b,1,sigma,wa,wb);
      const pc=project(res(a,b,1),sigma);
      ok(pc===TOP?w===TOP:subset(w,pc),"bad witness");
      outcomes[kind]++; pairs++;
    }
  }
}

// Split-gadget polarity and corruption controls independent of Python.
let rejected=0;
for(const signs of [[1,2,3],[-1,2,3],[1,-2,3],[1,2,-3],[-1,-2,-3]]) {
  const [l1,l2,l3]=signs,a=4;
  const p=norm([l1,l2,a]),q=norm([l1,l3,-a]);
  const good={1:1,2:2,3:3,4:l3};
  ok(key(project(p,good))===key(norm(signs)),"P alias");
  ok(project(q,good)===TOP,"Q alias");
  ok(key(res(p,q,a))===key(norm(signs)),"gadget RES");
  const bad={1:1,2:2,3:3,4:-l3};
  if(!(key(project(p,bad))===key(norm(signs)) && project(q,bad)===TOP)) rejected++;
}
try { res([1,4],[1,-4],-4); } catch { rejected++; }
try { compile([1,4],[1,-4],4,{1:1,4:1},[99],TOP); } catch { rejected++; }
ok(rejected===7,"negative controls");

const result={status:"PASS",model:"ordinary DAG Resolution only; not historical R_mix341 bytes",checks,transitions,witness_pairs:pairs,outcomes,hostile_controls_rejected:rejected};
result.sha256=crypto.createHash("sha256").update(JSON.stringify(result)).digest("hex");
console.log(JSON.stringify(result));
