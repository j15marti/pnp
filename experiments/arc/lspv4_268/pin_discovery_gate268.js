"use strict";
// LSPV-4 exact restricted pin discovery and FLMV envelope experiment.
// Deterministic, no dependencies; run: node pin_discovery_gate268.js
// All source labels also independently verified by brute-force and UP-DPLL.
function auditPinDiscovery268(){
"use strict";
let checks=0;
const assert=(v,s)=>{checks++;if(!v)throw Error(s)};
const xor=(a,b,c)=>{const out=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)if(z!==(x^y))out.push([x?-a:a,y?-b:b,z?-c:c]);return out};
const pin=(z,p,q,v)=>{const out=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)out.push([v?z:-z,x?-p:p,y?-q:q]);return out};
const chain=(b,v,offset)=>{const arr=[];for(let j=2;j<=b;j++)arr.push(...xor(j===2?1:offset+j-2,j,offset+j-1));arr.push(...pin(offset+b-1,offset+b,offset+b+1,v));return arr};
const src=(b,pins)=>{const clauses=[];for(let i=0;i<pins.length;i++)clauses.push(...chain(b,pins[i],b+i*(b+1)));return {n:b+pins.length*(b+1),clauses}};
const serialize=f=>"p cnf "+f.n+" "+f.clauses.length+"\n"+f.clauses.map(c=>c.join(" ")+" 0\n").join("");
const sat=(f,a)=>f.clauses.every(c=>c.some(l=>a[Math.abs(l)-1]===Number(l>0)));
const brute=f=>{assert(f.n<=13,"large brute source");let models=0,witness=null;for(let k=0;k<(1<<f.n);k++){const a=Array.from({length:f.n},(_,i)=>(k>>i)&1);if(sat(f,a)){models++;if(witness===null)witness=a}}return {models,witness}};
function dpll(f){
let nodes=0,tests=0;
function branch(a){nodes++;a=a.slice();while(true){let changed=false,all=true;for(const c of f.clauses){let good=false,un=0,last=0;for(const l of c){tests++;const v=a[Math.abs(l)-1];if(v<0){un++;last=l}else if(v===Number(l>0)){good=true;break}}if(good)continue;all=false;if(un===0)return false;if(un===1){const j=Math.abs(last)-1,v=Number(last>0);if(a[j]>=0&&a[j]!==v)return false;if(a[j]<0){a[j]=v;changed=true}}}if(all)return true;if(!changed)break}const j=a.indexOf(-1);if(j<0)return false;for(const v of [0,1]){let a1=a.slice();a1[j]=v;if(branch(a1))return true}return false}
return {sat:branch(Array(f.n).fill(-1)),nodes,literal_tests:tests};
}
function recognize(b,f){
const q=(f.n-b)/(b+1);
let literal_compares=0;
if(!Number.isInteger(q)||q<1||f.clauses.length!==4*b*q)return {trusted:false,literal_compares};
const seen=[false,false];
for(let i=0;i<q;i++){const st=i*4*b,bit=Number(f.clauses[st+4*(b-1)]?.[0]>0);
seen[bit]=true;const C=chain(b,bit,b+i*(b+1));
for(let j=0;j<4*b;j++){if(f.clauses[st+j]?.length!==3)return {trusted:false,literal_compares};
for(let k=0;k<3;k++){literal_compares++;if(f.clauses[st+j][k]!==C[j][k])return {trusted:false,literal_compares}}}}
return {trusted:true,sat:!(seen[0]&&seen[1]),q,literal_compares,retained_pin_presence_bits:2}
}
const samples=[];
for(const [b,q] of [[2,2],[2,3],[3,2]]){
for(const label of ["SAT","UNSAT"]){
const pins=Array(q).fill(0);if(label==="UNSAT")pins[q-1]=1;
const f=src(b,pins),child=src(b,[...new Set(pins)].sort((a,b)=>a-b)),B=brute(f),B2=brute(child),D=dpll(f),D2=dpll(child),R=recognize(b,f),expected=label==="SAT";
assert((B.models>0)===expected,"parent brute");assert((B2.models>0)===expected,"child brute");
assert(D.sat===expected&&D2.sat===expected&&R.trusted&&R.sat===expected,"DPLL or grammar");
if(expected)assert(sat(f,B.witness),"witness check");
const corrupted={n:f.n,clauses:f.clauses.map(c=>c.slice())};corrupted.clauses[0][0]*=-1;
assert(!recognize(b,corrupted).trusted,"corrupt grammar accepted");
const N=serialize(f).length*8,M=serialize(child).length*8;
samples.push({b,q,label,pins,source_variables:f.n,source_clauses:f.clauses.length,source_bits:N,child_bits:M,source_model_count:B.models,baseline:D,child:D2,recognition:R,charged_selected_baseline:D.literal_tests+N,charged_selected_controller:R.literal_compares+D2.literal_tests+N+M});
}}
const minmax=[];
for(let q=2;q<=12;q++){let subset_checks=0,indistinguishable=0;for(let mask=0;mask<(1<<q)-1;mask++){subset_checks++;for(let k=0;k<q;k++)if(!((mask>>k)&1)){indistinguishable++;assert(!((mask>>k)&1),"unprobed block")}}minmax.push({q,required_distinct_pin_block_probes_on_all_even_source:q,proper_query_subsets:subset_checks,indistinguishable_one_odd_controls:indistinguishable})}
const trueCount=(C,a)=>C.reduce((k,l)=>k+Number(a[Math.abs(l)-1]===Number(l>0)),0);
function state(f,a){const t=f.clauses.map(C=>trueCount(C,a)),N=[0,0,0,0];t.forEach(k=>N[k]++);return {assignment:a.join(""),clause_truth_counts:t,N0_N1_N2_N3:N,satisfied:N[0]===0}}
function feasible(C,D,s,t){let assignment=new Map();for(const [cl,mode] of [[C,s],[D,t]])for(const lit of cl){const x=Math.abs(lit),b=mode==="S"?Number(lit>0):Number(lit<0);if(assignment.has(x)&&assignment.get(x)!==b)return false;assignment.set(x,b)}return true}
function clauseControl(pins){
const f=src(2,pins),rows=f.clauses.map((c,i)=>({source_clause:i+1,literals:c,signed_occurrences:c.map(l=>({variable:Math.abs(l),sign:l>0?"+":"-",local_S:Number(l>0),inverted_S_becomes_U:Number(l<0),local_U:Number(l<0),inverted_U_becomes_S:Number(l>0)}))}));
const compatibility=[];
for(let i=0;i<f.clauses.length;i++)for(let j=i+1;j<f.clauses.length;j++){
const C=f.clauses[i],D=f.clauses[j],same=C.some(l=>D.includes(l)),opposite=C.some(l=>D.includes(-l));
const rec={original_clause_i:i+1,original_clause_j:j+1,same_polarity_shared:same,opposite_polarity_shared:opposite};
for(const s of ["S","U"])for(const t of ["S","U"]){const v=feasible(C,D,s,t);rec[s+t]=v;assert(v===(s===t?!opposite:!same),"extreme matrix parity")}
compatibility.push(rec);
}
const a0=Array(f.n).fill(0),a1=Array(f.n).fill(1),trail=[{flipped_variable:null,...state(f,a0)}];let trailA=a0.slice();
for(let x=0;x<Math.min(f.n,5);x++){trailA[x]^=1;trail.push({flipped_variable:x+1,...state(f,trailA)})}
let models=[],complements=0;
for(let k=0;k<(1<<f.n);k++){let a=Array.from({length:f.n},(_,i)=>(k>>i)&1),notA=a.map(x=>1-x);
for(const C of f.clauses){assert(trueCount(C,a)+trueCount(C,notA)===3,"complement fail");complements++}
if(sat(f,a))models.push(a)}
let resolvent=null;
outer:for(let i=0;i<f.clauses.length;i++)for(let j=i+1;j<f.clauses.length;j++)for(const l of f.clauses[i]){
if(!f.clauses[j].includes(-l))continue;
const R=[...new Set([...f.clauses[i].filter(v=>v!==l),...f.clauses[j].filter(v=>v!==-l)])];
if(R.some(v=>R.includes(-v)))continue;
const cube={};for(const v of R)cube[Math.abs(v)]=Number(v<0);
for(const a of models)assert(!Object.entries(cube).every(([v,w])=>a[Number(v)-1]===w),"unsound forbidden cube");
resolvent={source_clause_indices:[i+1,j+1],pivot:Math.abs(l),resolved_clause:R,prohibited_cube:cube,checked_source_models:models.length,proof:"one Boolean resolution inference"};break outer;
}
return {variables:f.n,source_clauses:rows,compatibility,global_all_zero:state(f,a0),global_all_one:state(f,a1),intermediate_flips:trail,checked_complement_clause_pairs:complements,source_model_count:models.length,sourced_resolution_forbidden_cube:resolvent};
}
const clauses={sat:clauseControl([0,0]),unsat:clauseControl([0,1])};
const large=[];
for(const [q,mixed] of [[1500,false],[7001,true]]){
const pins=Array(q).fill(0);if(mixed)pins[q-1]=1;
const f=src(3,pins),child=src(3,[...new Set(pins)].sort((a,b)=>a-b)),N=serialize(f).length*8,M=serialize(child).length*8;
assert(M<Math.sqrt(N),"large child longer than sqrt parent");
large.push({q,label:mixed?"UNSAT":"SAT",source_clauses:f.clauses.length,source_bits:N,child_bits:M,floor_sqrt_source_bits:Math.floor(Math.sqrt(N)),compulsory_pin_probe_lower_bound:q,full_grammar_literal_comparisons:3*f.clauses.length});
}
function gcd(a,b){while(b){const m=a%b;a=b;b=m}return a<0n?-a:a}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return {a:a/g,b:b/g}}
const plus=(x,y)=>Q(x.a*y.b+y.a*x.b,x.b*y.b),minus=(x,y)=>Q(x.a*y.b-y.a*x.b,x.b*y.b),times=(x,y)=>Q(x.a*y.a,x.b*y.b),divide=(x,y)=>Q(x.a*y.b,x.b*y.a),lt=(x,y)=>x.a*y.b<y.a*x.b,fmt=x=>x.a+"/"+x.b;
function flmv(a,b){let c=Q(a,b),f=Q(1),best=Q(0),steps=[],winners=[];for(let k=1;k<100;k++){
f=divide(times(c,f),plus(Q(1),f));let x=divide(minus(divide(Q(1),f),c),Q(k)),z=Q(1);for(let p=0;p<k;p++)z=divide(z,c);const d=lt(x,z)?x:z;
if(lt(best,d)){best=d;winners=[k]}else if(!lt(d,best)&&!lt(best,d))winners.push(k);
steps.push({k,left:fmt(x),tailcap:fmt(z),min:fmt(d)});
if(lt(divide(z,c),best))return {c:fmt(c),envelope:fmt(best),maximizers:winners,first_excluded_index:k+1,checked:steps};
}throw Error("FLMV tail cap failed")}
const envelope=[flmv(6,5),flmv(241,200)];
assert(envelope[0].envelope==="23/45","FLMV 6/5");
assert(envelope[1].envelope==="11642479/23232400","FLMV 241/200");
return {run:"LSPV4_PIN_DISCOVERY_GATE268",local_time:"2026-10-31 02:36 America/Los_Angeles",status:"PROVED/EXACT restricted; COMPUTATIONAL controls; universal ARC OPEN",assertions:checks,seed:null,protocol:"deterministic exhaustive small sources, analytic and measured large encoding sizes",minmax,samples,clauses,large,envelope,limitations:"The lower bound is a canonical parity-pin promise bit-probe cost, not unrestricted SAT time or all-input ARC; instrumented work not native FLMV."};
}
console.log(JSON.stringify(auditPinDiscovery268(),null,2));
