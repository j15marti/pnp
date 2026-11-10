// LSPV-2/531: self-contained independent V8 replay. 444 SAT mutation witnesses.
// Run with Node.js: node experiments/arc/lspv2_531_sign_sensitivity_v8.js
const graphEdges={
 K4:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
 prism:[[0,1],[0,2],[0,3],[1,2],[1,4],[2,5],[3,4],[3,5],[4,5]],
 cube:[[0,1],[0,3],[0,4],[1,2],[1,7],[2,3],[2,6],[3,5],[4,5],[4,7],[5,6],[6,7]],
 petersen:[[0,1],[0,4],[0,5],[1,2],[1,6],[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]],
 bridge_cut:[[0,2],[0,3],[0,8],[1,2],[1,3],[1,8],[2,3],[4,6],[4,7],[4,9],[5,6],[5,7],[5,9],[6,7],[8,9]]
};
function verify(){
let assertions=0,records=[];
for(const [name,edges] of Object.entries(graphEdges)){
 const h=Math.max(...edges.flat())+1,n=edges.length,inc=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});
 if(!inc.every(x=>x.length===3))throw Error("not cubic");
 const C=[];
 for(let v=0;v<h;v++)for(let b=0;b<8;b++){
  const z=((b>>2)&1)^((b>>1)&1)^(b&1);
  if(z===(v===0?1:0))continue;
  C.push(inc[v].map((i,j)=>(b&(1<<(2-j)))?-(i+1):i+1));
 }
 const witnesses=Array(C.length).fill(-1);
 let originalModels=0;
 for(let a=0;a<2**n;a++){
  const parity=inc.map(idx=>idx.reduce((p,i)=>p^((a>>i)&1),0));
  if(parity.every((p,v)=>p===(v===0?1:0)))originalModels++;
  for(let v=0;v<h;v++){
   if(parity[v]===(v===0?1:0))continue;
   if(parity.some((p,u)=>u!==v&&p!==(u===0?1:0)))continue;
   for(let ci=4*v;ci<4*v+4;ci++){
    if(witnesses[ci]<0&&!C[ci].some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0)))witnesses[ci]=a;
   }
  }
 }
 if(originalModels!==0)throw Error("odd original SAT");
 let sat=0,fail=0;
 for(let ci=0;ci<C.length;ci++)for(let j=0;j<3;j++){
  const D=C.map(row=>row.slice());D[ci][j]=-D[ci][j];
  const a=witnesses[ci];
  if(a<0){fail++;continue}
  if(!D.every(row=>row.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))
   throw Error("invalid SAT witness");
  sat++;assertions++;
 }
 if(name!=="bridge_cut"&&sat!==12*h)throw Error("not every sign sensitive");
 if(name==="bridge_cut"&&fail!==12)throw Error("cut-vertex control mismatch");
 records.push({name,vertices:h,edge_variables:n,sat_mutations:sat,all_mutations:12*h,not_sat:fail});
}
if(assertions!==444)throw Error("total mismatch");
return {pass:true,assertions,records};
}
if(typeof console!=="undefined")console.log(JSON.stringify(verify()));
