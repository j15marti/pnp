/* LSPV2/379: independent original-variable correlation and bypass test */
const correlatedCutTest=function correlatedCutTest(bank){
 let checks=0;function a(c,m){checks++;if(!c)throw Error(m)}
 const discovered=new Map();const feasible=new Set();let pair=null;
 for(let t=0;t<32;t++){
  const x=Array.from({length:5},(_,i)=>(t>>i)&1);
  const cut=[x[0]&x[1],x[0]^x[1],x[2]^x[3]^x[4]];
  const key=cut.join("");
  feasible.add(key);
  if(discovered.has(key)&&discovered.get(key)[1]!==x[4]&&!pair)pair=[discovered.get(key)[0],t,key];
  else if(!discovered.has(key))discovered.set(key,[t,x[4]]);
  let values=cut.slice();
  for(let i=0;i<bank.gates.length;i++){
    const g=bank.gates[i];a(g.id===values.length,"gate order");
    values.push((values[g.a[0]]^g.a[1])&(values[g.b[0]]^g.b[1]));
  }
  const c=cut[0]|(cut[1]<<1)|(cut[2]<<2);
  for(let m=0;m<256;m++){const l=bank.ports[m];a((values[l[0]]^l[1])===((m>>c)&1),"cut-substitution mask "+m+" assignment "+t);}
 }
 a(pair!==null,"must find bypass witness");
 // This is not a fake contradiction. It shows x4 cannot be represented
 // solely as a function of cut wires, even though most outputs can.
 const [p,q,c]=pair;
 a(((p>>4)&1)!==((q>>4)&1),"bypass differs");
 return {status:"PASS",assertions:checks,original_inputs:5,cut_wire_count:3,original_assignments:32,reachable_cut_vectors:feasible.size,port_comparisons:8192,cut_wire_functions:["a=x0 AND x1","b=x0 XOR x1","c=x2 XOR x3 XOR x4"],bypass_output:"x4",same_cut_different_bypass_witness:{assignment_1:p,assignment_2:q,cut_bits:c},component_paid_defs:bank.gates.length};
};
if (typeof require !== 'undefined' && require.main === module) { const b=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8')); console.log(JSON.stringify(correlatedCutTest(b),null,2)); }
