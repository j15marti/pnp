"use strict";
// Self-contained, deterministic exhaustive verifier; Node.js 18+
const result = (function producer(){
  "use strict";
  let assertions=0;
  function check(ok,why){assertions++;if(!ok)throw Error("producer: "+why);}
  function classify(bits){
    if(bits.length<3||bits.charAt(0)!=="1")return "M";
    let pos=1;
    let c=Number.parseInt(bits.slice(pos,pos+2),2);pos+=2;
    const clauses=[];
    for(let i=0;i<c;i++){
      if(pos+2>bits.length)return "M";
      const l=Number.parseInt(bits.slice(pos,pos+2),2);pos+=2;
      let clause=[];
      for(let j=0;j<l;j++){
        if(pos+2>bits.length)return "M";
        let v=bits.charCodeAt(pos)-48,s=bits.charCodeAt(pos+1)-48;pos+=2;
        clause.push([v,s]);
      }
      clauses.push(clause);
    }
    if(pos!==bits.length)return "M";
    for(let mask=0;mask<4;mask++){
      let satisfied=true;
      for(const clause of clauses){
        let trueLiteral=false;
        for(const [v,s] of clause){
          if((((mask>>v)&1)^s)===1){trueLiteral=true;break;}
        }
        if(!trueLiteral){satisfied=false;break;}
      }
      if(satisfied)return "S";
    }
    return "U";
  }
  const expected={3:{S:1,M:14,U:0},5:{S:1,M:61,U:1},7:{S:5,M:248,U:2},9:{S:21,M:991,U:11},11:{S:97,M:3939,U:59},13:{S:217,M:15875,U:291}};
  let rows=[],validExamples=[];
  for(const N of [3,5,7,9,11,13]){
    let counts={S:0,U:0,M:0},traceSteps=0;
    for(let len=0;len<=N;len++){
      for(let id=0;id<2**len;id++){
        const bits=(len===0?"":id.toString(2).padStart(len,"0"));
        const label=classify(bits);
        check(label==="S"||label==="U"||label==="M","classification partition");
        counts[label]++;
        traceSteps+=len+1; // one transition per bit, one terminal EOS step
      }
    }
    for(const label of ["S","U","M"])check(counts[label]===expected[N][label],`N=${N} label=${label}`);
    check(counts.S+counts.U+counts.M===2**(N+1)-1,"complete binary prefix tree");
    rows.push({horizon:N,prefix_states:2**(N+1)-1,code_size_upper_bound_O:"O(N*2^N)",runtime_per_horizon_input_upper_bound:N+1,counts,offline_trie_transition_count:2*(2**(N+1)-1),precomputed_label_evaluations:2**(N+1)-1,finite_prefix_total_steps:traceSteps});
  }
  const examples=[
    ["100","S"], // empty formula
    ["10100","U"], // empty clause
    ["11001000101","U"], // (x1) AND (not x1)
    ["11001000100","S"], // (x1) AND (x1)
    ["000","M"],["","M"],["10","M"],["1010","M"],["1000","M"],["111111","M"]
  ];
  for(const [bits,label] of examples){const found=classify(bits);check(found===label,`${bits} expected ${label} got ${found}`);validExamples.push({bits,label})}
  function k4(odd){
    const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
    let models=0;
    for(let mask=0;mask<64;mask++){
      let good=true;
      for(let v=0;v<4;v++){
        let p=0;for(let e=0;e<edges.length;e++)if(edges[e].includes(v))p^=(mask>>e)&1;
        if(p!==(odd&&v===0?1:0)){good=false;break;}
      }
      if(good)models++;
    }
    return models;
  }
  check(k4(false)===8,"even K4 models");
  check(k4(true)===0,"odd K4 models");
  const res={experiment:"LSPV1_377_FINITE_HORIZON_MINIMAX_FIREWALL",date:"2026-11-03 19:00 PST",kind:"exhaustive two-variable toy-CNF binary grammar",parser:"1|cc|(ll|vs)*, cc=2-bit clause count, ll=2-bit clause length, vs=1-bit variable ID and 1-bit negation; no suffix",labels:["S=SAT","U=UNSAT","M=MALFORMED"],horizons:rows,examples:validExamples,k4:{even_models:8,odd_models:0},producer_assertions:assertions,theorem_scope:"Any decidable binary language, full SAT included, via exponential static machine description for each finite horizon; no single uniform polynomial-time SAT decider follows",publication_notice:"Finite checks only; no asymptotic lower bound is inferred."};
  return res;
})();
console.log(JSON.stringify(result,null,2));
