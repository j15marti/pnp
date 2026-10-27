// LSPV-2 CNF-COUNTER-IMAGE176, self-contained Node.js audit. No external modules.
// Run: node 2026-10-27_0912_CNF_COUNTER_IMAGE176_repro.mjs
const audit=function audit(){
  "use strict";
  let assertions=0;
  function ok(v,msg){assertions++;if(!v)throw new Error("AUDIT_FAILURE "+msg);}
  const W1=[
    [-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],
    [-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],
    [1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],
    [-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],
    [4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]
  ];
  const Alice=[6,11],Bob=[17,9],fixed=W1.map((_,i)=>i).filter(i=>!Alice.includes(i)&&!Bob.includes(i));
  const magic="10100110111100000011110010101010";
  const bin=(v,w)=>v.toString(2).padStart(w,"0");
  const lay=m=>{let w=Math.floor(Math.log2(20*m))+1;return {m,w,header:32+3*w,stride:3*(w+1),V:15*m,C:20*m,N:32+3*w+60*m*(w+1),gap:48*m*(w+1)};};
  function H(a,b){return W1.map((c,k)=>c.map((v,j)=>{
    if((k===6&&j===0||k===11&&j===0)&&a===0)return -v;
    if((k===17&&j===2||k===9&&j===2)&&b===0)return -v;
    return v;
  }));}
  function sat(clause,mask){return clause.some(v=>Number(!!(mask&(1<<(Math.abs(v)-1))))===Number(v>0));}
  function supportConnected(cf){
    const adj=Array.from({length:16},()=>new Set());
    for(const c of cf)for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){
      const a=Math.abs(c[j]),b=Math.abs(c[k]);adj[a].add(b);adj[b].add(a);
    }
    const seen=new Set([1]), stack=[1];
    while(stack.length){let v=stack.pop();for(const n of adj[v])if(!seen.has(n)){seen.add(n);stack.push(n);}}
    return seen.size===15;
  }
  let modeCounts={},modeSupportConnected={};
  for(let a=0;a<2;a++)for(let b=0;b<2;b++){
    let cf=H(a,b), models=0;
    for(let mask=0;mask<(1<<15);mask++)if(cf.every(c=>sat(c,mask)))models++;
    modeCounts[""+a+b]=models;
    modeSupportConnected[""+a+b]=supportConnected(cf);
    ok(modeSupportConnected[""+a+b],"connected 15-variable 20-clause support");
    const plus=Array(16).fill(0),minus=Array(16).fill(0),seen=new Set();
    for(let c of cf){ok(c.length===3&&new Set(c.map(v=>Math.abs(v))).size===3,"proper");
      seen.add(c.join(","));for(let v of c)(v>0?plus:minus)[Math.abs(v)]++;}
    ok(seen.size===20,"distinct");
    for(let v=1;v<=15;v++)ok(plus[v]===2&&minus[v]===2,"2P2N");
  }
  ok(JSON.stringify(modeCounts)===JSON.stringify({"10":272,"11":0,"00":772,"01":272}),"truth four modes");
  ok(H(0,0).every(c=>sat(c,616))&&H(0,1).every(c=>sat(c,616)),"Alice0 witness616");
  ok(H(1,0).every(c=>sat(c,4742)),"Alice1 witness4742");
  function clause(m,a,b,row){
    let orig,idx,flA=1,flB=1;
    if(row<2*m){idx=Math.floor(row/2);orig=Alice[row%2];flA=(typeof a==="function"?a(idx):a[idx]);}
    else if(row<18*m){idx=Math.floor((row-2*m)/16);orig=fixed[(row-2*m)%16];}
    else {idx=Math.floor((row-18*m)/2);orig=Bob[(row-18*m)%2];flB=(typeof b==="function"?b(idx):b[idx]);}
    return W1[orig].map((v,j)=>{
      if((orig===6||orig===11)&&j===0&&!flA)v=-v;
      if((orig===17||orig===9)&&j===2&&!flB)v=-v;
      return (v>0?1:-1)*(Math.abs(v)+15*idx);
    });
  }
  function signLocation(m,side,i){
    let x=lay(m);
    if(side==="A")return x.header+(2*i)*x.stride;
    return x.header+(18*m+2*i)*x.stride+2*(x.w+1);
  }
  function encode(m,a,b){
    let x=lay(m),header=magic+bin(x.V,x.w)+bin(x.C,x.w)+bin(m,x.w);
    let payload=[];
    for(let row=0;row<x.C;row++)for(let v of clause(m,a,b,row))
      payload.push((v>0?"1":"0")+bin(Math.abs(v),x.w));
    const out=header+payload.join("");
    ok(out.length===x.N,"physical length");
    return out;
  }
  function findM(N){
    if(N<lay(1).N)return null;
    let lo=1,hi=N;
    while(lo<=hi){let mid=Math.floor((lo+hi)/2),a=lay(mid).N;
      if(a===N)return mid; if(a<N)lo=mid+1;else hi=mid-1;}
    return null;
  }
  function verifyRaw(data,strict){
    let probes=0, arithmetic=0;
    const read=p=>{probes++;ok(p>=0&&p<data.length,"input bounds");return data[p];};
    let m=findM(data.length);arithmetic+=Math.ceil(Math.log2(data.length+1))*12;
    if(m===null)return {valid:false,accept:false,probes,arithmetic};
    let x=lay(m);
    // Do NOT store m control bits: on-demand source reads with O(log N) indices.
    const a=i=>Number(read(signLocation(m,"A",i)));
    const b=i=>Number(read(signLocation(m,"B",i)));
    let disjoint=true;
    for(let i=0;i<m;i++){if(a(i)&&b(i))disjoint=false;arithmetic+=20;}
    if(!strict)return {valid:null,accept:disjoint,probes,arithmetic,m};
    const header=magic+bin(x.V,x.w)+bin(x.C,x.w)+bin(m,x.w);
    // Stream the expected literal bit from a fixed 20-row ROM, not a stored CNF.
    let mismatch=-1;
    for(let p=0;p<data.length;p++){
      const actual=read(p);let expected;
      if(p<x.header)expected=header[p];
      else{
        const body=p-x.header,row=Math.floor(body/x.stride);
        const within=body%x.stride,j=Math.floor(within/(x.w+1)),offset=within%(x.w+1);
        const v=clause(m,a,b,row)[j];
        expected=((v>0?"1":"0")+bin(Math.abs(v),x.w))[offset];
      }
      arithmetic+=19;
      if(actual!==expected){mismatch=p;break;}
    }
    return {valid:mismatch<0,accept:mismatch<0&&disjoint,probes,arithmetic,m,mismatch};
  }
  let tests=0,positive=0,negative=0,bit_checks=0,probesFull=0;
  let examples=[];
  for(let m=1;m<=4;m++){
    let total=1<<m;
    for(let aN=0;aN<total;aN++)for(let bN=0;bN<total;bN++){
      let a=Array.from({length:m},(_,i)=>(aN>>i)&1);
      let b=Array.from({length:m},(_,i)=>(bN>>i)&1);
      let data=encode(m,a,b),x=lay(m);
      const found=verifyRaw(data,true),prom=verifyRaw(data,false);
      const expect=a.every((v,i)=>!(v&&b[i]));
      ok(found.valid&&found.accept===expect&&prom.accept===expect,"full/promise decision");
      const cp=Array(x.V+1).fill(0),cn=Array(x.V+1).fill(0),seen=new Set();
      for(let row=0;row<x.C;row++){
        let c=clause(m,a,b,row);
        ok(c.length===3&&new Set(c.map(v=>Math.abs(v))).size===3,"multi proper");
        seen.add(c.join(","));
        for(let v of c)(v>0?cp:cn)[Math.abs(v)]++;
        if(expect){
          // no precomputed per-instance source index or occurrence table
          const model=(i)=>a[i]===0?616:4742;
          ok(c.some(v=>((model(Math.floor((Math.abs(v)-1)/15)) >> ((Math.abs(v)-1)%15))&1)===(v>0?1:0)),"SAT source witness");
        }
      }
      ok(seen.size===x.C,"multi distinct");
      for(let v=1;v<=x.V;v++)ok(cp[v]===2&&cn[v]===2,"multi 2P2N");
      probesFull+=found.probes;bit_checks+=x.N;tests++;
      if(expect)positive++;else negative++;
      if(m===4&&aN===3&&bN===4)examples.push({N:x.N,m,valid:found.valid,answer:found.accept,source_bit_probes:found.probes,promise_bit_probes:prom.probes});
    }
  }
  const mtest=2,a=[0,1],b=[0,0],data=encode(mtest,a,b);
  let flipped=0;
  for(let p=0;p<data.length;p++){
    let arr=data.split("");arr[p]=arr[p]==="0"?"1":"0";
    let r=verifyRaw(arr.join(""),true);
    ok(!r.valid,"single physical bit must invalidate template p="+p);
    flipped++;
  }
  // Two consistent source sign toggles change the formula while staying canonical.
  let arr=data.split("");
  for(let row of [0,1]){
    let p=lay(mtest).header+row*lay(mtest).stride;
    arr[p]=arr[p]==="0"?"1":"0";
  }
  let r2=verifyRaw(arr.join(""),true);ok(r2.valid,"two paired sign flips canonical");
  class Tape {
    constructor(){this.head=0;this.max=0;this.D=1;this.moves=0;this.reads=0;}
    read(){this.reads++;return this.head===0?"@":"_";}
    zero(){return this.read()==="@";}
    inc(){this.head++;this.moves++;this.max=Math.max(this.max,this.head);}
    dec(){ok(!this.zero(),"decrement negative");this.head--;this.moves++;}
  }
  // Actual finite-control input + counter-head traversal.  Numeric address
  // formation is an external arithmetic caller here and NOT charged by this
  // seek-core test. The report proves separate unary-arithmetic compilation.
  function counterSeek(data,pos,lab){
    const A=new Tape(),B=new Tape();
    let inputHead=0,TM=2,headMoves=0,probes=0;
    for(let j=0;j<pos;j++){A.inc();TM++;}
    while(!A.zero()){A.dec();B.inc();inputHead++;headMoves++;TM+=4;}
    while(!B.zero()){B.dec();A.inc();TM+=3;}
    ok(inputHead===pos,"seek target");probes++;TM++;
    const value=data[inputHead];
    headMoves+=pos;TM+=pos; // return physical input head to input start
    return {value, D:A.D+B.D,S:A.max+1+B.max+1,work_moves:A.moves+B.moves,input_moves:headMoves,T:TM,probes};
  }
  let counterCases=[], totalCounterSteps=0,correctCounter=0;
  for(let m=1;m<=4;m++){
    const a=Array.from({length:m},(_,i)=>(i%2));
    const b=Array.from({length:m},(_,i)=>(1-(i%2)));
    let data=encode(m,a,b),native=[],meter={T:0,work_moves:0,input_moves:0,S_max:0,D:2};
    for(let i=0;i<m;i++)for(let side of ["A","B"]){
      let pos=signLocation(m,side,i),out=counterSeek(data,pos);
      ok(out.value===(side==="A"?String(a[i]):String(b[i])),"exact raw anchored bit");
      meter.T+=out.T;meter.work_moves+=out.work_moves;meter.input_moves+=out.input_moves;
      meter.S_max=Math.max(meter.S_max,out.S);
      correctCounter++;
      if(i===0)native.push({side,position:pos,value:out.value});
    }
    totalCounterSteps+=meter.T;counterCases.push({m,N:data.length,reads:2*m,...meter,first_anchors:native});
  }
  const modelSingle=(m)=>{
    const x=lay(m);
    let h=0,steps=0,moves=0,answer=true;
    let a=Array(m).fill(1),b=Array(m).fill(0);
    for(let i=0;i<m;i++){
      for(let pos of [signLocation(m,"A",i),signLocation(m,"B",i)]){
        moves+=Math.abs(pos-h);steps+=Math.abs(pos-h)+1;h=pos;
      }
      answer&&=!(a[i]&&b[i]);
    }
    return {steps,moves,answer};
  };
  const modelDual=(m)=>{
    let pA=0,pB=0,moves=0,probes=0;
    for(let i=0;i<m;i++){
      let a=signLocation(m,"A",i),b=signLocation(m,"B",i);
      moves+=Math.abs(a-pA)+Math.abs(b-pB);pA=a;pB=b;probes+=2;
    }
    return {moves,probes};
  };
  let tapeComparisons=[];
  for(let m of [1,2,4,8,16,32])tapeComparisons.push({m,N:lay(m).N,Mk_one_input: modelSingle(m),two_input_heads:modelDual(m),RAM_indexed_probe_count:2*m});
  return {
    run:"LSPV2-CNF-COUNTER-IMAGE176",date:"2026-10-27",
    status:"COMPUTATIONAL independent controls; exact restricted lemmas conditional on model and formal proof",
    preregistered_falsifiers:[
      "H1 physical canonical CNF sign-bit decoder is template-only under full bit validation",
      "H2 one-bit mutation can avoid image validation",
      "H3 permanent origin markers allow counter reads without additional symbol changes",
      "H4 cheap Alice-only witness stream is a sound SAT acceptor"
    ],
    source:{W1_variables:15,W1_clauses:20,modes:modeCounts,connected_SAT_UNSAT_modes:modeSupportConnected,alice_witness_616:true,alice_witness_4742:true},
    tests:{assertion_groups:assertions,complete_physical_cases:tests,SAT:positive,UNSAT:negative,
           signed_literal_bits_checked:bit_checks,full_indexed_input_probes:probesFull,
           malformed_one_bit_mutations:flipped,paired_flips_are_canonical:r2.valid,
           counter_raw_source_anchor_reads:correctCounter,total_primitive_counter_seek_cost:totalCounterSteps,
           fail:0},
    counter_seek:counterCases,tape_model_comparisons:tapeComparisons,
    sample:examples,
    limits:["Counter-seek finite tests have externally computed addresses; full register arithmetic transport proved separately, not executed here.",
            "Canonical image rejection does not solve ordinary unrestricted SAT.",
            "Marked work tape initial symbols are charged as actual symbol changes.",
            "No resource transfer from sequential input to FLMV indexed RAM without simulation.",
            "No all-input ARC contraction nor P versus NP proof."]
  };
};
process.stdout.write(JSON.stringify(audit(),null,2)+"\n");
