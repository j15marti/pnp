// Independent V8 verifier for symbolic last-write semantics, including adaptive
// addresses, conditional writes, repeated aliases and source-backed reads.
// The persistent event-list interpreter does not share code or expression AST
// with the Python symbolic term compiler.
const scenarios=[]; let checks=0,failures=0,totalCases=0;
function assert(v,msg){checks++;if(!v){failures++;throw new Error(msg)}}
function imperative(m,rounds,input,a){
 const mem=input.slice();let prev=0;
 for(let i=0;i<rounds;i++){
  const r=mem[(a+prev+i)%m];const target=(a+r+i+1)%m;
  if(i%2===0||r===1)mem[target]=r^(i%2);
  prev=r;
 }
 return mem[(a+prev+rounds+1)%m];
}
function persistent(m,rounds,input,a){
 const stores=[];let prev=0,aliased=0;
 function read(index){
  let val=input[index];
  for(const s of stores){
   aliased++;
   if(s.enable && s.addr===index)val=s.val;
  }
  return val;
 }
 for(let i=0;i<rounds;i++){
  const idx=(a+prev+i)%m;const r=read(idx);
  stores.push({addr:(a+r+i+1)%m,val:r^(i%2),enable: i%2===0||r===1});
  prev=r;
 }
 return {value:read((a+prev+rounds+1)%m),aliasCandidates:aliased};
}
for(const m of [2,4,8]){
 for(let rounds=1;rounds<=8;rounds++){
  let c=0,alias=rounds*(rounds+1)/2;
  for(let mask=0;mask<(1<<m);mask++){
   const input=Array.from({length:m},(_,j)=>(mask>>j)&1);
   for(let a=0;a<m;a++){
    const x=imperative(m,rounds,input,a),y=persistent(m,rounds,input,a);
    assert(x===y.value,"value m="+m+",rounds="+rounds+",mask="+mask+",a="+a);
    assert(y.aliasCandidates===alias,"alias m="+m+",rounds="+rounds+",mask="+mask+",a="+a);
    c++;totalCases++;
   }
  }
  scenarios.push({memory_cells:m,rounds,source_assignment_checks:c,read_write_alias_candidates:alias});
 }
}
const result={model:'independent persistent event log vs native mutable RAM',scenarios,checks,failures,totalCases};
console.log(JSON.stringify(result,null,2));
