#!/usr/bin/env node
"use strict";
/* TMR-3/041. Pure ES2020, no npm dependencies. Research calibration, not compiled Turing machine. */
function audit041() {
  "use strict";
  let tests=0, failures=0, qCases=0, randomCases=0, physicalRows=0, gaugeControls=0, malformed=0, fallbackCases=0;
  const check=(b,msg)=>{tests++;if(!b){failures++;throw Error("AUDIT041 FAIL "+msg)}};
  let seed=0x41A57C23;
  const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;};
  const shuffle=a=>{a=[...a];for(let i=a.length-1;i>0;i--){let j=rnd()%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;};
  const canon=c=>[...c].sort((a,b)=>(Math.abs(a)-Math.abs(b))||(a-b));
  const key=c=>canon(c).join(",");
  const val=(lit,asgn)=>{const v=asgn.get(Math.abs(lit))||0;return lit<0?1-v:v};
  const satisfied=(formula,asgn)=>formula.every(c=>c.some(l=>val(l,asgn)===1));
  function privateLeaf(formula) {
    const unique=new Map();
    for(const c of formula){
      if(c.length!==3||c.some(x=>!Number.isSafeInteger(x)||x===0)||new Set(c.map(Math.abs)).size!==3)return null;
      unique.set(key(c),canon(c));
    }
    const groups=new Map();
    for(const c of unique.values()){
      let d=canon(c.map(x=>-x)), a=key(c), b=key(d), gk=a<b?a:b;
      if(!groups.has(gk))groups.set(gk,{orient:a<b?c:d,seen:new Set()});
      groups.get(gk).seen.add(a);
    }
    if([...groups.values()].some(g=>g.seen.size!==2))return null;
    const occurrences=new Map(), arr=[...groups.values()].map(g=>g.orient);
    for(const c of arr)for(const v of c)occurrences.set(Math.abs(v),(occurrences.get(Math.abs(v))||0)+1);
    const ans=new Map([...occurrences.keys()].map(v=>[v,0])), leaves=[];
    for(const c of arr){
      const leaf=c.find(l=>occurrences.get(Math.abs(l))===1);
      if(leaf===undefined)return null;
      leaves.push(Math.abs(leaf));
      const others=c.filter(l=>Math.abs(l)!==Math.abs(leaf));
      const a=val(others[0],ans),b=val(others[1],ans);
      const need=(a===b)?1-a:0;
      ans.set(Math.abs(leaf),leaf<0?1-need:need);
    }
    if(!satisfied(formula,ans))throw Error("Invalid private-leaf witness");
    return {assignment:ans,groups:arr.length,leaves,distinctClauses:unique.size};
  }
  function brute(formula){
    const vars=[...new Set(formula.flat().map(Math.abs))];
    if(vars.length>16)throw Error("brute too large");
    for(let bits=0;bits<(1<<vars.length);bits++){
      const a=new Map(vars.map((v,i)=>[v,(bits>>i)&1]));
      if(satisfied(formula,a))return a;
    }
    return null;
  }
  function family(k){
    let out=[],z=3*k+1;
    function nae(a,b,c){out.push([a,b,c],[-a,-b,-c])}
    for(let i=1;i<=k;i++)nae(i,k+i,2*k+i);
    for(let i=1;i<=k;i++)for(let j=i+1;j<=k;j++)nae(i,j,z++);
    return out;
  }
  const degreeWitness=formula=>{
    const uniq=new Map(formula.map(c=>[key(c),canon(c)]));
    const counts=new Map();
    for(const c of uniq.values())for(const l of c)counts.set(Math.abs(l),(counts.get(Math.abs(l))||0)+1);
    return new Map([...counts].map(([v,d])=>[v,d>2?0:1]));
  };
  for(let k=2;k<=7;k++){
    const base=family(k), ans=privateLeaf(base), n=3*k+k*(k-1)/2;
    check(ans!==null,"Q family recognized "+k);
    check(ans.groups===k*(k+1)/2,"Q group count "+k);
    check(ans.assignment.size===n,"Q var count "+k);
    check(satisfied(base,ans.assignment),"Q formula witness "+k);
    check(satisfied(base,degreeWitness(base)),"original degree witness "+k);
    const vars=shuffle(Array.from({length:n},(_,i)=>i+1));
    for(let trial=0;trial<48;trial++){
      const ids=shuffle([...vars]).map(x=>x+10001+(trial%3)*1000000);
      const renaming=new Map(Array.from({length:n},(_,i)=>[i+1,ids[i]]));
      const flipped=new Set(Array.from({length:n},(_,i)=>i+1).filter(()=>rnd()&1));
      let f=base.map(c=>shuffle(c.map(l=>Math.sign(l)*(flipped.has(Math.abs(l))?-1:1)*renaming.get(Math.abs(l)))));
      f=shuffle(f);
      for(let j=0;j<Math.min(10,f.length);j++)if(rnd()%3===0)f.push([...f[rnd()%f.length]]);
      const w=privateLeaf(f);
      check(w!==null,"gauge+rename+permutation+duplicate accepted "+k);
      check(satisfied(f,w.assignment),"gauge satisfying "+k);
      check(w.groups===ans.groups,"deduplicated group count "+k);
      check(w.assignment.size===n,"deduplicated source vars "+k);
      gaugeControls++;
    }
    qCases++;
  }
  {
    const flipX1=family(2).map(c=>c.map(l=>Math.abs(l)===1?-l:l));
    check(!satisfied(flipX1,degreeWitness(flipX1)),"forced sign gauge defeats naive degree witness");
    const fixed=privateLeaf(flipX1);
    check(fixed!==null&&satisfied(flipX1,fixed.assignment),"private leaf repairs signed gauge");
    const eight=[];
    for(let m=0;m<8;m++)eight.push([1,2,3].map((v,i)=>(m&(1<<i))?-v:v));
    check(brute(eight)===null,"full eight source is UNSAT");
    check(privateLeaf(eight)===null,"no private leaf over full eight");
    const parity=eight.filter((_,i)=>(i.toString(2).replace(/0/g,"").length%2)===0);
    check(privateLeaf(parity)===null,"affine four clause group not incorrectly shortcut");
    const drop=family(3).slice(1);
    check(privateLeaf(drop)===null,"missing complement rejected");
    const controls=[[[1,2]],[[1,1,2]],[[1,2,-2]],[[0,1,2]],[[1,2,NaN]],[[1,2,3],[-1,-2,3]]];
    for(let i=0;i<controls.length;i++){check(privateLeaf(controls[i])===null,"malformed or unmatched control "+i);malformed++}
  }
  for(let n=3;n<=6;n++)for(let j=0;j<250;j++){
    let f=[],m=1+rnd()%12;
    for(let a=0;a<m;a++){
      const vars=shuffle(Array.from({length:n},(_,i)=>i+1)).slice(0,3);
      f.push(vars.map(v=>(rnd()&1)?v:-v));
      if(rnd()%7===0)f.push([...f[f.length-1]]);
    }
    const r=privateLeaf(f),b=brute(f);
    check(!r||satisfied(f,r.assignment),"random witnessed clause validity");
    check(!r||b!==null,"random soundness versus brute");
    if(r===null)fallbackCases++;
    randomCases++;
  }
  const signatures=new Map();
  // Exhaustively check output-tape one-step signed changes for all states
  // B<=6, all ternary cells BLANK/0/1; local one-cell overwrite and optional HALT.
  for(let B=1;B<=6;B++){
    const pow=3**B;
    for(let state=0;state<pow;state++){
      let cells=[],q=state;
      for(let i=0;i<B;i++){cells.push(q%3);q=Math.floor(q/3)}
      let blanks=cells.filter(v=>v===0).length;
      for(let pos=0;pos<B;pos++)for(const next of [0,1,2])for(const halt of [false,true]){
        const old=cells[pos],after=blanks+(old===0?0:1)-(next===0?0:1);
        const di=blanks-after,dm=halt?1:0,wt=1;
        check(di<=1&&di+0*dm<=wt,"output physical lambda=(1,0)");
        const sk=`${di},${dm}`;signatures.set(sk,(signatures.get(sk)||0)+1);
        physicalRows++;
      }
    }
  }
  check(signatures.has("1,1"),"fused last write and halt real local row");
  check(signatures.has("-1,0"),"erase creates negative discharge");
  check(signatures.has("0,1"),"halt without output writes exists");
  const exactRows=[
    {rule:"NOP_OR_OVERWRITE",delta:[0,0,0,0,0,0,0],w:1},
    {rule:"FILL_OUTPUT_CELL",delta:[0,0,0,0,0,1,0],w:1},
    {rule:"HALT_NO_WRITE",delta:[0,0,0,0,0,0,1],w:1},
    {rule:"FILL_LAST_AND_HALT",delta:[0,0,0,0,0,1,1],w:1},
    {rule:"ERASE_OUTPUT_CELL",delta:[0,0,0,0,0,-1,0],w:1},
    {rule:"ERASE_AND_HALT",delta:[0,0,0,0,0,-1,1],w:1}
  ];
  const rationalChecks=[];
  for(let a=0;a<=12;a++)for(let b=0;b<=12;b++){
    let feasible=exactRows.every(row=>a*row.delta[5]+b*row.delta[6]<=12*row.w);
    check(feasible===(a+b<=12),"exact grid cone matches lambda5+lambda6<=1");
    rationalChecks.push(feasible?1:0);
  }
  check(failures===0,"zero failures");
  return {
    id:"TMR3_LEAFNAE080",mode:"exact finite V8 audit; symbolic theorem independently stated",
    seed:"0x41A57C23",cases:{qFamilies:qCases,gaugeControls,randomCases,fallbackCases,malformed,physicalRows},
    assertions:tests, failures, signatures:Object.fromEntries([...signatures].sort()), 
    tariff:{columns:["CNF","aff","sep","fus","Gamma","interface","machine"],rows:exactRows,
      exactCone:"lambda_interface>=0,lambda_machine>=0,lambda_interface+lambda_machine<=1; all other weights zero in this subprotocol",
      rationalGridDenominator:12,feasibleGridPoints:rationalChecks.reduce((a,b)=>a+b,0),
      witness:["0","0","0","0","0","1","0"],badDoubleCharge:["0","0","0","0","0","1","1"]}
  };
}
const result=audit041();
process.stdout.write(JSON.stringify(result,null,2)+"\n");
