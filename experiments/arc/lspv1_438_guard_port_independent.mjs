// Independent finite test for Theorem 438.1. Run: node lspv1_438_guard_port_independent.mjs
// No SAT solver or native R_mix341 proof checker is invoked.
let checks=0; const ok=(p)=>{checks++;if(!p)throw Error("FAILED at "+checks)};
const graphs=[
["K4",Array.from({length:4},(_,i)=>Array.from({length:3-i},(_,j)=>[i,i+j+1])).flat(),4],
["K33",Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat(),6],
["cube",Array.from({length:8},(_,i)=>Array.from({length:7-i},(_,j)=>[i,i+j+1])).flat().filter(([a,b])=>{let x=a^b;return (x&(x-1))===0}),8]
];const rows=[];
for(const [name,edges,h] of graphs){
 const n=edges.length,inc=Array.from({length:h},()=>[]),charge=Array.from({length:h},(_,v)=>Number(v===0));
 edges.forEach(([a,b],e)=>{inc[a].push(e);inc[b].push(e)});ok(inc.every(a=>a.length===3));
 let left=new Set(),right=0;for(let v=0;v<h;v++){
  for(const e of inc[v])left.has(e)?left.delete(e):left.add(e);
  if(charge[v])left.has(-1)?left.delete(-1):left.add(-1);right^=charge[v];
 }
 ok(left.size===1&&left.has(-1)&&right===1);
 let odd0=0,odd1=0,even0=0;
 for(let mask=0;mask<2**n;mask++){
  const x=Array.from({length:n},(_,i)=>(mask>>i)&1);
  for(const g of [0,1]){
   const w=x.map(b=>b&(1-g));let all=true,even=true;
   for(let v=0;v<h;v++){
    const parity=inc[v].reduce((s,e)=>s^x[e],0);
    const lhs=inc[v].reduce((s,e)=>s^w[e],0)^(charge[v]&g);
    const guarded=Boolean(g)||parity===charge[v];
    const row=lhs===charge[v];ok(guarded===row);all&&=row;even&&=(Boolean(g)||parity===0);
   }
   if(!g&&all)odd0++;if(g&&all)odd1++;if(!g&&even)even0++;
  }
 }
 ok(odd0===0&&odd1===2**n&&even0===2**(n-h+1));
 rows.push({graph:name,vertices:h,edges:n,checks:2**(n+1)*h,odd_g0_models:odd0,odd_g1_models:odd1,even_g0_models:even0,final_equation:"g=1"});
}
const x=[1,0,0],g=1,chi=0;ok((x.reduce((a,b)=>a^b,0)^(g&chi))!==chi);
console.log(JSON.stringify({checks,wrong_port_rejected:true,rows},null,2));