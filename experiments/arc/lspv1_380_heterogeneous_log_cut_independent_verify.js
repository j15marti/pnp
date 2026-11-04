const verify=function verifier380(r){
  let checks=0;
  const B=r.B;
  const valid=c=>{
    if(c.B!==B||!Array.isArray(c.gates)||!Array.isArray(c.outputs))return false;
    for(let i=0;i<c.gates.length;i++){const g=c.gates[i];if(!Array.isArray(g)||g.length!==2)return false;for(const ref of g)if(!Number.isInteger(ref)||ref===0||Math.abs(ref)>B+i)return false;}
    return c.outputs.every(ref=>Number.isInteger(ref)&&ref!==0&&Math.abs(ref)<=B+c.gates.length);
  };
  if(!valid(r.source)||!valid(r.bank))throw Error("bad graph");
  const evaluator=(c,mask)=>{
    const cache=new Map();
    const value=ref=>{
      const x=Math.abs(ref);
      let bit;
      if(x<=B)bit=(mask>>(x-1))&1;
      else if(cache.has(x))bit=cache.get(x);
      else {
        const gate=c.gates[x-B-1];if(!gate)throw Error("dangling");
        bit=value(gate[0]) & value(gate[1]);cache.set(x,bit);
      }
      return ref<0?1-bit:bit;
    };
    return c.outputs.map(value);
  };
  const deps=(c,ref)=>{
    const set=new Set();const seen=new Set();
    const visit=x=>{
      x=Math.abs(x);
      if(seen.has(x))return;seen.add(x);
      if(x<=B){set.add(x);return;}
      const g=c.gates[x-B-1];if(!g)throw Error("bad dependency");
      visit(g[0]);visit(g[1]);
    };visit(ref);
    return [...set].sort((a,b)=>a-b);
  };
  for(let j=0;j<r.R;j++){
    const observed=deps(r.source,r.source.outputs[j]);
    if(JSON.stringify(observed)!==JSON.stringify(r.cuts[j])||observed.length>3)throw Error("bad certified cut");
    for(let m=0;m<(1<<observed.length);m++){
      let testMask=0;
      observed.forEach((v,i)=>{testMask|=((m>>i)&1)<<(v-1);});
      if(evaluator(r.source,testMask)[j]!==r.truth[j][m])throw Error("incorrect reported truth");
      checks++;
    }
    checks++;
  }
  for(let mask=0;mask<(1<<B);mask++){
    let v=evaluator(r.source,mask),w=evaluator(r.bank,mask);
    for(let j=0;j<r.R;j++){if(v[j]!==w[j])throw Error(`mismatch ${mask} ${j}`);checks++;}
  }
  if(r.bank.gates.length>r.R*3*8||r.bank.outputs.length!==r.R)throw Error("bad bound");checks+=2;
  for(const [modify,which] of [
    [s=>{s.bank.gates[0][0]=B+s.bank.gates.length+1},0],
    [s=>{s.bank.outputs[0]=0},0],
    [s=>{s.source.outputs[0]=B+s.source.gates.length+1},1]
  ]){
    let clone=JSON.parse(JSON.stringify(r));modify(clone);
    if(which===0&&valid(clone.bank)||which===1&&valid(clone.source))throw Error("malformed accepted");
    checks++;
  }
  // Corrupt a verified truth-vector bit: the independent checker must reject it.
  const corrupted=JSON.parse(JSON.stringify(r));corrupted.truth[0][0]^=1;
  let witnessed=false;
  const z=deps(corrupted.source,corrupted.source.outputs[0]);
  const checkmask=0;
  if(evaluator(corrupted.source,checkmask)[0]!==corrupted.truth[0][0])witnessed=true;
  if(!witnessed)throw Error("failed corruption control");checks++;
  // SAT, UNSAT, malformed controls use a separate direct CNF semantics.
  const cnf=(clauses,n)=>{
    if(!Array.isArray(clauses)||clauses.some(c=>!Array.isArray(c)||c.length===0||c.some(v=>!Number.isInteger(v)||v===0||Math.abs(v)>n)))return null;
    let models=0;
    for(let m=0;m<(1<<n);m++){
      if(clauses.every(c=>c.some(l=> ((m>>(Math.abs(l)-1))&1)===(l>0?1:0))))models++;
    }
    return models;
  };
  if(cnf([[1]],1)!==1||cnf([[1],[-1]],1)!==0||cnf([[0]],1)!==null)throw Error("CNF labels");checks+=3;
  // K4 independent face parity identity.
  let odd=0,even=0;
  const incidence=[[0,1,2],[0,3,4],[1,3,5],[2,4,5]];
  for(let mask=0;mask<64;mask++){
    const par=incidence.map(es=>es.reduce((a,e)=>a^((mask>>e)&1),0));
    if(par.every(q=>q===0))even++;
    if(par[0]===1&&par.slice(1).every(q=>q===0))odd++;
  }
  if(odd!==0||even!==8||JSON.stringify(r.oddEvenK4)!==JSON.stringify([0,8]))throw Error("K4 labels");checks+=2;
  if(r.B!==7||r.R!==12||r.source.gates.length!==377||r.bank.gates.length!==73)throw Error("unexpected fixtures");checks+=4;
  return {kind:"HETEROGENEOUS_LOG_CUT_COMPILER380 independent",status:"COMPUTATIONAL",checks,all_inputs:1<<B,all_observation_comparisons:(1<<B)*r.R,source_gates:r.source.gates.length,bank_gates:r.bank.gates.length,cuts_verified:r.R,malformed_and_corrupted_rejected:4,oddEvenK4:[odd,even],deterministic:true};
};
if(typeof require!=='undefined'){
 const fs=require('fs');const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
 process.stdout.write(JSON.stringify(verify(raw),null,2)+'\n');
}
