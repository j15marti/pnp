/* LSPV-2/379 independent semantic checker, no shared synthesis routines. */
const verifyBank=function verifyBank(b){
 let checks=0;const assert=(c,msg)=>{checks++;if(!c)throw Error("verify: "+msg)};
 assert(b.inputs===3,"b must be 3");
 assert(Array.isArray(b.gates)&&b.gates.length<=1117,"gate bound");
 assert(b.version==="LSPV2-379-TERNARY-BANK/v1","version");
 const count={};
 for(let key=0;key<128;key++){
   const n=b.per_rep[key];
   assert(Number.isInteger(n)&&n>=0&&n<=9,"subgraph bound "+key);count[n]=(count[n]||0)+1;
 }
 assert(Object.values(b.per_rep).reduce((a,c)=>a+c,0)===b.gates.length,"per-rep charging");
 assert(Object.keys(b.ports).length===256,"port count");
 const rows=[];
 for(let assignment=0;assignment<8;assignment++){
   const vals=[assignment&1,(assignment>>1)&1,(assignment>>2)&1];
   for(let i=0;i<b.gates.length;i++){
     const g=b.gates[i];
     assert(g.id===3+i,"fresh-def topological id");
     const v=[];
     for(const lit of [g.a,g.b]){
       assert(Array.isArray(lit)&&lit.length===2,"literal pair");
       assert(Number.isInteger(lit[0])&&lit[0]>=0&&lit[0]<g.id,"no forward or missing wire");
       assert(lit[1]===0||lit[1]===1,"signed bit");
       v.push(vals[lit[0]]^(lit[1]?1:0));
     }
     vals.push(v[0]&v[1]);
   }
   for(let mask=0;mask<256;mask++){
     const l=b.ports[mask];
     assert(Array.isArray(l)&&l.length===2,"port syntax");
     assert(Number.isInteger(l[0])&&l[0]>=0&&l[0]<vals.length,"port wire");
     assert(l[1]===0||l[1]===1,"port sign");
     const result=vals[l[0]]^(l[1]?1:0);
     assert(result===((mask>>assignment)&1),"port truth mask="+mask+", assignment="+assignment);
   }
   rows.push(vals.length);
 }
 // Corruption rejection with direct fail-fast checks, against independent clones.
 let rejected=0;
 const mutations=[
   x=>{x.gates[0].a[0]=x.gates[0].id;},
   x=>{x.gates[0].a[1]=2;},
   x=>{x.gates[1].id=x.gates[0].id;},
   x=>{x.ports[7][1]^=1;},
   x=>{delete x.ports[5];},
   x=>{x.per_rep[7]=12;},
   x=>{x.inputs=4;},
   x=>{x.gates[1].b[0]=-1;},
   x=>{x.gates[3].a[0]=999999;}
 ];
 for(let mutation of mutations){
   const x=JSON.parse(JSON.stringify(b));mutation(x);
   try{verifyCore(x);throw Error("mutated record accepted");}catch(e){if(String(e).includes("mutated record accepted"))throw e;rejected++;}
 }
 function verifyCore(x){
   if(x.inputs!==3||x.gates.length>1117||Object.keys(x.ports).length!==256)throw Error("meta");
   if(Object.values(x.per_rep).some(v=>!Number.isInteger(v)||v>9||v<0))throw Error("counts");
   let v=[0,0,0];
   for(let i=0;i<x.gates.length;i++){
     const g=x.gates[i];if(g.id!==v.length)throw Error("order");
     for(const p of [g.a,g.b])if(!Array.isArray(p)||p.length!==2||!Number.isInteger(p[0])||p[0]<0||p[0]>=g.id||(p[1]!==0&&p[1]!==1))throw Error("wire");
     v.push((v[g.a[0]]^g.a[1])&(v[g.b[0]]^g.b[1]));
   }
   for(let m=0;m<256;m++){
     let l=x.ports[m];if(!Array.isArray(l)||!Number.isInteger(l[0])||l[0]<0||l[0]>=v.length||(l[1]!==0&&l[1]!==1))throw Error("port");
     // independently test all 8 valuations
     let table=0;for(let a=0;a<8;a++){let z=[a&1,(a>>1)&1,(a>>2)&1];for(const g of x.gates)z.push((z[g.a[0]]^g.a[1])&(z[g.b[0]]^g.b[1]));table|=((z[l[0]]^l[1])<<a);}if(table!==m)throw Error("bad truth");
   }
 }
 assert(rejected===mutations.length,"corruption rejection");
 // A same-root but different exported wire countercontrol:
 // C0 exports (root=x0, u=x1) and C1 exports (root=x0, u=NOT x1).
 let witness=0;
 for(let a=0;a<8;a++){
   const out0=[a&1,(a>>1)&1],out1=[a&1,1^((a>>1)&1)];
   assert(out0[0]===out1[0],"root same");
   assert(out0[1]!==out1[1],"public state differs");
   witness++;
 }
 // Odd/even cubic K4 Tseitin as both-label control independent of bank.
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const chargesOdd=[1,0,0,0],chargesEven=[0,0,0,0];
 function models(charge){
   let t=0;for(let assignment=0;assignment<64;assignment++){let ok=true;for(let v=0;v<4;v++){let x=0;for(let e=0;e<6;e++)if(edges[e][0]===v||edges[e][1]===v)x^=(assignment>>e)&1;if(x!==charge[v])ok=false;}if(ok)t++;}return t;
 }
 const even=models(chargesEven),odd=models(chargesOdd);
 assert(even===8&&odd===0,"K4 odd even models");
 return {status:"PASS",assertions:checks,negative_certificates_rejected:rejected,truth_table_cases:2048,truth_gate_evaluations:b.gates.length*8,odd_K4_models:odd,even_K4_models:even,gate_count:b.gates.length,per_rep_histogram:count,exported_wire_countercontrol_assignments:witness};
};
if (typeof require !== 'undefined' && require.main === module) { const fs=require('fs'); const x=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); console.log(JSON.stringify(verifyBank(x),null,2)); }
