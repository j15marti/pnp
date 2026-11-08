"use strict";
// Independent V8/Node replay of the LSPV-5/439 terminal-peel table.
// This is ordinary exact Resolution only, not the historical R_mix341 checker.

let checks = 0;
const ck = (x, m) => { checks++; if (!x) throw new Error(m || "assertion"); };
const norm = c => [...new Set(c)].sort((a,b) => Math.abs(a)-Math.abs(b) || b-a);
const key = c => norm(c).join(",");
const parse = k => k === "" ? [] : k.split(",").map(Number);
const sources = [
 [1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
 [2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
 [1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
 [4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7]
].map(norm);
const goals = [[-1,-3,7],[1,-7],[3,-7]].map(norm);
const sourceKeys = new Set(sources.map(key));

function resolvents(a,b) {
  const out = new Map();
  for (let p=1;p<=7;p++) for (const [l,r] of [[a,b],[b,a]]) {
    if (!l.includes(p) || !r.includes(-p)) continue;
    const c = norm(l.filter(x=>x!==p).concat(r.filter(x=>x!==-p)));
    if (c.some(x=>c.includes(-x))) continue;
    out.set(`${p}|${key(c)}`, {pivot:p, child:c});
  }
  return [...out.values()];
}

const known = new Map(sources.map(c=>[key(c),c]));
const rounds = [];
for (;;) {
  const arr = [...known.values()].sort((a,b)=>key(a).localeCompare(key(b)));
  const fresh = new Map();
  for (let i=0;i<arr.length;i++) for (let j=i+1;j<arr.length;j++) {
    for (const {child} of resolvents(arr[i],arr[j])) {
      const k=key(child); if (!known.has(k)) fresh.set(k,child);
    }
  }
  if (!fresh.size) break;
  rounds.push(fresh.size);
  for (const [k,c] of fresh) known.set(k,c);
}
ck(known.size===1270,"closure size");
ck(JSON.stringify(rounds)===JSON.stringify([43,444,766,1]),"closure rounds");

const closure=[...known.values()].sort((a,b)=>key(a).localeCompare(key(b)));
const options=new Map(); let optionCount=0;
for (let i=0;i<closure.length;i++) for (let j=i+1;j<closure.length;j++) {
  for (const {pivot,child} of resolvents(closure[i],closure[j])) {
    const k=key(child); if(!options.has(k)) options.set(k,[]);
    options.get(k).push({left:closure[i],right:closure[j],pivot}); optionCount++;
  }
}
ck(optionCount===253208,"parent option count");
ck(JSON.stringify(goals.map(g=>options.get(key(g)).length))===JSON.stringify([6,8,6]),"goal option counts");

const assignments=[];
for(let bits=0;bits<128;bits++) assignments.push(Array.from({length:8},(_,v)=>v?!!(bits&(1<<(v-1))):false));
const sat=(c,a)=>c.some(l=>a[Math.abs(l)]===(l>0));
const deletionModels=sources.map((_,missing)=>assignments.filter(a=>sources.every((c,i)=>i===missing||sat(c,a))));
const masks=new Map();
for(const c of closure){
  let m=0;
  for(let i=0;i<16;i++) if(deletionModels[i].some(a=>!sat(c,a))) m|=(1<<i);
  masks.set(key(c),m);
}

function connectedFloor(targets){
  const ms=[...targets].map(k=>masks.get(k)).filter(Boolean); if(!ms.length)return {floor:0,union:0,components:0};
  const par=ms.map((_,i)=>i); const find=x=>{while(par[x]!==x){par[x]=par[par[x]];x=par[x]}return x};
  const join=(a,b)=>{a=find(a);b=find(b);if(a!==b)par[b]=a};
  for(let i=0;i<ms.length;i++)for(let j=0;j<i;j++)if(ms[i]&ms[j])join(i,j);
  let u=0;for(const m of ms)u|=m;
  const components=new Set(ms.map((_,i)=>find(i))).size;
  let count=0;for(let i=0;i<16;i++)if(u&(1<<i))count++;
  return {floor:count-components,union:count,components};
}

const goalKeys=goals.map(key); const initial=connectedFloor(new Set(goalKeys));
ck(initial.floor===15&&initial.union===16&&initial.components===1,"initial floor");
const records=[];
for(let gi=0;gi<goals.length;gi++)for(const o of options.get(goalKeys[gi])){
  const t=new Set(goalKeys);t.delete(goalKeys[gi]);
  for(const p of [o.left,o.right])if(!sourceKeys.has(key(p)))t.add(key(p));
  const f=connectedFloor(t);
  records.push({sink:gi,left:o.left,right:o.right,pivot:o.pivot,remaining:f,total:1+f.floor});
}
ck(records.length===20,"20 sink branches");
ck(records.every(r=>r.total===16&&r.remaining.union===16&&r.remaining.components===1),"all branches floor 16");
for(const r of records)ck(resolvents(r.left,r.right).some(x=>x.pivot===r.pivot&&key(x.child)===goalKeys[r.sink]),"exact parent replay");

// Hostile controls.
const sample=records[0];
ck(!resolvents(sample.left,sample.right).some(x=>x.pivot===(sample.pivot%7+1)&&key(x.child)===goalKeys[sample.sink]),"wrong pivot rejected");
ck(connectedFloor(new Set(goalKeys)).floor!==14,"source omission table rejected");
ck(!sourceKeys.has(goalKeys[0]),"goal/source alias rejected");

console.log(JSON.stringify({
 status:"PASS", assertions:checks, closure_clauses:known.size,
 closure_round_new_counts:rounds, all_reachable_parent_options:optionCount,
 goal_parent_option_counts:goals.map(g=>options.get(key(g)).length),
 terminal_peel_branches:records.length, minimum_branch_floor:Math.min(...records.map(r=>r.total)),
 hostile_controls:3, historical_R_mix341_checker_run:false, p_vs_np:"OPEN"
},null,2));
