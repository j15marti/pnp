#!/usr/bin/env node
/* Independently validate explicit ER2 proofs and generated Resolution-only projections. */
'use strict';
const fs = require('fs');
const data = JSON.parse(fs.readFileSync(process.argv[2] || __dirname+'/lspv3_368_results.json','utf8'));
let assertions=0;
function ok(b,msg){assertions++;if(!b)throw Error(msg)}
function norm(c){ok(Array.isArray(c),'not list'); let u=[...new Set(c)];ok(u.every(v=>Number.isInteger(v)&&v!==0&&!u.includes(-v)),'bad clause');return u.sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:-1));}
function same(a,b){return JSON.stringify(norm(a))===JSON.stringify(norm(b))}
function resol(a,b,p){ok(Number.isInteger(p)&&p>0,'bad pivot');let A=new Set(a),B=new Set(b);
if(A.has(-p)&&B.has(p)){[A,B]=[B,A]};ok(A.has(p)&&B.has(-p),'pivot absents');return norm([...A,...B].filter(l=>l!==p&&l!==-p));}
function gate(v,a,b){ok(Number.isInteger(v)&&v>0&&Number.isInteger(a)&&Number.isInteger(b)&&a!==0&&b!==0&&Math.abs(a)!==Math.abs(b)&&Math.abs(a)<v&&Math.abs(b)<v,'bad gate');return [norm([-v,a]),norm([-v,b]),norm([v,-a,-b])];}
function replay(case0,projection){let known=new Map();for(let i=0;i<case0.source.length;i++){known.set('s'+i,norm(case0.source[i]));}
if(!projection){for(let i=0;i<case0.gates.length;i++){const [v,a,b]=case0.gates[i];gate(v,a,b).forEach((c,j)=>known.set('d'+i+':'+j,c));}}
const lines=projection?case0.projection:case0.original;
let charged=0;for(let rec of lines){if(rec.kind==='source'){ok(known.has(rec.id),'invalid source');ok(same(known.get(rec.id),rec.clause),'corrupted source');continue;}
if(rec.kind==='definition_slot'){ok(!projection,'def in projected proof');ok(known.has(rec.id),'missing def');ok(same(known.get(rec.id),rec.clause),'wrong definition');continue;}
ok(rec.kind==='resolve'&&rec.parents.length===2,'unexpected record');ok(!known.has(rec.id),'reused id');ok(known.has(rec.parents[0])&&known.has(rec.parents[1]),'missing parent');const z=resol(known.get(rec.parents[0]),known.get(rec.parents[1]),rec.pivot);ok(same(z,rec.clause),'wrong resolvent');known.set(rec.id,z);charged++;}
ok(same(lines.at(-1).clause,[]),'not a refutation');return charged;
}
function satCount(clauses){const vars=[...new Set(clauses.flat().map(x=>Math.abs(x)))];ok(vars.length<=12,'small-only brute force');let count=0;
for(let k=0;k<(1<<vars.length);k++){const val=new Map(vars.map((x,i)=>[x,!!(k&(1<<i))]));if(clauses.every(c=>c.some(l=>val.get(Math.abs(l))===(l>0))))count++;}return count;}
for(const r of data.cases){let fresh={source:r.source,gates:r.gates,original:r.original,projection:r.projection};let er=replay(fresh,false);let projected=replay(fresh,true);
ok(er===r.q_res,'wrong original count');ok(projected===r.projection_node_count,'wrong projected count');ok(r.S.length<=2*r.e,'support bound');ok(projected<=r.node_upper_bound,'size inequality');ok(r.node_upper_bound===(2**r.S.length)*(r.q_res+1)-1,'weak bound');ok(satCount(r.source)===0,'UNSAT control');
for(let i=0;i<r.source.length;i++){let alt=r.source.filter((_,j)=>i!==j);ok(satCount(alt)===r.deleted_clause_model_counts[i],'source deletion models');}
if(r.paired_sat_models!==undefined){let mate=[...r.source.slice(0,-1),[1,-2]];ok(satCount(mate)===r.paired_sat_models&&r.paired_sat_models>0,'matched SAT control')}
for(const type of ['pivot','conclusion']){let damaged=JSON.parse(JSON.stringify(r));let first=damaged.projection.find(z=>z.kind==='resolve');ok(!!first,'no projection node');if(type==='pivot')first.pivot=999;else first.clause=[998];let rejected=false;try{replay(damaged,true)}catch(err){rejected=true}ok(rejected,'accepted corrupted '+type);}
}
for(const c of [[1,-1],[0],[1,1.5],['a'],[1,-1,2]]){let rejected=false;try{norm(c)}catch(err){rejected=true}ok(rejected,'accepted malformed clause')}
for(const c of [[4,1,1],[4,1,-1],[2,3,1],[0,1,2]]){let rejected=false;try{gate(...c)}catch(err){rejected=true}ok(rejected,'accepted malformed gate')}
console.log(JSON.stringify({status:'PASS',independent_assertions:assertions,cases:data.cases.length,source_deletion_controls:data.cases.reduce((s,z)=>s+z.source.length,0),malformed_rejected:9,corruptions_rejected:6},null,2));
