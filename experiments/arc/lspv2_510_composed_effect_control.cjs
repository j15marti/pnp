// LSPV-2/510 compact independent effect-composition verifier.
// Abstract deterministic memory program. Not native FLMV / R_mix341.
"use strict";
function run(){
  let checks=0;
  const ck=(x,m)=>{checks++;if(!x)throw Error(m)};
  const A=[["read",2,"u"],["write",2,"u"],["write",5,"a"]];
  const B=[["read",2,"v"],["read",5,"w"],["read",8,"z"],
    ["writeDynamic",12,"z","v"],["write",8,"v"],["read",8,"t"]];
  function execute(ops,mem,regs){
    mem={...mem};regs={...regs};
    const live=new Map(),written=new Map();let high=0;
    for(const [op,x,y,z] of ops){
      if(op==="read"){
        const v=mem[x]||0; high=Math.max(high,x);
        if(!written.has(x))live.set(x,v); regs[y]=v;
      }else if(op==="write"){
        const v=regs[y]||0;mem[x]=v;written.set(x,v);
      }else if(op==="writeDynamic"){
        const a=x+(regs[y]||0),v=regs[z]||0;
        mem[a]=v;written.set(a,v);
      }
    }
    return {mem,regs,live,written,high};
  }
  function compose(p,q){
    const live=new Map(p.live),writes=new Map(p.written);
    for(const [a,v] of q.live)if(!p.written.has(a))live.set(a,v);
    for(const [a,v] of q.written)writes.set(a,v);
    return {live,writes,high:Math.max(p.high,q.high)};
  }
  const anchor={2:0,5:1,8:0,12:0,13:1,99:1};
  const reg0={a:1};
  const p=execute(A,anchor,reg0),q=execute(B,p.mem,p.regs),s=compose(p,q);
  ck([...s.live].map(x=>x[0]).join(",")==="2,8","composed live-ins");
  ck([...s.writes.keys()].sort((a,b)=>a-b).join(",")==="2,5,8,12","writes");
  let accepted=0,rejected=0;
  for(let m=0;m<64;m++){
    const mem={2:m&1,5:(m>>1)&1,8:(m>>2)&1,
      12:(m>>3)&1,13:(m>>4)&1,99:(m>>5)&1};
    const ok=[...s.live].every(([a,v])=>(mem[a]||0)===v);
    const direct=execute(B,execute(A,mem,reg0).mem,execute(A,mem,reg0).regs);
    if(ok){
      const patched={...mem};for(const [a,v] of s.writes)patched[a]=v;
      ck(JSON.stringify(patched)===JSON.stringify(direct.mem),
        "read/write effect replay mismatch");
      ck(patched[99]===mem[99]&&patched[13]===mem[13],"frame overwritten");
      accepted++;
    }else rejected++;
  }
  ck(accepted===16&&rejected===48,"expected guard split");
  const labelCounts={SAT:0,UNSAT:0};
  for(let mask=0;mask<16;mask++){
    const charge=Array.from({length:4},(_,v)=>(mask>>v)&1);
    const result=charge.reduce((a,b)=>a^b,0)?"UNSAT":"SAT";
    labelCounts[result]++;
    ck(result===(mask.toString(2).split("1").length%2===0?"UNSAT":"SAT"),
       "Tseitin charge parity");
  }
  ck(labelCounts.SAT===8&&labelCounts.UNSAT===8,"charge controls");
  return {status:"PASS",checks,accepted,rejected,live_in:[2,8],
    writes:[2,5,8,12],source_charges:16,labelCounts,
    scope:"abstract effect composition, finite cubic Tseitin parity control; not a native FLMV execution",
    p_vs_np:"OPEN"};
}
const result=run();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
