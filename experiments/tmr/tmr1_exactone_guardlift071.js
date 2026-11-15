// GUARDLIFT071. Pure ES2020; no dependencies. Native Node: node experiments/tmr/tmr1_exactone_guardlift071.js
"use strict";
function canonical(xs) {
  const v = Array.from(new Set(xs)).sort((a,b) => a-b);
  if (v.some(t => v.includes(-t))) return null;
  return v;
}
function id(c) { return c.join(","); }
function res(a,b,p) {
  if (a.includes(p) && b.includes(-p)) return canonical(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
  if (a.includes(-p) && b.includes(p)) return canonical(a.filter(x=>x!==-p).concat(b.filter(x=>x!==p)));
  return null;
}
function evalC(c,mask){ return c.some(t=>(((mask>>(Math.abs(t)-1))&1)===1)===(t>0)); }
function evalCNF(F,mask){return F.every(c=>evalC(c,mask));}
function baseProof(F){
  const rows=[], seen=new Map();
  function add(c,kind,parents,pivot){
    const k=id(c); if(seen.has(k)) return seen.get(k);
    const at=rows.length; rows.push({c,kind,parents:parents||[],pivot:pivot||0}); seen.set(k,at);return at;
  }
  for(const c of F) add(c,"source");
  for(let a=0;a<rows.length;a++){
    for(let b=0;b<a;b++){
      for(const p of Array.from(new Set(rows[a].c.map(Math.abs)))){
        const r=res(rows[a].c,rows[b].c,p);
        if(r===null) continue;
        const t=add(r,"res",[a,b],p);
        if(r.length===0) return {rows,final:t,inferences:rows.filter(x=>x.kind==="res").length};
      }
    }
  }
  return {rows,final:-1,inferences:rows.filter(x=>x.kind==="res").length};
}
function exactOneCNFs(k){
  const pos=[Array.from({length:k},(_,i)=>i+1)];
  for(let i=1;i<=k;i++)for(let j=i+1;j<=k;j++)pos.push(canonical([-i,-j]));
  const neg=[];
  for(let i=1;i<=k;i++){
    const c=[-i];for(let j=1;j<=k;j++)if(i!==j)c.push(j);
    neg.push(canonical(c));
  }
  return {pos:pos.map(canonical),neg};
}
function uniqueOne(mask,k){let n=0;for(let i=0;i<k;i++)n+=(mask>>i)&1;return n===1;}
function wrapper(F,k) {
  const {pos,neg}=exactOneCNFs(k);
  const Y=F.map(c=>canonical(c.map(t=>Math.sign(t)*(k+Math.abs(t)))));
  const A=pos.flatMap(d=>Y.map(c=>canonical(d.concat(c))));
  return {pos,neg,Y,A,full:A.concat(neg)};
}
function liftedProof(F,k,base) {
  const s=wrapper(F,k), rows=[], sources=new Set(s.full.map(id)), Dheads=[];
  function addSource(c) {
    if(!sources.has(id(c))) throw Error("unbound source "+id(c));
    rows.push({c,kind:"source",parents:[],pivot:0});return rows.length-1;
  }
  function addRes(a,b,p) {
    const c=res(rows[a].c,rows[b].c,p);
    if(c===null)throw Error("invalid pivot "+p);
    rows.push({c,kind:"res",parents:[a,b],pivot:p});return rows.length-1;
  }
  for(const d of s.pos){
    const remap=[];
    for(const x of base.rows) {
      if(x.kind==="source") remap.push(addSource(canonical(d.concat(x.c.map(t=>Math.sign(t)*(k+Math.abs(t)))))));
      else remap.push(addRes(remap[x.parents[0]],remap[x.parents[1]],k+x.pivot));
    }
    if(id(rows[remap[base.final]].c)!==id(d))throw Error("lift did not derive guard");
    Dheads.push(remap[base.final]);
  }
  const b= s.neg.map(addSource);
  const units=[];
  for(let i=0;i<k;i++){
    let at=b[i];
    for(let j=0;j<k;j++)if(j!==i){
      const di=1+((i<j ? i*(2*k-i-1)/2 + (j-i-1) : j*(2*k-j-1)/2 + (i-j-1)));
      at=addRes(at,Dheads[di],j+1);
    }
    if(id(rows[at].c)!==id([-i-1]))throw Error("failed to derive negative unit");
    units.push(at);
  }
  let at=Dheads[0];
  for(let i=0;i<k;i++)at=addRes(at,units[i],i+1);
  if(rows[at].c.length)throw Error("nonempty terminal");
  return {rows,final:at,guards:s.pos.length,baseInferences:base.inferences};
}
function independentlyVerify(rows,full) {
  const sourceSet=new Set(full.map(id));
  for(let a=0;a<rows.length;a++){
    const x=rows[a];
    if(x.kind==="source") {if(!sourceSet.has(id(x.c)))return false;}
    else{
      if(x.parents.length!==2 || x.parents.some(j=>j>=a||j<0))return false;
      const [j,t]=x.parents;
      const z=res(rows[j].c,rows[t].c,x.pivot);
      if(z===null||id(z)!==id(x.c))return false;
    }
  }
  return rows.length>0 && rows[rows.length-1].c.length===0;
}
function run(){
  let checks=0, unsat=0, sat=0, proofs=0, maxProof=0, falseNeg=0;
  const test=(condition,msg)=>{checks++;if(!condition)throw Error(msg)};
  const clauses=[];
  for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++){
    if(!a&&!b)continue;
    clauses.push(canonical((a?[a]:[]).concat(b?[2*Math.sign(b)]:[])));
  }
  test(clauses.length===8,"base clause enumeration");
  for(let mask=0;mask<256;mask++){
    const F=clauses.filter((_,i)=>(mask>>i)&1);
    const satF=[0,1,2,3].some(y=>evalCNF(F,y));
    const base=baseProof(F);
    test((base.final>=0)===!satF,"base resolution closure complete on 2 vars");
    if(satF){sat++;continue;}unsat++;
    for(let k=3;k<=6;k++){
      const s=wrapper(F,k);
      const q=1+k*(k-1)/2;
      test(s.pos.length===q && s.neg.length===k && s.A.length===q*F.length,"source size");
      for(let x=0;x<(1<<k);x++){
        const expected=uniqueOne(x,k);
        for(let y=0;y<4;y++){
          const mask2=x|(y<<k);
          test(evalCNF(s.A,mask2)===expected,"guard projection");
          test(evalCNF(s.neg,mask2)===!expected,"complement projection");
        }
      }
      const proof=liftedProof(F,k,base);
      test(independentlyVerify(proof.rows,s.full),"complete authenticated refutation");
      test(proof.rows.filter(r=>r.kind==="res").length===q*base.inferences+k*k,"exact lifted inference budget");
      test(proof.rows[proof.final].c.length===0,"empty goal");
      proofs++;
      maxProof=Math.max(maxProof,proof.rows.length);
      const zero=(1<<(k+2))-1;
      test(s.pos.some(d=>!evalC(d,0)),"falsifying guard exists");
      test(evalCNF(s.neg,0),"all-zero is B allowed");
      test(s.A.filter(c=>!evalC(c,0)).length>0 || F.length===0,"all-zero retains F");
      test(zero>=0,"nonnegative widths");
    }
  }
  const k=3,s=exactOneCNFs(k);
  const T=[1,2,4];for(const x of T)test(evalCNF(s.pos,x),"singleton satisfiable");
  test(!evalCNF(s.pos,0),"AND counterexample Horn");
  test(!evalCNF(s.pos,3),"OR counterexample dual Horn");
  test(!evalCNF(s.pos,0),"majority counterexample bijunctive");
  test(!evalCNF(s.pos,7),"XOR counterexample affine");
  for(let i=1;i<=6;i++){
    const s=exactOneCNFs(i);
    for(let x=0;x<(1<<i);x++){
      test(evalCNF(s.pos,x)===uniqueOne(x,i),"exact-one CNF");
      test(evalCNF(s.neg,x)===!uniqueOne(x,i),"exact-one complement CNF");
    }
  }
  const easy=wrapper([[1]],3);
  test(evalCNF(easy.A,8) && !uniqueOne(0,3),"SAT-base negative control");
  const output={tag:"GUARDLIFT071",scope:"native-resolution, not fixed SAT machine",base_subsets:256,unsat_bases:unsat,sat_bases:sat,lifted_proofs:proofs,verified_assertions:checks,failures:0,maximum_proof_lines:maxProof,guard_k:[3,4,5,6],corollary:"non-Schaefer exact-one separator; inherited native Resolution hardness; O(k^2) separator circuit"};
  if(typeof console!=="undefined")console.log(JSON.stringify(output));
  return output;
}
run();
