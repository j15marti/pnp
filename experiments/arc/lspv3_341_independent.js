"use strict";
/* LSPV-3 341 independent no-import verifier.
   node experiments/arc/lspv3_341_independent.js full_raw.json */
const fs=require("fs"),assert=require("assert");
let checks=0,flips=0,nodes=0,corrupted=0,malformed=0;
function ck(v,m){checks++;assert.ok(v,m);}
function eq(a,b,m){checks++;assert.deepStrictEqual(a,b,m);}
function truth(clauses,a){return clauses.every(c=>c.some(l=>a[Math.abs(l)-1]===Number(l>0)));}
function pop(n){let q=0;while(n){n&=n-1;q++;}return q;}
function cut(mask,edges){return edges.filter(([u,v])=>Boolean(mask&(1<<u))!==Boolean(mask&(1<<v))).length;}
function connected(mask,h,edges){
 let seen=0;for(let v=0;v<h;v++)if(mask&(1<<v)){seen=1<<v;break;}
 if(!seen)return false;
 let changed=true;while(changed){changed=false;for(const [u,v] of edges){
  if(!(mask&(1<<u))||!(mask&(1<<v)))continue;
  if((seen&(1<<u))&&!(seen&(1<<v))){seen|=1<<v;changed=true;}
  if((seen&(1<<v))&&!(seen&(1<<u))){seen|=1<<u;changed=true;}
 }}return seen===mask;
}
function minimax(h,edges){
 const dp=Array(1<<h).fill(1e9),con=Array(1<<h).fill(false);
 for(let s=1;s<(1<<h);s++)con[s]=connected(s,h,edges);
 const order=Array.from({length:(1<<h)-1},(_,i)=>i+1).sort((a,b)=>pop(a)-pop(b));
 for(const mask of order){if(!con[mask])continue;
  if(pop(mask)===1){dp[mask]=cut(mask,edges);continue;}
  for(let a=(mask-1)&mask;a;a=(a-1)&mask){let b=mask^a;
    if((a&(mask&-mask))&&con[a]&&con[b])
      dp[mask]=Math.min(dp[mask],Math.max(cut(mask,edges),dp[a],dp[b]));
  }
 }return dp[(1<<h)-1];
}
function strictDIMACS(txt){
 const lines=txt.trim().split(/\r?\n/);
 ck(/^p cnf [1-9][0-9]* [1-9][0-9]*$/.test(lines[0]),"header");
 const hdr=lines[0].split(" "),n=+hdr[2],m=+hdr[3];
 ck(lines.length===m+1,"clause count");
 return lines.slice(1).map(line=>{
  ck(/^[-0-9 ]+$/.test(line),"literal chars");
  let a=line.trim().split(/\s+/).map(Number);
  ck(a.length>=2&&a[a.length-1]===0,"zero terminator");
  ck(a.slice(0,-1).every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=n),"literal range");
  return a.slice(0,-1);
 });
}
function verify(c){
 const h=c.vertices,t=c.selectors,e=c.edges,F=c.clauses;
 ck(e.length*2===3*h,"cubic");
 ck(c.nclauses===1+4*h*t&&F.length===c.nclauses,"source shape");
 ck(connected((1<<h)-1,h,e),"connected");
 for(let v=0;v<h;v++)ck(connected(((1<<h)-1)^(1<<v),h,e),"vertex-deletion connected");
 const dim="p cnf "+c.nvars+" "+F.length+"\n"+F.map(x=>x.join(" ")+" 0").join("\n")+"\n";
 eq(strictDIMACS(dim),F,"DIMACS round trip");
 ck(Buffer.byteLength(dim)*8===c.encoded_bits,"exact encoded bits");
 ck(F.reduce((s,x)=>s+x.length,0)===c.nsource_signs,"sign count");
 ck(c.sign_flip_witnesses.length===F.length,"deletion witnesses");
 for(let i=0;i<F.length;i++){const a=c.sign_flip_witnesses[i];
  ck(a.length===c.nvars,"witness width");
  for(let j=0;j<F.length;j++)if(j!==i)ck(truth([F[j]],a),"deleted source SAT");
  for(let k=0;k<F[i].length;k++){
   let G=F.map(x=>x.slice());G[i][k]*=-1;ck(truth(G,a),"sign-neighbor SAT");flips++;
  }
 }
 ck(truth(c.sat_control.clauses,c.sat_control.assignment),"even control SAT");
 const by={};F.forEach((clause,i)=>by["s"+i]={kind:"clause",clause});
 for(let index=0;index<c.certificate.length;index++){
  const x=c.certificate[index];
  ck(x.id==="p"+index,"proof DAG topological index");
  const ps=x.parents.map(id=>{ck(Object.hasOwn(by,id),"parent present");return by[id];});
  let res=null;
  if(x.rule==="guarded_xor3"){
   ck(ps.length===4&&x.vars.length===3,"four-parent XOR3");
   const seen=new Set();
   for(const p of ps){
    ck(p.kind==="clause"&&p.clause.length===4&&p.clause[0]===x.guard,"guard fixed");
    eq(p.clause.slice(1).map(Math.abs).sort((a,b)=>a-b),x.vars,"XOR3 support");
    let pat=0;for(let k=0;k<3;k++)if(p.clause.slice(1).find(l=>Math.abs(l)===x.vars[k])<0)pat|=1<<k;
    ck((pop(pat)&1)!==x.rhs,"wrong parity forbidden");
    seen.add(pat);
   }ck(seen.size===4,"four forbidden patterns");
   res={kind:"row",guard:x.guard,vars:x.vars,rhs:x.rhs};
  }else if(x.rule==="xor_add"){
   ck(ps.length===2&&ps.every(p=>p.kind==="row"),"row inputs");
   ck(ps[0].guard===ps[1].guard&&ps[0].guard===x.guard,"same guard");
   const set=new Set(ps[0].vars);
   for(const v of ps[1].vars){if(set.has(v))set.delete(v);else set.add(v);}
   eq([...set].sort((a,b)=>a-b),x.vars,"row support cancellation");
   ck((ps[0].rhs^ps[1].rhs)===x.rhs,"XOR right hand");
   res={kind:"row",guard:x.guard,vars:x.vars,rhs:x.rhs};
  }else if(x.rule==="guard_contradiction"){
   ck(ps.length===1&&ps[0].kind==="row","guard parent");
   ck(ps[0].vars.length===0&&ps[0].rhs===1,"0=1 row");
   eq(x.clause,[ps[0].guard],"guard output");
   res={kind:"clause",clause:x.clause};
  }else if(x.rule==="resolution"){
   ck(ps.length===2&&ps.every(p=>p.kind==="clause"),"resolution parents");
   ck(ps[0].clause.includes(x.pivot)&&ps[1].clause.includes(-x.pivot),"signed pivot");
   const cl=[...new Set(ps[0].clause.filter(l=>l!==x.pivot).concat(
      ps[1].clause.filter(l=>l!==-x.pivot)))].sort((a,b)=>a-b);
   eq([...new Set(x.clause)].sort((a,b)=>a-b),cl,"resolvent correctness");
   res={kind:"clause",clause:x.clause};
  }else throw Error("invalid rule "+x.rule);
  by[x.id]=res;nodes++;
 }
 eq(by["p"+(c.certificate.length-1)],{kind:"clause",clause:[]},"empty clause");
 ck(c.proof_nodes===t*(2*h+1),"upper certificate length");
 ck(c.source_fanin_lower===Math.ceil(4*h*t/3),"lower fan-in");
 const w=minimax(h,e);
 ck(c.dense_minimax_cut_width===w,"all-orders restricted width");
 ck(c.dense_minimax_peak_entries===2**(w-1),"allowed tuple count");
 return {graph:c.graph,selectors:t,source_clauses:F.length,proof_nodes:c.proof_nodes,width:w};
}
const file=process.argv[2]||"lspv3_341_raw.json";
const r=JSON.parse(fs.readFileSync(file,"utf8")),cases=r.cases.map(verify);
for(const c of r.cases){
 const copy=JSON.parse(JSON.stringify(c));copy.certificate[0].rhs^=1;
 assert.throws(()=>verify(copy),"corrupt proof rejected");corrupted++;
}
for(const s of ["p cnf 2 1\n1 0\n2 0\n","p cnf 2 1\n3 0\n",
 "p cnf 2 1\n0\n","p cnf x 1\n1 0\n","p cnf 2 1\n1 xx 0\n"]){
 assert.throws(()=>strictDIMACS(s),"malformed source rejected");malformed++;
}
console.log(JSON.stringify({status:"PASS",checks,sign_checks:flips,
 proof_node_visits:nodes,corrupt_rejected:corrupted,malformed_rejected:malformed,cases},null,2));
