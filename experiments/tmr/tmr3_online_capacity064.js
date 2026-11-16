"use strict";
// Executable exact finite audit, TMR-3/064. JavaScript function below was executed unchanged in this tool.
function audit(){
  "use strict";
  const REV="tmr3-online-capacity064-v1";
  let checks=0, cases=0, malformed=0, executions=0, accepted=0, overflow=0, mismatch=0, maxWidth=0, totalQueries=0, maxQueries=0, zeroWidth=0;
  function ok(cond,why){checks++;if(!cond)throw Error("assert "+checks+": "+why);}
  function parse(s){
    if(!s || /[^01]/.test(s))return null;
    let n=0;while(n<s.length && s[n]==="1")n++;
    if(n<1||s[n]!=="0"||s.length!==2*n+1)return null;
    return [...s.slice(n+1)].map(Number);
  }
  function headAt(x,h,j){
    let pos=0;
    for(let k=0;k<j;k++){
      const right=(h===0 ? x[k]===1 : x[k]===0);
      pos=right?pos+1:Math.max(0,pos-1);
    }
    return pos;
  }
  function gen(x,c,h,j){
    const B=x.length;
    if(c===0)return Math.min(j,B-1-j);
    if(c===1)return 0;
    let pos=headAt(x,h,j);
    if(c===2)return pos;
    if(c===3)return pos+(j===Math.floor(B/2)?1:0);
    if(c===4){
      const cut=Math.floor(3*B/4);
      return j<cut?pos:headAt(x,h,cut);
    }
    throw Error("bad candidate");
  }
  function genuine(x){
    const cells=new Map(),pos=[0,0];let q=0;
    const words=[[],[]];
    for(let j=0;j<x.length;j++){
      for(let h=0;h<2;h++)words[h].push(pos[h]);
      const a="0:"+pos[0],b="1:"+pos[1];
      const v0=(cells.get(a)||0)^x[j],v1=(cells.get(b)||0)^v0;
      cells.set(a,v0);cells.set(b,v1);q^=v1;
      for(let h=0;h<2;h++){
        const right=h===0?x[j]===1:x[j]===0;
        pos[h]=right?pos[h]+1:Math.max(0,pos[h]-1);
      }
    }
    return {q,words};
  }
  function width(x,c){
    let maximum=0;
    for(let j=0;j<x.length;j++){
      let live=new Set();
      for(let h=0;h<2;h++)for(let i=0;i<=j;i++){
        const a=gen(x,c,h,i);
        for(let k=j+1;k<x.length;k++)
          if(gen(x,c,h,k)===a){live.add(h+":"+a);break;}
      }
      maximum=Math.max(maximum,live.size);
    }
    return maximum;
  }
  function attempt(x,c,H){
    const cache=new Map(),heads=[0,0];let q=0,query=0,peak=0;
    function G(h,j){query++;return gen(x,c,h,j);}
    for(let j=0;j<x.length;j++){
      let key=[],vals=[];
      for(let h=0;h<2;h++){
        const z=G(h,j);
        if(z!==heads[h])return {status:"MISMATCH",queries:query,peak};
        key.push(h+":"+z);
      }
      let v0=(cache.get(key[0])||0)^x[j];
      let v1=(cache.get(key[1])||0)^v0;
      vals=[v0,v1];q^=v1;
      const later=[false,false];
      for(let h=0;h<2;h++){
        for(let r=j+1;r<x.length;r++){
          if(G(h,r)===heads[h]){later[h]=true;break;}
        }
      }
      // Drop all dead blocks BEFORE inserting any updated live blocks.
      for(let h=0;h<2;h++)if(!later[h])cache.delete(key[h]);
      for(let h=0;h<2;h++)if(later[h]){
        if(!cache.has(key[h])&&cache.size>=H)return {status:"OVERFLOW",queries:query,peak};
        cache.set(key[h],vals[h]);
      }
      peak=Math.max(peak,cache.size);
      ok(peak<=H,"capacity never exceeded");
      for(let h=0;h<2;h++){
        const right=h===0?x[j]===1:x[j]===0;
        heads[h]=right?heads[h]+1:Math.max(0,heads[h]-1);
      }
    }
    return {status:"MATCH",q,queries:query,peak};
  }
  function run(x){
    const B=x.length,w=width(x,2),original=genuine(x);
    ok(original.words.length===2,"genuine two tapes");
    for(let h=0;h<2;h++)for(let j=0;j<B;j++)
      ok(gen(x,2,h,j)===original.words[h][j],"source-generated authentic word");
    const authentic=attempt(x,2,w);
    ok(authentic.status==="MATCH" && authentic.q===original.q,"exact authentic replay");
    ok(authentic.queries<=B*(B+1),"quadratic index bound on authentic replay");
    if(w>0)ok(attempt(x,2,w-1).status==="OVERFLOW","authentic capacity is exact");
    let rounds=0,H=0,found=null,sumQ=0;
    const R=2+Math.ceil(Math.log2(2*B+1));
    while(rounds<R){
      rounds++;
      for(const c of [0,1,3,4,2]){
        const r=attempt(x,c,H);executions++;sumQ+=r.queries;
        ok(r.queries<=B*(B+1),"per-attempt G bound");
        if(r.status==="OVERFLOW")overflow++;
        if(r.status==="MISMATCH")mismatch++;
        if(r.status==="MATCH"){
          accepted++;
          ok(r.q===original.q,"no wrong output on success");
          found={answer:r.q,H,rounds};
          break;
        }
      }
      if(found)break;
      H=H===0?1:H*2;
    }
    ok(found!==null,"coverage ensures termination");
    ok(found.H <= 2*Math.max(1,w),"no large false-candidate cache");
    ok(found.rounds<=R,"round count bound");
    ok(sumQ<=5*R*B*(B+1),"total G bound");
    totalQueries+=sumQ;maxQueries=Math.max(maxQueries,sumQ);
    maxWidth=Math.max(maxWidth,w);
    if(w===0)zeroWidth++;
    return found;
  }
  for(let B=4;B<=8;B++)for(let bits=0;bits<(1<<B);bits++){
    const x=Array.from({length:B},(_,j)=>(bits>>(B-1-j))&1);
    const source="1".repeat(B)+"0"+x.join("");
    ok(JSON.stringify(parse(source))===JSON.stringify(x),"authenticated roundtrip");
    for(const bad of [source+"0",source.slice(1),source+"x"]){
      ok(parse(bad)===null,"malformed rejected");malformed++;
    }
    run(x);cases++;
  }
  // Boundary and unique-case controls.
  for(const s of ["", "0", "1", "10", "110", "1110000x", "0101"])ok(parse(s)===null,"boundary malformed");
  return {revision:REV,seed:null,model:"finite b=1 local-head two-tape authenticated simulation; generator bit operations instrumented by calls only",
    source_encoding:"1^B 0 x, B=4..8 exhaustive; x_j drives both local work-head motions; each stage reads/writes canonical cells",
    cases,malformed_rejections:malformed,attempts:executions,accepted_attempts:accepted,cache_overflows:overflow,wrong_schedule_rejections:mismatch,
    zero_frontier_sources:zeroWidth,max_authentic_frontier:maxWidth,generator_calls:totalQueries,
    max_calls_one_source:maxQueries,assertions:checks,failures:0,
    theoretical_per_candidate_G_max:"p*B*(B+1)/2, p=2",
    limitations:["Finite b=1 microstage model; not an implementation of legal-width HPV conversion.",
      "JavaScript Maps store full finite test data, not a physical low-space certification.",
      "Candidate generator is specially source-indexable; no general polynomial candidate coverage.",
      "The generic nonassociative Tree Evaluation improvement remains OPEN.",
      "Query counts are exact calls; native local input-head seeks and bit-machine costs are proved symbolically, not microtraced."]};
}
console.log(JSON.stringify(audit(),null,2));
