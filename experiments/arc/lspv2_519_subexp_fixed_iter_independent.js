// LSPV-2/519 independent pure JavaScript finite check.
// No source imports; exact scope is arithmetic envelope + K4 original strict 3-CNF.
const verify = function(){
  "use strict";
  let checks=0;const assert=(ok,why)=>{checks++;if(!ok)throw Error(why)};
  const beta=t=>((t+2)/(t*t)-t)/2;
  let lo=1.2,hi=1.25;
  for(let i=0;i<90;i++){let m=(lo+hi)/2;if(beta(m)>0.5)lo=m;else hi=m;}
  const root=(lo+hi)/2;
  assert(Math.abs(beta(1.2)-.5-1/90)<1e-12,"gap");
  assert(Math.abs(beta(root)-.5)<1e-12,"root");
  const PS=[12,16,24,32,48,64,96,128],rows=[];
  for(const p of PS){
    const n=2**p,N=n*(p+1);
    const t0=2+n*Math.log2(p)**2/(Math.sqrt(p)*Math.log2(N));
    const f=t=>Math.max(1.1,.6+.5*t);
    assert(t0>root,"positive upper envelope");
    for(const fixed of [4,8,12]){
      const tj=1.2+(t0-1.2)/2**fixed;
      assert(Math.abs(tj-(function(){let t=t0;for(let k=0;k<fixed;k++)t=f(t);return t;})())<=Math.max(1e-9,tj*1e-13),"closed recurrence");
    }
    let j=0;
    while(1.2+(t0-1.2)/2**j >=root){j++;assert(j<250,"iteration cutoff");}
    assert(1.2+(t0-1.2)/2**(j-1)>=root,"minimality");
    rows.push({p,t0,j});
  }
  assert(rows.every((r,i)=>i===0||r.j>rows[i-1].j),"strict growth in sample");
  const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], incidence=[0,1,2,3].map(v=>E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean));
  function clauses(charge) {
    let all=[];
    for(let v=0;v<4;v++)for(let mask=0;mask<8;mask++){
      const parity=((mask&1)+((mask>>1)&1)+((mask>>2)&1))&1;
      if(parity!==((charge>>v)&1))all.push(incidence[v].map((e,i)=>(mask>>i)&1?-e:e));
    }
    return all;
  }
  function encode(cs){return "p cnf 6 16\n"+cs.map(c=>c.join(" ")+" 0\n").join("");}
  function parse(s){
    const lines=s.trimEnd().split("\n");
    if(lines.length!==17||lines[0]!=="p cnf 6 16")throw Error("MALFORMED");
    return lines.slice(1).map(line=>{
      const ints=line.trim().split(/\s+/).map(Number);
      if(ints.length!==4||ints[3]!==0||!ints.slice(0,3).every(Number.isInteger)||
         !ints.slice(0,3).every(v=>v!==0&&Math.abs(v)<=6)||
         new Set(ints.slice(0,3).map(Math.abs)).size!==3)throw Error("MALFORMED");
      return ints.slice(0,3);
    });
  }
  function sat(cs){
    for(let mask=0;mask<64;mask++)if(cs.every(c=>c.some(l=>l>0?Boolean((mask>>(l-1))&1):!Boolean((mask>>(-l-1))&1))))return true;
    return false;
  }
  let counts={SAT:0,UNSAT:0,MALFORMED:0},sources=[];
  for(let charge=0;charge<16;charge++){
    let txt=encode(clauses(charge)),cs=parse(txt),r=sat(cs);
    assert(cs.length===16&&cs.every(c=>c.length===3),"proper 3CNF");
    assert(r===((charge.toString(2).replaceAll("0","").length%2)===0),"parity");
    counts[r?"SAT":"UNSAT"]++;
    sources.push({charge,bytes:txt.length});
  }
  const good=encode(clauses(0));
  const damaged=["","p cnf 6 15\n","\uffff",good.split("\n").slice(0,-2).join("\n"),good.replace(" 0\n"," 7\n"),good.replace(" 0\n"," 0 0\n")];
  for(const bad of damaged){let rejected=false;try{parse(bad)}catch(e){rejected=true}assert(rejected,"malformed must reject");counts.MALFORMED++;}
  return {checks,root,rows,controls:counts,source_samples:sources,assertion_scope:"Pure JS/Number finite arithmetic and K4 DIMACS truth tables. No FLMV machine, Lean build, historical R_mix341 checker or asymptotic SAT hardness."};
};
if (typeof console !== 'undefined') console.log(JSON.stringify(verify(), null, 2));
