// LSPV-3/382: coNP-complete semantic-support locality barrier.
// Node 22+, deterministic, no dependencies, no random data.
// Proof of asymptotic theorem appears in role report; finite checks are controls.
"use strict";
function runSupportAudit() {
  const m = 3, y = 4, n = m + y;
  const refs = Array.from({length:n}, (_,id)=>({id,neg:false}));
  const inv = a=>({id:a.id,neg:!a.neg});
  const val = (r, bits)=> Boolean((bits >> r.id) & 1) !== r.neg;
  const clauses = Array.from({length:8},(_,mask)=>
      Array.from({length:3},(_,i)=>({id:i,neg:Boolean((mask>>i)&1)})));
  const clauseValue = (cl,bits)=>cl.some(l=>val(l,bits));
  const formulaValue = (mask,bits)=>
      clauses.every((cl,j)=>!((mask>>j)&1)||clauseValue(cl,bits));
  function build(mask) {
    const gates = []; const and=(a,b)=>{
      const r={id:n+gates.length,neg:false};gates.push({a,b});return r;
    };
    const or=(a,b)=>inv(and(inv(a),inv(b)));
    let root = null;
    for(let j=0;j<8;j++)if((mask>>j)&1) {
      const cl=clauses[j];
      const t=or(or(cl[0],cl[1]),cl[2]);
      root = root===null ? t : and(root,t);
    }
    if(root===null) root=inv(and(refs[0],inv(refs[0]))); // TRUE, no constant axiom
    for(let j=m;j<n;j++)root=and(root,refs[j]);
    return {gates,root};
  }
  function validate(c) {
    if(!c || !Array.isArray(c.gates) || !c.root) return false;
    function goodRef(r,limit) {
      return r && Number.isInteger(r.id) && r.id>=0 && r.id<limit &&
             typeof r.neg==="boolean";
    }
    for(let i=0;i<c.gates.length;i++) {
      const g=c.gates[i];
      if(!g || !goodRef(g.a,n+i)|| !goodRef(g.b,n+i))return false;
    }
    return goodRef(c.root,n+c.gates.length);
  }
  function circuitValue(c,bits) {
    if(!validate(c))throw Error("malformed circuit");
    const t=Array.from({length:n},(_,i)=>Boolean((bits>>i)&1));
    for(let i=0;i<c.gates.length;i++) {
      const {a,b}=c.gates[i];
      t.push((t[a.id]!==a.neg)&&(t[b.id]!==b.neg));
    }
    return t[c.root.id]!==c.root.neg;
  }
  function supportByTruthTable(fn) {
    let ans=[];
    for(let i=0;i<n;i++){
      let found=false;
      for(let bits=0;bits<(1<<n);bits++) {
        if((bits>>i)&1)continue;
        if(fn(bits)!==fn(bits^(1<<i))){ found=true; break; }
      }
      if(found)ans.push(i);
    }
    return ans;
  }
  let checks=0, sat=0, unsat=0, maxGate=0, essentialCount={};
  let witnessPairs=0; const errors=[];
  for(let mask=0;mask<256;mask++) {
    const c=build(mask);
    if(!validate(c)) errors.push("invalid generated: "+mask);
    maxGate=Math.max(maxGate,c.gates.length);
    let models=0;
    for(let bits=0;bits<(1<<m);bits++)models+=formulaValue(mask,bits)?1:0;
    const isSat=models>0;
    sat+=isSat?1:0; unsat+=isSat?0:1;
    for(let bits=0;bits<(1<<n);bits++){
      let direct=formulaValue(mask,bits)&&
         [3,4,5,6].every(i=>Boolean((bits>>i)&1));
      if(direct!==circuitValue(c,bits))errors.push("semantic mismatch: "+mask+","+bits);
      checks++;
    }
    const support=supportByTruthTable(bits=>circuitValue(c,bits));
    checks+=n*(1<<(n-1));
    essentialCount[support.length]=(essentialCount[support.length]||0)+1;
    if((support.length<=3)!==(!isSat))errors.push("coNP reduction mismatch: "+mask);
    // Independent four witnessed essential variables, from a satisfying x input.
    if(isSat) {
      let x=Array.from({length:1<<m},(_,i)=>i).find(v=>formulaValue(mask,v));
      const allY=x| (15<<m);
      for(let i=m;i<n;i++) {
        if(!circuitValue(c,allY) || circuitValue(c,allY^(1<<i)))
          errors.push("bad support witness: "+mask+","+i);
        witnessPairs++;checks+=2;
      }
    }
  }
  const good=build(0); const cloned=c=>JSON.parse(JSON.stringify(c));
  const malformed=[
    null,{}, {gates:[],root:{id:99,neg:false}},
    {...cloned(good),root:{id:0,neg:"notbool"}},
    {...cloned(good),gates:[{a:{id:n,neg:false},b:{id:0,neg:false}}]},
    {...cloned(good),gates:[{a:{id:0,neg:false},b:{id:-1,neg:false}}]},
    {...cloned(good),gates:[{a:{id:0,neg:false}}]}
  ];
  for(const c of malformed){
    if(validate(c))errors.push("accepted malformed "+JSON.stringify(c));
    checks++;
  }
  const correct=build(254);
  const tamperedRoot=cloned(correct);
  tamperedRoot.root.neg=!tamperedRoot.root.neg;
  const tamperedGate=cloned(correct);
  const last=tamperedGate.gates.length-1;
  tamperedGate.gates[last].a.neg=!tamperedGate.gates[last].a.neg;
  const corrupt=[tamperedRoot,tamperedGate];
  for(let j=0;j<corrupt.length;j++){
    if(!validate(corrupt[j]))errors.push("wrongly rejected well-typed corruption "+j);
    let found=false;
    for(let b=0;b<(1<<n);b++){
      if(circuitValue(corrupt[j],b)!==circuitValue(correct,b)){found=true;break;}
    }
    if(!found)errors.push("undetected functional corruption "+j);
    checks++;
  }
  return {status:errors.length===0?"PASS":"FAIL",cases:256,
    sat_cases:sat,unsat_cases:unsat,checks,max_gate_count:maxGate,
    essential_support_histogram:essentialCount,
    support_witness_pairs:witnessPairs,malformed_rejected:malformed.length,corrupt_semantics_rejected:corrupt.length,
    canonical_satisfiable_mask:254,canonical_unsatisfiable_mask:255,
    errors:errors.slice(0,8),method:"exhaustive 256 3-CNF subformula masks, 7-bit gate and truth-table outputs; signed two-input AND DEF circuits"};
}
if(typeof module!=="undefined" && module.exports) module.exports={runSupportAudit};
if(typeof require!=="undefined" && require.main===module)
  process.stdout.write(JSON.stringify(runSupportAudit(),null,2)+"\n");
