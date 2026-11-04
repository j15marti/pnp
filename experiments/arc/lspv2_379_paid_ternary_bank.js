/* LSPV-2/379; standalone Node.js, no dependencies. */
const buildBank=function buildBank(){
 const masks=[0xaa,0xcc,0xf0], gates=[], reps={}, counts={};
 const neg=l=>[l[0],l[1]^1];
 const add=(a,b)=>{const id=masks.length; const mask=(masks[a[0]]^(a[1]?255:0)) & (masks[b[0]]^(b[1]?255:0)); gates.push({id,a,b});masks.push(mask);return [id,0]};
 const disj=(a,b)=>neg(add(neg(a),neg(b)));
 function synth2(t){
  const ones=[];for(let k=0;k<4;k++)if((t>>>k)&1)ones.push(k);
  if(ones.length>2)return neg(synth2(t^15));
  if(!ones.length)return add([0,0],[0,1]);
  function term(k){return add([0,(k&1)?0:1],[1,(k&2)?0:1]);}
  let out=term(ones[0]);if(ones.length==2)out=disj(out,term(ones[1]));return out;
 }
 function synth3(t){
  const lo=t&15,hi=(t>>>4)&15;
  if(lo===hi)return synth2(lo);
  const a=synth2(lo),b=synth2(hi);
  return disj(add([2,1],a),add([2,0],b));
 }
 const triv={0:null,15:[2,1],51:[1,1],85:[0,1]};
 for(let m=0;m<128;m++){
   const before=gates.length;
   reps[m]=(Object.prototype.hasOwnProperty.call(triv,m)&&triv[m]!==null)?triv[m]:synth3(m);
   counts[m]=gates.length-before;
   const o=reps[m],got=masks[o[0]]^(o[1]?255:0);
   if(got!==m||counts[m]>9)throw Error("synthesis invalid:"+m+":"+got);
 }
 const ports={};
 for(let m=0;m<256;m++){const rep=Math.min(m,255-m),base=reps[rep]; ports[m]=[base[0],base[1]^(m!==rep?1:0)];const out=masks[ports[m][0]]^(ports[m][1]?255:0);if(out!==m)throw Error("port mismatch "+m);}
 const ntriv=Object.values(counts).filter(x=>x===0).length, maximum=Math.max(...Object.values(counts));
 const histogram={};for(const n of Object.values(counts))histogram[n]=(histogram[n]||0)+1;
 return {version:"LSPV2-379-TERNARY-BANK/v1", semantics:"fresh paid DEF wire = signed AND2 of existing wires, complement is a signed literal view",inputs:3,input_masks:masks.slice(0,3),gates,ports,per_rep:counts,stats:{number_of_semantic_functions:256,number_of_complement_classes:128,number_of_reps_with_no_new_gates:ntriv,max_gates_per_rep:maximum,gates_total:gates.length,upper_bound_3var_synthesis:9,upper_bound_complete_bank:1117,histogram,verify_truth_pairs:256*8,tag:"syntactic common original support <=3; no source-conditional inference, no payload wire export from untyped LOCAL-CONVERT"}};
};
if (typeof require !== 'undefined' && require.main === module) console.log(JSON.stringify(buildBank()));
