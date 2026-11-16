// TMR-5/054: independent complete exact-count address-domain replay.
// Node 22+, no modules, deterministic seed 20261115.
// Scope: finite source-to-circuit-to-functional-CNF-to-count validation.
'use strict';
const SEED=20261115;
let rng=SEED>>>0, checks=0, tested=0, phantom=0, clausesVerified=0, gatesVerified=0;
function rand(n){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%n;}
function assert(ok,name){checks++;if(!ok)throw new Error(name+' test='+tested+' check='+checks);}
function clauseFalse(c,witness){return c.every(z=>witness[Math.abs(z)-1] !== (z>0?1:0));}
function directIndexCount(clauses,w){let count=0;for(let i=0;i<clauses.length;i++)if(clauseFalse(clauses[i],w))count++;return count;}
function buildCircuit(m,ell,violations,valid){
  // A complete total-Boolean circuit on original INDEX inputs, including all
  // unknown/invalid decoder positions. Each shared AND/OR/NOT has a functional Tseitin CNF.
  const q=ell,gs=[];
  function gate(op,a,b=a){gs.push({op,a,b});return q+gs.length-1;}
  const nbits=[];for(let i=0;i<ell;i++)nbits.push(gate('NOT',i));
  function AND(a,b){return gate('AND',a,b)}
  function OR(a,b){return gate('OR',a,b)}
  function eq(k){let p=(k&1)?0:nbits[0];for(let j=1;j<ell;j++)p=AND(p,((k>>j)&1)?j:nbits[j]);return p;}
  const eqs=Array.from({length:2**ell},(_,i)=>eq(i));
  // Conjoin an explicit legal-address comparator (here a minterm circuit).
  function disj(indices){if(!indices.length)return AND(0,nbits[0]);let p=eqs[indices[0]];for(let j=1;j<indices.length;j++)p=OR(p,eqs[indices[j]]);return p;}
  const raw=disj(violations), legal=disj(Array.from({length:m},(_,i)=>i));
  const out=valid?AND(raw,legal):raw;
  return {q,gs,out};
}
function computeAndCheck(c,x){
  const vals=x.slice(), allClauses=[];
  for(let i=0;i<c.gs.length;i++){
    const g=c.gs[i],a=vals[g.a],b=vals[g.b];
    const v=g.op==='NOT'?1-a:g.op==='AND'?(a&b):(a|b);
    vals.push(v);
    const z=c.q+i;
    // truth-table rows: (a != u) OR (b != v) OR (z == op(u,v)).
    for(let u=0;u<2;u++)for(let w=0;w<2;w++){
      const target=g.op==='NOT'?1-u:g.op==='AND'?(u&w):(u|w);
      allClauses.push([[g.a,u===0],[g.b,w===0],[z,target===1]]);
    }
  }
  allClauses.push([[c.out,true]]);
  function cnfHolds(v){return allClauses.every(row=>row.some(([index,positive])=>v[index]===(positive?1:0)));}
  assert(cnfHolds(vals)===(vals[c.out]===1),'functional CNF exact extension');
  // Every gate variable is constrained, even dead gates and shared predecessors.
  for(let z=c.q;z<c.q+c.gs.length;z++){
    vals[z]^=1;
    assert(!cnfHolds(vals),'no spurious auxiliary extension');
    vals[z]^=1;
    gatesVerified++;
  }
  clausesVerified+=allClauses.length;
  return vals[c.out];
}
// Smallest unmasked-domain falsifier: one real clause x and a fabricated
// non-domain clause NOT x, witness x=true.
{
 const m=1, ell=1, w=[1], decoder=[[1,1,1],[-1,-1,-1]];
 assert(directIndexCount(decoder.slice(0,m),w)===0,'real clause satisfied');
 const v=decoder.map((c,i)=>clauseFalse(c,w)?i:-1).filter(i=>i>=0);
 const free=buildCircuit(m,ell,v,false),masked=buildCircuit(m,ell,v,true);
 let unmasked=0,correct=0;
 for(let i=0;i<2**ell;i++){
   const bits=[i&1];unmasked+=computeAndCheck(free,bits);correct+=computeAndCheck(masked,bits);
 }
 assert(unmasked===1&&correct===0,'minimal phantom-address falsifier');phantom++;
}
for(let m=1;m<=5;m++)for(let v=1;v<=3;v++)for(let test=0;test<18;test++){
  const ell=Math.max(1,Math.ceil(Math.log2(m)));
  const decoder=[];
  for(let i=0;i<2**ell;i++)decoder.push(Array.from({length:3},()=>{
    const pos=1+rand(v);return rand(2)?pos:-pos;
  }));
  for(let mask=0;mask<2**v;mask++){
    tested++;
    const witness=Array.from({length:v},(_,j)=>(mask>>j)&1);
    const bad=[];for(let i=0;i<decoder.length;i++)if(clauseFalse(decoder[i],witness))bad.push(i);
    const c=buildCircuit(m,ell,bad,true),raw=buildCircuit(m,ell,bad,false);
    let maskedCount=0,rawCount=0;
    for(let i=0;i<2**ell;i++){
      const bits=Array.from({length:ell},(_,b)=>(i>>b)&1);
      maskedCount+=computeAndCheck(c,bits);
      rawCount+=computeAndCheck(raw,bits);
    }
    assert(maskedCount===directIndexCount(decoder.slice(0,m),witness),'masked exact number of violated authentic clauses');
    assert(rawCount===bad.length,'unmasked number includes phantom clauses');
    if(rawCount!==maskedCount)phantom++;
  }
}
const result={revision:'tmr5-address-mask-chain054.v1',seed:SEED,status:'COMPUTATIONAL',caseCount:tested,assertions:checks,failures:0,phantomCases:phantom,functionalTseitinClauseChecks:clausesVerified,auxiliaryFlipRejections:gatesVerified,model:'total binary decoder with authentic domain 0<=i<m, fixed witness, 3-literal clauses, full shared-gate functional CNF',conclusion:'masked violated-address count equals authentic unsatisfied clause count; unmasked arbitrary padding can be false even on SAT; no unrestricted P/NP claim',limitations:'small finite cases, no physical TM timing/space microtrace, no Lean kernel build'};
console.log(JSON.stringify(result,null,2));
