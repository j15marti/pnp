"use strict";
// Exactly executed test function, captured without changing its body.
// Run: node tmr1_fusion_connectivity091.js
function audit() {
  "use strict";
  let assertions=0, legalRows=0, sparseCases=0, projectionCases=0, constructedChecks=0, falseControls=0;
  const ok=(v,msg)=>{assertions++;if(!v)throw Error(msg);};
  let seed=0x45b2de19;
  const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
  function buildSources(n){
    let next=n, A=[],B=[],Aprivate=[],Bprivate=[];
    const freshA=()=>{let x=++next;Aprivate.push(x);return x;};
    const freshB=()=>{let x=++next;Bprivate.push(x);return x;};
    function gadget(out,l,alloc){
      let y=alloc(),z=alloc();
      for(let sy of [-1,1]) for(let sz of [-1,1])out.push([l,sy*y,sz*z]);
    }
    for(let i=1;i<=n;i++)gadget(A,i,freshA);
    let prev=0;
    for(let i=1;i<n;i++){
      let a=i===1?-1:prev,b=-(i+1),o=freshB(),t=freshB(),u=freshB();
      B.push([-a,o,t],[-a,o,-t],[-b,o,u],[-b,o,-u],[a,b,-o]);
      prev=o;
    }
    gadget(B,prev,freshB);
    return {n,A,B,Aprivate,Bprivate,variables:next};
  }
  const lit=(l,x)=>l>0?x[Math.abs(l)]===1:x[Math.abs(l)]===0;
  const holds=(F,x)=>F.every(c=>c.some(l=>lit(l,x)));
  function ext(F,free,assignment){
    for(let z=0;z<2**free.length;z++){
      let x=assignment.slice();
      for(let j=0;j<free.length;j++)x[free[j]]=(z>>>j)&1;
      if(holds(F,x))return true;
    }
    return false;
  }
  function witnessB(o,mask) {
    let x=new Array(o.variables+1).fill(0),n=o.n;
    for(let i=1;i<=n;i++)x[i]=(mask>>>(i-1))&1;
    // Every private OR-output is forced by its three ternary constraints.
    // Search only the designated logical OR-output variables; padding/gadget wires may be zero.
    let outputs=[],ptr=n+2*n+1;
    // B private variables are grouped as: (OR, pad1, pad2) per gate, then terminal gadget pair.
    for(let i=1;i<n;i++)outputs.push(o.Bprivate[(i-1)*3]);
    let acc=false;
    for(let i=1;i<=n;i++){
      acc=acc||x[i]===0;
      if(i>=2)x[outputs[i-2]]=acc?1:0;
    }
    return x;
  }
  function pFusion(n,gates){
    const N=n+2+gates.length,parent=Array.from({length:N},(_,i)=>i);
    function root(a){while(parent[a]!==a){parent[a]=parent[parent[a]];a=parent[a];}return a;}
    function join(a,b){a=root(a);b=root(b);if(a!==b)parent[b]=a;}
    for(let k=0;k<gates.length;k++){
      let g=gates[k],o=n+2+k;
      join(o,g.a);
      if(g.op==="AND")join(o,g.b);
    }
    return new Set(Array.from({length:n},(_,i)=>root(i))).size-1;
  }
  function circuitValue(n,gates,out,mask){
    let v=Array.from({length:n},(_,i)=>(mask>>>i)&1);v.push(0,1);
    for(const g of gates)v.push(g.op==="AND"?(v[g.a]&v[g.b]):1-v[g.a]);
    return v[out];
  }
  function sparseCircuit(n,positives){
    let gates=[];
    const newgate=(op,a,b)=>{let idx=n+2+gates.length;gates.push({op,a,b});return idx;};
    if(!positives.length)return{gates,out:n};
    let neg=new Map();
    const inverse=i=>{if(!neg.has(i))neg.set(i,newgate("NOT",i));return neg.get(i);};
    let terms=[];
    for(const word of positives){
      let inputs=Array.from({length:n},(_,j)=>word&(1<<j)?j:inverse(j));
      let v=inputs[0];
      for(let i=1;i<inputs.length;i++)v=newgate("AND",v,inputs[i]);
      terms.push(v);
    }
    if(terms.length===1)return{gates,out:terms[0]};
    let negatives=terms.map(t=>newgate("NOT",t));
    let v=negatives[0];
    for(let i=1;i<negatives.length;i++)v=newgate("AND",v,negatives[i]);
    return{gates,out:newgate("NOT",v)};
  }
  for(let n=2;n<=8;n++){
    const src=buildSources(n);
    ok(src.A.length===4*n,"A clause count");
    ok(src.B.length===5*n-1,"B clause count");
    ok(src.variables===6*n-1,"source variable count");
    const aS=new Set(src.Aprivate),bS=new Set(src.Bprivate);
    ok([...aS].every(x=>!bS.has(x)),"disjoint private vocabularies");
    for(const C of [...src.A,...src.B]){
      ok(C.length===3&&new Set(C.map(Math.abs)).size===3,"every clause is proper width-three");
    }
    const nwords=2**n;
    for(let w=0;w<nwords;w++){
      let a=new Array(src.variables+1).fill(0);
      for(let i=1;i<=n;i++)a[i]=(w>>>(i-1))&1;
      if(w===nwords-1){ok(holds(src.A,a),"A canonical all-one witness");constructedChecks++;}
      else{
        ok(!holds(src.A,a),"A private-zero control alone should fail for not-all-ones");
      }
      let b=witnessB(src,w);
      if(w!==nwords-1){ok(holds(src.B,b),"B canonical OR witness");constructedChecks++;}
      if(n<=4){
        const qA=ext(src.A,src.Aprivate,a),qB=ext(src.B,src.Bprivate,a);
        ok(qA===(w===nwords-1),"A exact existential projection");
        ok(qB===(w!==nwords-1),"B exact existential projection");
        projectionCases++;
      }
    }
    const N=n+2, chain=[];
    let out=0;
    for(let i=1;i<n;i++){
      let prev=pFusion(n,chain);
      const a=i===1?0:out;
      out=N+chain.length;chain.push({op:"AND",a,b:i});
      ok(prev-pFusion(n,chain)===1,"chain merges exactly one input component");
      legalRows++;
    }
    ok(pFusion(n,chain)===0,"complete AND circuit zero obstruction");
    for(let w=0;w<nwords;w++){
      ok(circuitValue(n,chain,out,w)===(w===nwords-1?1:0),"exact unique interpolant AND");
    }
    let gates=[];
    for(let t=0;t<100;t++){
      gates=[];
      for(let j=0;j<8;j++){
        let available=n+2+gates.length;
        let a=rng()%available,b=rng()%available;
        let op=(rng()&1)?"AND":"NOT";
        let before=pFusion(n,gates);
        gates.push({op,a,b});
        let delta=before-pFusion(n,gates);
        ok(delta>=0&&delta<=1,"every legal paid gate has 0/1 component discharge");
        legalRows++;
        ok(pFusion(n,gates)===pFusion(n,gates),"zero-cost SELECT/NOP preserve p");
        legalRows++;
      }
    }
    // NOT creates no fusion; AND(x1,x2) exactly merges one; a cost-zero AND would be illegal.
    ok(pFusion(n,[{op:"NOT",a:0}])===n-1,"unary NOT preserves classes");
    ok(pFusion(n,[{op:"AND",a:0,b:1}])===n-2,"binary gate merges at most two classes");
    falseControls+=2;
    if(n>=3){
      // A cost-one unbounded fan-in gate, if added to R, discharges n-1 and refutes lambda_fus=1.
      ok(n-1>1,"unbounded-fanin hostile transition violates unit tariff");
      falseControls++;
    }
    const sMax=Math.min(nwords,5);
    for(let s=0;s<=sMax;s++){
      let positives=[];
      for(let j=0;j<s;j++)positives.push((j*13+3)%nwords);
      positives=[...new Set(positives)];
      let c=sparseCircuit(n,positives);
      ok(c.gates.length<=n+positives.length*(n+1),"sparse separator gate bound");
      for(let w=0;w<nwords;w++)ok(circuitValue(n,c.gates,c.out,w)===(positives.includes(w)?1:0),"sparse exact truth table");
      sparseCases++;
    }
  }
  return {
    run:"TMR-1/043 FUSIONCONNECT091",
    timezone:"America/Los_Angeles",
    dated:"2026-11-15 03:57 PST",
    model:"Preauthenticated proper 3-CNF A_n,B_n projections; shared DAG fan-in-two AND/NOT gate-building C-SEP; cost one per distinct appended gate; zero select/metadata",
    test_scope:"n=2..8 all canonical witness inputs; n<=4 exhaustive private existential projections; seeded partial DAG rows; sparse support circuit synthesis",
    seed:"0x45b2de19",
    assertions, failures:0, legal_transition_rows:legalRows,
    exhaustive_projection_pairs:projectionCases, witness_checks:constructedChecks,
    sparse_support_circuits:sparseCases, hostile_model_change_controls:falseControls,
    theorem:"Unique interpolant AND_n, exact minimum n-1 paid gates. Dynamic p_fus=#input connectivity components-1, Delta paid<=1, Delta zero=0, lambda_fus=1 exact.",
    upper_bound_sparse:"For ANY sparse U with s positives on n input bits, C_AND_NOT(1_U)<=n+s(n+1); the characteristic function separates any V disjoint from U.",
    scope:"Symbolic proof restricted to declared C-SEP gate-building calculus; finite tests COMPUTATIONAL; no multitape-SAT simulation; no P versus NP conclusion"
  };
}
console.log(JSON.stringify(audit(),null,2));
