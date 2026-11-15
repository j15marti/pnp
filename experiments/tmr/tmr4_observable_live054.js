"use strict";
// TMR-4/054 finite exact counterexample audit. Native Node; no external packages.
const result = (function audit() {
  const revision = "tmr4-observable-live054.v1";
  let assertions = 0, evaluations = 0, faultReplays = 0, cnfChecks = 0, auxChecks = 0;
  const check = (p,msg) => {assertions++; if(!p) throw new Error(msg)};
  function build(n,k,kind) {
    let gates=[]; const input=i=>i;
    const push=(op,a,b=null)=>{let id=n+gates.length; gates.push({id,op,a,b});return id};
    let out;
    if(kind === "singleton") out = input(0);
    else if(kind === "disj") {
      let r=n/2;
      for(let i=0;i<r;i++) {
        let nx=push("not",input(i)), ny=push("not",input(r+i));
        let clause=push("or",nx,ny);
        out=(i===0)?clause:push("and",out,clause);
      }
    } else throw Error("kind");
    const baseG=gates.length;
    for(let j=0;j<k;j++) {
      let z=input(1+j%(n-1));
      let nz=push("not",z);
      let yes=push("and",out,z);
      let no=push("and",out,nz);
      out=push("or",yes,no);
    }
    const V=n+gates.length;
    const clauses=[];
    const add=(...lits)=>clauses.push(lits);
    for(let g of gates) {
      const z=g.id,a=g.a,b=g.b;
      if(g.op==="not") {add(-z-1,-a-1);add(z+1,a+1)}
      if(g.op==="and") {add(-z-1,a+1);add(-z-1,b+1);add(z+1,-a-1,-b-1)}
      if(g.op==="or") {add(z+1,-a-1);add(z+1,-b-1);add(-z-1,a+1,b+1)}
    }
    add(out+1);
    return {n,k,kind,gates,baseG,out,V,clauses};
  }
  function evaluate(C,bits,faultId=-1) {
    const v=bits.slice();
    for(const g of C.gates){
      let a=v[g.a], b=(g.b===null?0:v[g.b]), z=g.op==="not" ? 1-a : g.op==="and" ? a&b : a|b;
      if(g.id===faultId) z^=1;
      v.push(z);
    }
    return {v,out:v[C.out]};
  }
  function cnfSat(C,values) {
    return C.clauses.every(clause=>clause.some(lit=>{let v=values[Math.abs(lit)-1];return lit>0 ? v===1 : v===0}));
  }
  function certify(C) {
    const edges=Array.from({length:C.V},()=>[]);
    let wires=0;
    for(const g of C.gates){
      for(let a of g.b===null?[g.a]:[g.a,g.b]) {edges[g.id].push(a);wires++}
    }
    const anc=new Set(),stack=[C.out];
    while(stack.length) {let v=stack.pop();if(v<C.n||anc.has(v))continue;anc.add(v);stack.push(...edges[v])}
    check(anc.size===C.gates.length,"dead syntactic gate");
    const used=new Set();for(const g of C.gates)for(let v of edges[g.id])if(v<C.n)used.add(v);
    if(C.k>=C.n-1)check(used.size===C.n,"input missing");
    check(C.gates.length===C.baseG+4*C.k,"wrong gate count");
    let extra=C.kind==="disj"?10*(C.n/2)-2:1;
    check(C.clauses.length===extra+11*C.k,"wrong clause count");
    check(wires===(C.kind==="disj"?6*(C.n/2)-2:0)+7*C.k,"wrong wire count");
    let unique=new Set(C.clauses.map(c=>c.join(",")));
    check(unique.size===C.clauses.length,"duplicate clause");
    check(C.clauses.every(c=>c.length<=3),"wide clause");
    const influential=new Set(), witness={};let sat=0;
    for(let word=0;word<2**C.n;word++) {
      const bits=Array.from({length:C.n},(_,i)=>(word>>i)&1);
      const good=evaluate(C,bits);evaluations++;
      let want=C.kind==="singleton"?bits[0]:+Array.from({length:C.n/2},(_,i)=>!(bits[i]&&bits[C.n/2+i])).every(Boolean);
      check(good.out===want,"function changed");sat+=good.out;
      check(cnfSat(C,good.v)===(good.out===1),"canonical Tseitin witness mismatch");cnfChecks++;
      // A wire-cut fault overrides ONE gate output and recomputes its descendants.
      for(let g of C.gates){
        let bad=evaluate(C,bits,g.id);faultReplays++;
        if(bad.out!==good.out && !influential.has(g.id)){
          influential.add(g.id);witness[g.id]={input_word:word,normal:good.out,faulty:bad.out};
        }
        if(bad.v[g.id]!==good.v[g.id]){
          check(!cnfSat(C,bad.v),"wrong gate assignment accepted CNF");cnfChecks++;
        }
      }
      // Direct uniqueness is inductive. Tiny cases enumerate every auxiliary assignment.
      if(C.gates.length<=11){
        let valid=0;
        for(let aux=0;aux<2**C.gates.length;aux++){
          let vs=bits.concat(Array.from({length:C.gates.length},(_,i)=>(aux>>i)&1));
          if(cnfSat(C,vs))valid++;
          auxChecks++;
        }
        check(valid===want,"nonunique accepting extension");
      }
    }
    check(influential.size===C.gates.length,"gate not fault observable");
    const expected=C.kind==="singleton"?2**(C.n-1):3**(C.n/2);
    check(sat===expected,"count mismatch");
    return {kind:C.kind,n:C.n,k:C.k,base_gates:C.baseG,gates:C.gates.length,wires,variables:C.V,clauses:C.clauses.length,literal_occurrences:C.clauses.reduce((a,c)=>a+c.length,0),satisfying_inputs:sat,all_gates_live:true,all_gates_fault_observable:true,gate_witnesses:Object.keys(witness).length,gate_example:witness[C.n]};
  }
  let rows=[];
  for(let n of [2,3,4,5,6])for(let k of [n-1,n+1])rows.push(certify(build(n,k,"singleton")));
  for(let r of [2,3,4])for(let k of [2*r-1,2*r+1])rows.push(certify(build(2*r,k,"disj")));
  for(let r of [2,3,4])rows.push(certify(build(2*r,0,"disj")));
  for(let n of [2,3])for(let k of [1,2])rows.push(certify(build(n,k,"singleton")));
  return {revision,seed:null,status:"COMPUTATIONAL for finite audit; symbolic lemma in report",cases:rows.length,assertions,evaluations,fault_replays:faultReplays,cnf_checks:cnfChecks,auxiliary_assignments_checked:auxChecks,failures:0,rows};
})();
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(result,null,2)+"\n");
