"use strict";
/* ARC-PRIME-CHAIN-GUARD267. Node >=18. No external packages or randomness.
   Finite original 3CNF controls and instrumented UP-DPLL, NOT FLMV timings. */
const check=(v,s)=>{if(!v)throw Error(s||"failed")};
const uniq=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function chain(h){const x=i=>h+2+i,c=[[x(1),1,2]];
 for(let j=1;j<h-1;j++)c.push([-x(j),x(j+1),j+2]);
 c.push([-x(h-1),h+1,h+2]);return {name:"chain"+h+"_SAT",n:2*h+1,h,c};}
function unit3(l,u,v){return [[l,u,v],[l,u,-v],[l,-u,v],[l,-u,-v]]}
function pinned(h){const o=chain(h),c=o.c.map(z=>z.slice());let n=o.n;
 for(let i=1;i<=h+2;i++){const u=++n,v=++n;c.push(...unit3(-i,u,v));}
 return {name:"chain"+h+"_pinned_UNSAT",n,h,c};}
const eight=[[-1,-2,-3],[-1,-2,3],[-1,2,-3],[-1,2,3],[1,-2,-3],[1,-2,3],[1,2,-3],[1,2,3]];
function examples(){return [...[2,3,4,5].map(chain),pinned(2),pinned(3),
 {name:"H7_SAT",n:3,c:eight.slice(1)},{name:"H8_UNSAT",n:3,c:eight},
 {name:"XOR4_SAT",n:3,c:eight.filter(c=>c.filter(x=>x<0).length%2===0)},
 {name:"XOR8_UNSAT",n:3,c:eight},
 {name:"Horn_SAT",n:4,c:[[-1,-2,3],[-3,-4,2],[-2,-3,4]]},
 {name:"dualHorn_SAT",n:4,c:[[1,2,-3],[3,4,-2],[2,3,-4]]}]}
function counts(c,a){return c.map(row=>row.reduce((z,l)=>z+((a[Math.abs(l)]===1)===(l>0)?1:0),0))}
function sat(c,a){return counts(c,a).every(x=>x!==0)}
function res(c,d,p){check(c.includes(p)&&d.includes(-p),"bad resolution pivot");
 const r=uniq([...c.filter(x=>x!==p),...d.filter(x=>x!==-p)]);
 check(r.every(x=>!r.includes(-x)),"tautology");return r;}
function proof(o){const {h,c}=o,steps=[];let cur=c[0].slice();
 for(let i=1;i<h;i++){const p=h+2+i,next=res(cur,c[i],p);
  steps.push({kind:"chain",original_parent_index:i+1,pivot:p,left:cur.slice(),right:c[i].slice(),out:next.slice()});cur=next;}
 const R=Array.from({length:h+2},(_,i)=>i+1);check(eq(uniq(cur),R),"wrong projection");
 if(o.name.endsWith("pinned_UNSAT")){for(let i=1;i<=h+2;i++){
   const j=h+4*(i-1),q=c.slice(j,j+4),u=Math.abs(q[0][1]),v=Math.abs(q[0][2]);
   const p1=res(q[0],q[1],v),p2=res(q[2],q[3],v),p3=res(p1,p2,u);
   check(eq(p3,[-i]),"gadget unit");
   steps.push({kind:"gadget",source_indices:[j+1,j+2,j+3,j+4],pivot1:v,pivot2:u,derived:[p1,p2,p3]});
   cur=res(cur,p3,i);steps.push({kind:"refutation",pivot:i,out:cur.slice()});
 }check(cur.length===0,"no empty clause");}
 return {R,steps,empty:o.name.endsWith("pinned_UNSAT")};}
function project(h){const o=chain(h);let checked=0;
 for(let am=0;am<(1<<(h+2));am++){let exists=false;
  for(let xm=0;xm<(1<<(h-1));xm++){const a=Array(o.n+1).fill(0);
   for(let j=1;j<=h+2;j++)a[j]=(am>>(j-1))&1;
   for(let j=1;j<h;j++)a[h+2+j]=(xm>>(j-1))&1;
   if(sat(o.c,a))exists=true;checked++;
  }check(exists===(am!==0),"projection error");}
 for(let k=0;k<h;k++){let found=false;
  for(let xm=0;xm<(1<<(h-1));xm++){const a=Array(o.n+1).fill(0);
   for(let j=1;j<h;j++)a[h+2+j]=(xm>>(j-1))&1;
   if(sat(o.c.filter((_,i)=>i!==k),a))found=true;
  }check(found,"original leaf not indispensable");}
 return {h,source_clauses:h,prime_implicate_width:h+2,pointwise_checks:checked,indispensable_source_leaves:h};}
