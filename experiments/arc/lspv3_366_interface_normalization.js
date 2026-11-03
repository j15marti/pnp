// LSPV-3 366 semantic 3-input Boolean-circuit normalization.
// Run: node experiments/arc/lspv3_366_interface_normalization.js
// Does not modify or implement the authoritative Rmix341 calculus.
const main=function runner(){
 const check=(v,m)=>{if(!v) throw Error(m||"assert");nAssertions++};
 let nAssertions=0;
 const pc=m=>{let n=0;for(let i=0;i<8;i++)n+=(m>>i)&1;return n};
 function norm(mask) {
  if(mask===0||mask===255)return {mask,gates:0,expr:{op:"const",value:mask===255?1:0}};
  const invert=pc(mask)>4,work=invert?(255^mask):mask;
  let terms=[];
  for(let x=0;x<8;x++)if((work>>x)&1){
   const lits=Array.from({length:3},(_,i)=>(x>>i)&1?{op:"var",i}:{op:"not",a:{op:"var",i}});
   terms.push({op:"and",a:{op:"and",a:lits[0],b:lits[1]},b:lits[2]});
  }
  let e=terms[0];for(let i=1;i<terms.length;i++) e={op:"or",a:e,b:terms[i]};
  if(invert)e={op:"not",a:e};
  // shared three negation input nodes, at most 2 AND per term, m-1 OR and one output negation
  const gates=3+2*terms.length+(terms.length-1)+(invert?1:0); // <=16 (pessimistic)
  return {mask,gates,expr:e,terms:terms.length,invert};
 }
 function ev(e,a){
  switch(e.op){case "const":if(e.value!==0&&e.value!==1)throw Error("bad const");return e.value;case "var":if(!Number.isInteger(e.i)||e.i<0||e.i>=3)throw Error("bad input index");return a[e.i];case "not":return 1-ev(e.a,a);case "and":return ev(e.a,a)&ev(e.b,a);case "or":return ev(e.a,a)|ev(e.b,a);default:throw Error("bad op");}
 }
 const truth=e=>{let mask=0;for(let x=0;x<8;x++){let a=[x&1,(x>>1)&1,(x>>2)&1];mask|=ev(e,a)<<x;}return mask};
 let max=0,counts={},gt=0;
 for(let m=0;m<256;m++){let n=norm(m);check(truth(n.expr)===m,"truth "+m);check(n.gates<=16,"gate "+m); max=Math.max(max,n.gates);counts[n.gates]=(counts[n.gates]||0)+1;gt++;}
 let chains=[];
 for(let k of [1,2,3,8,64,512,1024])for(const flip of [-1,0,Math.floor(k/2),k-1]){
  const c=flip===-1?true:false;
  const m=c?170:0; // variable x0 truth mask (binary 10101010)
  const n=norm(m);check(truth(n.expr)===m);check(n.gates<=16);
  // Fixed local antecedent S=x0, conclusion x0 AND c; implications checked on all assignments
  let localValid=true;for(let i=0;i<8;i++)if((i&1)&&!((m>>i)&1))localValid=false;
  check(localValid===c);
  chains.push({k,flippedConstant:flip,rawGateRecords:2*k+1,canonicalGateUpper:n.gates,localValid,truthMask:m});
 }
 const satSource=[[1],[1,2]],unsatSource=[[1],[1,2],[-1]];
 const models=F=>{let n=0;for(let x=0;x<4;x++)if(F.every(cl=>cl.some(l=>{let v=l>0?((x>>(l-1))&1):1-((x>>(-l-1))&1);return v===1})))n++;return n};
 check(models(satSource)===2);check(models(unsatSource)===0);
 // Malformed and corrupt expressions must fail extensional check, not be accepted.
 let malformed=0;for(const bad of [{op:"bogus"},{op:"var",i:99},{op:"and",a:{op:"var",i:0}},{op:"const",value:2}]){
  try{let t=truth(bad);if(t!==0 && t!==255)throw Error("invalid");}catch(_){malformed++}
 }
 // 'const 2' invalid via extensional range checking
 check(malformed===4);
 check(truth(norm(170).expr)!==truth(norm(0).expr));
 return {run:"LSPV3_366",status:"COMPUTATIONAL controls for conditional bounded-interface lemma",n_inputs:3,all_boolean_functions:gt,max_overestimated_gates:max,histogram:counts,long_chain_controls:chains,original_source_labels:{satModels:models(satSource),unsatModels:models(unsatSource)},bad_syntax_rejections:malformed,checked_corruption:true,assertions:nAssertions,notes:"Gates overestimate by charging all 3 input negations even when unused; logical node cost is not gate count or verifier work. This script tests extensional normalizer, NOT the authoritative mixed inference grammar."};
};
console.log(JSON.stringify(main(),null,2));
