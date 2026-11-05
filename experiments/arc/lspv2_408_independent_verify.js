#!/usr/bin/env node
// Independently authored verifier of LSPV-2/408 raw JSON. No imports except fs.
const fs=require('fs');
const f=process.argv[2]||'/mnt/data/lspv2_408_facet_raw.json';
const rec=JSON.parse(fs.readFileSync(f,'utf8'));
let assertions=0;
function insist(x,msg){assertions++;if(!x)throw new Error(msg);}
function value(mask,a,b){return (mask>>(2*a+b))&1;}
function forward(gates,base){const vals=new Map(Object.entries(base).map(([k,v])=>[+k,v]));
  for(const g of gates){insist(Number.isInteger(g.mask)&&g.mask>=0&&g.mask<=15,'bad mask');
    insist(!vals.has(g.out)&&vals.has(g.left)&&vals.has(g.right),'fresh/order');
    vals.set(g.out,value(g.mask,vals.get(g.left),vals.get(g.right)));}return vals;}
function canonical(z){let s=[...new Set(z)];for(const x of s)if(s.includes(-x))return null;
 return s.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function clauseVal(c,vs){return c.some(l=>vs.get(Math.abs(l))===(l>0?1:0));}
const trace=rec.proof;
const ax=rec.normalized_definition_clauses;
insist(rec.original.length===2 && rec.normalized.length===10,'gate counts');
insist(eq(trace.target,[3,4,-5]),'facet target');
insist(rec.all_facets.length===8,'all facets');
let modelsSAT=0,modelsUNSAT=0;
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){
 const inp={1:a,2:b,3:c}; const old=forward(rec.original,inp),nn=forward(rec.normalized,inp);
 for(const g of rec.original)insist(old.get(g.out)===nn.get(g.out),'public function changed');
 for(const orig of rec.source_clauses_original)insist(clauseVal(orig,nn),'old facet invalid');
 for(const cl of ax)insist(clauseVal(cl,nn),'normalized gate facet invalid');
 for(const facet of rec.all_facets)insist(clauseVal(facet.target,nn),'facet not entailed');
 if(a===1)modelsSAT++;
 if(a===1 && a===0)modelsUNSAT++;
}
insist(modelsSAT===4 && modelsUNSAT===0,'source controls');
function check(T){
 insist(T.nodes.length>=ax.length && T.root<T.nodes.length,'bad DAG size');
 let steps=0;
 T.nodes.forEach((node,i)=>{
  insist(eq(node.clause,canonical(node.clause)),'malformed/taut clause');
  if(i<ax.length){insist(node.kind==='source'&&eq(node.clause,ax[i]),'not authentic paid DEF facet');return;}
  insist(node.kind==='res'&&node.parents.length===2,'not RES');
  const [u,v]=node.parents, p=node.pivot;
  insist(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v>=0&&u<i&&v<i&&u!==v,'bad parent');
  const A=T.nodes[u].clause,B=T.nodes[v].clause;
  insist(A.includes(p)&&B.includes(-p),'bad RES pivot');
  const C=canonical([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
  insist(C!==null&&eq(C,node.clause),'bad RES result');steps++;
 });
 insist(T.nodes[T.root].clause.every(l=>T.target.includes(l)),'not subclause conclusion');
 insist(steps===T.res_nodes,'incorrect charge');return steps;
}
const nRes=check(trace);insist(nRes===19,'unexpected proof length');
let bad=JSON.parse(JSON.stringify(trace));let k=bad.nodes.findIndex(n=>n.kind==='res');bad.nodes[k].pivot=777;
try{check(bad);throw Error('accepted corrupted pivot')}catch(e){insist(!e.message.includes('accepted corrupted'),'corruption not rejected')}
let bad2=JSON.parse(JSON.stringify(trace));bad2.nodes[0].clause=[1,2,3];
try{check(bad2);throw Error('accepted forged gate facet')}catch(e){insist(!e.message.includes('accepted forged'),'forgery not rejected')}
insist(eq(rec.all_facets.map(x=>x.res_nodes),[17,17,17,17,19,19,19,19]),'facet counts');
console.log(JSON.stringify({result:'PASS',independent_assertions:assertions,proof_steps:nRes,all_facet_costs:rec.all_facets.map(x=>x.res_nodes),original_gate_count:rec.original.length,normalized_paid_gate_count:rec.normalized.length,full_evidence_bytes:fs.statSync(f).size}));
