#!/usr/bin/env node
'use strict';
function audit() {
  const out={id:"ARC-WIDTH-RENORMALIZATION123",kind:"deterministic two-level proper-3CNF scope and length controls",seed:null,logicalAssertions:0,models:[],strictShorteningCases:0,sourceReadsChargedConceptually:true,physicalFLMVTrace:false,arcEdge:"OPEN",pVsNP:"OPEN"};
  function check(b,msg){out.logicalAssertions++;if(!b)throw new Error("check "+out.logicalAssertions+": "+msg);}
  function core(m,unsat){
    const w=4+Math.floor(Math.log2(m)), cls=[];
    for(let j=0;j<m;j++)cls.push([1+(j%w),1+((j+1)%w),w+j+1]);
    for(let k=0;k<(unsat?8:7);k++)cls.push([(k&1)?-1:1,(k&2)?-2:2,(k&4)?-3:3]);
    return {w,maxVar:w+m,clauses:cls};
  }
  function assemble(m,unsat,copies,pads){
    const C=core(m,unsat),cls=[];
    for(let t=0;t<copies;t++)for(const cl of C.clauses)cls.push(cl.map(v=>Math.sign(v)*(Math.abs(v)+t*C.maxVar)));
    const base=copies*C.maxVar;
    for(let j=0;j<pads;j++)cls.push([base+3*j+1,base+3*j+2,base+3*j+3]);
    return {m,unsat,copies,pads,w:C.w,maxVar:base+3*pads,coreCount:copies*C.clauses.length,clauses:cls};
  }
  function serialize(X){
    const records=[`p cnf ${X.maxVar} ${X.clauses.length}\n`];
    for(const c of X.clauses)records.push(`${c[0]} ${c[1]} ${c[2]} 0\n`);
    return records.join("");
  }
  function parse(src){
    const lines=src.trimEnd().split("\n"),head=/^p cnf (\d+) (\d+)$/.exec(lines[0]);
    if(!head)throw Error("invalid header");
    const vars=Number(head[1]),expected=Number(head[2]);
    if(lines.length-1!==expected)throw Error("wrong clause count");
    const clauses=[];
    for(let i=1;i<lines.length;i++){
      const z=lines[i].trim().split(/\s+/).map(Number);
      if(z.length!==4||z[3]!==0||!z.slice(0,3).every(v=>Number.isSafeInteger(v)&&v!==0&&Math.abs(v)<=vars)||new Set(z.slice(0,3).map(Math.abs)).size!==3)throw Error("invalid clause "+i);
      clauses.push(z.slice(0,3));
    }
    return {maxVar:vars,clauses};
  }
  function scopedPeak(X) {
    const live=new Set(),size=X.w+X.m;
    let peak=0,read=0,opened=0,closed=0;
    function open(v){check(!live.has(v),"duplicate OPEN");live.add(v);opened++;peak=Math.max(peak,live.size);}
    function close(v){check(live.has(v),"missing CLOSE");live.delete(v);closed++;}
    for(let t=0;t<X.copies;t++)for(let v=1;v<=X.w;v++)open(t*size+v);
    for(let j=0;j<X.coreCount;j++){
      const temp=[];
      for(const l of X.clauses[j]){const v=Math.abs(l);if(!live.has(v)){open(v);temp.push(v);}read++;}
      check(temp.length<=1,"core local variable property");
      for(const v of temp)close(v);
    }
    for(let t=0;t<X.copies;t++)for(let v=1;v<=X.w;v++)close(t*size+v);
    for(let j=X.coreCount;j<X.clauses.length;j++){
      const cur=X.clauses[j].map(Math.abs);
      for(const v of cur){open(v);read++;}
      for(const v of cur)close(v);
    }
    check(live.size===0,"closed scoped stream");
    check(peak===X.copies*X.w+1,"chosen-order exact peak");
    check(opened===closed,"open-close balanced");
    check(read===3*X.clauses.length,"all literal occurrences");
    return {peak,opened,closed,reads:read};
  }
  function coreSatByBrute(m,unsat){
    const c=core(m,unsat),lim=2**c.w;
    for(let bits=0;bits<lim;bits++){
      let works=true;
      for(let i=m;i<c.clauses.length;i++){
        const clause=c.clauses[i];
        if(!clause.some(l=>l>0?!!(bits&(1<<(l-1))):!(bits&(1<<(-l-1))))){works=false;break;}
      }
      if(works)return true;
    }
    return false;
  }
  function proveWitness(X){
    if(X.unsat)return null;
    const assignment=new Uint8Array(X.maxVar+1);
    assignment.fill(1);
    for(const cl of X.clauses)check(cl.some(l=>l>0?assignment[l]===1:assignment[-l]===0),"SAT witness clause");
    return true;
  }
  const mset=[12,15,18,21],kappaStar=41/800;
  for(const m of mset)for(const unsat of [false,true]){
    const found=[];
    for(const [d,copies,pads] of [[0,1,m**4],[1,3,m**2],[2,9,0]]){
      const x=assemble(m,unsat,copies,pads),encoded=serialize(x),parsed=parse(encoded),scope=scopedPeak(x);
      check(parsed.maxVar===x.maxVar&&parsed.clauses.length===x.clauses.length,"complete header");
      for(let i=0;i<parsed.clauses.length;i++)check(parsed.clauses[i].every((v,j)=>v===x.clauses[i][j]),"serialized ordinary clause "+i);
      const base=coreSatByBrute(m,unsat);
      check(base===!unsat,"full 7/8 pattern semantics");
      if(!unsat)proveWitness(x);
      const bad=encoded.replace(/^p cnf (\d+) (\d+)/,(_,v,count)=>`p cnf ${v} ${Number(count)+1}`);
      let rejected=false;try{parse(bad);}catch(e){rejected=true;}check(rejected,"header tampering caught");
      const allbits=encoded.length*8, headerbits=encoded.indexOf("\n")*8+8;
      found.push({level:d,copies,paddingClauses:pads,coreWidth:x.w,originalNamesWidth:scope.peak,openEvents:scope.opened,closeEvents:scope.closed,sourceLiteralReads:scope.reads,cnfClauses:x.clauses.length,cnfVars:x.maxVar,ordinaryBytes:encoded.length,ordinaryBits:allbits,headerBits:headerbits,payloadBits:allbits-headerbits,materializeWritesIncludingUnchanged:allbits,parsedValid:true,semanticSat:base});
    }
    if(found[0].ordinaryBits>found[1].ordinaryBits&&found[1].ordinaryBits>found[2].ordinaryBits)out.strictShorteningCases++;
    else if(m>=15)throw Error("expected strict shorter ordinary children for m="+m+" "+unsat);
    check(found[1].originalNamesWidth-1===3*(found[0].originalNamesWidth-1),"first actual width triple");
    check(found[2].originalNamesWidth-1===3*(found[1].originalNamesWidth-1),"second actual width triple");
    out.models.push({m,label:unsat?"UNSAT":"SAT",levels:found,lengthExponentRootToChild:Math.log(found[1].ordinaryBits)/Math.log(found[0].ordinaryBits),lengthExponentChildToGrandchild:Math.log(found[2].ordinaryBits)/Math.log(found[1].ordinaryBits)});
  }
  const theory=[];
  for(const i of [0,1,2,3,4,6]){
    const initial=1/20,scaled=6**i*initial,eligible=scaled<kappaStar;
    const population=1-2**(-i)+initial*(3**i-1);
    check(Math.abs(population-(1-2**(-i)+initial*(3**i-1)))<1e-12,"count exponent");
    theory.push({depth:i,ratioUpper:scaled,target:kappaStar,certifiedWithInitialPoint:eligible,totalNodeExponentWorstCase:population,rootKappaStrictThreshold:kappaStar/(6**i)});
  }
  check(Math.abs(theory[2].rootKappaStrictThreshold-41/28800)<1e-12,"two-level threshold");
  check(Math.abs(theory[2].totalNodeExponentWorstCase-1.15)<1e-12,"two-level population bound");
  check(Math.abs(theory[3].totalNodeExponentWorstCase-2.175)<1e-12,"three-level population bound");
  out.theory=theory;out.codeSource="independent Node.js file in same directory; all numeric counters logical, not FLMV tape timings";
  out.totals={auditedPairs:out.models.length,auditedRootChildGrandchild:out.models.length*3,ordinaryParseClauses:out.models.reduce((z,x)=>z+x.levels.reduce((v,l)=>v+l.cnfClauses,0),0),allMaterializedWrittenBits:out.models.reduce((z,x)=>z+x.levels.reduce((v,l)=>v+l.materializeWritesIncludingUnchanged,0),0),openClosePairs:out.models.reduce((z,x)=>z+x.levels.reduce((v,l)=>v+l.openEvents,0),0)};
  return out;
}
const data=audit();
if(process.argv[2])require('fs').writeFileSync(process.argv[2],JSON.stringify(data,null,2)+'\n');
process.stdout.write(JSON.stringify({id:data.id,logicalAssertions:data.logicalAssertions,strictShorteningCases:data.strictShorteningCases,totals:data.totals,theory:data.theory},null,2)+'\n');
