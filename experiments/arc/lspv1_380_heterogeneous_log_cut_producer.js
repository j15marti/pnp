const run=function producer380() {
  const B=7, R=12, gates=[], outputs=[];
  const put=(a,b)=>{if(!a||!b||Math.abs(a)>B+gates.length||Math.abs(b)>B+gates.length)throw Error("bad ref");gates.push([a,b]);return B+gates.length;};
  for(let j=0;j<R;j++){
    const s=[(j%7)+1,((j+2)%7)+1,((j+4)%7)+1];
    let cur=s[0];
    const len=4+(j*19)%63;
    for(let i=0;i<len;i++){
      const v=s[i%3];
      if(i%5===0)cur=-put(-cur, i%2?-v:v);
      else cur=put((i%9===0)?-cur:cur,(i%4===0)?-v:v);
    }
    outputs.push(cur);
  }
  // Explicit, unobserved junk with global support. It is still parsed and charged.
  let trash=1;
  for(let i=0;i<20;i++)trash=put(trash,2+(i%6));
  const formula={B,gates,outputs};
  const val=(c,assign)=>{
    const bits=assign.slice();
    for(const [a,b] of c.gates){
      const read=r=>{let v=bits[Math.abs(r)-1];return r>0?v:1-v;};
      bits.push(read(a)&read(b));
    }
    return c.outputs.map(r=>r>0?bits[r-1]:1-bits[-r-1]);
  };
  const support=r=>{
    let reached=new Set(), todo=[Math.abs(r)];
    while(todo.length){const w=todo.pop();if(w<=B){reached.add(w);continue}const gate=gates[w-B-1];if(!gate)throw Error("bad gate");todo.push(Math.abs(gate[0]),Math.abs(gate[1]));}
    return [...reached].sort((a,b)=>a-b);
  };
  const bank=[],aliases=[],cuts=[],truth=[];
  const bp=(a,b)=>{if(!a||!b||Math.abs(a)>B+bank.length||Math.abs(b)>B+bank.length)throw Error("bank ref");bank.push([a,b]);return B+bank.length;};
  for(const out of outputs) {
    const cut=support(out);if(cut.length>3||!cut.length)throw Error("cut failed");
    cuts.push(cut);
    const on=[], truthVec=[];
    for(let mask=0;mask<(1<<cut.length);mask++){
      const a=Array(B).fill(0);
      cut.forEach((v,i)=>a[v-1]=(mask>>i)&1);
      const v=val({B,gates,outputs:[out]},a)[0];truthVec.push(v);
      if(v)on.push(mask);
    }
    truth.push(truthVec);
    let alias;
    if(on.length===0)alias=bp(cut[0],-cut[0]);
    else if(on.length===(1<<cut.length))alias=-bp(cut[0],-cut[0]);
    else{
      const terms=on.map(mask=>{
        const lit=cut.map((v,i)=>((mask>>i)&1)?v:-v);
        let t=lit[0];for(let k=1;k<lit.length;k++)t=bp(t,lit[k]);return t;
      });
      alias=terms[0];for(let i=1;i<terms.length;i++)alias=-bp(-alias,-terms[i]);
    }
    aliases.push(alias);
  }
  const replacement={B,gates:bank,outputs:aliases};
  let checks=0;
  for(let mask=0;mask<(1<<B);mask++){
    const a=Array.from({length:B},(_,i)=>(mask>>i)&1);
    const old=val(formula,a),neu=val(replacement,a);
    for(let j=0;j<R;j++){if(old[j]!==neu[j])throw Error("joint mismatch");checks++;}
  }
  for(let j=0;j<R;j++){
    if(bank.length>R*3*8)throw Error("bound");
    for(let m=0;m<(1<<cuts[j].length);m++) {
      const a=Array(B).fill(0);cuts[j].forEach((v,i)=>a[v-1]=(m>>i)&1);
      if(val({B,gates,outputs:[outputs[j]]},a)[0]!==truth[j][m])throw Error("truth");checks++;
    }
  }
  const bad1={B,gates,outputs:[0]};
  try{val(bad1,Array(B).fill(0));}catch{} // Invalid index is rejected by structural validator below.
  const validate=c=>{
    if(!Number.isInteger(c.B)||c.B<=0) return false;
    if(!Array.isArray(c.gates)||!Array.isArray(c.outputs))return false;
    for(let i=0;i<c.gates.length;i++){let g=c.gates[i];if(!Array.isArray(g)||g.length!==2||g.some(r=>!Number.isInteger(r)||r===0||Math.abs(r)>c.B+i))return false;}
    return c.outputs.every(r=>Number.isInteger(r)&&r!==0&&Math.abs(r)<=c.B+c.gates.length);
  };
  const malformed=[
    {B,gates:[[B+1,1]],outputs:[B+1]},
    {B,gates:[[0,1]],outputs:[1]},
    {B,gates:[[1,2]],outputs:[B+2]},
    {B,gates:[[1,2]],outputs:[null]},
    {B,gates:[[1,2],[-(B+2),1]],outputs:[B+2]},
    {B,gates:[[1,2,3]],outputs:[1]}
  ];
  for(const m of malformed){if(validate(m))throw Error("malformed accepted");checks++;}
  if(!validate(formula)||!validate(replacement))throw Error("valid rejected");checks+=2;
  const oddEvenK4=(parity)=>{
    const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
    let models=0;
    for(let m=0;m<64;m++){
      let ok=true;
      for(let v=0;v<4;v++){
        let row=0;for(let e=0;e<6;e++)if(edges[e].includes(v))row^=(m>>e)&1;
        if(row!==(v===0?parity:0))ok=false;
      }
      if(ok)models++;
    }
    return models;
  };
  if(oddEvenK4(0)!==8||oddEvenK4(1)!==0)throw Error("parity");checks+=2;
  // Same root, different observed internal wire: root-only replacement is unsafe.
  const C1={B:2,gates:[],outputs:[1,2]},C2={B:2,gates:[],outputs:[1,-2]};
  if(val(C1,[1,0])[0]!==val(C2,[1,0])[0]||val(C1,[1,0])[1]===val(C2,[1,0])[1])throw Error("root control");checks+=2;
  return {kind:"HETEROGENEOUS_LOG_CUT_COMPILER380",status:"COMPUTATIONAL exact finite assertions; symbolic theorem in report",B,R,source:formula,bank:replacement,cuts,truth,checks,malformed_rejected:malformed.length,oddEvenK4:[oddEvenK4(1),oddEvenK4(0)],root_only_counterexample:true,source_gates:gates.length,bank_gates:bank.length,gate_bound:R*3*8,aliases:R,random_seed:null,deterministic:true};
};
const result=run();
if(typeof process!=='undefined')process.stdout.write(JSON.stringify(result,null,2)+'\n');
