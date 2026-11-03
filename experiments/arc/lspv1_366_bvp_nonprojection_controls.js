#!/usr/bin/env node
'use strict';
const run = function run() {
  const sizes=[1,2,3,4,8,16,32,64];
  let checks=0;
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  const clauseOk=c=>Array.isArray(c)&&c.every(v=>Number.isInteger(v)&&v!==0)&&new Set(c).size===c.length&&c.every(v=>!c.includes(-v));
  const val=(c,a)=>c.some(l=>(l>0?!!a[Math.abs(l)]:!a[Math.abs(l)]));
  const res=(a,b,p)=>{
    if(!a.includes(p)||!b.includes(-p))throw Error("invalid pivot");
    const c=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
    if(!clauseOk(c))throw Error("tautological resolvent");return c;
  };
  const make=n=>{
    let source=[[n+1],[-(2*n+1)]], cells=[];
    for(let i=1;i<=n;i++){
      const x=i,c=n+i,d=n+i+1;
      const A=source.push([x,-c])-1;
      source.push([-x,c],[-d,x],[-d,c]);
      const K=source.push([-x,-c,d])-1;cells.push({A,K,x,c,d});
    }
    let proof=[], prev=0;
    const add=(left,right,p)=>{const cl=res(left<source.length?source[left]:proof[left-source.length].clause,right<source.length?source[right]:proof[right-source.length].clause,p);proof.push({left,right,pivot:p,clause:cl});return source.length+proof.length-1;};
    for(const t of cells){const imp=add(t.A,t.K,t.x);prev=add(imp,prev,-t.c);}
    add(prev,1,2*n+1);
    const dimacs=`p cnf ${2*n+1} ${source.length}\n`+source.map(c=>c.join(" ")+" 0").join("\n")+"\n";
    return {source,proof,cells,dimacs};
  };
  const sizesOut=[];
  for(const n of sizes){
    const {source,proof,cells,dimacs}=make(n); checks+=2;
    if(source.length!==5*n+2 ||proof.length!==2*n+1)throw Error("size mismatch");
    const nodes=source.slice();
    for(const step of proof){
      if(step.left>=nodes.length||step.right>=nodes.length)throw Error("forward ref");
      const computed=res(nodes[step.left],nodes[step.right],step.pivot);
      if(!eq(computed,step.clause))throw Error("incorrect conclusion");
      nodes.push(step.clause);checks+=3;
    }
    if(!eq(nodes[nodes.length-1],[]))throw Error("not contradiction");checks++;
    let witnesses=0;
    const chk=(assignment,ignore)=>{
      for(let j=0;j<source.length;j++)if(j!==ignore&&!val(source[j],assignment))return false;
      return true;
    };
    const zeros={};const ones={};for(let i=1;i<=2*n+1;i++){zeros[i]=false;ones[i]=true;}
    if(!chk(zeros,0)||!chk(ones,1))throw Error("boundary witness");checks+=2;witnesses+=2;
    for(let i=1;i<=n;i++){
      const makeAssign=xAt=>{
        const a={};
        for(let j=1;j<=n;j++)a[j]=j<i?true:j===i?xAt:false;
        for(let j=1;j<=n+1;j++)a[n+j]=j<=i;
        return a;
      };
      if(!chk(makeAssign(false),cells[i-1].A)||!chk(makeAssign(true),cells[i-1].K))throw Error("essentiality failed");
      witnesses+=2;checks+=2;
    }
    const badProof=proof.map(x=>({...x}));badProof[0].pivot=-badProof[0].pivot;
    let rejected=false;try{res(source[badProof[0].left],source[badProof[0].right],badProof[0].pivot);}catch(e){rejected=true;}
    if(!rejected)throw Error("bad pivot accepted");checks++;
    if(clauseOk([0])||clauseOk([1,1])||clauseOk([1,-1]))throw Error("malformed accepted");checks+=3;
    sizesOut.push({n,clauses:source.length,variables:2*n+1,proof_nodes:proof.length,indispensable_sources:witnesses,dimacs_bytes:dimacs.length,signed_pivot_checks:proof.length,corrupt_pivot_rejected:rejected});
  }
  const parity=(odd)=>{
    const es=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
    let models=0;
    for(let mask=0;mask<64;mask++){let v=[0,0,0,0];for(let j=0;j<6;j++)if(mask&(1<<j)){v[es[j][0]]^=1;v[es[j][1]]^=1;}
      if(v.every((b,k)=>b===(k===0&&odd?1:0)))models++;
    }
    return models;
  };
  const odd=parity(true),even=parity(false);if(odd!==0||even!==8)throw Error("K4 label mismatch");checks+=128;
  return {title:"LSPV1 BVP bitblast transfer firewall 366",timestamp_pst:"2026-11-03 09:03 PST",status:"COMPUTATIONAL signed source and proof controls; analytic no-backtranslation theorem relies on Alekseev 2026",checks,odd_K4_models:odd,even_K4_models:even,cases:sizesOut,limits:"Only strict Resolution proof certificates and restricted controls. Alekseev external theorem not computationally re-proved. Proof acquisition not measured. No mixed hard-family or B3 claim."};
};
console.log(JSON.stringify(run(), null, 2));
