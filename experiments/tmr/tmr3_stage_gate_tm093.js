"use strict";
// Executed body below is preserved exactly as V8 audit() function.
// Reproduce: node experiments/tmr/tmr3_stage_gate_tm093.js
function audit() {
  "use strict";
  const stats={cases:0,transitions:0,assertions:0,failures:0,rows:{},activationControls:0,physicalWriteControls:0,seed:"deterministic-exhaustive"};
  function check(cond,msg){stats.assertions++;if(!cond){stats.failures++;throw Error(msg);}}
  const get=(s,j)=>s.work.get(j)??"_";
  function potential(s,n){
    let q=0;for(let j=1;j<n;j++)if(get(s,j)!=="g")q++;
    const f=get(s,0)==="1"?0:n-1;
    const m=n-s.r+(s.state==="HALT"?0:1);
    return [0,0,0,f,0,q,m];
  }
  function make(n){return {input:"1".repeat(n)+"#",work:new Map(),ip:0,wp:0,r:-1,state:"INIT",steps:0,visited:new Set([0])};}
  function step(s,n){
    const in0=s.ip,work0=s.wp,state0=s.state;
    const sym=s.input[s.ip]??"_",out=get(s,s.wp),before=potential(s,n);
    let rule="";
    if(state0==="INIT"&&sym==="1"&&out==="_"){
      rule="INIT";s.work.set(s.wp,"0");s.ip++;s.wp++;s.state="SECOND";
    }else if((state0==="SECOND"||state0==="EMIT")&&sym==="1"&&out==="_"){
      rule="WRITE_GATE";s.work.set(s.wp,"g");s.ip++;s.wp++;s.state="EMIT";
    }else if(state0==="EMIT"&&sym==="#"&&out==="_"){
      rule="EOF_BACK";s.wp--;s.state="BACK";
    }else if(state0==="BACK"&&out==="g"){
      rule="BACK_G";s.wp--;
    }else if(state0==="BACK"&&out==="0"){
      rule="ACTIVATE";s.work.set(s.wp,"1");s.state="READY";
    }else if(state0==="READY"&&out==="1"){
      rule="HALT";s.state="HALT";
    }else throw Error("invalid machine configuration "+JSON.stringify({n,in0,work0,state0,sym,out}));
    s.r=Math.max(s.r,in0);s.visited.add(s.wp);s.steps++;
    const after=potential(s,n),delta=before.map((v,j)=>v-after[j]);
    check(Math.abs(s.ip-in0)<=1&&Math.abs(s.wp-work0)<=1,"nonlocal head");
    check(delta[3]>=0&&delta[5]>=0&&delta[6]>=0,"unexpected negative in intended monotone machine");
    check(delta[5]<=1&&delta[6]<=1,"single-component physical cap");
    check((delta[5]+delta[6])<=2,"coupled upper cap");
    check(delta[3]/(n-1)+delta[6]<=1+1e-12,"exact rational fixed-n tariff fails");
    check((delta[5]+delta[6])/2<=1,"half plus half tariff");
    check(rule==="ACTIVATE"?delta[3]===n-1&&delta[5]===0&&delta[6]===0&&s.state==="READY":delta[3]===0,"ACTIVATE exact row");
    if(rule==="WRITE_GATE")check(delta[5]===1&&delta[6]===1,"fused source and record");
    if(rule==="HALT")check(delta[6]===1,"halt row");
    stats.rows[rule]=(stats.rows[rule]??0)+1;stats.transitions++;
    return {rule,delta,before,after};
  }
  const examples={};
  for(let n=2;n<=256;n++){
    const s=make(n),trace=[];
    let act=null;const initial=potential(s,n);
    check(initial[3]===n-1&&initial[5]===n-1&&initial[6]===n+2,"initial vector");
    for(let j=0;j<2*n+8&&s.state!=="HALT";j++){
      const x=step(s,n);if(n<=5)trace.push({rule:x.rule,delta:x.delta.slice(3)});
      if(x.rule==="ACTIVATE")act=x;
    }
    check(s.state==="HALT"&&s.steps===2*n+2,"exact transitions");
    check(s.r===n&&s.ip===n&&s.wp===0,"head positions");
    check(get(s,0)==="1","active");
    for(let j=1;j<n;j++)check(get(s,j)==="g","record present");
    check(s.work.size===n&&s.visited.size===n+1,"physical work cells visited");
    check(potential(s,n).every(z=>z===0),"completed goal");
    check(act!==null&&act.delta[3]===n-1&&act.after[5]===0,"nonterminal gate activation");
    check(initial[3]/(n-1)+initial[6]===n+3,"primal fixed-length optimum");
    check(initial[6]===n+2&&n+3<=s.steps,"physical upper bound");
    if(n>=3){check(act.delta[3]>1,"unit gate tariff transfer falsified");stats.activationControls++;}
    if(n<=5)examples[n]=trace;
    stats.cases++;
  }
  for(let n=2;n<=25;n++){
    for(let j=1;j<n;j++)for(let from of ["_","0","1","g"])for(let to of ["_","0","1","g"]){
      const s=make(n);s.work.set(0,"0");s.work.set(j,from);
      const a=potential(s,n)[5];s.work.set(j,to);const b=potential(s,n)[5];
      check(Math.abs(a-b)<=1,"one-symbol physical correction cap");
      stats.physicalWriteControls++;
    }
  }
  return {status:"COMPUTATIONAL",model:"one fixed finite-state two-tape unary implicit-AND gate stager",...stats,examples,
    symbolic:{T:"2n+2",p_initial:"(0,0,0,n-1,0,n-1,n+2)",activated_step_delta:"(0,0,0,n-1,0,0,0)",gate_step_delta:"(0,0,0,0,0,1,1)",full_fixed_n_cone:"(n-1)*lambda_FUS<=1; lambda_INTERFACE+lambda_MACHINE<=1",uniform_cone:"lambda_FUS=0; lambda_INTERFACE+lambda_MACHINE<=1",max_initial_fixed_n:"n+3",max_initial_uniform:"n+2"}};
}
if (typeof require !== "undefined" && require.main === module) process.stdout.write(JSON.stringify(audit(),null,2)+"\n");