function extreme(o){const indexed=[],compat=[];let modes=0;
 o.c.forEach((c,i)=>indexed.push({clause_index:i+1,source:c,occ:c.map(l=>({literal:l,S:l>0?1:0,inverted_S:l>0?0:1,U:l>0?0:1,inverted_U:l>0?1:0}))}));
 for(let i=0;i<o.c.length;i++)for(let j=i+1;j<o.c.length;j++){
  const row={i:i+1,j:j+1,SS:false,SU:false,US:false,UU:false};
  for(const A of ["S","U"])for(const B of ["S","U"]){
   const req=new Map();let valid=true;
   for(const [idx,mode] of [[i,A],[j,B]])for(const l of o.c[idx]){
    const k=Math.abs(l),v=mode==="S"?(l>0?1:0):(l>0?0:1);
    if(req.has(k)&&req.get(k)!==v)valid=false;req.set(k,v);
   }row[A+B]=valid;modes++;
   const vs=[...new Set([...o.c[i],...o.c[j]].map(Math.abs))];let found=false;
   for(let mask=0;mask<(1<<vs.length);mask++){
    const a=Array(o.n+1).fill(0);vs.forEach((v,k)=>a[v]=(mask>>k)&1);
    const t=counts([o.c[i],o.c[j]],a);
    if(t[0]===(A==="S"?3:0)&&t[1]===(B==="S"?3:0))found=true;
   }check(valid===found,"extreme compatibility failed");
  }compat.push(row);}
 const z=Array(o.n+1).fill(0),w=Array(o.n+1).fill(1);
 const t0=counts(o.c,z),t1=counts(o.c,w);
 check(t0.every((x,i)=>t1[i]===3-x),"endpoint complement failure");
 const flips=[];let a=z.slice();
 for(let t=0;t<=Math.min(o.n,8);t++){if(t)a[t]^=1;
  const tt=counts(o.c,a),hist=[0,0,0,0];for(const x of tt)hist[x]++;
  flips.push({step:t,flipped_variable:t||null,truth_counts:tt,histogram:hist,assignment_sat:hist[0]===0});}
 return {indexed,compat,coherent_zero:{truth_counts:t0,sat:t0.every(x=>x>0)},
 coherent_one:{truth_counts:t1,sat:t1.every(x=>x>0)},flips,modes};}
function dpll(c,n){const stat={nodes:0,branches:0,clause_reads:0,literal_reads:0,unit_writes:0};
 function go(aa){stat.nodes++;const a=aa.slice();
  while(true){let changed=false;
   for(const row of c){stat.clause_reads++;let ok=false,empty=0,un=0;
    for(const l of row){stat.literal_reads++;const v=a[Math.abs(l)];
     if(v<0){empty++;un=l;}else if((v===1)===(l>0)){ok=true;break;}
    }if(ok)continue;if(!empty)return {yes:false};
    if(empty===1){const idx=Math.abs(un),value=un>0?1:0;
     if(a[idx]>=0&&a[idx]!==value)return {yes:false};
     if(a[idx]<0){a[idx]=value;changed=true;stat.unit_writes++;}
    }
   }if(!changed)break;
  }
  let k=0;for(let i=1;i<=n;i++)if(a[i]<0){k=i;break;}
  if(!k){check(sat(c,a),"incorrect full witness");return {yes:true,witness:a.slice(1)};}
  stat.branches++;for(let v of [0,1]){const b=a.slice();b[k]=v;
    const r=go(b);if(r.yes)return r;}
  return {yes:false};
 }
 return {...go(Array(n+1).fill(-1)),stat};}
function oracle(o){if(o.n>17)return null;let models=0;
 for(let mask=0;mask<(1<<o.n);mask++){const a=Array(o.n+1).fill(0);
  for(let i=1;i<=o.n;i++)a[i]=(mask>>(i-1))&1;
  if(sat(o.c,a))models++;
 }return models;}
function augment(o){let trials=0,reads=0,P=null;
 for(let h=2;h<=5;h++){trials++;const expected=chain(h).c;
  if(o.c.length<h)continue;
  let good=true;for(let i=0;i<h;i++){reads+=o.c[i].length+expected[i].length;
    if(!eq(o.c[i],expected[i])){good=false;break;}}
  if(good){P=proof({...o,h});break;}
 }
 const run=dpll(P?[...o.c,P.R]:o.c,o.n);if(run.yes)check(sat(o.c,[-1,...run.witness]),"bad original witness");
 const proofReads=P?6*o.h+2*(o.h-1)+(o.h+2):0;
 return {result:run,attempts:trials,authentication_reads:reads,proof_reads:proofReads,proof:P};
}
function main(){const rows=[];let modes=0;
 for(const o of examples()){const base=dpll(o.c,o.n),aug=augment(o),oracle_models=oracle(o);
  check(base.yes===aug.result.yes,"solver polarity mismatch");
  if(oracle_models!==null)check(base.yes===(oracle_models>0),"oracle polarity mismatch");
  const adversarial=extreme(o);modes+=adversarial.modes;
  const charge=x=>x.literal_reads+x.clause_reads+x.nodes+x.unit_writes;
  rows.push({name:o.name,n:o.n,m:o.c.length,label:base.yes?"SAT":"UNSAT",
    oracle_models,original_clauses:o.c,baseline:{...base.stat,selected_work:charge(base.stat)},
    adaptive:{...aug.result.stat,selected_work:charge(aug.result.stat)+aug.authentication_reads+aug.proof_reads,
    trials:aug.attempts,authentication_reads:aug.authentication_reads,proof_reads:aug.proof_reads,proof:aug.proof},
    adversarial});}
 const sum=f=>rows.reduce((s,x)=>s+f(x),0);
 return {tag:"ARC-PRIME-CHAIN-GUARD267",date:"2026-10-31 01:58 PDT",seed:null,
  scope:"restricted prime chain projection, not arbitrary SAT hardness or FLMV machine time",
  projection:[2,3,4,5,6].map(project),rows,
  totals:{formulas:rows.length,SAT:sum(x=>x.label==="SAT"?1:0),UNSAT:sum(x=>x.label==="UNSAT"?1:0),
   extreme_modes_checked:modes,baseline_nodes:sum(x=>x.baseline.nodes),
   augmented_nodes:sum(x=>x.adaptive.nodes),
   baseline_work:sum(x=>x.baseline.selected_work),augmented_work:sum(x=>x.adaptive.selected_work)},
  arbitrary_A_to_Phi_A:"OPEN",p_vs_np:"OPEN"};}
if(require.main===module)console.log(JSON.stringify(main(),null,2));
module.exports={main,chain,pinned,proof,resolve:res};