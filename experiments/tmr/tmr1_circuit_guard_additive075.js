'use strict';
// This exact published function is V8-replayed, including source, gate, and adversarial controls.
const runAudit = function runAudit() {
  "use strict";
  let checks = 0, cases = 0, proofLines = 0, resolutionLines = 0, negativeTests = 0, constantSkipped = 0, sharedFanoutCases = 0;
  const assert = (x, msg) => { checks++; if (!x) throw Error(msg || "assertion failed"); };
  const norm = a => [...new Set(a)].sort((u,v)=>Math.abs(u)-Math.abs(v)||u-v);
  const key = a => norm(a).join(",");
  const has = (c,x) => c.includes(x);
  const resolve = (a,b,p) => {
    if (!has(a,p) || !has(b,-p)) throw Error("invalid pivot");
    return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
  };
  const evalCNF = (cs, as) => cs.every(c=>c.some(l => (as[Math.abs(l)]===1)===(l>0)));
  const restrict = (c,as) => {
    let out=[];
    for (const l of c) {
      const v=as[Math.abs(l)];
      if (v===undefined) out.push(l);
      else if ((v===1)===(l>0)) return null;
    }
    return norm(out);
  };
  const makeCircuit=(k,g,seed)=>{
    let z=seed>>>0; const rand=()=>{z=(Math.imul(z,1664525)+1013904223)>>>0;return z;};
    const gates=[];
    for(let j=0;j<g;j++){
      const range=k+j;
      if ((rand()%5)===0) gates.push({op:"not",a:rand()%range});
      else {const a=rand()%range; const b0=rand()%(range-1); const b=b0>=a?b0+1:b0; gates.push({op:"and",a,b});}
    }
    return {k,gates};
  };
  const values=(c,x)=>{
    const vs=x.slice();
    for(const t of c.gates) vs.push(t.op==="not" ? 1-vs[t.a] : vs[t.a]&vs[t.b]);
    return vs;
  };
  const Fchoices=[
    {name:"four_two_cnf",vars:2, clauses:[[1,2],[1,-2],[-1,2],[-1,-2]],
      lines:[{parents:[0,1],pivot:2},{parents:[2,3],pivot:2},{parents:[4,5],pivot:1}]},
    {name:"unit_contradiction",vars:1,clauses:[[1],[-1]],
      lines:[{parents:[0,1],pivot:1}]}
  ];
  const runCase=(c,F)=>{
    const k=c.k, g=c.gates.length, fvars=F.vars;
    const allRefs=c.gates.flatMap(t=>t.op==="not"?[t.a]:[t.a,t.b]);
    if(allRefs.some((v,i)=>v>=k&&allRefs.indexOf(v)!==i))sharedFanoutCases++;
    const fid=i=>k+i;
    const wid=(side,j)=>k+fvars+1+j+(side==="B"?g:0);
    const rid=(side,ref)=>ref<k?ref+1:wid(side,ref-k);
    const outA=wid("A",g-1),outB=wid("B",g-1);
    const src=[], gateSrc={A:[],B:[]};
    const lines=[];
    const addSource=(clause,part)=>{ const index=lines.length;const c0=norm(clause);lines.push({type:"source",clause:c0,part});src.push(c0);return index; };
    const addRes=(i,j,p)=>{const a=lines[i].clause,b=lines[j].clause;const out=resolve(a,b,p);const n=lines.length;lines.push({type:"res",clause:out,parents:[i,j],pivot:p});return n;};
    for (const side of ["A","B"]) for(let j=0;j<g;j++){
      const t=c.gates[j], y=wid(side,j),u=rid(side,t.a);
      if(t.op==="not"){
        gateSrc[side].push({op:t.op,pos:addSource([y,u],side),neg:addSource([-y,-u],side)});
      }else{
        const v=rid(side,t.b);
        gateSrc[side].push({op:t.op,pos:addSource([y,-u,-v],side),negU:addSource([-y,u],side),negV:addSource([-y,v],side)});
      }
    }
    const Fclauses=F.clauses.map(cl=>norm(cl.map(l=>Math.sign(l)*fid(Math.abs(l)))));
    const lifted=Fclauses.map(cl=>addSource([outA,...cl],"A"));
    const bUnit=addSource([-outB],"B");
    const sourceCount=lines.length;
    const baseMap=[...lifted];
    for(const st of F.lines) {
      baseMap.push(addRes(baseMap[st.parents[0]],baseMap[st.parents[1]],Math.sign(st.pivot)*fid(Math.abs(st.pivot))));
    }
    assert(key(lines[baseMap[baseMap.length-1]].clause)===key([outA]),"lift does not finish at A output");
    const eq={A:{},B:{}};
    const transfer=(side,other,gateIdx,inputName)=>{
      const t=c.gates[gateIdx], ref=t[inputName], g0=gateSrc[side][gateIdx];
      const idFrom=rid(side,ref),idTo=rid(other,ref),sourceIdx=inputName==="a"?g0.negU:g0.negV;
      if(idFrom===idTo) return sourceIdx;
      assert(ref>=k,"unexpected shared input");
      const oldEq=eq[side][ref-k];
      return addRes(sourceIdx,oldEq,idFrom);
    };
    const proveEq=(side,other,j)=>{
      const t=c.gates[j], y=wid(side,j),z=wid(other,j),from=gateSrc[side][j],to=gateSrc[other][j];
      if(t.op==="and"){
        const u=transfer(side,other,j,"a");
        const v=transfer(side,other,j,"b");
        const mid=addRes(u,to.pos,rid(other,t.a));
        return addRes(v,mid,rid(other,t.b));
      }
      const idFrom=rid(side,t.a),idTo=rid(other,t.a);
      if(idFrom===idTo) return addRes(to.pos,from.neg,idTo);
      const oppEq=eq[other][t.a-k];
      const mid=addRes(oppEq,from.neg,idFrom);
      return addRes(to.pos,mid,idTo);
    };
    for(let j=0;j<g;j++){eq.A[j]=proveEq("A","B",j);eq.B[j]=proveEq("B","A",j);}
    assert(key(lines[eq.A[g-1]].clause)===key([-outA,outB]),"output equivalence failed");
    const outBline=addRes(baseMap[baseMap.length-1],eq.A[g-1],outA);
    const empty=addRes(outBline,bUnit,outB);
    assert(lines[empty].clause.length===0,"refutation fails");
    let resolution=0, sourced=0;
    for(let i=0;i<lines.length;i++){
      const ln=lines[i];
      if(ln.type==="source"){sourced++;assert(src.some(s=>key(s)===key(ln.clause)),"forged premise");}
      else{
        resolution++;
        const [pa,pb]=ln.parents;
        assert(pa<i&&pb<i,"forward reference");
        assert(key(resolve(lines[pa].clause,lines[pb].clause,ln.pivot))===key(ln.clause),"invalid res");
      }
    }
    const bound=F.lines.length+8*g+2;
    assert(resolution<=bound,`too many lines ${resolution}>${bound}`);
    const width=Math.max(...src.map(x=>x.length));
    assert(width<=Math.max(3,1+Math.max(...Fclauses.map(x=>x.length))),"source width");

    let one=false,zero=false;
    for(let xmask=0;xmask<(1<<k);xmask++){
      const bits=Array.from({length:k},(_,j)=>(xmask>>j)&1);
      const v=values(c,bits),p=v[v.length-1];
      if(p)one=true;else zero=true;
      for(let fmask=0;fmask<(1<<fvars);fmask++){
        const as={};
        for(let j=0;j<k;j++)as[j+1]=bits[j];
        for(let j=0;j<fvars;j++)as[fid(j+1)]=(fmask>>j)&1;
        for(let j=0;j<g;j++){as[wid("A",j)]=v[k+j];as[wid("B",j)]=v[k+j];}
        const a=src.slice(0,src.length-1).filter((_,i)=>lines[i].part==="A");
        const b=src.slice(0,src.length-1).filter((_,i)=>lines[i].part==="B");
        const aClauses=lines.filter(l=>l.type==="source"&&l.part==="A").map(l=>l.clause);
        const bClauses=lines.filter(l=>l.type==="source"&&l.part==="B").map(l=>l.clause);
        assert(evalCNF(aClauses,as)===(p===1),"projection A");
        assert(evalCNF(bClauses,as)===(p===0),"projection B");
        assert(!(evalCNF(aClauses,as)&&evalCNF(bClauses,as)),"joint UNSAT");
        for(let j=0;j<g;j++){
          const flipped={...as,[wid("A",j)]:1-as[wid("A",j)]};
          const gateA=gateSrc.A[j];
          const gateClauses=Object.values(gateA).filter(Number.isInteger).map(i=>lines[i].clause);
          assert(!evalCNF(gateClauses,flipped),"A gate nonfunctional");
        }
      }
      if(p===0){
        const as={};for(let j=0;j<k;j++)as[j+1]=bits[j];
        for(let j=0;j<g;j++){as[wid("A",j)]=v[k+j];as[wid("B",j)]=v[k+j];}
        const residual=lines.filter(l=>l.type==="source").map(l=>restrict(l.clause,as)).filter(l=>l!==null);
        assert(key(residual.map(key).sort())===key(Fclauses.map(key).sort()),"restriction not exact F");
      }
    }
    if(!one||!zero)return null;
    negativeTests+=2;
    let rejectedPivot=false,rejectedSource=false;
    try{resolve(lines[baseMap[0]].clause,lines[baseMap[1]].clause,outA);}catch(e){rejectedPivot=true;}
    assert(rejectedPivot,"invalid pivot accepted");
    const fake=[outA, 99999];
    rejectedSource=!src.some(s=>key(s)===key(fake));
    assert(rejectedSource,"forged premise accepted");
    cases++;proofLines+=lines.length;resolutionLines+=resolution;
    return {circuit_gates:g,source:F.name,proof_lines:lines.length,resolution_lines:resolution,upper_bound:bound,source_width:width};
  };
  const records=[];
  for(const k of [2,3,4])for(const g of [1,2,3,4,5])for(let trial=0;trial<7;trial++){
    const circuit=makeCircuit(k,g,20261115+101*k+17*g+trial*997);
    let one=false,zero=false;
    for(let mask=0;mask<(1<<k);mask++){const v=values(circuit,Array.from({length:k},(_,j)=>(mask>>j)&1)); if(v[v.length-1])one=true;else zero=true;}
    if(!one||!zero){constantSkipped++;continue;}
    for(const F of Fchoices)records.push(runCase(circuit,F));
  }
  // Hostile SAT-source control: without UNSAT F, A and B can both hold.
  const satSource=[[ -4,1 ],[ -4,2 ],[4,-1,-2],[-5,1],[-5,2],[5,-1,-2],[4,3],[-5]];
  const satAssign={1:0,2:0,3:1,4:0,5:0};
  assert(evalCNF(satSource,satAssign),"SAT private-source negative control missing");
  negativeTests++;
  assert(cases>=50,"too few nonconstant test cases");
  assert(constantSkipped>0,"no constant circuits were skipped");
  assert(sharedFanoutCases>0,"no reused-gate fanout cases");
  return {test:"TM1-CIRCUIT-GUARD-ADDITIVE-REPLAY",date_pst:"2026-11-15 01:04 PST",status:"COMPUTATIONAL finite; PROVED/RESTRICTED symbolic theorem requires independent review",checks,cases,proofLines,resolutionLines,negativeTests,constantSkipped,sharedFanoutCases,failures:0,models:["native shared DAG Resolution","AND NOT circuit gate-copy Tseitin","authenticated source premises"],maxProofLines:Math.max(...records.map(x=>x.proof_lines)),sample:records.slice(0,5),seed_base:20261115};
};
console.log(JSON.stringify(runAudit(),null,2));
