// Independent finite checker for the ordinary-Resolution retraction lemma.
// Distinct implementation from the Python audit; not an R_mix341 checker.

const TOP = Symbol("TOP");
const key = c => c === TOP ? "TOP" : [...c].sort((a,b)=>a-b).join(",");
const canon = xs => {
  const s = new Set(xs);
  for (const x of s) if (s.has(-x)) return TOP;
  return s;
};
const subset = (a,b) => a !== TOP && b !== TOP && [...a].every(x=>b.has(x));
const resolve = (a,b,p) => {
  if (!a.has(p) || !b.has(-p)) throw new Error("bad pivot");
  return canon([...a].filter(x=>x!==p).concat([...b].filter(x=>x!==-p)));
};
const imageLit = (l,s) => {
  const t=s.get(Math.abs(l));
  if (t==="F" || t==="T") return l>0?t:(t==="F"?"T":"F");
  return l>0?t:-t;
};
const imageClause = (c,s) => {
  const out=[];
  for(const l of c){
    const q=imageLit(l,s);
    if(q==="T") return TOP;
    if(q!=="F") out.push(q);
  }
  return canon(out);
};
const subs = c => {
  const a=[...c], out=[];
  for(let m=0;m<(1<<a.length);m++) out.push(new Set(a.filter((_,i)=>m&(1<<i))));
  return out;
};
function translateStep(pa,pb,c,p,s){
  const ci=imageClause(c,s);
  if(ci===TOP) return {kind:"drop"};
  if(pa!==null && subset(pa,ci)) return {kind:"reuse",clause:pa};
  if(pb!==null && subset(pb,ci)) return {kind:"reuse",clause:pb};
  const q=imageLit(p,s);
  if(q==="F"||q==="T"||pa===null||pb===null||!pa.has(q)||!pb.has(-q))
    throw new Error("missing translated pivot");
  const r=resolve(pa,pb,q);
  if(r===TOP||!subset(r,ci)) throw new Error("bad translated resolvent");
  return {kind:"resolve",clause:r};
}

const clauses=[];
for(const a of [-1,0,1]) for(const b of [-1,0,1]){
  const c=[]; if(a)c.push(a); if(b)c.push(2*b); clauses.push(new Set(c));
}
const targets=["F","T",3,-3,4,-4];
let cases=0,dropped=0,resolved=0;
for(const a of clauses) for(const b of clauses) for(const p of [1,2]){
  if(!a.has(p)||!b.has(-p)) continue;
  const c=resolve(a,b,p); if(c===TOP) continue;
  for(const x of targets) for(const y of targets){
    const s=new Map([[1,x],[2,y]]);
    const ai=imageClause(a,s), bi=imageClause(b,s);
    const ar=ai===TOP?[null]:subs(ai), br=bi===TOP?[null]:subs(bi);
    for(const pa of ar) for(const pb of br){
      const z=translateStep(pa,pb,c,p,s); cases++;
      if(z.kind==="drop") dropped++; else resolved++;
    }
  }
}
if(cases!==1976||dropped!==104||resolved!==1872) throw new Error("count mismatch");

// Strict-3 gadget: all eight sign patterns retract exactly.
let gadgetChecks=0;
for(const a of [-1,1]) for(const b of [-1,1]) for(const c of [-1,1]){
  const C=new Set([a,2*b,3*c]), l=[a,2*b,3*c], u=4,v=5;
  const G=[new Set([l[0],l[1],u]),new Set([-u,l[2],v]),new Set([-u,l[2],-v])];
  const s=new Map([[1,1],[2,2],[3,3],[4,l[2]],[5,"F"]]);
  const imgs=G.map(q=>imageClause(q,s));
  if(key(imgs[0])!==key(C)||imgs[1]!==TOP||imgs[2]!==TOP) throw new Error("gadget");
  gadgetChecks+=3;
}

// Reversed source-containment direction is false as a nonexpansive criterion.
const F=[new Set([1,2]),new Set([-1]),new Set([-2])];
const H=[new Set([1]),new Set([-1]),new Set([-2])];
if(!subset(H[0],F[0]) || subset(F[0],H[0])) throw new Error("orientation control");
const hEmpty=resolve(H[0],H[1],1);
const y=resolve(F[0],F[1],1);
const fEmpty=resolve(y,F[2],2);
if(hEmpty.size!==0||fEmpty.size!==0) throw new Error("counterexample proof");

console.log(JSON.stringify({
  status:"PASS",
  theorem_scope:"ordinary shared-DAG Resolution only",
  one_step:{cases,dropped,translated:resolved},
  strict3_gadget_checks:gadgetChecks,
  wrong_orientation:{F_inferences:2,H_inferences:1},
  historical_R_mix341:false,
  P_vs_NP:"OPEN"
},null,2));
