"use strict";
// LSPV-2 SUPPORT-PROFILE-TRANSFER366, finite local semantic-to-Resolution compiler.
// Zero-charge originals; each weakening and binary resolution in this
// temporary proof is counted; the independent subclause erasure then
// yields a strict Resolution proof of no greater cost.
function valid(n,F) {
 if(!Number.isInteger(n)||n<0||n>6||!Array.isArray(F)) return false;
 return F.every(c=>Array.isArray(c)&&c.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=n)
  &&new Set(c).size===c.length&&!c.some(x=>c.includes(-x)));
}
function val(C,m) {return C.some(x=>((m>>(Math.abs(x)-1))&1)===(x>0?1:0));}
function blocker(mask,n) {return Array.from({length:n},(_,i)=>((mask>>i)&1)?-(i+1):(i+1));}
function same(A,B) {return A.length===B.length&&A.every(x=>B.includes(x));}
function resolvent(A,B,p) {
 if(!A.includes(p)||!B.includes(-p)) return null;
 const C=[...new Set([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)])];
 if(C.some(x=>C.includes(-x))) throw Error("tautological resolvent");
 return C;
}
function compile(F,goal,n) {
 if(!valid(n,F)||!valid(n,[goal])) throw Error("malformed input");
 for(let m=0;m<2**n;m++)
  if(F.every(c=>val(c,m))&&!val(goal,m)) throw Error("not entailed");
 const rows=F.map((c,i)=>({op:"src",clause:c,source:i}));
 const free=Array.from({length:n},(_,i)=>i+1).filter(v=>!goal.some(x=>Math.abs(x)===v));
 let fixed=0;
 for(const l of goal) if(l<0) fixed|=1<<(Math.abs(l)-1);
 function visit(k,mask) {
  if(k===free.length) {
   const j=F.findIndex(c=>!val(c,mask));if(j<0) throw Error("soundness failure");
   const at=rows.length;
   rows.push({op:"weaken",parents:[j],clause:blocker(mask,n)});
   return at;
  }
  const v=free[k],a=visit(k+1,mask&~(1<<(v-1))),b=visit(k+1,mask|(1<<(v-1)));
  const at=rows.length;
  rows.push({op:"res",parents:[a,b],pivot:v,clause:resolvent(rows[a].clause,rows[b].clause,v)});
  return at;
 }
 const root=visit(0,fixed);
 if(!same(rows[root].clause,goal)) throw Error("goal mismatch");
 return {rows,root};
}
function independentCheckAndErase(F,pr,n,goal) {
 const reps=[],strict=F.map((c,i)=>({op:"src",clause:c,source:i}));
 let weaken=0,resolve=0,checks=0;
 for(let i=0;i<pr.rows.length;i++) {
  const r=pr.rows[i];
  if(!valid(n,[r.clause])) throw Error("invalid clause");
  if(r.op==="src") {
   if(!Number.isInteger(r.source)||r.source<0||r.source>=F.length||!same(r.clause,F[r.source]))
    throw Error("invalid source");
   reps[i]=r.source;
  } else if(r.op==="weaken") {
   const p=r.parents?.[0];
   if(!Number.isInteger(p)||p<0||p>=i||!pr.rows[p].clause.every(x=>r.clause.includes(x)))
    throw Error("illegal weakening");
   reps[i]=reps[p];weaken++;
  } else if(r.op==="res") {
   const [a,b]=r.parents||[],p=r.pivot;
   if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=i||b>=i||
     !same(resolvent(pr.rows[a].clause,pr.rows[b].clause,p)||[],r.clause))
    throw Error("illegal resolution");
   resolve++;
   const A=strict[reps[a]].clause,B=strict[reps[b]].clause;
   if(A.includes(p)&&B.includes(-p)) {
    const C=resolvent(A,B,p);
    reps[i]=strict.length;
    strict.push({op:"res",parents:[reps[a],reps[b]],pivot:p,clause:C});
   } else if(!A.includes(p)) reps[i]=reps[a];
   else reps[i]=reps[b];
  } else throw Error("unknown operation");
  checks++;
 }
 if(!same(pr.rows[pr.root].clause,goal)) throw Error("wrong result");
 const strong=strict[reps[pr.root]].clause;
 if(!strong.every(x=>goal.includes(x))) throw Error("erasure is unsound");
 return {weaken,resolve,strictRes:strict.length-F.length,checks,strictGoal:strong};
}
function run() {
 const n=3,F=[[1,2],[-1,3],[-2,3]],candidates=[];
 for(let k=0;k<3**n;k++) {let t=k,c=[];for(let v=1;v<=n;v++){let digit=t%3;t=Math.floor(t/3);if(digit)c.push(digit===1?v:-v);}candidates.push(c);}
 let count=0,rows=0,maxPaid=0,strict=0;
 for(const C of candidates){
  if(Array.from({length:2**n},(_,m)=>m).some(m=>F.every(c=>val(c,m))&&!val(C,m)))continue;
  const p=compile(F,C,n),check=independentCheckAndErase(F,p,n,C);
  const paid=check.weaken+check.resolve;
  if(paid>2**(n+1)||check.strictRes>check.resolve)throw Error("bound exceeded");
  count++; rows+=p.rows.length;maxPaid=Math.max(maxPaid,paid);strict+=check.strictRes;
 }
 const odd=[[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3],
            [-1,-2,-3],[-1,2,3],[1,-2,3],[1,2,-3]];
 const p=compile(odd,[],3),test=independentCheckAndErase(odd,p,3,[]);
 if(test.strictRes!==7||test.resolve!==7||test.weaken!==8)throw Error("odd parity");
 let rejected=0;
 for(const f of [
  ()=>compile(F,[99],3),
  ()=>compile(F,[3,-3],3),
  ()=>compile(F,[-3],3),
  ()=>compile(odd.slice(0,4),[],3),
  ()=>independentCheckAndErase(odd,{rows:p.rows.map((x,i)=>i===p.root?{...x,pivot:2}:x),root:p.root},3,[])
 ]){try{f();}catch(e){rejected++;}}
 if(rejected!==5)throw Error("bad negative controls");
 return {run:"SUPPORT_PROFILE_TRANSFER366",scope:"finite local compiler and subclause-erasure checks",
  n,source:F,entailed_clauses_checked:count,proof_rows_verified:rows,
  max_paid_per_local_clause:maxPaid,total_strict_resolution_nodes_across_cases:strict,
  odd_parity:{sources:odd.length,weakening_nodes:test.weaken,resolution_nodes:test.resolve,strict_nodes:test.strictRes},
  hostile_rejections:rejected,bounds:"each local implication <=2^(d+1) paid temporary steps",
  note:"not a global mixed optimum, not a B1/B2/B3 result"};
}
if(typeof module!=="undefined" && require.main===module){console.log(JSON.stringify(run(),null,2));}
