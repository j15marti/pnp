const BS05=require('./2026-11-24_1150_BS05_check.js');
function paddedControls(BS05){
 const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],f=lines.flatMap(c=>[c,c.map(x=>-x)]),out=[];
 for(const k of [1,3,6,16,64,128])for(const remove of [-1,0]){
  const c=f.filter((_,i)=>i!==remove);for(let i=0;i<k;i++){const a=[1,2,8+i];c.push(a,a.map(x=>-x));}
  const x={cnf:{n:7+k,clauses:c}},z=BS05(x,{blockCap:4096});
  const expected=(7+k<=12)?(remove<0?"UNSAT":"SAT"):"UNKNOWN";
  if(z.status!==expected||z.counters.blocks!==1||z.counters.deletions!==0||z.counters.maxBlockVolume!==String(1n<<BigInt(7+k)))throw Error("padding "+JSON.stringify(z));
  out.push({k,removed:remove,status:z.status,volume:z.counters.maxBlockVolume,deletions:z.counters.deletions,blocks:z.counters.blocks,tuples:z.counters.tuples});
 }
 return out;
}
console.log(JSON.stringify(paddedControls(BS05),null,2));
