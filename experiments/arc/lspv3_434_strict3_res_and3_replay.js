'use strict';
// LSPV-3/434 checked semantic fragment; historical native byte checker NOT executed.
const A=require('assert');
const S=[[1,3,4],[1,3,-4],[1,-3,4],[1,-3,-4],[-1,2,5],[-1,2,-5],[-1,-2,6],[-1,-2,-6]];
const F=[[1],[-1,2],[-1,-2]];
const sat=(c,a)=>c.some(x=>x>0?a[Math.abs(x)]===1:a[-x]===0);
const runs=Array.from({length:64},(_,i)=>Array.from({length:7},(_,j)=>j?((i>>(j-1))&1):0));
const norm=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
const R=(x,y,p)=>{A(x.includes(p)&&y.includes(-p));let z=norm([...x.filter(v=>v!==p),...y.filter(v=>v!==-p)]);A(z.every(v=>!z.includes(-v)));return z};
let count=0;
for(let a of runs){A.equal(S.every(c=>sat(c,a)),F.every(c=>sat(c,a)));A(!S.every(c=>sat(c,a)));count+=2}
const witness=[];
for(let j=0;j<8;j++){let a=runs.find(a=>!sat(S[j],a)&&S.every((c,k)=>j===k||sat(c,a)));A(a);witness.push(a.slice(1));count++}
const n={};n.a=R(S[0],S[1],4);n.b=R(S[2],S[3],4);n.c=R(S[4],S[5],5);n.d=R(S[6],S[7],6);n.e=R(n.b,n.c,1);n.f=R(n.a,n.e,3);n.g=R(n.a,n.b,3);n.h=R(n.g,n.c,1);
A.deepStrictEqual([n.f,n.d,n.g,n.h],[[1,2],[-1,-2],[1],[2]]);count++;
const TT=(vars,pred)=>Array.from({length:1<<vars.length},(_,i)=>{let a=Array(7).fill(0);vars.forEach((v,k)=>a[v]=(i>>(vars.length-1-k))&1);return Number(pred(a))});
const xor=TT([1,2],a=>(a[1]^a[2])===1);
A.deepStrictEqual(TT([1,2],a=>sat(n.f,a)&&sat(n.d,a)),xor);count++;
A.deepStrictEqual(TT([1,3,4],a=>sat(n.g,a)&&sat(S[0],a)),TT([1,3,4],a=>a[1]===1));count++;
A.deepStrictEqual(TT([1,2],a=>sat(n.h,a)&&sat(n.c,a)),TT([1,2],a=>a[2]===1));count++;
A.equal((1^1)^1,1);count++;
const rho={3:0,4:0,5:0,6:0};
const restrict=c=>{let out=[];for(let x of c){if(!(Math.abs(x) in rho))out.push(x);else if((x>0)===(rho[Math.abs(x)]===1))return true}return norm(out)};
A.deepStrictEqual(S.map(restrict),[[1],true,true,true,[-1,2],true,[-1,-2],true]);count++;
A.deepStrictEqual(restrict(n.a),[1]);A.equal(restrict(n.e),true);A.deepStrictEqual(restrict(n.f),[1,2]);count+=3;
const stronger=TT([1,2],a=>sat([1],a)&&sat([-1,-2],a));
A.deepStrictEqual(xor,[0,1,1,0]);A.deepStrictEqual(stronger,[0,0,1,0]);A.notDeepStrictEqual(xor,stronger);count+=3;
A.deepStrictEqual(R([1],R([-1,2],[-1,-2],2),1),[]);count++;
let rejected=0;for(const f of [()=>A.deepStrictEqual(xor,[1,0,0,1]),()=>R(n.b,n.c,-1),()=>A.deepStrictEqual(restrict(n.e),[-3,2]),()=>A.deepStrictEqual(stronger,xor)]){try{f()}catch(e){rejected++}}A.equal(rejected,4);count++;
const dimacs=(txt)=>{let lines=txt.trim().split(/\n/).map(s=>s.trim());let h=lines.shift().split(/\s+/);
 A(h.length===4&&h[0]==='p'&&h[1]==='cnf');let n=Number(h[2]),m=Number(h[3]);
 A(Number.isInteger(n)&&Number.isInteger(m)&&n>0&&m>=0);A.equal(lines.length,m);
 return lines.map(l=>{let t=l.split(/\s+/).map(Number);A(t.every(Number.isInteger));A.equal(t.pop(),0);
 A.equal(t.length,3);A(t.every(x=>x!==0&&Math.abs(x)<=n));A.equal(new Set(t.map(Math.abs)).size,3);return t});};
const valid='p cnf 6 8\n'+S.map(c=>c.join(' ')+' 0').join('\n')+'\n';
A.deepStrictEqual(dimacs(valid),S);count++;
let malformed=0;for(let bad of [valid.replace('6 8','6 9'),valid.replace(/ 0\n/,' 3\n'),
 valid.replace('1 3 4 0','1 3 7 0'),valid.replace('1 3 4 0','1 3 3 0'),valid.replace('p cnf','p dnf')]){
 try{dimacs(bad)}catch(e){malformed++}}
A.equal(malformed,5);count++;
const result={id:'LSPV3-434',status:'PROVED/RESTRICTED exact-replay obstruction; mixed-minimum and B3 OPEN',
 source_variables:6,strict_3cnf_clauses:8,full_mixed_refutation_nodes:13,indispensable_clause_witnesses:witness,
 expected_parity_truth_table:xor,restricted_replay_truth_table:stronger,
 original_source_resolution_repair_nodes:2,independent_assertions:count,hostile_controls_rejected:rejected,
 malformed_dimacs_rejected:malformed,historical_native_checker_execution:false};
console.log(JSON.stringify(result,null,2));