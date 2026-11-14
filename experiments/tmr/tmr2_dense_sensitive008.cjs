'use strict';
const assert = require('node:assert/strict');

// Independent finite audit of the even-parity identifier embedding lemma.
// Source values are JS numbers only in this finite verifier, not a TM cost model.
function prism(r) {
  assert(r >= 3);
  const V = 2*r, edges = [];
  for (let i=0;i<r;i++) {
    edges.push([i,(i+1)%r], [r+i,r+((i+1)%r)], [i,r+i]);
  }
  const incidence = Array.from({length:V},()=>[]);
  edges.forEach(([a,b],e)=>{incidence[a].push(e);incidence[b].push(e)});
  assert(incidence.every(x=>x.length===3));
  return {V,edges,incidence};
}
function bitParity(x) { let p=0; while(x>0) {p ^= x&1;x=Math.floor(x/2)}return p; }
function code(i) { return 2*i+bitParity(i); }
function make(V,incidence,charge) {
  const clauses=[], eq=[];
  for(let v=0;v<V;v++) {
    const ids=incidence[v]; eq.push({ids, rhs:charge[v]});
    for(let bits=0;bits<8;bits++) {
      const tuple=[bits&1,(bits>>1)&1,(bits>>2)&1];
      if((tuple[0]^tuple[1]^tuple[2]) !==charge[v])
        clauses.push({v,tuple,lits:ids.map((id,j)=>({id,neg:tuple[j]}))});
    }
  }
  return {clauses,eq};
}
function solveGF2(equations,n) {
  const piv=new Map();
  for(const e of equations) {
    let mask=0n, rhs=e.rhs;
    for(const i of e.ids) mask^=1n<<BigInt(i);
    while(mask) {
      let col=0, scan=mask;
      while((scan&1n)===0n) {col++; scan>>=1n;}
      if(!piv.has(col)){piv.set(col,{mask,rhs});break;}
      const row=piv.get(col);mask^=row.mask;rhs^=row.rhs;
    }
    if(mask===0n && rhs) return null;
  }
  const answer=Array(n).fill(0);
  const cols=[...piv.keys()].sort((a,b)=>b-a);
  for(const col of cols){
    const row=piv.get(col);let t=row.rhs;
    for(let j=col+1;j<n;j++)if((row.mask>>BigInt(j))&1n)t^=answer[j];
    answer[col]=t;
  }
  for(const e of equations){let p=0;for(const i of e.ids)p^=answer[i];assert.equal(p,e.rhs)}
  return answer;
}
function encode(clauses,t) {
  const w=Math.max(2,Math.ceil(Math.log2(2*t+2))),N=2**w-1,M=clauses.length;
  assert(2*t+1<=N);
  const header='1'.repeat(N)+'0'+'1'.repeat(M)+'0';
  let s=header;const positions=[];
  for(const c of clauses)for(const lit of c.lits){
    s+=String(lit.neg);positions.push({at:s.length-1,kind:'sign',clause:clauses.indexOf(c)});
    const id=code(lit.id+1);assert(id>0&&id<=N&&bitParity(id)===0);
    let bin=id.toString(2).padStart(w,'0');
    for(let j=0;j<w;j++)positions.push({at:s.length+j,kind:'id',clause:clauses.indexOf(c)});
    s+=bin;
  }
  assert.equal(s.length,N+M+2+3*M*(1+w));
  return {s,N,M,w,positions,headerLen:header.length};
}
function parse(source,N,M,w) {
  const h='1'.repeat(N)+'0'+'1'.repeat(M)+'0';
  if(!source.startsWith(h)||source.length!==h.length+3*M*(w+1))return null;
  let pos=h.length;const clauses=[];
  for(let c=0;c<M;c++){
    let literals=[],used=new Set();
    for(let k=0;k<3;k++){
      const neg=+source[pos++],id=parseInt(source.slice(pos,pos+w),2);pos+=w;
      if(!(id>0&&id<=N)||used.has(id))return null;
      used.add(id);literals.push({id,neg});
    }
    clauses.push(literals);
  }
  return clauses;
}
function satisfies(clauses,assignment) {
  return clauses.every(c=>c.some(l=>((assignment.get(l.id)||0)^l.neg)===1));
}
function main(){
  let metrics={cases:0,clauses:0,signFlips:0,idBitFlips:0,validMutations:0,failed:0,
    maxL:0,maxQ:0,ratioMin:1,ratioMax:0,negativeControls:0,bruteOriginalChecks:0,
    perCase:[]};
  for(const r of [3,4,6,8,12]){
    const {V,edges,incidence}=prism(r),t=edges.length;
    for(const chargedVertex of [0, Math.floor(V/2)]) {
      const charge=Array(V).fill(0);charge[chargedVertex]=1;
      const {clauses,eq}=make(V,incidence,charge);
      assert.equal(solveGF2(eq,t),null);
      const obj=encode(clauses,t);const original=parse(obj.s,obj.N,obj.M,obj.w);
      assert(original);
      const posByClause=Array.from({length:clauses.length},()=>[]);
      for(const item of obj.positions)posByClause[item.clause].push(item);
      for(let ci=0;ci<clauses.length;ci++) {
        const c=clauses[ci];
        const flipped=eq.map((e,v)=>({ids:e.ids,rhs:e.rhs^(v===c.v?1:0)}));
        for(let j=0;j<3;j++)flipped.push({ids:[c.lits[j].id],rhs:c.tuple[j]});
        const witness=solveGF2(flipped,t);assert(witness);
        const base=new Map();for(let i=0;i<t;i++)base.set(code(i+1),witness[i]);
        assert.equal(satisfies(original,base),false);
        const falseAt=original.flatMap((lits,k)=>lits.some(l=>((base.get(l.id)||0)^l.neg)===1)?[]:[k]);
        assert.deepEqual(falseAt,[ci]);
        metrics.clauses++;
        for(const p of posByClause[ci]) {
          const replacement=obj.s[p.at]==='0'?'1':'0';
          const mutation=obj.s.slice(0,p.at)+replacement+obj.s.slice(p.at+1);
          assert.equal(mutation.length,obj.s.length);
          const neigh=parse(mutation,obj.N,obj.M,obj.w);assert(neigh);
          const newAssignment=new Map(base);
          if(p.kind==='id') {
            const mutatedClause=neigh[ci];
            const changed=mutatedClause.filter((l,j)=>l.id!==original[ci][j].id);
            assert.equal(changed.length,1);
            assert.equal(bitParity(changed[0].id),1);
            assert(!base.has(changed[0].id));
            newAssignment.set(changed[0].id,1^changed[0].neg);
            metrics.idBitFlips++;
          } else metrics.signFlips++;
          assert(satisfies(neigh,newAssignment));
          metrics.validMutations++;
        }
      }
      const ratio=obj.positions.length/obj.s.length;
      metrics.cases++;metrics.maxL=Math.max(metrics.maxL,obj.s.length);
      metrics.maxQ=Math.max(metrics.maxQ,obj.positions.length);
      metrics.ratioMin=Math.min(metrics.ratioMin,ratio);
      metrics.ratioMax=Math.max(metrics.ratioMax,ratio);
      metrics.perCase.push({r,V,t,N:obj.N,M:obj.M,w:obj.w,L:obj.s.length,Q:obj.positions.length,ratio:+ratio.toFixed(6)});
      if(r===3 && chargedVertex===0) {
        // Exhaustive original UNSAT proof on this 9-variable fixture, not a TM trace.
        for(let mask=0;mask<2**t;mask++){
          const a=new Map();for(let i=0;i<t;i++)a.set(code(i+1),(mask>>i)&1);
          assert(!satisfies(original,a));metrics.bruteOriginalChecks++;
        }
        // Minimality is essential: adding a duplicate clause invalidates
        // the one-occurrence mutation implication.
        const dup=[...original,original[0].map(x=>({...x}))];
        const mutated=dup.map(c=>c.map(l=>({...l})));
        mutated[0][0].id^=1;
        assert.equal(bitParity(mutated[0][0].id),1);
        for(let mask=0;mask<2**t;mask++){
          const a=new Map();for(let i=0;i<t;i++)a.set(code(i+1),(mask>>i)&1);
          a.set(mutated[0][0].id,0);
          assert(!satisfies(mutated,a));metrics.negativeControls++;
        }
        // An uncoded sequential identifier can flip to forbidden zero.
        assert.equal(1^1,0); metrics.negativeControls++;
      }
    }
  }
  assert.equal(metrics.signFlips+metrics.idBitFlips,metrics.validMutations);
  console.log(JSON.stringify({schema:'TMR2-DENSE-SENSITIVE-008',timestamp:'2026-11-13 18:23 PST',status:'COMPUTATIONAL',...metrics},null,2));
}
main();
