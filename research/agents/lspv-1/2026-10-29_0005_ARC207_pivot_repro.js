#!/usr/bin/env node
'use strict';
// Full deterministic replayer. Node.js >= 18. Redirect stdout to JSON.
function run() {
  var rows=[],base=0,core=0,separators=0;
  function solve(t,mask) {
    var A=[],B=[],i,j;
    for(i=0;i<t;i++) A.push(Boolean((mask>>2*i)&1)||Boolean((mask>>(2*i+1))&1));
    for(j=0;j<t;j++) B.push(Boolean((mask>>(2*t+2*j))&1)||Boolean((mask>>(2*t+2*j+1))&1));
    var ex=false;
    for(var z=0;z<2;z++) {
      var ok=true;
      for(i=0;i<t;i++) if(!(z||A[i])) ok=false;
      for(j=0;j<t;j++) if(!(!z||B[j])) ok=false;
      if(ok) ex=true;
    }
    var cj=true;
    for(i=0;i<t;i++) for(j=0;j<t;j++) if(!(A[i]||B[j])) cj=false;
    var dag=A.every(Boolean)||B.every(Boolean);
    if(ex!==cj || ex!==dag) throw Error('projection mismatch t='+t+' mask='+mask);
    return ex;
  }
  for(var t=1;t<=4;t++) {
    var sat=0, minimal=0, mmax=1<<(4*t);
    for(var mask=0;mask<mmax;mask++) {
      var val=solve(t,mask);
      if(val) sat++;
      else {
        var ismin=true;
        for(var bit=0;bit<4*t;bit++) if(!(mask&(1<<bit)) && !solve(t,mask|(1<<bit))) ismin=false;
        if(ismin) minimal++;
      }
      for(var y=0;y<8;y++) {
        var R=(y!==0 && y!==7);
        if((R&&val)!==(R&&solve(t,mask))) throw Error('R mismatched');
        core++;
      }
    }
    for(var i=0;i<t;i++) for(var j=0;j<t;j++) {
      var special=mmax-1, zs=[2*i,2*i+1,2*t+2*j,2*t+2*j+1];
      zs.forEach(function(pos){special &= ~(1<<pos);});
      if(solve(t,special)) throw Error('minimal false point became true');
      zs.forEach(function(pos){if(!solve(t,special|(1<<pos)))throw Error('not minimal');});
      for(var p=0;p<t;p++) for(var q=0;q<t;q++) {
        var A=Boolean((special>>(2*p))&1)||Boolean((special>>(2*p+1))&1);
        var B=Boolean((special>>(2*t+2*q))&1)||Boolean((special>>(2*t+2*q+1))&1);
        if((A||B)===(p===i&&q===j)) throw Error('resolvent separation false');
        separators++;
      }
    }
    if(sat!==2*3**t*4**t-3**(2*t)||minimal!==t*t) throw Error('count mismatch');
    var w=Math.ceil(Math.log2(4*t+2));
    rows.push({t:t,assignments:mmax,satisfying:sat,minimal_false_points:minimal,
      parent_clauses:2*t,auxiliary_free_projection_clauses:t*t,
      compact_DAG_gates:4*t-1,variable_id_bits:w,
      parent_literal_token_bits:6*t*(w+1),
      projection_literal_token_bits:4*t*t*(w+1)});
    base+=mmax;
  }
  if(base!==69904||core!==8*69904||separators!==354)throw Error('audit size mismatch');
  return {id:'ARC207_SINGLE_CHILD_DESCENT',base_assignments:base,
    core_assignment_tests:core,irredundance_checks:separators,
    randomized:false,seed:null,mismatch_count:0,rows:rows,
    note:'Exhaustive finite controls only; no all-SAT contraction established.'};
}
console.log(JSON.stringify(run(),null,2));
