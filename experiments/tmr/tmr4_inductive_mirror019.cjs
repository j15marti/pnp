// TMR-4/019 standalone V8/Node-compatible finite controller exact replay
// One physical locally moving read-only head; two 1-cell work tapes.
// Run: node experiments/tmr/tmr4_inductive_mirror019.cjs
function run019() {
  "use strict";
  const P=(x)=>[...x].reduce((a,b)=>a^(b==="1"?1:0),0);
  const get=(x,p)=>p===0?"LEFT":p===x.length+1?"RIGHT":x[p-1];
  const proj=(s)=>({phase:s.phase,p:s.p,c:s.c,mask:s.mask,buf:s.buf,label:s.label});
  const I=(s,x)=>s.b===s.c && (s.phase==="S"?s.c===P(x.slice(0,Math.max(0,s.p-1))):s.c===P(x));
  const J=(a,x)=>a.phase==="S"?a.c===P(x.slice(0,Math.max(0,a.p-1))):a.c===P(x);
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const phi=(s,x)=>{let q=x.length+1,z=P(x);switch(s.phase){case"S":return 3*q-s.p+1+2*q*z;case"R":return s.p+q+1+2*q*z;case"D":return 3*q-s.p+1;case"E":return s.p+q+1;case"A":return q-s.p+1;case"H":return 0;default:throw Error("phase")}};
  function next(s,x,abstract){
    let t={...s},q=x.length+1,p=s.p;
    if(s.phase==="H")throw Error("halted");
    let observed=get(x,p); // one local current-cell observation per charged transition
    switch(s.phase){
      case "S":
        if(!(p<q && observed!=="RIGHT"))throw Error("S-position");
        if(observed==="1"){if(!abstract)t.b^=1;t.c^=1;}
        t.p++;if(t.p===q)t.phase="R";break;
      case "R":
        if(!(p>0))throw Error("R-position");
        t.p--;if(t.p===0)t.phase=(abstract?t.c:t.b)?"D":"A";break;
      case "D":
        if(!(p<q))throw Error("D-position");
        t.p++;if(t.p===q)t.phase="E";break;
      case "E":
        if(!(p>0))throw Error("E-position");
        t.p--;if(t.p===0)t.phase="A";break;
      case "A":
        if(p===q) {
          t.phase="H";t.label=t.buf?"MALFORMED":t.mask===255?"UNSAT":"SAT";
        }else{
          if(observed==="0"||observed==="1"){t.buf+=observed;if(t.buf.length===3){t.mask|=(1<<parseInt(t.buf,2));t.buf="";}}
          else if(observed!=="LEFT")throw Error("A-cell");
          t.p++;
        }break;
      default:throw Error("phase");
    }
    return t;
  }
  function independent(x){
    if(x.length%3)return "MALFORMED";
    for(let a=0;a<8;a++){let ok=true;for(let j=0;j<x.length;j+=3)if(parseInt(x.slice(j,j+3),2)===a){ok=false;break}if(ok)return "SAT";}
    return "UNSAT";
  }
  let r={run_id:"TMR4-IM19",seed:120140419,model:"one local source head; two one-cell mirrored work tapes; restricted 3-variable clause sign stream",inputs:0,edges:0,charged_concrete_transitions:0,charged_abstract_transitions:0,current_cell_input_observations:0,abstract_potential_tight_edges:0,labels:{SAT:0,UNSAT:0,MALFORMED:0},parity:{"0":0,"1":0},MAY_erasure_fake_shortcuts:0,MAY_erasure_missing_transitions:0,visited_writable_cells_concrete_peak:2,visited_writable_cells_quotient_peak:2,on_diagonal_gate_cases:0,off_diagonal_gate_counterexamples:0,assertion_failures:0};
  for(let u of ["LEFT","0","1","RIGHT"])for(let b=0;b<2;b++)for(let c=0;c<2;c++){let same=(b?"D":"A")===(c?"D":"A"); if((b===c)!==same)throw Error("fiber");if(same)r.on_diagonal_gate_cases++;else r.off_diagonal_gate_counterexamples++;}
  function test(x){
    const q=x.length+1,z=P(x);
    let s={phase:"S",p:0,b:0,c:0,mask:0,buf:"",label:""},a=proj(s),steps=0;
    if(!I(s,x)||!J(a,x)||phi(a,x)!==3*q+1+2*q*z)throw Error("start");
    while(s.phase!=="H"){
      if(!I(s,x)||!J(a,x)||!eq(proj(s),a))throw Error("invariant");
      const ns=next(s,x,false),na=next(a,x,true);
      if(!eq(proj(ns),na)||!I(ns,x)||!J(na,x))throw Error("step-simulation");
      if(phi(a,x)!==1+phi(na,x))throw Error("Bellman");
      s=ns;a=na;steps++;
      if(steps>5*q+2)throw Error("loop");
    }
    if(s.label!==independent(x)||steps!==3*q+1+2*q*z||phi(a,x)!==0)throw Error("terminal-or-runtime");
    r.inputs++;r.edges+=steps;r.charged_concrete_transitions+=steps;r.charged_abstract_transitions+=steps;r.current_cell_input_observations+=steps;r.abstract_potential_tight_edges+=steps;r.labels[s.label]++;r.parity[String(z)]++;
    if(z){r.MAY_erasure_fake_shortcuts++;r.MAY_erasure_missing_transitions+=2*q;}
  }
  for(let n=0;n<=11;n++)for(let v=0;v<2**n;v++)test(v.toString(2).padStart(n,"0").slice(n===0?1:0));
  let extra=["000001010011100101110111","001010100111","000".repeat(20),"111".repeat(21),"100".repeat(11),"101".repeat(17),"0".repeat(100),"1".repeat(101)];
  for(let n of [24,27,48,63,96,99])for(let j=0;j<6;j++){let s="";for(let k=0;k<n;k++)s+=(((k*13+j*7+n*3)%19)<9)?"0":"1";extra.push(s);}
  for(const x of extra)test(x);
  r.extra_fixtures=extra.length;
  if(r.inputs!==4095+extra.length)throw Error("count");
  r.status="COMPUTATIONAL finite runs; CANDIDATE/RESTRICTED symbolic theorem; P versus NP OPEN";
  return r;
}
console.log(JSON.stringify(run019(),null,2));
