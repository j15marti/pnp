"use strict";
// Independently authored original-source/Circuit-SAT UP verifier, no producer imports.
// Usage: node independent_source_tseitin325.js
const F=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
function ok(q,msg){if(!q)throw Error(msg)}
function v(l,a){let x=a.get(Math.abs(l));return x===undefined?null:(l>0?x:!x)}
function original(mask){return F.every(c=>c.some(z=>Boolean(mask&(1<<(Math.abs(z)-1)))===(z>0)))}
const gates=[],out=[];
function emit(t,a,b){let i=10+gates.length;gates.push([i,t,a,b]);return i}
for(let c of F)out.push(emit('O',emit('O',c[0],c[1]),c[2]));
let row=out;while(row.length>1){let next=[];for(let j=0;j<row.length;j+=2)next.push(j+1<row.length?emit('A',row[j],row[j+1]):row[j]);row=next}
const root=row[0],CNF=[];
for(let [id,t,a,b] of gates)CNF.push(...(t==='O'?[[-a,id],[-b,id],[a,b,-id]]:[[a,-id],[b,-id],[-a,-b,id]]));
CNF.push([root]);ok(gates.length===35&&CNF.length===106,'compiled architecture');
function evaluate(mask){let a=new Map();for(let j=1;j<=9;j++)a.set(j,!!(mask&(1<<(j-1))));for(let [i,t,x,y] of gates)a.set(i,t==='O'?(v(x,a)||v(y,a)):(v(x,a)&&v(y,a)));return a}
let good=[];for(let i=0;i<512;i++){const a=evaluate(i),want=original(i);ok(want===a.get(root),'gate truth');ok(want===CNF.every(c=>c.some(z=>v(z,a)===true)),'Tseitin functional truth');if(want)good.push(i)}
ok(good.length===70,'original models');
function up(F,p){let a=new Map(p),reads=0,scans=0;while(true){let newVal=false;for(let clause of F){scans++;let unknown=[];let sat=false;for(let z of clause){reads++;let x=v(z,a);if(x===true){sat=true;break}if(x===null)unknown.push(z)}if(sat)continue;if(unknown.length===0)return {conflict:true,a,reads,scans,residual:[]};if(unknown.length===1){a.set(Math.abs(unknown[0]),unknown[0]>0);newVal=true;break}}if(!newVal)break}
let residual=F.filter(c=>!c.some(z=>v(z,a)===true)).map(c=>c.filter(z=>v(z,a)===null));
return {conflict:false,a,reads,scans,residual}}
let exemplar=[[1,true],[4,false],[5,true],[8,false]],S=up(F,exemplar),T=up(CNF,exemplar);
ok(!S.conflict&&!T.conflict,'UP stalls');ok(S.residual.length===7&&S.residual.every(x=>x.length===2),'source binary');ok(T.residual.filter(x=>x.length===2).length===23&&T.residual.filter(x=>x.length===3).length===1,'Tseitin width profile');ok(T.residual.some(x=>x.join(',')==='-2,-3,-26'),'ternary private gate');
const chains=[[11,[9,-2]],[5,[-2,7]],[12,[7,-9]],[4,[-9,6]],[8,[6,-7]],[6,[-7,9]]];for(let [id,[a,b]] of chains){let q=F[id-1].filter(x=>!exemplar.some(([k])=>k===Math.abs(x)));ok(q.length===2&&q.includes(-a)&&q.includes(b),'invalid original SCC provenance '+id)}
let none=0,stalled=0,stalledTernary=0;for(let code=0;code<19683;code++){let k=code,p=[];for(let i=1;i<=9;i++){let r=k%3;k=Math.floor(k/3);if(r)p.push([i,r===2])}
if(good.some(mask=>p.every(([i,x])=>(!!(mask&(1<<(i-1))))===x)))continue;none++;
let s=up(F,p);if(!s.conflict){stalled++;ok(s.residual.every(c=>c.length<=2),'source width >2');let t=up(CNF,p);ok(!t.conflict,'unexpected circuit UP contradiction');if(t.residual.some(c=>c.length===3))stalledTernary++}}
ok(none===9175&&stalled===3&&stalledTernary===1,'cube histogram');
const pins=[[3,false],[5,true],[6,false],[7,false],[8,false]],pair=[false,true].map(x=>good.filter(mask=>[[1,x],...pins].every(([i,b])=>(!!(mask&(1<<(i-1))))===b)).length);
ok(pair[0]===2&&pair[1]===0,'same-original both-label');
function grammar(C){let cnt=Array.from({length:10},()=>[0,0]),unique=new Set();if(C.length!==12)return false;for(let c of C){if(c.length!==3||new Set(c.map(Math.abs)).size!==3||c.some(z=>!Number.isInteger(z)||z===0||Math.abs(z)>9||(z>0)!==(c[0]>0)))return false;let key=c.slice().sort((a,b)=>a-b).join(',');if(unique.has(key))return false;unique.add(key);for(let z of c)cnt[Math.abs(z)][z>0?1:0]++}return cnt.slice(1).every(x=>x[0]===2&&x[1]===2)}
const malformed=[F.slice(1),[F[0],F[0],...F.slice(2)],[[1,1,6],...F.slice(1)],[[1,-5,6],...F.slice(1)],[[1,5,10],...F.slice(1)],[[1,5,7],...F.slice(1)]];
ok(grammar(F)&&malformed.every(x=>!grammar(x)),'bad syntax control');
const result={PASS:true,source_model_count:good.length,all_full_source_circuit_rows:512,all_partial_original_cubes:19683,unsat_original_cubes:none,source_UP_stalled_UNSAT_cubes:stalled,circuit_ternary_while_source_binary:stalledTernary,original_residual_binary_clauses:S.residual.length,compiled_residual_binary_clauses:T.residual.filter(c=>c.length===2).length,compiled_residual_ternary_clauses:T.residual.filter(c=>c.length===3).length,compiled_dead_gate_ternary:[-2,-3,-26],source_up_clause_scans:S.scans,source_up_literal_reads:S.reads,compiled_up_clause_scans:T.scans,compiled_up_literal_reads:T.reads,same_original_sat_unsat_complete_counts:pair,malformed_rejected:malformed.length,proof_status:'finite restricted circuit syntax only; P versus NP OPEN'};
console.log(JSON.stringify(result,null,2));
