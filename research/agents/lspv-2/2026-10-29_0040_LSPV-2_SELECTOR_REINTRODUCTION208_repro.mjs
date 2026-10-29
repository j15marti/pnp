"use strict";
/* SELECTOR-REINTRODUCTION208: standalone JS/V8/Node audit, no dependencies.
   PROVED/EXACT restricted algebra is in accompanying .tex; this is finite.
   Run: node 2026-10-29_0040_LSPV-2_SELECTOR_REINTRODUCTION208_repro.mjs
*/
function audit() {
  const check=(v,msg)=>{if(!v)throw Error(msg);};
  const W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
    [5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
    [-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],
    [2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
  const Q=W1.filter((_,i)=>i!==7);
  const AB=t=>({A:Array.from({length:t},(_,i)=>[4*i+1,4*i+2]),
                B:Array.from({length:t},(_,i)=>[4*i+3,4*i+4])});
  const orig=t=>{const {A,B}=AB(t),z=4*t+1;return [...A.map(a=>[z,...a]),...B.map(b=>[-z,...b])];};
  const four=t=>{const {A,B}=AB(t);return A.flatMap(a=>B.map(b=>[...a,...b]));};
  const chain=t=>four(t).flatMap((c,i)=>[[c[0],c[1],4*t+1+i],[-(4*t+1+i),c[2],c[3]]]);
  function circuit(t) {
    const {A,B}=AB(t); const gates=[];const add=(op,x,y)=>{let v=4*t+1+gates.length;gates.push({v,op,x,y});return v;};
    let a=A.map(x=>add("OR",...x)), b=B.map(x=>add("OR",...x));
    while(a.length>1)a=[add("AND",a[0],a[1]),...a.slice(2)];
    while(b.length>1)b=[add("AND",b[0],b[1]),...b.slice(2)];
    const root=add("OR",a[0],b[0]);
    check(gates.length===4*t-1,"gate count");
    return {gates,root};
  }
  function tseitin(t) {
    const {gates,root}=circuit(t);
    const clauses=[];
    for(const {v,op,x,y} of gates) if(op==="OR")clauses.push([v,-x],[v,-y],[-v,x,y]);
                                else clauses.push([-v,x],[-v,y],[v,-x,-y]);
    clauses.push([root]);
    return {clauses,gates,root};
  }
  const bit=(mask,id)=>!!(mask&(1<<(id-1)));
  const lit=(l,mask,values)=>{const b=values&&values.has(Math.abs(l))?values.get(Math.abs(l)):bit(mask,Math.abs(l));return l>0?b:!b;};
  const sat=(cs,mask,values)=>cs.every(c=>c.some(l=>lit(l,mask,values)));
  const projected=(t,mask)=>{const {A,B}=AB(t);return A.every(c=>c.some(x=>bit(mask,x)))||B.every(c=>c.some(x=>bit(mask,x)));};
  function gateValues(gates,mask) {
    const v=new Map();
    for(const g of gates){const x=lit(g.x,mask,v),y=lit(g.y,mask,v);v.set(g.v,g.op==="OR"?(x||y):(x&&y));}
    return v;
  }
  let checks=0,yesCounts=[],gateChecks=0,per=[];
  for(let t=1;t<=4;t++){
    const F=orig(t),G=four(t),H=chain(t),C=tseitin(t),z=4*t+1;let yes=0;
    for(let mask=0;mask<(1<<(4*t));mask++){
      const p=projected(t,mask),byPivot=sat(F,mask)||sat(F,mask|(1<<(z-1)));
      const vals=gateValues(C.gates,mask);
      const extra=new Map(four(t).map((c,i)=>[4*t+1+i,!c.slice(0,2).some(v=>bit(mask,v))]));
      check(p===byPivot&&p===sat(G,mask)&&p===vals.get(C.root)&&p===sat(C.clauses,mask,vals)&&p===sat(H,mask,extra),
            "projection mismatch t="+t+" mask="+mask);
      yes+=+p;checks++;gateChecks+=C.gates.length;
    }
    yesCounts.push(yes);
    per.push({t,assignments:1<<(4*t),YES:yes,gates:C.gates.length,
      original_clauses:F.length,resolvents:G.length,chain_clauses:H.length,tseitin_clauses:C.clauses.length});
  }
  check(checks===69904&&yesCounts.join()==="15,207,2727,34911","projection baseline");
  let shortChecks=0;
  for(let t=1;t<=7;t++){
    const n=4*t;
    function one(vs) {
      for(let signs=0;signs<(1<<vs.length);signs++){
        const c=vs.map((v,j)=>(signs&(1<<j))?v:-v);
        let mask=(1<<n)-1;
        for(let l of c)if(l>0)mask&=~(1<<(l-1));
        check(!sat([c],mask)&&projected(t,mask),"short implicate found");
        shortChecks++;
      }
    }
    for(let i=1;i<=n;i++)one([i]);
    for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)one([i,j]);
    for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)for(let k=j+1;k<=n;k++)one([i,j,k]);
  }
  check(shortChecks===62720,"short-clause count");
  let w1=0,q=0;
  for(let mask=0;mask<(1<<15);mask++){w1+=+sat(W1,mask);q+=+sat(Q,mask);}
  check(w1===0&&q===244,"W1/Q fingerprints");
  const serialize=cs=>{
    const n=Math.max(0,...cs.flat().map(Math.abs));
    return "p cnf "+n+" "+cs.length+"\n"+cs.map(c=>c.join(" ")+" 0\n").join("");
  };
  const binaryLength=cs=>{
    const n=Math.max(0,...cs.flat().map(Math.abs));
    const w=Math.floor(Math.log2(Math.max(1,n,cs.length)))+1;
    return (w+1)+2*w+cs.reduce((sum,c)=>sum+(c.length+1)+c.length*(w+1),0);
  };
  const sizeCases=[];
  for(let t of [1,2,3,4,8,16,32,64,128]){
    const a=orig(t),b=orig(t),r=four(t),c=chain(t),d=tseitin(t).clauses;
    check(serialize(a)===serialize(b),"selector cycle");
    check(d.length===12*t-2&&d.flat().length===28*t-6,"Tseitin accounting");
    check(r.length===t*t&&c.length===2*t*t,"resolution accounting");
    const chars=[a,b,d,r,c].map(x=>serialize(x).length);
    const bins=[a,b,d,r,c].map(binaryLength);
    check(chars[2]>chars[0]&&bins[2]>bins[0],"Tseitin expansion");
    sizeCases.push({t,ASCII_bytes:{parent:chars[0],reselector:chars[1],tseitin:chars[2],resolution4:chars[3],chain3:chars[4]},
      binary_bits:{parent:bins[0],reselector:bins[1],tseitin:bins[2],resolution4:bins[3],chain3:bins[4]}});
  }
  const embedded=[];
  for(let t of [1,2,3,4,8]) for(const [name,R] of [["SAT",Q],["UNSAT",W1]]) {
    const shifted=R.map(cl=>cl.map(l=>l>0?l+4*t+1:l-4*t-1));
    const F=[...shifted,...orig(t)], rebuilt=[...shifted,...orig(t)];
    check(serialize(F)===serialize(rebuilt),"context fixed point");
    embedded.push({t,answer:name,original_bytes:serialize(F).length,child_bytes:serialize(rebuilt).length,iterations:3});
  }
  return {run:"SELECTOR-REINTRODUCTION208",date_utc:"2026-10-29T00:40Z",
    status:{theorems:"PROVED/EXACT restricted",finite:"COMPUTATIONAL",all_input_shortening:"OPEN",P_vs_NP:"OPEN"},
    projected_assignments:checks,projected_YES_counts:yesCounts,unique_gate_semantic_checks:gateChecks,
    signed_width_at_most3_counterassignments:shortChecks,W1_models:w1,Q_models:q,
    independent_W1_Q_assignments:65536,projection_cases:per,
    physical_sizes:sizeCases,context_SAT_UNSAT_fixed_point_cases:embedded,
    claims_not_made:["Not a general SAT runtime lower bound","Not a polynomial SAT decider","Not a bounded UTM step experiment"]};
}
if(typeof process!=="undefined"&&process.stdout) process.stdout.write(JSON.stringify(audit(),null,2)+"\n");
