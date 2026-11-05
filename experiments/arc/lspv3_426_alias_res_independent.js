/* LSPV-3/426 alias-versus-RES checker. Node/ES2020 compatible.
   A rule-local audit, not an authoritative full R_mix341 checker. */
"use strict";
const L=[-3,-2,-1,1,2,3];
const e=a=>a.reduce((m,v)=>{let k=L.indexOf(v);if(k<0)throw Error("bad literal");return m|(1<<k)},0);
const d=m=>L.filter((x,k)=>m&(1<<k));
const has=(m,x)=>Boolean(m&e([x]));
const ren=(m,f)=>e(d(m).map(f));
function res(a,b,p){if(!has(a,p)||!has(b,-p))throw Error("pivot");return (a&~e([p]))|(b&~e([-p]));}
const evalC=(m,a)=>d(m).some(x=>Boolean(a&(1<<(Math.abs(x)-1)))===(x>0));
function parse(s){
 let l=s.trim().split(/\r?\n/),h=/^p cnf ([0-9]+) ([0-9]+)$/.exec(l[0]);
 if(!h||h[1]!=="3"||h[2]!=="4"||l.length!==5)throw Error("header");
 return l.slice(1).map(v=>{
  if(!/^-?[0-9]+(?: -?[0-9]+)* 0$/.test(v))throw Error("line");
  let a=v.split(" ").map(Number).slice(0,-1);
  if(a.length===0||a.some(x=>x===0||Math.abs(x)>3))throw Error("lit");
  return e(a);
 });
}
function verify(s,steps){let c=parse(s);
 for(let [i,j,p,expect] of steps){
  if(!(i>=0&&j>=0&&i<c.length&&j<c.length))throw Error("parents");
  let got=res(c[i],c[j],p);
  if(got!==e(expect))throw Error("claimed clause");
  c.push(got);
 }
 return c[c.length-1]===0;
}
function audit(){
 const sig=x=>Math.sign(x)*(Math.abs(x)===2?1:Math.abs(x));
 let total=0,equal=0,bad=0,clean=0,sem=0;
 for(let a=0;a<64;a++)if(has(a,1))
 for(let b=0;b<64;b++)if(has(b,-1)){
  total++;
  let r=res(a,b,1),target=ren(r,sig),got=res(ren(a,sig),ren(b,sig),1);
  if((got&target)!==got)throw Error("subsumption");
  let left=ren(a&~e([1]),sig),right=ren(b&~e([-1]),sig);
  let criterion=!((has(left,1)&&!has(right,1))||(has(right,-1)&&!has(left,-1)));
  if((target===got)!==criterion)throw Error("equality criterion");
  if(target===got)equal++;else{
   bad++;
   const noT=m=>[1,2,3].every(x=>!(has(m,x)&&has(m,-x)));
   if(noT(a)&&noT(b))clean++;
  }
  for(let k=0;k<8;k++){
   if(evalC(a,k)&&evalC(b,k)&&!evalC(r,k))throw Error("RES soundness");
   sem++;
  }
 }
 const source="p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n3 0\n";
 const c=parse(source),proof=[[0,1,1,[2,-3]],[4,2,2,[-3]],[3,5,3,[]]];
 if(!verify(source,proof))throw Error("not empty");
 for(let k=0;k<8;k++)if(c.every(v=>evalC(v,k)))throw Error("SAT");
 let deletion=[];
 for(let i=0;i<4;i++){
  let w=Array.from({length:8},(_,j)=>j).find(k=>c.every((v,j)=>j===i||evalC(v,k)));
  if(w===undefined)throw Error("nonessential source");deletion.push(w);
 }
 let expected=ren(e([2,-3]),sig);
 let actual=res(ren(c[0],sig),ren(c[1],sig),1);
 if(expected===actual)throw Error("missing alias discrepancy");
 let corrupt=[
  ["p cnf 3 5\n1 2 0\n-1 -3 0\n-2 0\n3 0\n",proof],
  ["p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n",proof],
  ["p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n4 0\n",proof],
  [source,[[0,1,2,[2,-3]]]],[source,[[0,1,1,[-3]]]],
  [source,[[0,9,1,[2,-3]]]],
  ["p cnf 3 4\n1 2 0\n-1 3 0\n-2 0\n3 0\n",proof],
  ["p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n3 0 x\n",proof]];
 let rejected=0;for(let [s,p] of corrupt){
  try{if(verify(s,p))throw Error("accepted corrupt");}
  catch(err){if(err.message==="accepted corrupt")throw err;rejected++;}
 }
 if([total,equal,bad,clean,sem,rejected].join()!=="1024,784,240,27,8192,8")throw Error("counts");
 return {status:"PROVED/EXACT rule lemma + COMPUTATIONAL control",
  original_source:source,source_bytes:source.length,
  native_legal_res_nodes:3,all_four_sources_essential:true,
  source_deletion_witness_masks:deletion,
  oriented_pairs:total,exact_equal:equal,noncommuting_alias:bad,
  noncommuting_tautology_free_parents:clean,truth_checks:sem,
  bad_source_or_proof_rejections:rejected,
  counterexample:{parents:[[1,2],[-1,-3]],pivot:1,original_result:[-3,2],
    quotient_expected:d(expected),actual_oriented_resolvent:d(actual)},
  limitation:"Quotient is not source-preserving on original variables; this is a rule-local obstruction, not a full-native-normalization or B3 refutation."};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
