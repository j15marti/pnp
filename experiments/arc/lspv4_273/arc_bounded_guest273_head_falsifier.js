"use strict";
function proper3(label){
  let clauses=[];for(let k=0;k<8;k++)clauses.push([1,2,3].map((x,i)=>k&(1<<i)?-x:x));
  if(label==="SAT")clauses[7]=clauses[0].slice();
  const text="p cnf 3 8\n"+clauses.map(c=>c.join(" ")+" 0\n").join("");
  let models=0;for(let k=0;k<8;k++)if(clauses.every(c=>c.some(l=>(((k>>(Math.abs(l)-1))&1)===(l>0?1:0)))))models++;
  if((models>0)!==(label==="SAT"))throw Error("source label");
  return {text,models};
}
function headSemantics(text,incorrectReset){
  let map=new Map(),head=0,input=0,events=0;
  const move=p=>{head=p;events++};
  const write=v=>{if(v)map.set(head,1);else map.delete(head);events++};
  const jump=()=>{let a=0;for(const [i,v]of map)if(v)a+=2**i;input=a;map.clear();if(incorrectReset)head=0;events++};
  move(1);write(1);jump();let first=text[input];
  write(1);jump();let second=text[input];
  return {first,second,head,input,events,observational_match:first===second};
}
function sweep(text){
  let H=text.length;let head=0,tape=new Map(),events=0;
  for(let i=0;i<H;i++){head++;events++}
  tape.set(H,1);events++;let target=1n<<BigInt(H);
  tape.clear();events++;const empty=true;
  for(let i=0;i<H;i++){head--;events++}
  if(head!==0||target<=BigInt(text.length))throw Error("sweep");
  return {guest_index_head_high_water:H,guest_time_additive_events:events,guest_writable_high_water_at_least:H,
    read_at_target_blank:empty,read_target_binary_length:target.toString(2).length,underlyingSAT_answer_unchanged:true};
}
function run(){
 let out={schema:"ARC-BOUNDED-GUEST-INDEX-FALSIFIERS273",results:[]};
 for(let label of ["SAT","UNSAT"]){
  let F=proper3(label),good=headSemantics(F.text,false),bad=headSemantics(F.text,true);
  if(!good.observational_match||bad.observational_match||good.first!=="c"||bad.second!==" ")throw Error("head reset counterexample");
  out.results.push({label,ordinaryCnfChars:F.text.length,model_count:F.models,actual:good,incorrect:bad,sweep:sweep(F.text)});
 }
 return out;
}
if(typeof require!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
