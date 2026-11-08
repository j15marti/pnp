#!/usr/bin/env node
// Independent V8 replay of LSPV-5/440's exact tree-residual recursion.
// Fixed finite proper Resolution only; not historical R_mix341.
import fs from "node:fs";

const rawSources = [
  [1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
  [2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
  [1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
  [4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7],
];
const rawGoals = [[-1,-3,7],[1,-7],[3,-7]];
const norm = xs => [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
const key = xs => norm(xs).join(",");
const fromKey = k => k === "" ? [] : k.split(",").map(Number);
const S = rawSources.map(norm), G = rawGoals.map(norm);
const sk = new Map(S.map((c,i)=>[key(c),i]));
const full = (1<<16)-1;

function children(aa,bb) {
  const out = new Map();
  for (let p=1;p<=7;p++) for (const [a,b] of [[aa,bb],[bb,aa]]) {
    if (!a.includes(p) || !b.includes(-p)) continue;
    const c=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
    if (c.some(x=>c.includes(-x))) continue;
    out.set(`${p}|${key(c)}`,{pivot:p,clause:c});
  }
  return [...out.values()];
}

function buildClosure() {
  const db=new Map(S.map(c=>[key(c),c]));
  while (true) {
    const a=[...db.values()].sort((x,y)=>key(x).localeCompare(key(y)));
    const add=new Map();
    for(let i=0;i<a.length;i++) for(let j=i+1;j<a.length;j++)
      for(const z of children(a[i],a[j])) if(!db.has(key(z.clause))) add.set(key(z.clause),z.clause);
    if(!add.size) break;
    for(const [k,c] of add) db.set(k,c);
  }
  const clauses=[...db.values()].sort((x,y)=>key(x).localeCompare(key(y)));
  const opts=new Map();
  for(let i=0;i<clauses.length;i++) for(let j=i+1;j<clauses.length;j++)
    for(const z of children(clauses[i],clauses[j])) {
      const k=key(z.clause); if(!opts.has(k)) opts.set(k,[]);
      opts.get(k).push({left:clauses[i],right:clauses[j],pivot:z.pivot});
    }
  return {clauses,opts};
}

const sat=(c,bits)=>c.some(x=>Boolean(bits&(1<<(Math.abs(x)-1)))===(x>0));
function deletionMasks(clauses) {
  const models=[];
  for(let miss=0;miss<16;miss++) {
    const ms=[];
    for(let bits=0;bits<128;bits++) if(S.every((c,i)=>i===miss||sat(c,bits))) ms.push(bits);
    models.push(ms);
  }
  const ans=new Map();
  for(const c of clauses) {
    let m=0;
    for(let i=0;i<16;i++) if(models[i].some(bits=>!sat(c,bits))) m|=1<<i;
    ans.set(key(c),m);
  }
  return ans;
}
const bits=n=>{let z=0;while(n){n&=n-1;z++;}return z};
const sortedUnique=xs=>[...new Set(xs)].sort();

function run() {
  const started=performance.now();
  const {clauses,opts}=buildClosure();
  const essential=deletionMasks(clauses);
  const memo=new Map(), stats={states:0,hits:0,parentOptions:0,partitionPrunes:0,essentialPrunes:0};

  function possible(src, targets0) {
    const targets=sortedUnique(targets0), mk=`${src}|${targets.join(";")}`;
    if(memo.has(mk)){stats.hits++;return memo.get(mk)}
    stats.states++;
    for(const t of targets) if((essential.get(t)&~src)!==0){stats.essentialPrunes++;memo.set(mk,false);return false}
    if(bits(src)===1){const i=31-Math.clz32(src);const ok=targets.every(t=>t===key(S[i]));memo.set(mk,ok);return ok}
    if(!targets.length){memo.set(mk,false);return false}
    for(let si=0;si<targets.length;si++) {
      const sink=targets[si]; if(sk.has(sink)) continue;
      const rest=targets.filter((_,i)=>i!==si);
      for(const op of opts.get(sink)||[]) {
        stats.parentOptions++;
        const lk=key(op.left),rk=key(op.right);
        const free=rest.filter(t=>t!==lk&&t!==rk);
        for(let assign=0;assign<(1<<free.length);assign++) {
          const lt=[lk],rt=[rk];
          free.forEach((t,j)=>(assign&(1<<j)?rt:lt).push(t));
          let ln=0,rn=0; for(const t of lt)ln|=essential.get(t);for(const t of rt)rn|=essential.get(t);
          if((ln&rn)!==0||((ln|rn)&~src)!==0){stats.partitionPrunes++;continue}
          const rem=src&~(ln|rn); let sub=rem;
          while(true){const lm=ln|sub,rm=src^lm;
            if(lm&&rm&&possible(lm,lt)&&possible(rm,rt)){memo.set(mk,true);return true}
            if(sub===0)break;sub=(sub-1)&rem;
          }
        }
      }
    }
    memo.set(mk,false);return false;
  }

  const im=[
    [2,3,5,7,10,11,13,14],
    [0,1,8,9,12],
    [0,1,2,3,4,6,8,9,10,11,12,15],
  ].map(a=>a.reduce((m,i)=>m|(1<<i),0));
  const controls=G.map((g,i)=>possible(im[i],[key(g)]));
  const one=children(S[0],S[1])[0].clause;controls.push(possible(3,[key(one)]));
  if(JSON.stringify(controls)!==JSON.stringify([true,true,true,true]))throw Error("positive controls");

  const branches=[];
  for(let gi=0;gi<G.length;gi++) for(const op of opts.get(key(G[gi]))||[]) {
    const targets=G.filter((_,i)=>i!==gi).map(key);
    if(!sk.has(key(op.left)))targets.push(key(op.left));
    if(!sk.has(key(op.right)))targets.push(key(op.right));
    branches.push({peeled_goal:gi,left:op.left,right:op.right,pivot:op.pivot,residual_tree_exists:possible(full,targets)});
  }
  if(branches.length!==20||branches.some(x=>x.residual_tree_exists))throw Error("16-node branch survived");
  const result={
    status:"PROVED_RESTRICTED_COMPUTATIONAL_INDEPENDENT_REPLAY",
    closure_clauses:clauses.length,
    goal_parent_counts:G.map(g=>(opts.get(key(g))||[]).length),
    positive_tree_controls:controls,
    branches, all_16_node_proofs_excluded:true,
    stats, memo_states:memo.size, seconds:(performance.now()-started)/1000,
    historical_checker_executed:false,
    p_vs_np:"OPEN",
  };
  const rendered=JSON.stringify(result,null,2)+"\n";
  fs.writeFileSync("experiments/review/raw/lspv5_440_unicyclic_residual_node.json",rendered);
  return result;
}

console.log(JSON.stringify(run(),null,2));
