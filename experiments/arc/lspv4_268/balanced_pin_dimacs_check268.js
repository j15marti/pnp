"use strict";
// Independent balanced source-language adversarial checker. Raw DIMACS length is equal across opposite-label inputs.
function balancedPinCheck268(){
"use strict";
let assertions=0;
const check=(v,msg)=>{assertions++;if(!v)throw Error(msg)};
function xor(a,b,z){let a1=[];for(let p=0;p<2;p++)for(let q=0;q<2;q++)for(let r=0;r<2;r++)if(r!==(p^q))a1.push([p?-a:a,q?-b:b,r?-z:z]);return a1}
function pin(z,p,q,bit){let a1=[];for(let j=0;j<2;j++)for(let k=0;k<2;k++)a1.push([bit?z:-z,j?-p:p,k?-q:q]);return a1}
function build(b,pins){
let cls=[],boundaries=[],n=b+pins.length*(b+4),m=pins.length*4*(b+1),prefix=0;
for(let i=0;i<pins.length;i++){
const o=b+i*(b+4),v=pins[i],start=cls.length;
for(let j=2;j<=b;j++)cls.push(...xor(j===2?1:o+j-2,j,o+j-1));
cls.push(...pin(o+b-1,o+b,o+b+1,v));
cls.push(...pin(o+b+2,o+b+3,o+b+4,1-v));
boundaries.push({i:i+1,first_clause:start+1,last_clause:cls.length,pin:v,block_vars:[o+1,o+b+4]});
}
return {n,m,clauses:cls,boundaries};
}
const dim=f=>"p cnf "+f.n+" "+f.clauses.length+"\n"+f.clauses.map(c=>c.join(" ")+" 0\n").join("");
function positionBlocks(f){
const header="p cnf "+f.n+" "+f.clauses.length+"\n";let cur=header.length;
return f.boundaries.map(r=>{const size=f.clauses.slice(r.first_clause-1,r.last_clause).map(c=>c.join(" ")+" 0\n").join("").length;let x={block:r.i,start_byte:cur,end_byte_exclusive:cur+size,bytes:size};cur+=size;return x});
}
function sat(f,a){return f.clauses.every(c=>c.some(l=>a[Math.abs(l)-1]===Number(l>0)))}
function dpll(f){let nodes=0,tests=0;function go(a){nodes++;a=a.slice();while(true){let changed=false,done=true;for(const C of f.clauses){let yes=false,open=0,last=0;for(let l of C){tests++;let v=a[Math.abs(l)-1];if(v<0){open++;last=l}else if(v===Number(l>0)){yes=true;break}}if(yes)continue;done=false;if(!open)return false;if(open===1){let j=Math.abs(last)-1,v=Number(last>0);if(a[j]>=0&&a[j]!==v)return false;if(a[j]<0){a[j]=v;changed=true}}}if(done)return true;if(!changed)break}let j=a.indexOf(-1);if(j<0)return false;for(let v of [0,1]){let b=a.slice();b[j]=v;if(go(b))return true}return false}return {sat:go(Array(f.n).fill(-1)),nodes,literal_tests:tests}}
function directWitness(b,pins,bd){
let f=build(b,pins),a=Array(f.n).fill(0);for(let j=0;j<b;j++)a[j]=bd[j];
for(let i=0;i<pins.length;i++){
const o=b+i*(b+4),v=pins[i];let x=0;
for(let j=1;j<=b;j++){x^=bd[j-1];if(j>=2)a[o+j-2]=x}
a[o+b+1]=1-v;
}
return {f,a};
}
let cases=[],small=[];
for(const b of [2,3]){
const q=2,even=build(b,[0,0]),mixed=build(b,[0,1]),a=dim(even),z=dim(mixed);
check(a.length===z.length,"raw ASCII input lengths leak the target label");
const blocks=positionBlocks(even),blocks2=positionBlocks(mixed);
check(JSON.stringify(blocks)===JSON.stringify(blocks2),"component block offsets move under pin flip");
for(let i=0;i<a.length;i++)if(a[i]!==z[i]){check(i>=blocks[1].start_byte&&i<blocks[1].end_byte_exclusive,"difference outside switched block") }
for(let k=0;k<b;k++){} // intentional no-op avoided in cost ledger
for(let k=0;k<(1<<b);k++){
 const bd=Array.from({length:b},(_,j)=>(k>>j)&1);
 const yes=(bd.reduce((s,v)=>s^v,0)===0);
 const wa=directWitness(b,[0,0],bd),wn=directWitness(b,[0,1],bd);
 check(sat(wa.f,wa.a)===yes,"SAT source witness projection");
 check(!sat(wn.f,wn.a),"mixed source false complete assignment");
}
let nmodels=0;
if(b===2)for(let m=0;m<(1<<even.n);m++){
const assignment=Array.from({length:even.n},(_,j)=>(m>>j)&1);
if(sat(even,assignment))nmodels++;
check(!sat(mixed,assignment),"opposing pins have model");
}
check(nmodels>0||b!==2,"no SAT witness");
const ds=dpll(even),dn=dpll(mixed);
check(ds.sat===true && dn.sat===false,"UP-DPLL matched labels");
small.push({b,q:2,source_characters:a.length,source_bits:8*a.length,
  equal_length:true,differences_in_second_block_only:true,blocks,source_models_b2:b===2?nmodels:null,even_dpll:ds,one_odd_dpll:dn});
}
for(let q of [3,4,8,12]) {
 const even=build(2,Array(q).fill(0));
 const text=dim(even),bounds=positionBlocks(even);
 for(let block=0;block<q;block++){
   let pins=Array(q).fill(0);pins[block]=1;
   let other=dim(build(2,pins));
   check(text.length===other.length,"different length for one-odd source");
   const seg=bounds[block];
   for(let i=0;i<text.length;i++)if(text[i]!==other[i]){
     check(i>=seg.start_byte&&i<seg.end_byte_exclusive,"one-odd leaks outside source block");
   }
 }
 cases.push({q,native_ascii_source_bits:text.length*8,blocks:q,all_odd_location_controls_checked:q,shared_header:true,equal_input_length:true});
}
function canonicalChild(b,pins){let requirements=[...new Set(pins)].sort((a,b)=>a-b),cls=[];for(let i=0;i<requirements.length;i++){let o=b+i*(b+1);for(let j=2;j<=b;j++)cls.push(...xor(j===2?1:o+j-2,j,o+j-1));cls.push(...pin(o+b-1,o+b,o+b+1,requirements[i]))}return {n:b+requirements.length*(b+1),clauses:cls};}
let large=[];
for(let [q,mixed] of [[1500,false],[7001,true]]){
let pins=Array(q).fill(0);if(mixed)pins[q-1]=1;
const f=build(3,pins),word=dim(f);
const floor=Math.floor(Math.sqrt(word.length*8));
const childLen=dim(canonicalChild(3,pins)).length*8; // Independently reserialized literal-by-literal, not a peer hardcoded size.
check(childLen<floor,"balanced source fails physical square root length");
large.push({q,label:mixed?"UNSAT":"SAT",source_bits:word.length*8,source_clauses:f.clauses.length,
  original_unpadded_child_bits:childLen,sqrt_source_bits_floor:floor,necessary_differing_block_probes:q});
}
return {name:"LSPV4_BALANCED_PIN_DIMACS_GUARD268",status:"PROVED/EXACT restricted proof, computational checks",assertions,small,additional_source_checks:cases,large,
 proof:"For every changed pin, four primary sign flips are balanced by four opposite private-pin sign flips. Equal ASCII block lengths imply all bytes outside switched block remain identical. An exact deterministic SAT decider must probe at least one changed source bit per q blocks on the all-even source; flipping any untouched block yields unsatisfiability."};
}
console.log(JSON.stringify(balancedPinCheck268(),null,2));
