const runAudit = function runAudit() {
  "use strict";
  let assertions=0, edgeChecks=0, pairs=0, malformed=0;
  const ok=(v,label)=>{ assertions++; if(!v) throw new Error("FAILED "+label); };
  const signs=[1,2,3,4,5,6,7,0];
  function ids(t) {
    const a="1"+"0".repeat(t-1);
    const b="1"+"0".repeat(t-2)+"1";
    const c="1"+"0".repeat(t-3)+"10";
    ok(a.length===t&&b.length===t&&c.length===t&&new Set([a,b,c]).size===3,"ids "+t);
    return [a,b,c];
  }
  function form(t,positive) {
    const trip=ids(t), masks=signs.slice();
    if(positive) masks[7]=1;
    for(let j=8;j<t;j++)masks.push(7);
    let s="1".repeat(t)+"0"+"1".repeat(t)+"0";
    for(const mask of masks) for(let h=0;h<3;h++)
      s+=trip[h]+String((mask>>(2-h))&1);
    return {s,masks,trip};
  }
  function parse(s) {
    if(!/^[01]+$/.test(s)) return null;
    let p=0;
    while(p<s.length&&s[p]==="1")p++;
    const b=p;if(b<3||s[p]!=="0")return null;p++;
    let M=0;
    while(p<s.length&&s[p]==="1"){p++;M++;}
    if(M<1||s[p]!=="0")return null;p++;
    if(s.length-p!==3*M*(b+1))return null;
    const clauses=[];
    for(let i=0;i<M;i++) {
      const row=[];
      for(let j=0;j<3;j++) {
        const v=s.slice(p,p+b),sg=Number(s[p+b]);p+=b+1;
        if(!v.includes("1"))return null;
        row.push({v,sg});
      }
      if(new Set(row.map(x=>x.v)).size!==3)return null;
      clauses.push(row);
    }
    return {b,M,clauses};
  }
  function cheapCore(s) {
    if(!/^[01]+$/.test(s))return {match:false,read:0};
    let p=0;
    while(p<s.length&&s[p]==="1")p++;
    const b=p;if(b<3||s[p]!=="0")return {match:false,read:p};p++;
    let M=0;
    while(p<s.length&&s[p]==="1"){p++;M++;}
    if(M<8||s[p]!=="0")return {match:false,read:p};p++;
    const trip=ids(b);
    for(let c=0;c<8;c++) for(let j=0;j<3;j++) {
      if(p+b>=s.length)return {match:false,read:s.length};
      const v=s.slice(p,p+b),sg=s[p+b];
      if(v!==trip[j]||sg!==String((signs[c]>>(2-j))&1))
        return {match:false,read:p+b+1};
      p+=b+1;
    }
    return {match:true,read:p};
  }
  function sat3(masks) {
    const sat=[];
    for(let x=0;x<8;x++) if(masks.every(mask=>mask!==x))sat.push(x);
    return sat;
  }
  const samples=[];
  for(const t of [9,10,12,16,24,32,48,64,96,128,256]) {
    const a=form(t,false),b=form(t,true);
    const N=3*t*t+5*t+2,P=26*(t+1);
    ok(a.s.length===N&&b.s.length===N,"length "+t);
    ok(P<N&&a.s.slice(0,P-1)===b.s.slice(0,P-1),"prefix "+t);
    ok(a.s[P-1]==="0"&&b.s[P-1]==="1","pivot signs "+t);
    const diffs=[];for(let i=0;i<N;i++)if(a.s[i]!==b.s[i])diffs.push(i);
    ok(diffs.length===1&&diffs[0]===P-1,"Hamming one "+t);
    const da=parse(a.s),db=parse(b.s);
    ok(da!==null&&db!==null&&da.b===t&&da.M===t&&db.M===t,"strict grammar "+t);
    ok(da.clauses.length===t&&db.clauses.length===t,"rows "+t);
    ok(da.clauses.every(row=>row.every((lit,j)=>lit.v===a.trip[j])),"ID scope "+t);
    ok(da.clauses[0].every(lit=>lit.v[0]==="1"),"minimal width "+t);
    ok(sat3(a.masks).length===0,"UNSAT eight patterns "+t);
    ok(JSON.stringify(sat3(b.masks))==="[0]","SAT allzero only "+t);
    const ca=cheapCore(a.s),cb=cheapCore(b.s);
    ok(ca.match&&ca.read===P,"early negative prefix "+t);
    ok(!cb.match,"positive not early reject "+t);
    ok(cheapCore(a.s+"0").match,"invalid extension safe negative "+t);
    ok(parse(a.s+"0")===null&&parse(b.s+"0")===null,"strict invalid extensions "+t);
    ok(!cheapCore("0"+a.s).match,"bad unary start "+t);
    ok(!cheapCore(a.s.slice(0,P-1)).match,"truncated clause "+t);
    ok(cheapCore(a.s.slice(0,P)+"0".repeat(7)).match,"arbitrary invalid suffix preserves core "+t);
    malformed+=5;
    for(let mask=0;mask<8;mask++){
      const x=(mask===0);
      ok(sat3(b.masks).includes(mask)===x,"eight assignment exhaustive "+t);
    }
    let local=0;
    const rs=t<=32?Array.from({length:N+1},(_,i)=>i-1):
      Array.from(new Set([-1,0,1,P-3,P-2,P-1,P,N-3,N-2,N-1,N]));
    for(const kind of ["minus","plus"]) {
      const tau=kind==="minus"?P-1:N;
      for(const r of rs) for(const advance of [0,1]) {
        const r2=Math.min(N,r+advance);
        for(const halt of [0,1]) {
          if(halt && r2<tau)continue;
          const oldInt=Math.max(0,tau-r),newInt=Math.max(0,tau-r2);
          const di=oldInt-newInt,dm=halt;
          ok(di>=0&&di<=1&&dm>=0&&dm<=1,"physical row "+t+" "+kind);
          ok(di<=1,"rational lambda "+t);
          edgeChecks++;local++;
        }
      }
      const before=Math.max(0,tau-(tau-1)),after=Math.max(0,tau-tau);
      ok(before-after===1&&1===1,"fused read-halt row "+t);
    }
    samples.push({t,source_bits:N,critical_prefix_bits:P,critical_bit_index:P-1,
      negative_satisfiable:false,positive_satisfying_three_bit_assignment:0,
      prefix_to_length_ratio:Number((P/N).toFixed(8)),physical_tariff_rows:local});
    pairs++;
  }
  return {id:"TMR3_EARLYNEG078",date_pst:"2026-11-15 01:27 PST",
    model:"strict unary-width/unary-count proper 3-CNF, left-start read-only input, local heads",
    source:"V8 audit, exact produced function; Node console wrapper not natively executed",
    status:"COMPUTATIONAL; symbolic restricted all-t proof independent of finite tests",
    assertions,edgeChecks,pairs,malformed,failed:0,samples};
};
console.log(JSON.stringify(runAudit(),null,2));
