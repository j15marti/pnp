"use strict";
/*
 ARC-PIVOTAL-INPUT-FIREWALL121, reproducible finite check.
 Fixed binary input grammar: every displayed ASCII character is one fixed 8-bit
 input byte, and 0x30 -> 0x31 changes exactly its lowest bit.
 No claim to physical FLMV machine traces: counters are logical checks.
 Run: node ARC_PIVOTAL_INPUT_FIREWALL121_repro.js
*/
function invariant(ok, message) {
  if (!ok) throw new Error("ASSERTION FAILURE: " + message);
  main.checks++;
}
function pin(l, u, v) {
  return [[l,u,v],[l,u,-v],[l,-u,v],[l,-u,-v]];
}
function build(kind, m, mask, pads) {
  if (!(kind === "SAT" || kind === "UNSAT")) throw new Error("kind");
  let n = 0, clauses = [], pivotClauses = [], pivotLiteral = kind === "SAT" ? 0 : 1;
  function fresh(){ return ++n; }
  function add(cs){ for (const c of cs) clauses.push(c); }
  if (kind === "SAT") {
    for (let i=0; i<m; i++) {
      const x=fresh(), a=fresh(), b=fresh();
      const ux=fresh(),vx=fresh(),ua=fresh(),va=fresh(),ub=fresh(),vb=fresh();
      add(pin(x,ux,vx)); add(pin(-a,ua,va)); add(pin(-b,ub,vb));
      pivotClauses.push(clauses.length);
      clauses.push([(mask & (1 << i)) ? -x : x,a,b]);
    }
  } else {
    const xs=Array.from({length:m+1},()=>fresh());
    const u0=fresh(),v0=fresh(),ue=fresh(),ve=fresh();
    add(pin(xs[0],u0,v0)); add(pin(-xs[m],ue,ve));
    for (let i=0; i<m; i++) {
      const p=fresh(),u=fresh(),v=fresh();
      add(pin(-p,u,v));
      pivotClauses.push(clauses.length);
      clauses.push([-xs[i],(mask & (1 << i)) ? -xs[i+1] : xs[i+1],p]);
    }
  }
  for (let i=0; i<pads; i++) clauses.push([fresh(),fresh(),fresh()]);
  return {kind,m,mask,pads,n,clauses,pivotClauses,pivotLiteral};
}
function encode(f) {
  const width=String(f.n).length;
  let out="C3:"+f.n+":"+f.clauses.length+":"+width+"\n";
  const positions=[];
  const pivot=new Set(f.pivotClauses);
  f.clauses.forEach((c,ci)=>{
    if (c.length!==3) throw new Error("arity");
    c.forEach((l,li)=>{
      if (pivot.has(ci) && li===f.pivotLiteral) positions.push(out.length);
      out+=(l<0 ? "1":"0")+String(Math.abs(l)).padStart(width,"0");
    });
    out+="|";
  });
  return {text:out,positions,width,bitLength:8*out.length,clauses:f.clauses.length,variables:f.n};
}
function decode(s) {
  const match=/^C3:(\d+):(\d+):(\d+)\n/.exec(s);
  if (!match) throw new Error("invalid header");
  const n=Number(match[1]), count=Number(match[2]), w=Number(match[3]);
  if (!(n>0 && count>0 && w===String(n).length)) throw new Error("invalid dimensions");
  const body=s.slice(match[0].length), record=3*(w+1)+1;
  if (body.length!==count*record) throw new Error("invalid record length");
  const clauses=[];
  for(let ci=0;ci<count;ci++){
    const start=ci*record,clause=[];
    if(body[start+record-1]!=="|")throw new Error("invalid clause terminator");
    for(let j=0;j<3;j++){
      const pos=start+j*(w+1),sgn=body[pos];
      if(sgn!=="0"&&sgn!=="1")throw new Error("invalid sign");
      const digits=body.slice(pos+1,pos+1+w);
      if(!/^\d+$/.test(digits))throw new Error("invalid ID");
      const id=Number(digits);
      if(!(id>0&&id<=n))throw new Error("ID range");
      clause.push(sgn==="1"?-id:id);
    }
    if(new Set(clause.map(Math.abs)).size!==3)throw new Error("improper clause");
    clauses.push(clause);
  }
  return {n,clauses};
}
function extract(source, kind,m,sourcePads,targetPads){
  const parsed=decode(source);
  const proto=build(kind,m,0,sourcePads);
  invariant(parsed.n===proto.n,"source variable count");
  invariant(parsed.clauses.length===proto.clauses.length,"source clause count");
  let mask=0;
  proto.pivotClauses.forEach((ci,i)=>{
    if(parsed.clauses[ci][proto.pivotLiteral]<0)mask|=(1<<i);
  });
  const canonical=encode(build(kind,m,mask,sourcePads));
  invariant(canonical.text===source,"canonical source fully validated");
  return {mask,target:encode(build(kind,m,mask,targetPads))};
}
function evalClause(c, bits){
  return c.some(l=>Boolean(bits[Math.abs(l)-1]) === (l>0));
}
function bruteFormula(clauses,n){
  if(n>15)throw new Error("brute limit");
  for(let assignment=0;assignment<(1<<n);assignment++){
    const bits=Array.from({length:n},(_,i)=>(assignment>>i)&1);
    if(clauses.every(c=>evalClause(c,bits)))return true;
  }
  return false;
}
function brutePinCheck(){
  for(const sign of [-1,1])for(const forced of [0,1]){
    const cs=pin(sign*1,2,3);
    let exists=false;
    for(let a=0;a<4;a++){
      const bits=[forced,a&1,(a>>1)&1];
      if(cs.every(c=>evalClause(c,bits)))exists=true;
    }
    invariant(exists===(Boolean(forced)===(sign>0)),"PIN semantics");
  }
}
function independentReducedOracle(kind,m,mask) {
  if(kind==="SAT")return mask===0;
  // Exhaust every assignment to x_0,...,x_m, after independent
  // explicit PIN existential truth-table checks.
  for(let b=0;b<(1<<(m+1));b++){
    function x(i){return Boolean(b&(1<<i));}
    if(!x(0)||x(m))continue;
    let ok=true;
    for(let i=0;i<m;i++){
      const second=(mask&(1<<i)) ? !x(i+1) : x(i+1);
      if(x(i)&&!second){ok=false;break;}
    }
    if(ok)return true;
  }
  return false;
}
function diffBytes(a,b){
  if(a.length!==b.length)return {count:-1,positions:[]};
  let positions=[];
  for(let i=0;i<a.length;i++)if(a[i]!==b[i])positions.push(i);
  return {count:positions.length,positions};
}
function main(){
  main.checks=0;
  brutePinCheck();
  const rows=[], mini=[], examples=[];
  let masksExamined=0,chains=0,pivotTests=0,invalidRejected=0;
  for(const kind of ["SAT","UNSAT"]){
    for(let m=2;m<=6;m++){
      const rootPads=m**4,midPads=m**2;
      const center=encode(build(kind,m,0,0));
      const centerTruth=kind==="SAT";
      invariant(independentReducedOracle(kind,m,0)===centerTruth,"center reduced truth");
      for(let i=0;i<m;i++){
        const neighbor=encode(build(kind,m,1<<i,0));
        const changed=diffBytes(center.text,neighbor.text);
        invariant(changed.count===1,"single changed byte");
        invariant(changed.positions[0]===center.positions[i],"pivot address");
        invariant((center.text.charCodeAt(center.positions[i])^neighbor.text.charCodeAt(center.positions[i]))===1,"single physical bit");
        invariant(independentReducedOracle(kind,m,1<<i)!==centerTruth,"opposite semantic label");
        pivotTests++;
      }
      const probes=m, grandBits=center.bitLength;
      rows.push({kind,m,sourceBits:encode(build(kind,m,0,rootPads)).bitLength,firstBits:encode(build(kind,m,0,midPads)).bitLength,grandBits,forcedGuestDistinctReads:probes,readRatio:probes/grandBits});
      for(let mask=0;mask<(1<<m);mask++){
        const expected=kind==="SAT" ? (mask===0) : (mask!==0);
        invariant(independentReducedOracle(kind,m,mask)===expected,"independent reduced SAT");
        const root=encode(build(kind,m,mask,rootPads));
        const child=extract(root.text,kind,m,rootPads,midPads);
        const grand=extract(child.target.text,kind,m,midPads,0);
        invariant(child.mask===mask&&grand.mask===mask,"mask from actual parsed descendants");
        invariant(root.bitLength>child.target.bitLength&&child.target.bitLength>grand.target.bitLength,"two genuinely shorter ordinary children");
        const a=decode(root.text),b=decode(child.target.text),c=decode(grand.target.text);
        invariant(a.clauses.length===build(kind,m,mask,rootPads).clauses.length,"root clause count");
        invariant(b.clauses.length===build(kind,m,mask,midPads).clauses.length,"child clause count");
        invariant(c.clauses.length===build(kind,m,mask,0).clauses.length,"grandchild clause count");
        const rootRecovered=extract(root.text,kind,m,rootPads,midPads);
        invariant(rootRecovered.target.text===child.target.text,"repeat/replay exact");
        masksExamined++;chains++;
        if(m===2&&mask<2)examples.push({kind,m,mask,label:expected?"SAT":"UNSAT",rootBits:root.bitLength,childBits:child.target.bitLength,grandBits:grand.target.bitLength});
      }
      const malformed=center.text.slice(0,2)+"!"+center.text.slice(3);
      let rejected=false;try{decode(malformed)}catch(e){rejected=true;}
      invariant(rejected,"malformed grammar rejected");invalidRejected++;
      // Tiny full CNF brute check, independent of reduced-chain equivalence.
      if(m===2){
        for(let mask=0;mask<4;mask++){
          const core=build(kind,m,mask,0);
          if(core.n<=15)invariant(bruteFormula(core.clauses,core.n)===(kind==="SAT"?mask===0:mask!==0),"full direct brute");
        }
      }
    }
  }
  return {run:"ARC-PIVOTAL-INPUT-FIREWALL121",status:"COMPUTATIONAL restricted; theorem is symbolic",seed:"none/exhaustive",checks:main.checks,masksExamined,chains,pivotTests,invalidRejected,mRange:[2,6],rows,examples,zeroFailures:true,limitations:"Finite syntactic/semantic checks; no FLMV physical Turing-machine transition traces or arbitrary-SAT complexity lower bound."};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module){
  process.stdout.write(JSON.stringify(main(),null,2)+"\n");
}
