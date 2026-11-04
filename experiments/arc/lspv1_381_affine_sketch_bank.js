'use strict';
// LSPV-1/381 deterministic two-stage affine-sketch synthesis experiment.
// Node >=16. No packages, no random seed from environment.
const assert = require('assert');
const seed0 = 3811103;
let seed = seed0, assertions = 0;
const check = (p, m) => { assert(p, m); assertions++; };
function rand() { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed; }
const ops = {
  AND:(a,b)=>a&b, OR:(a,b)=>a|b, XOR:(a,b)=>a^b,
  NAND:(a,b)=>1-(a&b), NOR:(a,b)=>1-(a|b), XNOR:(a,b)=>1-(a^b)
};
function strict(spec) {
  check(Number.isInteger(spec.B)&&spec.B>=1,'B');
  check(Number.isInteger(spec.k)&&spec.k>=1&&spec.k<=spec.B,'k');
  check(Array.isArray(spec.rows)&&spec.rows.length===spec.k,'rows');
  for(const r of spec.rows){check(Array.isArray(r.bits)&&r.bits.length===spec.B,'row width');check(r.bits.every(b=>b===0||b===1),'row bits');check(r.c===0||r.c===1,'offset');}
  check(Array.isArray(spec.gates),'gates');
  for(let j=0;j<spec.gates.length;j++){
    const g=spec.gates[j];check(Object.hasOwn(ops,g.op),'op');
    check(Number.isInteger(g.a)&&g.a>=0&&g.a<spec.k+j,'a');
    check(Number.isInteger(g.b)&&g.b>=0&&g.b<spec.k+j,'b');
  }
  check(Array.isArray(spec.outputs)&&spec.outputs.length>0,'outputs');
  check(spec.outputs.every(id=>Number.isInteger(id)&&id>=0&&id<spec.k+spec.gates.length),'public indices');
  return true;
}
function sketch(spec, input) {
  return spec.rows.map(r=>{ let v=r.c;for(let j=0;j<spec.B;j++) if(r.bits[j])v^=input[j];return v;});
}
function privateValues(spec,s) {
  let v=s.slice();for(const g of spec.gates) v.push(ops[g.op](v[g.a],v[g.b]));return v;
}
function evalOriginal(spec,input){ const s=sketch(spec,input),v=privateValues(spec,s);return spec.outputs.map(id=>v[id]); }
function makeBank(spec){
  strict(spec);
  let ands=[];
  const node=(a,sa,b,sb)=>{ const id=spec.B+ands.length;ands.push({a:a.id,sa:sa*a.s,b:b.id,sb:sb*b.s});return {id,s:1}; };
  const NOT=x=>({id:x.id,s:-x.s});
  const ref=id=>({id,s:1});
  const OR=(a,b)=>NOT(node(a,-1,b,-1));
  const XOR=(a,b)=>{const t=node(a,-1,b,-1),u=node(a,1,b,1);return node(t,-1,u,-1);};
  const f0=node(ref(0),1,ref(0),-1), f1=NOT(f0);
  let srefs=[];
  for(const row of spec.rows){
    let selected=[];row.bits.forEach((bit,i)=>{if(bit)selected.push(ref(i));});
    let z=selected.length?selected.reduce((a,b)=>XOR(a,b)):f0;
    srefs.push(row.c?NOT(z):z);
  }
  const functions=spec.outputs.map(()=>[]);
  for(let t=0;t<(1<<spec.k);t++){
    const sv=Array.from({length:spec.k},(_,j)=>(t>>j)&1), vals=privateValues(spec,sv);
    for(let j=0;j<functions.length;j++)functions[j].push(vals[spec.outputs[j]]);
  }
  const outputs=[];
  for(const truth of functions){
    const terms=[];
    for(let t=0;t<truth.length;t++)if(truth[t]===1){
      let literals=srefs.map((ref,j)=> ((t>>j)&1)?ref:NOT(ref));
      terms.push(literals.reduce((a,b)=>node(a,1,b,1)));
    }
    outputs.push(terms.length ? terms.reduce(OR) : f0);
  }
  return {B:spec.B,ands,outputs,sketchRows:spec.k};
}
function evalBank(bank,input){
  let vals=input.slice();
  for(const g of bank.ands){
    if(!Number.isInteger(g.a)||!Number.isInteger(g.b)||g.a<0||g.b<0||g.a>=vals.length||g.b>=vals.length||![1,-1].includes(g.sa)||![1,-1].includes(g.sb))throw Error('bad gate');
    let a=g.sa===1?vals[g.a]:1-vals[g.a],b=g.sb===1?vals[g.b]:1-vals[g.b];vals.push(a&b);
  }
  return bank.outputs.map(ref=>{if(ref.id<0||ref.id>=vals.length||![1,-1].includes(ref.s))throw Error('bad alias');return ref.s===1?vals[ref.id]:1-vals[ref.id];});
}
function generated(B,k,g,r){
  const rows=Array.from({length:k},()=>({bits:Array.from({length:B},()=>rand()%2),c:rand()%2}));
  rows[0].bits=Array(B).fill(1);
  const gates=Array.from({length:g},(_,j)=>({op:Object.keys(ops)[rand()%Object.keys(ops).length],a:rand()%(k+j),b:rand()%(k+j)}));
  const outputs=Array.from({length:r},(_,j)=>j%2===0?k+g-1:rand()%(k+g));
  return {B,k,rows,gates,outputs};
}
function k4Models(charge){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  let count=0;
  for(let mask=0;mask<64;mask++)if([0,1,2,3].every(v=>{
    let d=0;edges.forEach(([a,b],i)=>{if(a===v||b===v)d^=(mask>>i)&1;});return d===charge[v];
  }))count++;
  return count;
}
function experiment(){
  const cases=[], fixtures=[];
  for(const [B,k,g,r] of [[3,1,3,3],[4,2,16,8],[6,2,64,13],[8,3,128,21],[10,3,256,40]]){
    const spec=generated(B,k,g,r),bank=makeBank(spec);
    const qbound=3*k*B+r*k*(1<<k)+1;
    check(bank.ands.length<=qbound,'gate bound');
    for(let mask=0;mask<(1<<B);mask++){
      const a=Array.from({length:B},(_,i)=>(mask>>i)&1);
      check(JSON.stringify(evalOriginal(spec,a))===JSON.stringify(evalBank(bank,a)),'all outputs');
    }
    fixtures.push({spec,bank});
    cases.push({B,k,private_gates:g,public_outputs:r,original_gate_payload:g,bank_paid_gates:bank.ands.length,gate_bound:qbound,assignments:1<<B});
  }
  const specimen=generated(4,2,7,4),base=makeBank(specimen),trials=[
    {...specimen,rows:[]}, {...specimen,rows:specimen.rows.map(x=>({...x,bits:[1]}))},
    {...specimen,rows:[{...specimen.rows[0],c:2},specimen.rows[1]]},
    {...specimen,gates:[{op:'AND',a:9,b:0}]},
    {...specimen,gates:[{op:'UNKNOWN',a:0,b:1}]},
    {...specimen,outputs:[999]},
  ];
  let malformed=0;
  for(const x of trials){try{strict(x)}catch(e){malformed++;} }
  check(malformed===trials.length,'all bad syntax rejected');
  let corrupt=0;
  for(const edit of [b=>b.ands[0].a=1e8,b=>b.ands[0].sa=0,b=>b.outputs[0].id=-1,b=>b.outputs[0].s=0]){
    const bank=makeBank(specimen);edit(bank);try{evalBank(bank,[0,0,0,0])}catch(e){corrupt++;}
  }
  check(corrupt===4,'corrupt checker');
  // 3-variable OR fails every one-bit affine quotient.
  for(let row=1;row<8;row++){
    let fibers=[new Set(),new Set()];
    for(let a=0;a<8;a++){let s=0;for(let j=0;j<3;j++)s^=(((a>>j)&1)&((row>>j)&1));fibers[s].add(a===0?0:1);}
    check(fibers.some(s=>s.size>1),'OR must break every 1-bit affine quotient');
  }
  check(k4Models([1,0,0,0])===0,'odd parity UNSAT');
  check(k4Models([0,0,0,0])===8,'even parity SAT');
  return {...(process.argv.includes("--fixtures")?{fixtures}:{}),run:'AFFINE_SKETCH_BANK381',seed:seed0,mode:'exhaustive all boundary assignments per deterministic seeded specimen',cases,malformed_rejected:malformed,corrupt_rejected:corrupt,odd_k4_models:0,even_k4_models:8,assertions,limitations:['Only typed, two-stage syntactically authenticated circuits. No Rmix341 end-to-end compiler','Does not prove superpolynomial node minimum or computational SAT lower bound']};
}
console.log(JSON.stringify(experiment(),null,2));
